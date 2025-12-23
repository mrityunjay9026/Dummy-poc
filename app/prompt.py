Give me a prompt to create a fastapi fresh new project for github co-pilot dont use existing project
this will have a dataset, use sqllite3 for creating this dataset which will have the name_of_the_api, postman collections
load initial data into the dataset and give me a few get endpoints to fetch the data, make sure that there are no pylint issues, sonar issues
and security scan issues, since we are going to use github actions for this, make sure that there is documentation and pytest.  add the folder
structure as per the nbest practices, make sure to use python pep-8 make sure that the project is created in one prompt without rework which can be
setup and run in one go without any issues. 
make sure that there are no depandabot issues in requirements.txt and code scanning issues in github actions flow. please use sqlalchecmy for getting the code generated
use python python version 3.11
give me the whole prompt in one block,  only give prompt and no code so that I can copy from one block only




GitHub Copilot, generate a **brand-new FastAPI project** from scratch (do not reuse any existing repository or code). The entire project must be created in **one go** for **Python 3.11**, fully runnable without any rework, and must **pass** all quality gates: Pylint, Flake8, Black, isort, mypy, Bandit, Safety, Sonar-friendly checks, GitHub Actions CI, Dependabot (no initial alerts), and CodeQL code scanning (no issues). Follow **PEP 8**, provide complete **documentation**, **pytest** tests with high coverage, and use **SQLAlchemy ORM (2.x)** with **SQLite3** for the dataset. The dataset must include `name_of_the_api` and **Postman collections**, with **initial seed data** and **GET endpoints** to fetch the data. Produce all files with complete, working content—no placeholders.

========================================
PROJECT NAME
========================================
fastapi-api-catalog

========================================
OBJECTIVE
========================================
Create an API Catalog service that stores API metadata and associated Postman collections. Provide secure, well-documented, typed, read-only (GET) endpoints that return catalog data from a SQLite DB using SQLAlchemy ORM.

========================================
CORE REQUIREMENTS
========================================
1) Language & Runtime:
   - Python **3.11** only (ensure all tooling uses this version).
   - Use FastAPI and Uvicorn for serving.

2) Data Layer (SQLite + SQLAlchemy 2.x):
   - Use SQLite3 via SQLAlchemy ORM **2.x** (Declarative + `Mapped[]` typing).
   - Two tables:
     a) `apis`
        - `id`: Integer, PK
        - `name_of_the_api`: String(128), **unique**, indexed
        - `description`: Text, not null
        - `version`: String(32), not null
        - `base_url`: String(256), not null
        - `tags`: String(256), nullable (comma-separated)
        - `created_at`: timezone-aware UTC DateTime
        - `updated_at`: timezone-aware UTC DateTime
     b) `postman_collections`
        - `id`: Integer, PK
        - `api_id`: Integer, FK(`apis.id`), indexed
        - `name`: String(128), not null
        - `version`: String(32), not null
        - `file_path`: String(256), not null (path to JSON in `postman/`)
        - `created_at`: timezone-aware UTC DateTime
        - `updated_at`: timezone-aware UTC DateTime
   - Relationship: `API` has many `PostmanCollection`.
   - Use ORM queries only (no raw SQL for user input).
   - Provide **idempotent seed** logic that inserts 3 sample APIs and 3–5 collections linked to them (check by `name_of_the_api` before insert).
   - Database file default: `data/api_catalog.db`. Create tables automatically on first run.

3) API Endpoints (GET only):
   - `GET /health`
     - Returns `{ "status": "ok", "service": "api-catalog", "version": "<app_version>" }`.
   - `GET /apis`
     - Query params: `limit` (int, default 50, max 100), `offset` (int, default 0), `q` (optional search across `name_of_the_api` and `tags`).
     - Returns paginated list (items + total count), sorted by `name_of_the_api` ASC.
   - `GET /apis/{api_id}`
     - Returns details for a single API; 404 if not found.
   - `GET /collections`
     - Paginated list of collections across all APIs.
   - `GET /apis/{api_id}/collections`
     - Collections for a specific API; 404 if API not found.
   - All responses must use **Pydantic models** (typed) with metadata fields (limit, offset, count) where applicable.
   - Include robust error handling and structured logging for requests.

