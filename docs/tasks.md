# Aegis — Task Tracker

> Tasks are grouped by milestone. Within each milestone, tasks are ordered by dependency.
> Status: ✅ Done | 🔄 In Progress | ⏳ Todo | 🚫 Blocked

---

## M3 — Authentication (Current)

### Backend

| # | Task                                               | Status | Notes |
|---|-----------------------------------------------------|--------|-------|
| 3.1 | `POST /register` endpoint                        | ✅ Done | Returns `UserResponse` |
| 3.2 | `POST /login` endpoint (OAuth2 form)             | ✅ Done | Returns JWT token |
| 3.3 | bcrypt password hashing                           | ✅ Done | `passlib[bcrypt]` |
| 3.4 | JWT creation (`create_access_token`)              | ✅ Done | 7-day expiry |
| 3.5 | JWT verification (`get_current_user` dependency)  | ✅ Done | Decodes + DB lookup |
| 3.6 | `CurrentUser` annotated dependency                | ✅ Done | Used in `GET /users/me` |
| 3.7 | `GET /users/me` protected endpoint               | ✅ Done | Returns current user |

### Frontend

| # | Task                                                   | Status       | Notes |
|---|--------------------------------------------------------|--------------|-------|
| 3.8  | Login page UI                                        | ✅ Done      | Uses shadcn Card, Input, Button |
| 3.9  | Login form connected to `POST /api/v1/login`         | ✅ Done      | Stores JWT in localStorage |
| 3.10 | Register page UI                                     | ✅ Done      | UI exists |
| 3.11 | Register form connected to `POST /api/v1/register`   | ⏳ Todo      | Needs API call wiring |
| 3.12 | Error display on login failure                       | ✅ Done      | Shows API error message |
| 3.13 | Loading state on login submit                        | ✅ Done      | "Signing in..." button |
| 3.14 | Redirect to `/dashboard` on successful login         | ✅ Done      | `router.push('/dashboard')` |
| 3.15 | `fetchWithAuth()` — Bearer token injection           | ✅ Done      | `src/lib/api.ts` |
| 3.16 | `fetchWithAuth()` — 401 redirect to login            | ✅ Done      | Clears token, redirects |
| 3.17 | Next.js middleware for route protection              | ⏳ Todo      | Protect `/dashboard`, `/investigation`, `/case`, `/report`, `/settings` |
| 3.18 | Auth context or user hook (`useUser`)                | ⏳ Todo      | Read user from `/users/me`, expose across app |
| 3.19 | Logout functionality                                 | ⏳ Todo      | Clear token, redirect to `/login` |
| 3.20 | Session validation on dashboard load                 | ⏳ Todo      | Verify token still valid on first render |
| 3.21 | Auth layout for login/register pages                 | ✅ Done      | Route group `(auth)/layout.tsx` |

---

## M4 — Project & Investigation Management

### Backend

| # | Task                                                    | Status  | Notes |
|---|---------------------------------------------------------|---------|-------|
| 4.1  | Project Pydantic schemas (Create, Response, Update)  | ⏳ Todo |       |
| 4.2  | `GET /projects` — list user's projects               | ⏳ Todo | Filtered by `current_user.id` |
| 4.3  | `POST /projects` — create project                    | ⏳ Todo |       |
| 4.4  | `GET /projects/{id}` — get single project            | ⏳ Todo | Ownership check |
| 4.5  | `PUT /projects/{id}` — update project                | ⏳ Todo | Ownership check |
| 4.6  | `DELETE /projects/{id}` — delete project             | ⏳ Todo | Cascade to investigations |
| 4.7  | Investigation Pydantic schemas                        | ⏳ Todo |       |
| 4.8  | `GET /projects/{id}/investigations`                  | ⏳ Todo |       |
| 4.9  | `POST /projects/{id}/investigations` — create        | ⏳ Todo | Validate target format |
| 4.10 | `GET /investigations/{id}`                           | ⏳ Todo | Ownership check through project |
| 4.11 | `DELETE /investigations/{id}`                        | ⏳ Todo |       |
| 4.12 | Service layer: `project_service.py`                  | ⏳ Todo | Business logic separate from routes |
| 4.13 | Service layer: `investigation_service.py`            | ⏳ Todo |       |
| 4.14 | Register project + investigation routers in endpoints.py | ⏳ Todo |   |
| 4.15 | Write first Alembic migration version                | ⏳ Todo | Replace `create_all` with proper migrations |

