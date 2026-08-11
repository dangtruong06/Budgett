# Budgett

A full-stack expense tracker with a Flask REST API, PostgreSQL, and a React frontend, featuring JWT authentication, filtering, pagination, and a tested backend.

## Features

- **Auth** — register/login with hashed passwords (bcrypt) and JWT-based sessions
- **Expense CRUD** — create, view, edit, and delete expenses, each scoped and ownership-checked per user
- **Filtering** — filter expenses by category and/or date range via query params
- **Pagination** — server-side pagination (10 per page), with full metadata (`total`, `total_pages`) returned alongside results
- **Dashboard** — summary cards (spent this month, entry count, top category), a category/date filter bar, and a numbered pagination control
- **Protected routes** — logged-out users are redirected to login on the frontend; the backend enforces auth independently via `@jwt_required()`
- **Automated tests** — a pytest suite covering auth, full CRUD (including ownership/403 and not-found/404 paths), and filtering
- **CI** — GitHub Actions automatically runs the test suite on every push

## Tech Stack

**Backend:** Python 3.12, Flask, PostgreSQL, SQLAlchemy 2.0, Flask-Migrate, Flask-JWT-Extended, bcrypt, Flask-CORS, pytest

**Frontend:** React (Vite), React Router, Axios, Tailwind CSS

## Project Structure

```
budgett/
├── backend/
│   ├── main.py            # app factory, all routes
│   ├── models.py          # User, Expense models
│   ├── extensions.py      # db = SQLAlchemy(), decoupled from the app instance
│   ├── config.py          # Config (dev/prod) and TestConfig (in-memory SQLite)
│   ├── migrations/
│   └── tests/
│       ├── conftest.py    # shared fixtures: app, client, auth_headers
│       ├── test_auth.py
│       ├── test_create.py
│       ├── test_get.py
│       ├── test_update.py
│       └── test_delete.py
├── frontend/
│   └── src/
│       ├── api/axios.js         # configured axios instance, auto-attaches JWT
│       ├── context/AuthContext.jsx
│       ├── pages/                # LandingPage, LoginPage, RegisterPage, Dashboard, ExpenseForm
│       └── components/           # Navbar, ProtectedRoute
└── .github/workflows/            # CI config
```

## API Overview

| Method | Route | Description |
|---|---|---|
| POST | `/api/register` | Create a new user |
| POST | `/api/login` | Authenticate, returns a JWT |
| GET | `/api/expenses` | List expenses for the logged-in user. Supports `?category=`, `?start_date=`, `?end_date=`, `?page=` |
| GET | `/api/expenses/<id>` | Get a single expense |
| POST | `/api/expenses` | Create an expense |
| PUT | `/api/expenses/<id>` | Update an expense (partial updates supported) |
| DELETE | `/api/expenses/<id>` | Delete an expense |

All `/api/expenses*` routes require a valid JWT and return `403` if the requested expense doesn't belong to the authenticated user.

### Example: list with filters

```
GET /api/expenses?category=Food&start_date=2026-08-01&end_date=2026-08-31&page=1
```

```json
{
  "expenses": [ ... ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 23,
    "total_pages": 3
  }
}
```

## Getting Started

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt --break-system-packages
```

Create a `.env` file in `backend/`:

```
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/budgett
JWT_SECRET_KEY=<your-secret>
```

Run migrations, then start the server:

```bash
flask db upgrade
python main.py
```

The API runs on `http://localhost:5001`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Running tests

```bash
cd backend
pytest -v
```

Tests run against an isolated in-memory SQLite database (`TestConfig`), so they never touch your real Postgres data.

## Testing

The backend is covered by a pytest suite using Flask's app factory pattern to spin up an isolated test app per test, with `db.create_all()` building a fresh schema each time. Key fixtures:

- `client` — a Flask test client for making fake HTTP requests
- `auth_headers` / `other_auth_headers` — register + log in two distinct users, returning ready-to-use JWT auth headers, used to test ownership boundaries (e.g. confirming a 403 when User B tries to access User A's expense)

Coverage includes registration/login (success and failure paths), full CRUD per route (success, 404, and 403 cases), and category/date-range filtering on the list endpoint.

## CI

A GitHub Actions workflow runs the full pytest suite on every push, so regressions are caught automatically before merging.

