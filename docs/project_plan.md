# Aegis — Project Plan

> This plan reflects the actual current state of the project and what needs to be done next.
> Status markers: ✅ Complete | 🔄 In Progress | ⏳ Planned | 🚫 Blocked

---

## Milestone Overview

| # | Milestone                        | Status         |
|---|----------------------------------|----------------|
| 1 | Frontend Foundation              | ✅ Complete    |
| 2 | Backend Foundation               | ✅ Complete    |
| 3 | Authentication                   | 🔄 In Progress |
| 4 | Project & Investigation Management | ⏳ Next      |
| 5 | Security Engine Integration      | ⏳ Planned     |
| 6 | AI Intelligence (Ollama)         | ⏳ Planned     |
| 7 | Reports & Learning Mode          | ⏳ Planned     |
| 8 | Testing & UX Polish              | ⏳ Planned     |
| 9 | Docker & Deployment              | ⏳ Planned     |

---

## M1 — Frontend Foundation ✅

**Goal:** Establish the complete frontend shell with all pages, routing, and component architecture.

**Delivered:**
- Next.js 16 with TypeScript and App Router
- Tailwind CSS v4 + shadcn/ui component library
- Framer Motion for animations
- Dark/light theme support (next-themes)
- Route structure: Landing, Dashboard, Investigation [id], Case [id], Report [id], Settings
- Auth route group: Login, Register
- Component organization: auth/, case/, dashboard/, investigation/, landing/, layout/, shared/, ui/
- Custom hooks: `use-sidebar.ts`
- API client: `fetchWithAuth()` with Bearer token injection and 401 redirect
- Mock data layer (`mock-data.ts`) for all non-auth pages
- TypeScript types defined

**Known gaps from M1:**
- All pages except login/register use static mock data
- No route protection middleware implemented

---

## M2 — Backend Foundation ✅

**Goal:** Establish a working FastAPI backend with database, ORM models, and API structure.

**Delivered:**
- FastAPI application with CORS middleware
- SQLite database (`aegis.db`) via SQLAlchemy
- Declarative ORM base + session management
- All ORM models: User, Project, Investigation, Finding, Report
- Alembic configured (no migration versions yet — tables via `create_all`)
- Configuration via `pydantic-settings` (`.env` support)
- Health check endpoint
- Swagger UI at `/docs`
- `requirements.txt` with all dependencies

**Known gaps from M2:**
- CORS `allow_origins=["*"]` — needs restriction for production
- Alembic has no actual migration files
- `JWT_SECRET_KEY` has an insecure dev default

---

## M3 — Authentication 🔄 In Progress

**Goal:** Complete end-to-end authentication — backend and frontend.

**Backend (✅ Complete):**
- `POST /api/v1/register` — creates user with bcrypt-hashed password
- `POST /api/v1/login` — OAuth2 form login, returns JWT
- `GET /api/v1/users/me` — protected endpoint, returns current user
- `get_current_user` dependency with JWT decode + DB lookup
- `CurrentUser` typed dependency for use in route handlers

**Frontend (🔄 Partial):**
- Login page (`/login`) — connected to real backend API ✅
- Register page (`/register`) — exists, needs backend wiring ⏳
- JWT stored in `localStorage` as `aegis_token` ✅
- Auto-redirect on 401 in `fetchWithAuth()` ✅
- No route protection middleware ⏳
- No auth context / user session across pages ⏳
- No logout functionality ⏳

**Remaining M3 work:**
1. Wire register page to `POST /api/v1/register`
2. Add Next.js middleware for route protection (redirect to `/login` if no token)
3. Create auth context / user hook (`useUser()` or similar)
4. Add logout button that clears token and redirects
5. Verify current user on dashboard load and handle invalid tokens

---

## M4 — Project & Investigation Management ⏳

**Goal:** Full CRUD for Projects and Investigations, replacing all mock data.

**Backend to build:**
- Projects router: `GET /projects`, `POST /projects`, `GET /projects/{id}`, `PUT /projects/{id}`, `DELETE /projects/{id}`
- Investigations router: `GET /projects/{id}/investigations`, `POST /projects/{id}/investigations`, `GET /investigations/{id}`
- Strict ownership: all endpoints must verify `project.user_id == current_user.id`
- Pydantic schemas for Project and Investigation
- Service layer functions in `app/services/`

**Frontend to update:**
- Dashboard: replace mock projects with real API data
- Investigation list: real data per project
- Investigation detail: real data from backend
- New investigation form: connect to create endpoint
- New project form: connect to create endpoint
- Error and loading states for all API calls

**Data model decisions:**
- Investigation status enum: `pending | running | completed | failed`
- Scan profiles defined as constants (Quick / Standard / Deep)
- Target validation (domain / IP / URL format)

---

## M5 — Security Engine Integration ⏳

**Goal:** Execute real security tools and store normalized findings.

**Backend to build:**

