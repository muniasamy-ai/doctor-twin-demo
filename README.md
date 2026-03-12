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

- Activate the venv first so `python` is available. If you see `command not found: python`, use **`python3 -m scripts.init_db`** or **`.venv/bin/python -m scripts.init_db`**.
- Use **`python -m uvicorn`** so the venv’s Python (and its installed `psycopg2-binary`, `pgvector`) is used; plain `uvicorn` can cause `ModuleNotFoundError: No module named 'psycopg2'` in the reloader subprocess.
- After updating **`data/scenarios.json`** (e.g. adding scenarios from the Scenario Library), re-run **`python -m scripts.init_db`** to re-seed the RAG index (migrations + embeddings).

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

## Project structure (database)

- **`app/db/`** — Versioned migrations in `app/db/migrations/versions/` (e.g. `001_initial_schema.py`). Run with `python -m scripts.run_migrations` or as part of `init_db`.
- **`app/repositories/`** — DB connection (`engine.py`) and schema/SQL (`models.py`).
- **`scripts/`** — `create_db`, `run_migrations`, `init_db` (migrations + seed), `migrate_db` (export/import).

## Migrating the database

To move or clone the PostgreSQL + pgvector database (e.g. to another server), see **[MIGRATION.md](./MIGRATION.md)**. It covers dump/restore, versioned migrations, and the `scripts/migrate_db.py` export/import helper.
