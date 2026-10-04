# Aegis — Architecture Reference

> **Status as of:** October 2026
> This document reflects the **actual implemented state** of the codebase, not aspirational design. Future and planned items are clearly labeled.

---

## System Overview

```
Browser (Next.js)
        │
        │  HTTP / JSON + JWT
        ▼
FastAPI Backend  (port 8000)
  ├── Auth Layer       → JWT + bcrypt
  ├── API Routers      → /api/v1/...
  ├── ORM Layer        → SQLAlchemy
  ├── SQLite DB        → aegis.db
  ├── Security Engine  → [M5 — not yet implemented]
  │    ├── Nmap
  │    ├── WhatWeb
  │    ├── Gobuster
  │    └── Nuclei
  └── AI Service       → [M6 — not yet implemented]
       └── Ollama (local)
```

---

## Frontend

### Framework & Libraries

| Package         | Version  | Role                              |
|-----------------|----------|-----------------------------------|
| Next.js         | 16.2.10  | React framework, App Router        |
| React           | 19.2.4   | UI rendering                      |
| TypeScript      | 5.x      | Type safety                       |
| Tailwind CSS    | 4.x      | Utility-first styling             |
| shadcn/ui       | 4.x      | Component library (base-ui based) |
| Framer Motion   | 12.x     | Animations                        |
| next-themes     | 0.4.x    | Dark/light theme support          |
| lucide-react    | 1.x      | Icon library                      |

### Route Structure (App Router)

```
src/app/
├── layout.tsx              # Root layout
├── page.tsx                # Landing page (/)
├── not-found.tsx           # 404 page
├── globals.css             # Global styles
├── (auth)/                 # Auth route group (no sidebar)
│   ├── layout.tsx
│   ├── login/page.tsx      # Login form — partially connected to backend
│   └── register/page.tsx   # Register form — partially connected to backend
├── dashboard/
│   └── page.tsx            # Dashboard — static/mock data
├── investigation/
│   └── [id]/               # Investigation detail — static/mock data
├── case/
│   └── [id]/               # Case detail — static/mock data
├── report/
│   └── [id]/               # Report — static/mock data
└── settings/
    └── page.tsx            # Settings — static UI only
```

### Components

```
src/components/
├── auth/           # Auth-specific components
├── case/           # Case page components
├── dashboard/      # Dashboard components
├── investigation/  # Investigation page components
├── landing/        # Landing page sections
├── layout/         # Sidebar, topbar, shell
├── shared/         # Shared/reusable components
└── ui/             # shadcn/ui primitives (Button, Card, Input, etc.)
```

### State & Data

- **Auth state**: JWT token stored in `localStorage` under `aegis_token`
- **API client**: `src/lib/api.ts` — `fetchWithAuth()` appends Bearer token to all requests; redirects to `/login` on 401
- **Mock data**: `src/lib/mock-data.ts` — used by all pages except login/register, which hit the real API
- **No global state manager** (Zustand/Context) yet — pages use local state and mock data

### Auth Flow (Current State)

```
Login page → POST /api/v1/login (form-encoded) → JWT stored in localStorage
Register page → POST /api/v1/register (JSON) → redirect to login
fetchWithAuth() → reads token → adds Authorization: Bearer header
```

**Not yet implemented:**
- Route protection (middleware or client-side guards)
- Session persistence beyond token in localStorage
- Logout button connected to API
- User context provider

---

## Backend

### Framework & Libraries

| Package             | Role                              |
|---------------------|-----------------------------------|
| FastAPI             | Web framework, OpenAPI docs       |
| uvicorn             | ASGI server                       |
| SQLAlchemy          | ORM                               |
| Alembic             | Database migrations               |
| pydantic            | Data validation, settings         |
| pydantic-settings   | Config from environment           |
| passlib[bcrypt]     | Password hashing                  |
| python-jose         | JWT creation and verification     |
| python-multipart    | Form data parsing (login)         |
| email-validator     | Email validation in Pydantic      |

### Application Layout

```
backend/
├── main.py                  # FastAPI app creation, CORS, router registration, table creation
├── requirements.txt
├── .env.example
├── alembic.ini
├── alembic/
│   ├── env.py               # Alembic env config (reads DATABASE_URL)
│   └── versions/            # Migration files (currently empty — tables created via create_all)
└── app/
    ├── api/
    │   ├── deps.py           # SessionDep, TokenDep, CurrentUser, get_current_user
    │   ├── endpoints.py      # Main router — aggregates sub-routers
    │   └── routers/
    │       ├── auth.py       # POST /register, POST /login
    │       └── users.py      # GET /users/me
    ├── core/
    │   ├── config.py         # Settings (pydantic-settings, reads .env)
    │   └── security.py       # create_access_token, verify_password, get_password_hash
    ├── database/
    │   ├── base.py           # DeclarativeBase
    │   └── session.py        # engine, SessionLocal, get_db()
    ├── models/               # SQLAlchemy ORM models
    │   ├── user.py
    │   ├── project.py
    │   ├── investigation.py
    │   ├── finding.py
    │   └── report.py
    ├── schemas/              # Pydantic schemas
    │   └── user.py           # UserBase, UserCreate, UserLogin, UserResponse, Token, TokenData
    ├── services/             # Business logic (empty — M4+)
    └── utils/                # Utility functions (empty)
```