### Frontend

| # | Task                                                    | Status  | Notes |
|---|---------------------------------------------------------|---------|-------|
| 4.16 | Replace mock projects on dashboard with real API     | ⏳ Todo |       |
| 4.17 | Create project modal/form                            | ⏳ Todo |       |
| 4.18 | Delete project with confirmation                     | ⏳ Todo |       |
| 4.19 | Replace mock investigations on investigation list    | ⏳ Todo |       |
| 4.20 | Investigation detail page with real data             | ⏳ Todo |       |
| 4.21 | Create investigation form (target, scan profile)     | ⏳ Todo |       |
| 4.22 | Loading skeletons for project/investigation lists    | ⏳ Todo |       |
| 4.23 | Empty state: no projects                             | ⏳ Todo |       |
| 4.24 | Empty state: no investigations                       | ⏳ Todo |       |
| 4.25 | Error states for API failures                        | ⏳ Todo |       |

---

## M5 — Security Engine

| # | Task                                                       | Status  | Notes |
|---|------------------------------------------------------------|---------|-------|
| 5.1  | Define `BaseScanner` abstract interface                | ⏳ Todo | `app/engine/base.py` |
| 5.2  | Define `NormalizedFinding` internal data model         | ⏳ Todo | Standard format all scanners output |
| 5.3  | Nmap adapter (`nmap.py`)                               | ⏳ Todo | Port scan + service detection |
| 5.4  | WhatWeb adapter (`whatweb.py`)                         | ⏳ Todo | Technology fingerprinting |
| 5.5  | Gobuster adapter (`gobuster.py`)                       | ⏳ Todo | Directory discovery |
| 5.6  | Nuclei adapter (`nuclei.py`)                           | ⏳ Todo | Template-based vulnerability scan |
| 5.7  | Engine runner (`runner.py`)                            | ⏳ Todo | Orchestrates adapters for an investigation |
| 5.8  | `POST /investigations/{id}/run` endpoint               | ⏳ Todo | Triggers async scan |
| 5.9  | Investigation status lifecycle management              | ⏳ Todo | pending → running → completed/failed |
| 5.10 | Store tool results as `Finding` records               | ⏳ Todo | Normalized output to DB |
| 5.11 | Target validation before tool execution               | ⏳ Todo | No shell injection |
| 5.12 | Async scan execution (FastAPI BackgroundTasks or queue) | ⏳ Todo |     |
| 5.13 | Frontend: "Run Investigation" button                  | ⏳ Todo | Triggers scan + shows status |
| 5.14 | Frontend: Real-time status polling or SSE             | ⏳ Todo | Show scan progress |
| 5.15 | Frontend: Display findings from real data             | ⏳ Todo | Replace mock findings |

---

## M6 — AI Intelligence

| # | Task                                                       | Status  | Notes |
|---|------------------------------------------------------------|---------|-------|
| 6.1 | Ollama HTTP client (`app/ai/client.py`)                 | ⏳ Todo | Uses `OLLAMA_BASE_URL` + `OLLAMA_MODEL` |
| 6.2 | Prompt templates for finding analysis                  | ⏳ Todo | Per finding type |
| 6.3 | `POST /investigations/{id}/analyze` endpoint           | ⏳ Todo | Triggers AI analysis of all findings |
| 6.4 | AI response schema + DB storage                        | ⏳ Todo | Store per finding |
| 6.5 | Finding schema: add AI analysis fields                 | ⏳ Todo | explanation, attack_scenario, remediation, resources |
| 6.6 | Graceful degradation when Ollama unavailable           | ⏳ Todo | Don't crash investigation |
| 6.7 | Frontend: Case page — display AI explanation sections | ⏳ Todo |       |
| 6.8 | Frontend: Investigation — AI summary section          | ⏳ Todo |       |
| 6.9 | Frontend: Loading state for AI analysis               | ⏳ Todo |       |

---

## M7 — Reports & Learning Mode

