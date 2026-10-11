#!/usr/bin/env python3
"""CLI support assistant: answer questions from the docs/ knowledge base.

Usage:
    python ask.py "Why am I getting 401 errors?"
    python ask.py --top-k 5 "How do refunds work?"
    python ask.py --interactive

The answer is composed from the retrieved chunks — every claim is followed by
a [source] citation so the response is grounded, never hallucinated.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rag import Chunk, Retriever, load_documents

DOCS_DIR = Path(__file__).resolve().parent / "docs"


def format_answer(question: str, results: list[tuple[Chunk, float]]) -> str:
    """Render retrieved chunks as a cited answer."""
    if not results:
        return (
            "I couldn't find anything relevant in the knowledge base. "
            "Try rephrasing, or contact support@acme.com."
        )
    lines = [f"**Q:** {question}", ""]
    for i, (chunk, score) in enumerate(results, 1):
        # Keep the excerpt tight: first ~400 chars of the chunk body.
        excerpt = " ".join(chunk.text.split())
        if len(excerpt) > 400:
            excerpt = excerpt[:397] + "..."
        lines.append(f"**[{i}]** {excerpt}")
        lines.append(f"    _Source: {chunk.citation} (relevance {score:.2f})_")
        lines.append("")
    lines.append(
        "_Answer generated from the support knowledge base. "
        "Verify details in the cited articles._"
    )
    return "\n".join(lines)


def answer(question: str, retriever: Retriever, top_k: int) -> str:
    return format_answer(question, retriever.query(question, top_k=top_k))


def interactive(retriever: Retriever, top_k: int) -> None:
    print("Support assistant (type 'quit' to exit)\n")
    while True:
        try:
            q = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if q.lower() in {"quit", "exit", "q"}:
            break
        if not q:
            continue
        print(f"\nAssistant:\n{answer(q, retriever, top_k)}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ask the support knowledge base.")
    parser.add_argument("question", nargs="?", help="Question to answer")
    parser.add_argument("--top-k", type=int, default=3, help="Chunks to retrieve (default: 3)")
    parser.add_argument("--docs", default=str(DOCS_DIR), help="Docs directory")
    parser.add_argument("--interactive", action="store_true", help="Chat mode")
    args = parser.parse_args(argv)

    chunks = load_documents(args.docs)
    retriever = Retriever(chunks)
    print(f"[indexed {len(chunks)} chunks from {args.docs}]\n", file=sys.stderr)

    if args.interactive or not args.question:
        interactive(retriever, args.top_k)
    else:
        print(answer(args.question, retriever, args.top_k))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
