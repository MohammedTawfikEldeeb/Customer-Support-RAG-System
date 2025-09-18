## Customer Support RAG System

Delightfully fast, production-ready Retrieval-Augmented Generation for cafe-style customer support. Built with a clean architecture for ingestion, processing, retrieval, and generation — and a pragmatic memory strategy that preserves answer quality.

### Highlights for Recruiters
- Consistently accurate answers with natural multi-turn memory.
- Split responsibilities into two assistants — one for conversational context, one for factual retrieval — to avoid quality regressions when adding memory.
- Improving `k_retrieval` from 3 to 10 increased context recall from 0.975 → 1.000 while maintaining high faithfulness (0.975) and answer relevancy (0.955). See `src/evaluation/observation.txt`.

---

### Tech Stack
- FastAPI, Uvicorn
- LangChain Core and Runnables
- Google Generative AI (`gemini-1.5-flash`) for generation
- Pinecone for vector search
- HuggingFace Embeddings (`intfloat/multilingual-e5-small`)
- Jinja2 (templates) + vanilla CSS for the UI
- dotenv for configuration
- Optional: LangSmith for tracing and evaluation tracking

---

### The Problem We Hit When Adding “Memory”
Our base system (without memory) performed excellently. For direct questions like “What desserts do you have?”, answers were complete and well-structured.

When we bolted on a naive memory layer, the system started acting like an overloaded agent trying to both remember and retrieve at the same time. On a clear first-turn question, it sometimes over-corrected based on “imagined prior context,” issuing an impoverished search term like just “desserts,” and returning an incomplete list (sometimes only one item instead of all available options).

---

### The Smart Fix: Specialist Assistants
We separated concerns instead of overloading one model:

1) Context Assistant
- Focus: Understand prior turns and decide whether the new user message is context-dependent.
- If yes, it rewrites the message into a fully specified question.
- If the new message is already clear, it passes it through untouched.

2) Knowledge Assistant (High-precision RAG)
- Focus: Always receives a clear, unambiguous question (either the original or the rewritten one) and retrieves the best structured answer.

This preserves the strong retrieval quality of the base system while enabling natural, multi-turn conversations.

---

### Why k_retrieval = 10 (and not 3)
From `src/evaluation/observation.txt`:

```text
--------- k_retrival == 3 -----------
faithfulness         0.950
answer_relevancy     0.950
context_precision    0.917
context_recall       0.975

--------- k_retrival == 10 -----------
faithfulness         0.975
answer_relevancy     0.955
context_precision    0.911
context_recall       1.000
```

Operational intuition: in categories like drinks where we have ~10 items, returning only 3 contexts can truncate the final answer when users ask “What drinks do you have?”. With `k=10`, recall hits 1.000 and answers become complete without sacrificing faithfulness.

---

### Quickstart

Requirements are managed with `uv` (or use `pip` if you prefer):

```bash
# Using uv (fast Python package manager)
uv sync
uv run python src/app.py

# Or using pip
pip install -r requirements.txt
python src/app.py
```

Environment configuration lives in `src/config.py`. The main web entrypoint is `src/app.py` with templates under `src/templates` and static assets under `src/static`.

#### Environment Variables
Create a `.env` file in the project root:

```bash
PINECONE_API_KEY=your_pinecone_key
GOOGLE_API_KEY=your_google_api_key

# Optional LangSmith tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=customer-support-rag
```

Then run with `uv run python src/app.py` or `python src/app.py`.

#### Enable LangSmith Tracing
With the env vars above set, LangChain will automatically send traces. You can also set them temporarily for a single run:

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=...
export LANGCHAIN_PROJECT=customer-support-rag
uv run python src/app.py
```

---

### Project Structure

```text
src/
  ingestion/       # Data loaders
  processing/      # Chunking, metadata
  vectorstore/     # Embeddings & store integrations
  retrieval/       # Semantic retrieval
  generation/      # Chains / orchestration
  evaluation/      # Metrics & experiments
  templates/       # UI
  static/          # CSS, images
  helpers/         # Utility scripts (e.g., data processing)
app.py             # FastAPI app
config.py          # Env & constants
main.py            # Entry/script runner if needed
data/              # Raw and processed data
```

---

### Evaluation
Automated evaluation scripts live in `src/evaluation`. Use `evaluate.py` to benchmark faithfulness, answer relevancy, context precision, and recall across different retrieval settings. We keep result snapshots and notes in `observation.txt` to drive decisions (like setting `k_retrieval = 10`).

---