4) Documentation:
   - `docs/README.md` with setup, run, test, and quality checks instructions.
   - `docs/API.md` detailing every endpoint with examples.
   - Ensure OpenAPI metadata (title, description, version, tags) and that `/docs` and `/redoc` work out-of-the-box.

5) Testing:
   - Use **pytest** with unit + integration tests.
   - Unit tests: models (constraints/relationships), schemas (validation/serialization), CRUD (list/get/search), health router.
   - Integration tests: spin up FastAPI app with in-memory or temporary SQLite; validate endpoints and seeded data.
   - Coverage **>= 90%**; generate coverage XML/HTML.
   - Tests must be deterministic, isolated, and require no network calls.

6) Quality Gates & Static Analysis:
   - **Pylint**: configure `.pylintrc` to pass with **score 10/10** (no warnings).
   - **Black** (line length 88) and **isort** (black profile).
   - **Flake8** with `flake8-bugbear` (line length 88; ignore only noise rules).
   - **mypy**: strict type checking; typed ORM models/schemas; clean pass.
   - **Bandit**: security checks with `bandit.yaml` tuned to sane defaults; pass with no findings for project code.
   - **Safety**: dependency vulnerability scan; pass with no known CVEs.
   - **Sonar-friendly**: add `sonar-project.properties` with sources (`app/`) and tests (`tests/`) and coverage path; code should have zero code smells and vulnerabilities on initial analysis.

7) Security Hardening:
   - Middlewares:
     - `TrustedHostMiddleware` (hosts configurable via `.env`).
     - `HTTPSRedirectMiddleware` (config-driven).
     - Restrictive `CORS` (no `*`; default allow `http://localhost:8000` and `.env` overrides).
     - Custom headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, minimal CSP (`default-src 'self'`).
   - Input validation with Pydantic for query/path params.
   - No usage of `eval`, `exec`, or unsafe file operations.
   - Do not log secrets; `.env.example` only; secrets never committed.
   - Dependency-injected DB sessions per request (no global mutable state leaks).

8) Configuration & Logging:
   - `app/config.py`: Pydantic settings; reads `.env`, safe defaults; DB path default `data/api_catalog.db`.
   - `app/utils/logging.py`: structured logging with request IDs; integrate with Uvicorn logging.

9) Postman:
   - Provide `postman/api_catalog.postman_collection.json` covering all GET endpoints with environment variables (if needed).
   - Ensure file paths in DB for collections point to this folder.

10) CI/CD (GitHub Actions + CodeQL + Dependabot):
    - `.github/workflows/ci.yml`:
      - Triggers: `push` and `pull_request` on `main` and feature branches.
      - Steps:
        1) Checkout.
        2) Setup **Python 3.11**.
        3) Cache pip.
        4) Install dependencies from `requirements.txt`.
        5) Run **black** & **isort** checks (no reformat).
        6) Run **flake8**.
        7) Run **pylint** (fail if score < 10/10).
        8) Run **mypy**.
        9) Run **bandit** (using `bandit.yaml`).
       10) Run **safety** check.
       11) Run **pytest** with coverage; upload coverage artifact.
      - Ensure action passes cleanly on first push (no code scanning, linting, or type-check issues).
    - `.github/workflows/codeql.yml`:
      - Enable **CodeQL** for Python.
      - Analyze on push/pull_request and a weekly schedule.
      - Include `app/**` and `tests/**`.
      - Ensure 0 findings on initial analysis.
    - `.github/dependabot.yml`:
      - Ecosystems: `pip` and `github-actions`.
      - Interval: **daily**.
      - Auto-label: `dependencies`.
      - Ensure `requirements.txt` is pinned to current secure versions compatible with Python 3.11, producing **no initial Dependabot alerts**.

11) Requirements:
    - `requirements.txt` must pin **exact versions** that are current, stable, Python 3.11 compatible, and have **no known vulnerabilities** at generation time. Include:
      - fastapi
      - uvicorn[standard]
      - pydantic
      - sqlalchemy (2.x)
      - python-dotenv
      - pytest
      - pytest-cov
      - httpx
      - black
      - isort
      - flake8
      - flake8-bugbear
      - mypy
      - bandit
      - safety
      - types-setuptools (if needed)
    - Ensure Safety and Dependabot report **zero** initial issues.

