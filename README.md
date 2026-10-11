# RAG Support Assistant

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-TF--IDF-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

A retrieval-augmented Q&A assistant over a sample support knowledge base.
Ask a question in plain English; the assistant retrieves the most relevant
doc sections and answers **with citations** — every claim traces back to a
source chunk, so nothing is hallucinated.

Built as a portfolio demo of the RAG pattern: chunking → retrieval → grounded
answer composition.

## How it works

```
docs/*.md ──▶ chunk by heading ──▶ TF-IDF matrix ──▶ cosine similarity
                                                        │
user question ──▶ TF-IDF vector ──────────────────────▶ top-k chunks
                                                        │
                                              cited answer (ask.py)
```

1. **Ingestion** (`rag.py::load_documents`): every markdown file in `docs/`
   is split into heading-scoped chunks — one section per chunk, so each
   retrieved passage is self-contained and citable.
2. **Retrieval** (`rag.py::Retriever`): scikit-learn `TfidfVectorizer`
   (unigrams + bigrams, sublinear TF, English stop words) with cosine
   similarity ranking.
3. **Answering** (`ask.py`): the top-k chunks are rendered as an answer with
   `[n]` citations, source file + heading, and a relevance score.

> **Upgrade path:** swap `TfidfVectorizer` for `sentence-transformers`
> (`all-MiniLM-L6-v2`) dense embeddings — the chunking and citation logic
> stays identical. TF-IDF was chosen here so the demo runs with zero
> model downloads.

## Quickstart

```bash
pip install -r requirements.txt

# ask a single question
python ask.py "Why am I getting 401 errors from the API?"

# retrieve more context per question
python ask.py --top-k 5 "How do refunds work?"

# interactive chat mode
python ask.py --interactive
```

## Example Q&As

**Q: Why am I getting 401 errors from the API?**

> **[1]** A `401` response means the request did not include valid credentials.
> Common causes: **Missing Authorization header** — every request must include
> `Authorization: Bearer <API_KEY>`; **revoked or rotated key**; **wrong
> environment** (`sk_test_` vs `sk_live_`).
> *Source: api-authentication-troubleshooting.md > 401 Unauthorized*

**Q: How do I get a refund?**

> **[1]** Monthly plans: refunds within **14 days** of the charge if usage
> stayed under 10% of quota. Annual plans: **30 days** from renewal. Overage
> charges are non-refundable. Request via support@acme.com with workspace ID
> and invoice number.
> *Source: billing-faq.md > Can I get a refund?*

**Q: My webhooks stopped working, what should I check?**

> **[1]** Confirm the endpoint shows **Active** (not Paused) under
> Settings > Webhooks. **[2]** Check the delivery log for failure codes
> (`410` auto-disables after 50 consecutive). **[3]** Verify the
> `X-Acme-Signature` against the **raw body bytes**. **[4]** Check the
> event-type filter — `*` subscribes to all.
> *Source: webhook-debugging-guide.md*

## Project structure

```
rag-support-assistant/
├── ask.py              # CLI: single question or interactive chat
├── rag.py              # chunking + TF-IDF retriever
├── docs/               # sample knowledge base (6 support articles)
│   ├── api-authentication-troubleshooting.md
│   ├── rate-limiting-guide.md
│   ├── billing-faq.md
│   ├── webhook-debugging-guide.md
│   ├── sso-setup-guide.md
│   └── data-export-guide.md
└── requirements.txt
```

## Notes

- The knowledge base is **sample data written for this demo** (a fictional
  "Acme API"); retrieval quality on real docs depends on chunking strategy
  and corpus size.
- TF-IDF is a sparse lexical baseline — great for keyword-heavy support
  content, weaker on paraphrase. That's exactly what the dense-embedding
  upgrade path addresses.