```
app/engine/
├── base.py          # Abstract Scanner interface
├── runner.py        # Orchestration: runs multiple scanners for an investigation
├── nmap.py          # Nmap adapter
├── whatweb.py       # WhatWeb adapter
├── gobuster.py      # Gobuster adapter
└── nuclei.py        # Nuclei adapter
```

**Scanner interface (per adapter):**
- `run(target: str, config: dict) → list[NormalizedFinding]`
- Execute via `subprocess` with explicit argument list (no shell=True)
- Parse stdout/stderr
- Return structured finding objects

**Investigation execution flow:**
- `POST /investigations/{id}/run` → triggers async scan execution
- Investigation status updated: `pending → running → completed/failed`
- Each tool runs in sequence (or parallel in future)
- Results stored as `Finding` records in DB

**Security requirements:**
- No shell injection — use `subprocess.run([...], shell=False)`
- Validate and sanitize target before passing to tools
- Tool execution isolated (Docker in M9)
- No arbitrary user-controlled commands

**Tools to implement:**
1. Nmap — port scan, service/version detection
2. WhatWeb — technology fingerprinting
3. Gobuster — directory/content discovery
4. Nuclei — vulnerability template scanning

---

## M6 — AI Intelligence (Ollama) ⏳

**Goal:** Transform raw findings into AI-powered security intelligence.

**Backend to build:**

```
app/ai/
├── client.py        # Ollama HTTP client
└── analyzer.py      # Prompt templates and analysis logic
```

**Analysis per finding:**
- What was discovered
- Why it matters (security impact)
- Potential attack scenarios
- Real-world context / examples
- Remediation recommendations
- Suggested learning resources

**Requirements:**
- AI only analyzes actual collected evidence — never invents findings
- Model configurable via `OLLAMA_MODEL` env var
- Responses stored in DB linked to findings
- Graceful degradation if Ollama is unavailable

**API endpoint:**
- `POST /investigations/{id}/analyze` → triggers AI analysis of all findings

**Frontend updates:**
- Case page: display AI explanation sections
- Investigation detail: AI summary
- Loading state while analysis runs

---

## M7 — Reports & Learning Mode ⏳

**Goal:** Generate structured reports and enable learning-focused presentation.

**Report generation:**
- `POST /investigations/{id}/report` → generates and stores report
- Report sections: Executive Summary, Security Posture, Technology Profile, Attack Surface, Findings, Recommendations, Learning Resources, Appendix
- Report stored in DB, retrievable via `GET /reports/{id}`

**Export formats (priority order):**
1. HTML (in-app view — already has frontend page)
2. PDF (future)
3. Markdown (future)

**Learning Mode:**
- Each finding page explains the vulnerability type in educational context
- Links to external resources (OWASP, CVE, etc.)
- "What to study next" section per finding type

---

## M8 — Testing & UX Polish ⏳

**Goal:** Quality, reliability, and a polished user experience.

**Testing:**
- Backend unit tests (pytest): security functions, service layer, API endpoints
- Frontend component tests: auth forms, dashboard
- Integration tests: full investigation flow (tool → finding → AI)
- Security testing: auth bypass attempts, input validation

**UX Polish:**
- Responsive design audit
- Loading skeletons for all async states
- Error boundary components
- Empty states for all list views
- Notification/toast system for async operations
- Accessibility pass (keyboard nav, ARIA)

**Security hardening:**
- Replace `allow_origins=["*"]` with explicit origins
- Add rate limiting to auth endpoints
- HTTPS enforcement in production config
- Remove hardcoded dev secret

---

## M9 — Docker & Deployment ⏳

**Goal:** Runnable via `docker compose up` with persistent storage.

**Docker setup:**
```
docker-compose.yml
├── backend service     (FastAPI + uvicorn)
├── frontend service    (Next.js)
└── [optional] DB       (if migrating to PostgreSQL)
```

**Dockerfiles:**
- `backend/Dockerfile` — Python, venv, uvicorn
- `frontend/Dockerfile` — Node.js, npm build, Next.js server

**Requirements:**
- Persistent volume for SQLite `aegis.db`
- Environment variables via `.env` file (not baked into image)
- Security tools (Nmap, WhatWeb, Gobuster, Nuclei) installed in backend container
- Ollama reachable from backend container (either as sidecar or external)

---

## Dependency Graph

```
M1 ─┐
    ├──→ M3 (auth) ──→ M4 (CRUD) ──→ M5 (engine) ──→ M6 (AI) ──→ M7 (reports)
M2 ─┘                                                                    │
                                                                         ▼
                                                                   M8 (polish)
                                                                         │
                                                                         ▼
                                                                   M9 (docker)
```

---

## Current Priority

**Right now: complete M3.**

Remaining M3 tasks (in order):
1. Wire register page to backend
2. Add Next.js route protection middleware
3. Add auth context / `useUser()` hook
4. Add logout
5. Session validation on dashboard load
