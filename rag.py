"""
RAG retrieval core: chunk markdown docs and retrieve with TF-IDF + cosine similarity.

Pipeline
--------
1. `load_documents(docs_dir)` reads every ``*.md`` file and splits it into
   chunks. A chunk is a heading plus the text under it (roughly one section),
   so retrieved passages are self-contained and citable.
2. `Retriever` builds a TF-IDF matrix over the chunks (scikit-learn).
   `query(question, top_k)` returns the most similar chunks with scores.

Upgrade path: swap `TfidfVectorizer` for sentence-transformers embeddings
(`all-MiniLM-L6-v2`) and cosine similarity over dense vectors — the chunking
and citation logic stays identical.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Chunk:
    """One retrievable passage with its source for citations."""

    doc_name: str      # e.g. "billing-faq.md"
    heading: str       # section heading the chunk belongs to
    text: str          # chunk body

    @property
    def citation(self) -> str:
        return f"{self.doc_name} > {self.heading}"


def chunk_markdown(text: str, doc_name: str) -> list[Chunk]:
    """Split a markdown document into heading-scoped chunks.

    Every ``##`` (or ``#``) heading starts a new chunk; prose before the
    first heading becomes an "Overview" chunk. Empty chunks are dropped.
    """
    chunks: list[Chunk] = []
    heading: str | None = None
    buf: list[str] = []

    def flush() -> None:
        body = "\n".join(buf).strip()
        if body:
            chunks.append(Chunk(doc_name, heading or "Overview", body))
        buf.clear()

    for line in text.splitlines():
        m = re.match(r"#{1,3}\s+(.*)", line)
        if m:
            flush()
            heading = m.group(1).strip()
        else:
            buf.append(line)
    flush()
    return chunks


def load_documents(docs_dir: str | Path) -> list[Chunk]:
    """Load and chunk every ``*.md`` file in *docs_dir* (sorted for determinism)."""
    docs_dir = Path(docs_dir)
    chunks: list[Chunk] = []
    for path in sorted(docs_dir.glob("*.md")):
        chunks.extend(chunk_markdown(path.read_text(encoding="utf-8"), path.name))
    if not chunks:
        raise FileNotFoundError(f"No markdown documents found in {docs_dir}")
    return chunks


class Retriever:
    """TF-IDF retriever over document chunks."""

    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        # Sublinear TF + unigrams/bigrams: cheap, robust baseline for short
        # support articles. English stop words removed to cut noise.
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1,
        )
        self.matrix = self.vectorizer.fit_transform(c.text for c in chunks)

    def query(self, question: str, top_k: int = 3) -> list[tuple[Chunk, float]]:
        """Return the *top_k* chunks ranked by cosine similarity to *question*."""
        q = self.vectorizer.transform([question])
        scores = cosine_similarity(q, self.matrix).ravel()
        order = np.argsort(scores)[::-1][:top_k]
        return [(self.chunks[i], float(scores[i])) for i in order if scores[i] > 0]
