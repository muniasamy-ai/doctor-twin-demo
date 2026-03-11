# Database migration guide (PostgreSQL + pgvector)

This project uses **PostgreSQL** with the **pgvector** extension. The main table is `scenario_chunks` (vector embeddings + metadata). Schema changes are managed by **versioned migrations** in `app/db/migrations/versions/` (e.g. `001_initial_schema.py`). Run migrations with `python -m scripts.run_migrations` or as part of `python -m scripts.init_db`.

## Current schema (reference)

- **Extension:** `vector` (pgvector)
- **Table:** `scenario_chunks`  
  - Columns: `id`, `scenario_id`, `intent`, `risk`, `trigger`, `script`, `actions` (JSONB), `hard_stop`, `metadata` (JSONB), `chunk_text`, `embedding` (vector(1536)), `created_at`
  - Index: `idx_scenario_chunks_embedding` (IVFFlat for cosine similarity)

---

## How to migrate database tables

### Option 1: Full database dump and restore (recommended for moving DB)

Use PostgreSQL’s native tools to copy the whole database (schema + data + extension usage).

**1. Export from source (e.g. old server or current DB):**

```bash
# Full dump (schema + data); use same PostgreSQL major version on target
pg_dump -h SOURCE_HOST -p 5432 -U USER -d scenario_rag -F c -f scenario_rag.dump

# Or custom format with compression (good for large DBs)
pg_dump -h SOURCE_HOST -p 5432 -U USER -d scenario_rag -F c -Z 6 -f scenario_rag.dump
```

**2. Create the target database and restore:**

```bash
# On target server: create empty DB (extension will be created during restore if you use -d scenario_rag and restore into it)
createdb -h TARGET_HOST -p 5432 -U USER scenario_rag

# Restore (this restores schema, data, and extension creation)
pg_restore -h TARGET_HOST -p 5432 -U USER -d scenario_rag -v scenario_rag.dump
```

**3. Point the app to the new DB:**

Set `DATABASE_URL` in `.env` to the new host/port/database (e.g. `postgresql://USER:PASSWORD@TARGET_HOST:5432/scenario_rag`).

---

### Option 2: Schema-only + re-seed from scenarios (fresh install)

If you only need the **table structure** on a new database and will re-build embeddings from `data/scenarios.json`:

**1. Create the database:**

```bash
cd src
source .venv/bin/activate
python -m scripts.create_db
```

(Or create the DB manually and set `DATABASE_URL` in `.env`.)

**2. Run migrations and seed:**

```bash
python -m scripts.init_db
```

This runs all pending migrations (e.g. `001_initial_schema.py`: extension + `scenario_chunks` table), then seeds from `data/scenarios.json`. To run migrations only (no seed): `python -m scripts.run_migrations`.

---

### Option 3: Export schema + data as SQL (portable)

If you want a single SQL file (e.g. to version or run on another host without `pg_restore`):

**1. Export schema and data:**

```bash
pg_dump -h SOURCE_HOST -p 5432 -U USER -d scenario_rag --no-owner --no-acl -f scenario_rag.sql
```

**2. On the target server:**

```bash
createdb -h TARGET_HOST -U USER scenario_rag
psql -h TARGET_HOST -U USER -d scenario_rag -f scenario_rag.sql
```

Then set `DATABASE_URL` to the new connection string.

---

### Option 4: Run the migration script (export/import)

A small helper script is provided to export and import schema + data via SQL files, so you can migrate without using `pg_dump`/`pg_restore` on the same machine.

**Export (from current DB):**

```bash
cd src
source .venv/bin/activate
python -m scripts.migrate_db export migration_backup.sql
```

**Import (into a new DB):**

1. Create the target database and set `DATABASE_URL` in `.env` to point to it.
2. Run:

```bash
python -m scripts.migrate_db import migration_backup.sql
```

See `scripts/migrate_db.py` for details.

---

## Folder structure (production-grade)

```
app/
├── db/                          # Migrations
│   ├── __init__.py              # run_migrations()
│   └── migrations/
│       ├── env.py               # Migration runner (discovers versions, tracks in schema_migrations)
│       └── versions/
│           ├── 001_initial_schema.py   # pgvector extension + scenario_chunks
│           └── 002_...py               # Add new migrations here
├── repositories/                # Database access
│   ├── engine.py                # get_connection(), EMBEDDING_DIM
│   └── models.py                # ScenarioRow, SCENARIOS_TABLE, INSERT/SELECT SQL
├── core/                        # Config (get_settings, SCENARIOS_JSON_PATH)
├── models/                      # Re-exports ScenarioRow, scenario_from_row from repositories
└── ...
scripts/
├── create_db.py                # Create DB if missing
├── run_migrations.py            # Run pending migrations only
├── init_db.py                  # Migrations + seed from scenarios.json
└── migrate_db.py               # Export/import full dump (pg_dump/psql)
```

## Changing the schema in the future

1. Add a new file under `app/db/migrations/versions/` with a higher number, e.g. `002_add_foo_column.py`.
2. Implement a single function: `def upgrade(conn):` that runs the SQL (e.g. `ALTER TABLE scenario_chunks ADD COLUMN ...`).
3. Run `python -m scripts.run_migrations` (or redeploy); the runner applies only pending versions and records them in `schema_migrations`.
4. Update `app/repositories/models.py` if you add columns or tables used by the app.

---

## Checklist for migrating to a new server

- [ ] Install PostgreSQL and pgvector on the target server.
- [ ] Create the database (e.g. `createdb scenario_rag` or `python -m scripts.create_db` with new `DATABASE_URL`).
- [ ] Either:
  - **Restore:** `pg_restore -d scenario_rag scenario_rag.dump`, or  
  - **Migrations + re-seed:** run `python -m scripts.run_migrations` then `python -m scripts.init_db`, or just `python -m scripts.init_db` (runs migrations then seeds; ensure `data/scenarios.json` is present).
- [ ] Set `DATABASE_URL` in `.env` to the new host/database.
- [ ] Run the API and test `/api/v1/check` (and any other endpoints) against the new DB.

---

## Production considerations

- **Backup before import**  
  Import overwrites or conflicts with existing data. Take a backup of the target DB first (e.g. `pg_dump` or `migrate_db export`) if it already has data.

- **Credentials**  
  Use `DATABASE_URL` from the environment (e.g. CI/secrets). For passwords with special characters, percent-encode them in the URL. The migration script uses `PGPASSWORD` only for the subprocess and does not log the URL.

- **Import atomicity**  
  `scripts/migrate_db.py` runs `psql` with `--single-transaction` and `ON_ERROR_STOP=1`, so the import is all-or-nothing and stops on first SQL error.

- **Dump storage**  
  Do not commit `.sql`/`.dump` files that contain real data to version control. Store backups in a secure, access-controlled location.

- **PostgreSQL client tools**  
  The migration script requires `pg_dump` and `psql` on `PATH`. On minimal or container images, install the PostgreSQL client package (e.g. `postgresql-client`).

- **Logging**  
  The script logs to stderr with standard `logging`; you can redirect or adjust log level via the environment (e.g. `LOG_LEVEL=DEBUG`) if you add level configuration.
