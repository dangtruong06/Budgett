# Budgett

A full-stack expense tracker: Flask REST API + PostgreSQL on the backend, React on the frontend, fully containerized with Docker Compose.

## Stack

**Backend** — Python 3.12, Flask (app factory pattern), SQLAlchemy 2.0, PostgreSQL, Flask-Migrate, JWT auth, bcrypt, pytest
**Frontend** — React (Vite), React Router, Axios, Tailwind
**Infra** — Docker Compose (backend, frontend, Postgres), GitHub Actions CI

## Run it

Only Docker required — no local Python, Node, or Postgres setup.

```bash
git clone https://github.com/dangtruong06/Budgett.git
cd Budgett
cp .env.example .env
docker compose up --build
```

Visit `http://localhost:8080`. Migrations run automatically on backend startup — nothing else to configure.

**What's running:**
- `frontend` — React build served by nginx, which reverse-proxies `/api` to the backend (no CORS needed)
- `backend` — Flask + gunicorn, runs `flask db upgrade` before boot
- `db` — Postgres with a persistent volume and healthcheck; backend waits for it to actually accept connections, not just for the container to start

## API

| Method | Route | Notes |
|---|---|---|
| POST | `/api/register` | |
| POST | `/api/login` | Returns JWT |
| GET | `/api/expenses` | `?category=&start_date=&end_date=&page=` |
| GET/PUT/DELETE | `/api/expenses/<id>` | Ownership-checked — 403 if it's not yours |
| POST | `/api/expenses` | |

## Testing

```bash
cd backend
pytest -v
```

Runs against an isolated in-memory SQLite DB (`TestConfig`) — never touches real data. Covers auth (success/failure), full CRUD per route (success/404/403), and category/date-range filtering. Two-user fixtures (`auth_headers`/`other_auth_headers`) specifically test that users can't touch each other's expenses.

CI runs this suite on every push and PR via GitHub Actions.

## Local dev (without Docker)

**Backend**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt --break-system-packages
```
Create `backend/.env` from `.env.example`, then:
```bash
flask db upgrade
python main.py   # http://localhost:5001
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

## Structure
backend/
├── main.py # app factory, routes
├── models.py # User, Expense
├── extensions.py # db = SQLAlchemy(), kept separate to avoid circular imports
├── config.py # Config (dev/prod) + TestConfig (in-memory SQLite)
├── entrypoint.sh # runs migrations, then starts gunicorn
├── migrations/
└── tests/

frontend/src/
├── api/axios.js # JWT auto-attached via interceptor
├── context/AuthContext.jsx
├── pages/ # Landing, Login, Register, Dashboard, ExpenseForm
└── components/ # Navbar, ProtectedRoute

.github/workflows/ # CI
docker-compose.yml
