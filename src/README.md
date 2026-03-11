# Scenario RAG API (src)

PostgreSQL + pgvector + OpenAI. Question → safety check → vector search → scenario response.

## .env (required)

Copy `.env.example` to `.env` and set:

- **OPENAI_API_KEY** — required for embeddings
- **DATABASE_URL** — e.g. `postgresql://localhost:5432/scenario_rag`

## Run locally

```bash
cd src
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit .env
python -m scripts.create_db
python -m scripts.init_db
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Use **`python -m uvicorn`** so the venv’s Python (and its installed `psycopg2-binary`, `pgvector`) is used; plain `uvicorn` can cause `ModuleNotFoundError: No module named 'psycopg2'` in the reloader subprocess.

## See the table

```bash
psql -d scenario_rag -c "\dt"
psql -d scenario_rag -c "SELECT scenario_id, intent FROM scenario_chunks LIMIT 5;"
```

## Ask a question

**Browser:** http://localhost:8000/docs → **POST /api/v1/check** → body: `{"question": "I need to refill my medication"}`

**curl:**

```bash
curl -X POST http://localhost:8000/api/v1/check \
  -H "Content-Type: application/json" \
  -d '{"question": "I need to refill my blood pressure medication"}'
```

Response includes `response` (answer script), `scenario_id`, `matches`, `safety_triggered`.

See project root **README.md** for full steps and examples.