| # | Task                                                       | Status  | Notes |
|---|------------------------------------------------------------|---------|-------|
| 7.1 | Report ORM model (expand existing model)               | ⏳ Todo |       |
| 7.2 | Report Pydantic schemas                                | ⏳ Todo |       |
| 7.3 | `POST /investigations/{id}/report` — generate report   | ⏳ Todo | Aggregates findings + AI |
| 7.4 | `GET /reports/{id}` — retrieve report                 | ⏳ Todo |       |
| 7.5 | Report section: Executive Summary                      | ⏳ Todo |       |
| 7.6 | Report section: Security Posture                       | ⏳ Todo |       |
| 7.7 | Report section: Technology Profile                     | ⏳ Todo |       |
| 7.8 | Report section: Attack Surface                         | ⏳ Todo |       |
| 7.9 | Report section: Findings with severity/evidence        | ⏳ Todo |       |
| 7.10 | Report section: Recommendations                       | ⏳ Todo |       |
| 7.11 | Report section: Learning Resources                    | ⏳ Todo |       |
| 7.12 | Frontend: Report page with real data                  | ⏳ Todo |       |
| 7.13 | HTML export of report                                 | ⏳ Todo |       |
| 7.14 | Learning mode: per-finding educational content        | ⏳ Todo |       |
| 7.15 | Learning mode: "What to study next" per finding type  | ⏳ Todo |       |

---

## M8 — Testing & UX Polish

| # | Task                                                       | Status  | Notes |
|---|------------------------------------------------------------|---------|-------|
| 8.1  | Backend unit tests: `security.py` functions            | ⏳ Todo |       |
| 8.2  | Backend unit tests: auth endpoints                     | ⏳ Todo |       |
| 8.3  | Backend unit tests: project + investigation CRUD       | ⏳ Todo |       |
| 8.4  | Backend integration test: full scan → finding → AI     | ⏳ Todo |       |
| 8.5  | Frontend: loading skeletons for all async views        | ⏳ Todo |       |
| 8.6  | Frontend: error boundary components                    | ⏳ Todo |       |
| 8.7  | Frontend: toast/notification system                    | ⏳ Todo |       |
| 8.8  | Frontend: responsive design audit                      | ⏳ Todo |       |
| 8.9  | Frontend: keyboard navigation and ARIA                 | ⏳ Todo |       |
| 8.10 | Backend: restrict CORS origins                         | ⏳ Todo | Remove `*` |
| 8.11 | Backend: rate limiting on auth endpoints               | ⏳ Todo |       |
| 8.12 | Remove hardcoded `JWT_SECRET_KEY` default              | ⏳ Todo | Require via env |
| 8.13 | Audit all endpoints for proper ownership checks        | ⏳ Todo |       |

---

## M9 — Docker & Deployment

| # | Task                                                       | Status  | Notes |
|---|------------------------------------------------------------|---------|-------|
| 9.1 | `backend/Dockerfile`                                    | ⏳ Todo | Python, venv, uvicorn |
| 9.2 | `frontend/Dockerfile`                                   | ⏳ Todo | Node.js, build, Next.js |
| 9.3 | `docker-compose.yml`                                    | ⏳ Todo | backend + frontend services |
| 9.4 | Persistent volume for `aegis.db`                        | ⏳ Todo |       |
| 9.5 | Security tools in backend container                     | ⏳ Todo | Nmap, WhatWeb, Gobuster, Nuclei |
| 9.6 | Ollama sidecar or external config                       | ⏳ Todo |       |
| 9.7 | `.env.example` updated with all required vars           | ⏳ Todo |       |
| 9.8 | `docker compose up` brings full system online           | ⏳ Todo |       |
| 9.9 | Production CORS and security config                     | ⏳ Todo |       |

---

## Backlog / Future

| Task                              | Notes |
|-----------------------------------|-------|
| PDF report export                 | After HTML export |
| PostgreSQL migration              | When SQLite becomes a bottleneck |
| ffuf integration                  | V2 security engine |
| Burp Suite integration            | V2 |
| SQLMap integration                | V3 |
| Nikto integration                 | V3 |
| AWS security scanning             | V4 |
| Team/workspace support            | Post-MVP |
| Scheduled scans                   | Post-MVP |
| Webhook alerting                  | Post-MVP |