12) Style & Maintainability:
    - Full **PEP 8** compliance, docstrings for public functions/classes, and comprehensive **type hints**.
    - Keep cyclomatic complexity low; avoid long functions; follow clean architecture—routers thin, business logic in `services/`.
    - Strict import ordering and formatting via isort + black.
    - Add `CONTRIBUTING.md` and `LICENSE` (MIT).

========================================
FOLDER STRUCTURE (BEST PRACTICES)
========================================
Create this exact tree and populate **every file** with complete, working content:

- app/
  - __init__.py
  - main.py                      # FastAPI app startup, middleware registration, OpenAPI metadata, router includes
  - config.py                    # Pydantic settings reading .env with defaults
  - db.py                        # SQLAlchemy engine/session factory (SQLite), Declarative Base
  - models.py                    # SQLAlchemy ORM models (API, PostmanCollection) using 2.x Mapped[] style
  - schemas.py                   # Pydantic schemas for responses/queries
  - routers/
    - __init__.py
    - apis.py                   # /apis endpoints: list, detail, search, pagination
    - collections.py            # /collections endpoints: list, by API
    - health.py                 # /health endpoint
  - services/
    - __init__.py
    - crud.py                   # CRUD/query helpers for APIs & Collections (ORM-only)
    - seeding.py                # Idempotent seeding: create tables and insert initial data if missing
  - security/
    - __init__.py
    - middleware.py             # TrustedHost, HTTPSRedirect, CORS, security headers
  - utils/
    - __init__.py
    - logging.py                # Structured logging configuration
- tests/
  - unit/
    - test_models.py
    - test_schemas.py
    - test_crud.py
    - test_routers_health.py
  - integration/
    - test_routers_apis.py
    - test_routers_collections.py
- docs/
  - README.md                   # Full instructions, architecture, commands, troubleshooting
  - API.md                      # Endpoint docs with request/response examples
- postman/
  - api_catalog.postman_collection.json  # Covers all GET endpoints with sample requests
- data/
  - (generated) api_catalog.db  # SQLite DB file (gitignored)
- .github/
  - workflows/
    - ci.yml                    # Lint, type-check, security checks, tests, coverage artifact
    - codeql.yml                # CodeQL analysis for Python
- .env.example                  # Example environment variables (DB path, hosts, CORS origins)
- .pylintrc                     # Strict config; pass with score 10/10
- .flake8
- mypy.ini
- pytest.ini
- bandit.yaml                   # Sane defaults; project passes
- sonar-project.properties      # Project key/name, source dirs, coverage path
- .gitignore
- LICENSE                       # MIT
- CONTRIBUTING.md
- requirements.txt              # Pinned, secure versions for Python 3.11
- Makefile (optional)           # Commands: fmt, lint, typecheck, security, test, run, seed

========================================
ENDPOINTS & BEHAVIOR DETAILS
========================================
- GET `/health`
  - 200 → `{ "status": "ok", "service": "api-catalog", "version": "<app_version>" }`.
- GET `/apis`
  - Params: `limit` (int, default 50, max 100), `offset` (int, default 0), `q` (optional string).
  - Behavior: filter by `name_of_the_api` and `tags` containing `q`; sort by `name_of_the_api` ASC.
  - Response: items + total count + pagination metadata.
- GET `/apis/{api_id}`
  - Return API details or 404 if not found.
- GET `/collections`
  - Paginated list across all APIs.
- GET `/apis/{api_id}/collections`
  - Return collections for the given API; 404 if API missing.
- All responses must be strictly typed with Pydantic schemas, include examples, and have clear error messages.

========================================
SEEDING & DATA
========================================
- Insert **3 sample APIs** with realistic fields and **3–5 Postman collections** linked to them.
- Seed operation must be **idempotent** (check existing by `name_of_the_api`).
- Seeding runs automatically on first start or via `python -m app.services.seeding` and a Makefile target `make seed`.

