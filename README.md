# Aegis

**AI-Assisted Cybersecurity Investigation Platform**

Aegis combines real security tooling with an AI security copilot to help you discover, understand, investigate, and learn from security vulnerabilities. It is designed to feel like a professional SaaS product — clean, technical, and trustworthy.

---

## Investigation Flow

```
Target → Reconnaissance → Tool Analysis → Findings → AI Explanation → Attack Story → Remediation → Learning → Report
```

Rather than dumping raw scanner output, Aegis transforms findings into structured intelligence — explaining *what* was found, *why* it matters, *how* it could be exploited, and *how to fix it*.

---

## Who It's For

- Cybersecurity students
- Security researchers
- Developers learning application security
- Junior penetration testers
- Security professionals

---

## Tech Stack

| Layer      | Technology                                                         |
|------------|--------------------------------------------------------------------|
| Frontend   | Next.js 16, TypeScript, Tailwind CSS v4, shadcn/ui, Framer Motion |
| Backend    | FastAPI, Python, SQLAlchemy, Alembic                               |
| Database   | SQLite (MVP) → PostgreSQL-ready                                    |
| Auth       | JWT (python-jose), bcrypt (passlib)                                |
| AI         | Ollama (local, configurable)                                       |
| Tools (V1) | Nmap, WhatWeb, Gobuster, Nuclei                                    |
| Infra      | Docker, Docker Compose (M9)                                        |

---

## Project Structure

```
Aegis/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routers/       # auth.py, users.py
│   │   │   ├── deps.py        # JWT auth dependency, DB session
│   │   │   └── endpoints.py   # Router aggregation
│   │   ├── core/              # config.py, security.py
│   │   ├── database/          # SQLAlchemy session and declarative base
│   │   ├── models/            # ORM: User, Project, Investigation, Finding, Report
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── services/          # Business logic layer (M4+, currently empty)
│   │   └── utils/
│   ├── alembic/               # Database migrations
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── src/
│       ├── app/
│       │   ├── (auth)/        # Login, Register pages
│       │   ├── dashboard/     # Dashboard page
│       │   ├── investigation/ # Investigation detail [id]
│       │   ├── case/          # Case/Finding detail [id]
│       │   ├── report/        # Report page [id]
│       │   └── settings/      # Settings page
│       ├── components/        # auth, dashboard, investigation, landing, layout, shared, ui
│       ├── hooks/             # use-sidebar.ts
│       ├── lib/               # api.ts, mock-data.ts, utils.ts
│       └── types/             # TypeScript type definitions
└── docs/
    ├── SSD/                   # System design documents
    ├── architecture.md
    ├── PRD.md
    ├── project_plan.md
    └── tasks.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- Ollama (for AI features — M6)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env — set JWT_SECRET_KEY to a strong random value
uvicorn main:app --reload
```

API at `http://localhost:8000` | Docs at `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App at `http://localhost:3000`

---

## Environment Variables

| Variable                      | Default                          | Notes                                  |
|-------------------------------|----------------------------------|----------------------------------------|
| `APP_NAME`                    | `Aegis`                          |                                        |
| `DATABASE_URL`                | `sqlite:///./aegis.db`           | Swap to `postgresql://` for production |
| `JWT_SECRET_KEY`              | *(insecure dev default)*         | **Must override in production**        |
| `JWT_ALGORITHM`               | `HS256`                          |                                        |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080` (7 days)                 |                                        |
| `OLLAMA_BASE_URL`             | `http://localhost:11434`         |                                        |
| `OLLAMA_MODEL`                | `llama3`                         |                                        |
| `API_PREFIX`                  | `/api/v1`                        |                                        |
| `NEXT_PUBLIC_API_URL`         | `http://localhost:8000/api/v1`   | Frontend env var                       |

> ⚠️ The hardcoded `JWT_SECRET_KEY` in `config.py` is for development only. Always override via `.env` in production.

---

## API Reference

Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint     | Auth | Description           |
|--------|--------------|------|-----------------------|
| GET    | `/`          | No   | Welcome message       |
| GET    | `/health`    | No   | Health check          |
| POST   | `/register`  | No   | Register new user     |
| POST   | `/login`     | No   | Login, returns JWT    |
| GET    | `/users/me`  | Yes  | Current user profile  |

---


---

## Security

- Passwords hashed with bcrypt — never stored in plaintext
- JWT tokens validated on every protected request via `CurrentUser` dependency
- `JWT_SECRET_KEY` must be overridden in production
- CORS is `allow_origins=["*"]` for development — restrict in production
- Users scoped to their own data (enforced in M4+)
- Security tool execution is backend-controlled — no arbitrary command injection via user input

---

## Documentation

- [`docs/architecture.md`](docs/architecture.md) — Architecture reference
- [`docs/PRD.md`](docs/PRD.md) — Product requirements document
- [`docs/project_plan.md`](docs/project_plan.md) — Milestone plan
- [`docs/tasks.md`](docs/tasks.md) — Task tracker
- [`docs/SSD/`](docs/SSD/) — Detailed system design documents