### Configuration (`app/core/config.py`)

All configuration is loaded from environment variables via `pydantic-settings`. Falls back to `.env` file.

| Setting                     | Default                          |
|-----------------------------|----------------------------------|
| `APP_NAME`                  | `Aegis`                          |
| `DATABASE_URL`              | `sqlite:///./aegis.db`           |
| `JWT_SECRET_KEY`            | *(hardcoded dev default)*        |
| `JWT_ALGORITHM`             | `HS256`                          |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080` (7 days)               |
| `OLLAMA_BASE_URL`           | `http://localhost:11434`         |
| `OLLAMA_MODEL`              | `llama3`                         |
| `API_PREFIX`                | `/api/v1`                        |

### Authentication Flow

```
POST /api/v1/login (form: username, password)
        │
        ├── Query User by email
        ├── verify_password (bcrypt)
        ├── create_access_token (JWT, 7d expiry)
        └── Return { access_token, token_type }

Protected route dependency:
        GET /api/v1/users/me
        │
        └── CurrentUser = Annotated[User, Depends(get_current_user)]
                │
                ├── Extract Bearer token from Authorization header
                ├── Decode JWT → extract email (sub)
                ├── Query User by email
                └── Return User or 401
```

### Implemented API Endpoints

| Method | Path                    | Auth | Status    |
|--------|-------------------------|------|-----------|
| GET    | `/`                     | No   | ✅ Done   |
| GET    | `/health`               | No   | ✅ Done   |
| GET    | `/api/v1/`              | No   | ✅ Done   |
| GET    | `/api/v1/health`        | No   | ✅ Done   |
| POST   | `/api/v1/register`      | No   | ✅ Done   |
| POST   | `/api/v1/login`         | No   | ✅ Done   |
| GET    | `/api/v1/users/me`      | Yes  | ✅ Done   |

---

## Database

### Engine

- SQLite (`aegis.db` in `backend/`) for the MVP
- SQLAlchemy is configured to support PostgreSQL with a URL swap
- Tables are created via `Base.metadata.create_all()` on startup (no Alembic migrations run yet)

### ORM Models

```
User
  id, name, email, hashed_password, created_at, updated_at
  → has many: Project

Project
  id, user_id (FK→User), name, description, created_at, updated_at
  → belongs to: User
  → has many: Investigation

Investigation
  id, project_id (FK→Project), target, investigation_profile,
  status, started_at, completed_at, duration
  → belongs to: Project
  → has many: Finding, Report

Finding
  id, investigation_id (FK→Investigation), title, category,
  severity, summary, evidence, recommendation, references (JSON)
  → belongs to: Investigation

Report
  id, investigation_id (FK→Investigation), ... (schema defined but minimal)
  → belongs to: Investigation
```

### Status

- ✅ ORM models defined and mapped
- ✅ Tables auto-created on startup
- ⚠️ Alembic migrations directory exists but no versions written — schema changes require `drop_all` + `create_all` in dev
- ⏳ No CRUD endpoints for Project, Investigation, Finding, Report yet (M4)

---

## Security Engine (Planned — M5)

Not yet implemented. Design intent:

```
backend/app/
└── engine/
    ├── base.py          # Abstract scanner interface
    ├── nmap.py          # Nmap adapter
    ├── whatweb.py       # WhatWeb adapter
    ├── gobuster.py      # Gobuster adapter
    └── nuclei.py        # Nuclei adapter
```

Each adapter will:
1. Accept a validated target and scan config
2. Execute the tool as a subprocess with controlled arguments (no shell injection)
3. Parse stdout/stderr output
4. Return normalized findings in Aegis's internal format

---

## AI Service (Planned — M6)

Not yet implemented. Design intent:

```
backend/app/
└── ai/
    └── ollama.py        # Ollama client wrapper
```

Will:
- Connect to Ollama at `OLLAMA_BASE_URL` using `OLLAMA_MODEL`
- Accept structured findings from the security engine
- Return AI-generated explanations, attack stories, and remediation advice
- **Never invent findings** — analysis is strictly based on real evidence

---

## Known Gaps & TODOs

| Area               | Gap                                                  |
|--------------------|------------------------------------------------------|
| Frontend           | All pages except login/register use mock data        |
| Frontend           | No route protection middleware                       |
| Frontend           | No auth context / persistent session beyond token    |
| Backend            | No CRUD for Project, Investigation, Finding, Report  |
| Backend            | CORS is `allow_origins=["*"]` — not production-safe  |
| Backend            | Alembic has no migration versions                    |
| Backend            | `JWT_SECRET_KEY` hardcoded dev default               |
| Security Engine    | Not implemented                                      |
| AI Service         | Not implemented                                      |
| Docker             | Not implemented                                      |