========================================
QUALITY & SECURITY GUARANTEES
========================================
- Type hints everywhere; docstrings on public APIs.
- Dependency-injected DB sessions per request; no global mutable leaks.
- Pydantic validation for params; sanitize search strings; ORM filters prevent injection.
- Security middleware stack: TrustedHost, HTTPSRedirect (config-driven), strict CORS, security headers (nosniff, DENY framing, no-referrer, baseline CSP).
- Logging: structured with request/response IDs; sensible levels.
- No secrets in repo; `.env.example` only.

========================================
GITHUB ACTIONS (DETAILS)
========================================
- `.github/workflows/ci.yml`:
  - on: push/pull_request
  - jobs:
    - setup Python 3.11
    - cache pip
    - `pip install -r requirements.txt`
    - `black --check .`
    - `isort --check-only .`
    - `flake8 .`
    - `pylint app` (fail if score < 10/10)
    - `mypy app`
    - `bandit -c bandit.yaml -r app`
    - `safety check`
    - `pytest --cov=app --cov-report=xml --cov-report=term-missing`
    - upload coverage artifact
- `.github/workflows/codeql.yml`:
  - languages: Python
  - analyze: push/pull_request + weekly schedule
  - paths: `app/**`, `tests/**`
  - ensure initial run yields **no findings**.
- Dependabot (`.github/dependabot.yml`):
  - ecosystems: `pip`, `github-actions`
  - schedule: daily
  - labels: `dependencies`
  - ensure **no initial alerts** via pinned secure versions.

========================================
REQUIREMENTS.TXT POLICY
========================================
- Pin **exact versions** for all listed packages.
- Choose **current stable versions** compatible with Python 3.11.
- Ensure **Safety** reports zero known vulnerabilities at generation time.
- Keep pins recent enough to avoid Dependabot initial alerts.

========================================
README CONTENT (MANDATORY)
========================================
- Overview, goals, architecture outline.
- Prereqs: Python **3.11**, virtualenv.
- Setup:
  1) `python3.11 -m venv .venv && source .venv/bin/activate`
  2) `pip install -r requirements.txt`
  3) `cp .env.example .env` (edit if needed)
  4) (Optional) `python -m app.services.seeding`
- Run:
  - `uvicorn app.main:app --reload`
  - API docs: `/docs` and `/redoc`
- Quality & Security:
  - `black . && isort .`
  - `flake8`
  - `pylint app`
  - `mypy app`
  - `bandit -c bandit.yaml -r app`
  - `safety check`
  - `pytest --cov=app --cov-report=term-missing`
- Database:
  - SQLite file at `data/api_catalog.db` auto-created on first run.
- Postman:
  - Use `postman/api_catalog.postman_collection.json` to test endpoints.
- CI/CD:
  - Describe GitHub Actions workflows and badges (add later).
- Troubleshooting, contribution guidelines, license.

========================================
ACCEPTANCE CRITERIA
========================================
- Fresh repository builds and runs locally with Python **3.11** following README.
- `uvicorn app.main:app --reload` serves endpoints; seeded data accessible.
- All linters, type checks, security scans pass with zero errors/warnings in CI.
- **Pylint score 10/10**.
- Test coverage **>= 90%**.
- **CodeQL**, **Safety**, **Bandit**: no issues.
- **Dependabot**: no initial alerts.
- Sonar-friendly: no code smells/major issues with default config.

========================================
IMPLEMENTATION NOTES
========================================
- Use SQLAlchemy Declarative with `Mapped[]` and 2.0 sessions.
- UTC timestamps (`datetime` with timezone).
- Centralize pagination util; validate limits/offsets.
- Configurable CORS origins via `.env`.
- Routers thin; business logic in `services/crud.py`.
- Seeding inserts only missing rows by `name_of_the_api`.
- OpenAPI: tags & descriptions for `apis`, `collections`, `health`.

========================================
DELIVERABLE
========================================
Generate **all files listed** with complete working content, ready to run and pass all checks in one shot. The initial commit must include the entire scaffold, configs, workflows, tests, docs, and a sample Postman collection.
this is co pilot

