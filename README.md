# AI Knowledge Base SaaS

This repository contains a FastAPI-based multi-tenant RAG backend that uses PostgreSQL, Milvus, and a local Ollama LLM to provide private AI assistants per organization.

Quick start (development - local):

1. Start dependencies with Docker (Postgres + Milvus):

```bash
cp .env.sample .env
docker-compose up -d --build
```

2. Install Python dependencies (recommended in a venv):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the FastAPI app locally:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. Ensure Ollama is running locally with a model (example `llama3:latest`) and accessible from the app. If running the API in Docker, the default `.env.sample` uses `host.docker.internal` for `OLLAMA_URL`.

Endpoints:
- `POST /auth/register` — register user
- `POST /auth/login` — login (OAuth2 password form)
- `POST /documents` — upload documents (ingest pipeline)
- `POST /rag/query` — ask a question; returns `answer` and `retrieved_chunks`

Notes:
- Do not commit a real `.env` with secrets. Use `.env.sample` as a template.
- The Milvus collection is created at app startup.

Contributing and next steps
- Add CI, tests, and production deployment configuration.

