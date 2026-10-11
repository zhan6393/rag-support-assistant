# RAG Support Assistant 🤖

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **grounded** support Q&A assistant: every answer comes from your docs and carries **[n] citations** — no hallucinations. TF-IDF retrieval baseline with a clean upgrade path to dense embeddings.

## Quickstart

```bash
pip install -r requirements.txt

# Ask a question — the answer cites the docs it came from
python ask.py "How do I rotate an API key?"

# Show more retrieved context
python ask.py "What should I do when I hit a 429?" --top-k 3

# Interactive REPL mode
python ask.py --interactive
```

## How it works

1. **Chunk** — `rag.py` splits each markdown doc in `docs/` into sections on `##` headings, keeping the doc title + section as the citation label.
2. **Retrieve** — scikit-learn TF-IDF vectors + cosine similarity rank chunks against your question.
3. **Answer** — `ask.py` prints the top chunks' text with `[n]` citations and their source files.

## Project structure

| Path | What it does |
|---|---|
| `rag.py` | `chunk_markdown`, `load_documents`, and the `Retriever` (TF-IDF + cosine) |
| `ask.py` | CLI: `--top-k`, `--interactive`, `--docs`; prints answers with `[n]` citations |
| `docs/` | Sample knowledge base: API auth, rate limiting, billing, webhooks, SSO, data export |
| `requirements.txt` | `scikit-learn`, `numpy` |

## CLI options

| Flag | Default | Meaning |
|---|---|---|
| `--top-k` | 1 | How many retrieved chunks to show |
| `--interactive` | off | REPL mode: ask follow-up questions |
| `--docs` | `docs` | Knowledge-base directory |

## Honest caveats

- TF-IDF is a lexical baseline — it misses paraphrases and synonyms. The `Retriever` is a deliberate seam: swap the vectorizer for a dense encoder (e.g. sentence-transformers) without touching `ask.py`.
- Answers are extractive (the best retrieved chunk), not generated — grounding is guaranteed, fluency is not. That's the point.

## License

MIT — see [LICENSE](LICENSE).
