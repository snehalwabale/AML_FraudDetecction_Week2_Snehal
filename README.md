# AML & Fraud Detection Investigation Co-Pilot

A LangChain-based AML & Fraud Detection Investigation Co-Pilot with Retrieval-Augmented Generation (RAG), session memory, FastAPI backend, and Streamlit frontend.

## 1. Create and activate a virtual environment

```bash
python3 -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure environment variables

Copy the example file and fill in real values:

```bash
cp .env.example .env
```

Edit `.env` and set:

```text
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=""
LANGSMITH_PROJECT="aml-fraud-copilot"
VECTOR_DB="./vector_db"
```

## 4. Ingest documents into the vector store

This loads the AML knowledge base, chunks it, creates embeddings using OpenAI, and stores them in the FAISS vector database. Run this once before starting the API (and again any time the knowledge base changes):

```bash
python rag/vectorstore.py
```

## 5. Run the backend API

```bash
uvicorn app.main:app --reload
```

* `GET /health` — checks application status
* `POST /chat` — `{"message": "...", "session_id": "..."}` → AML investigation response
* `POST /reset` — clears conversation memory
* `POST /retrieve` — retrieve relevant AML documents
* `POST /ingest` — ingest new documents into the vector database
* `GET /sources` — list indexed documents
* `DELETE /sources/{doc_id}` — delete an indexed document

API docs:

```
http://localhost:8000/docs
```

## 6. Run the Streamlit frontend

In a second terminal (with the venv activated):

```bash
streamlit run frontend/streamlit.py
```

Open http://localhost:8501 and chat with the AML Investigation Co-Pilot. It communicates with the FastAPI backend running on `http://localhost:8000`.

## 7. Run the evaluation harness

Measures retrieval quality and answer quality against the predefined AML evaluation dataset.

```bash
python -m eval.run_eval
```

Results are written to the evaluation results directory.

## Project structure

```text
app/
  main.py              FastAPI app: /chat, /reset, /health
  chains.py            LangChain conversation chain
  tools.py             AML investigation tools + document ingestion
  models.py            Pydantic request/response models
  prompts.py           System prompt and chat prompt
  memory.py            Session conversation memory
  logger.py            Structured interaction logging

rag/
  loaders.py           Document loaders
  chunkers.py          Document chunking
  embeddings.py        OpenAI embedding model
  vectorstore.py       FAISS vector database
  retriever_hybrid.py  Hybrid retrieval
  query_transform.py   Query rewriting
  reranker.py          Document reranking
  qa_chain.py          RAG question answering pipeline

documents/
  AML knowledge base documents

eval/
  dataset.py           AML evaluation dataset
  run_eval.py          Evaluation runner

frontend/
  streamlit.py         Chat UI
```
