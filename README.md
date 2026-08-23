# Budgett

A full-stack expense tracker built with a **Flask REST API + PostgreSQL** backend and a **React** frontend, fully containerized with Docker Compose.

## Tech Stack

| Layer              | Technologies                                                                       |
| ------------------ | ---------------------------------------------------------------------------------- |
| **Backend**        | Python, Flask, Google-OAuth, PostgreSQL, Flask-Migrate, JWT, bcrypt, pytest        |
| **Frontend**       | React, Vite, React Router, Axios, Tailwind CSS                                     |
| **Infrastructure** | Docker Compose, Nginx, GitHub Actions CI                                           |

## Getting Started

> **Prerequisite:** Docker must be installed.

```bash
git clone https://github.com/dangtruong06/Budgett.git
cd Budgett
cp .env.example .env
docker compose up --build
```

Once the containers are running, open:

**http://localhost:8080**

### Docker Services

* **`frontend`** — React production build served by Nginx. Reverse-proxies `/api` requests to the backend, eliminating the need for CORS.
* **`backend`** — Flask application served with Gunicorn. Runs database migrations with `flask db upgrade` before starting.
* **`db`** — PostgreSQL database with a persistent volume and healthcheck. The backend waits for PostgreSQL to accept connections before starting.

## 📡 API

| Method   | Endpoint             | Description                                              |
| -------- | -------------------- | -------------------------------------------------------- |
| `POST`   | `/api/register`      | Register a new user                                      |
| `POST`   | `/api/login`         | Authenticate and receive a JWT                           |
| `GET`    | `/api/expenses`      | Retrieve expenses with optional filtering and pagination |
| `POST`   | `/api/expenses`      | Create a new expense                                     |
| `GET`    | `/api/expenses/<id>` | Retrieve a specific expense                              |
| `PUT`    | `/api/expenses/<id>` | Update a specific expense                                |
| `DELETE` | `/api/expenses/<id>` | Delete a specific expense                                |

### Expense Filtering

```text
/api/expenses?category=&start_date=&end_date=&page=
```

All expense operations are **ownership-checked**. Users cannot access or modify another user's expenses; unauthorized access returns `403 Forbidden`.

## Testing

```bash
cd backend
pytest -v
```

The test suite runs against an isolated **in-memory SQLite database** using `TestConfig`, so production data is never touched.

Tests cover:

* Authentication success and failure cases
* Full expense CRUD functionality
* `404 Not Found` handling
* `403 Forbidden` ownership checks
* Category filtering
* Date-range filtering
* Multi-user authorization scenarios

Two-user fixtures (`auth_headers` and `other_auth_headers`) specifically verify that users cannot access each other's expenses.

**GitHub Actions CI** automatically runs the test suite on every push and pull request.

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt --break-system-packages
```

Create `backend/.env` from `.env.example`, then run:

```bash
flask db upgrade
python main.py
```

Backend runs at:

**http://localhost:5001**

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```text
Budgett/
├── backend/
│   ├── main.py                  # App factory and routes
│   ├── models.py                # User and Expense models
│   ├── extensions.py            # SQLAlchemy instance
│   ├── config.py                # Development, production, and test configs
│   ├── entrypoint.sh            # Runs migrations and starts Gunicorn
│   ├── migrations/              # Database migrations
│   └── tests/                   # Backend test suite
│
├── frontend/
│   └── src/
│       ├── api/
│       │   └── axios.js         # Axios client with JWT interceptor
│       ├── context/
│       │   └── AuthContext.jsx  # Authentication state
│       ├── pages/                # Landing, Login, Register, Dashboard, ExpenseForm
│       └── components/           # Navbar, ProtectedRoute
│
├── .github/
│   └── workflows/               # GitHub Actions CI
│
└── docker-compose.yml
```
