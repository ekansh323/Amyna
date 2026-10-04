# Aegis — Product Requirements Document

**Version:** 1.0
**Date:** October 2026
**Status:** Active development

---

## 1. Product Overview

### 1.1 What Is Aegis?

Aegis is an AI-assisted cybersecurity investigation platform. It allows users to run security assessments against targets using industry-standard security tools, then uses a local AI model to transform raw technical findings into understandable, actionable intelligence.

Aegis is NOT a simple vulnerability scanner. It is a full investigation workflow platform that combines:
- Real security tooling (Nmap, WhatWeb, Gobuster, Nuclei)
- AI-powered analysis and explanation
- A learning-oriented interface that teaches *why* findings matter
- Professional-grade reporting

### 1.2 Core Investigation Flow

```
User defines Target
        ↓
Reconnaissance (Nmap, WhatWeb)
        ↓
Attack Surface Discovery (Gobuster)
        ↓
Vulnerability Assessment (Nuclei)
        ↓
Findings collected and normalized
        ↓
AI Explanation (Ollama)
          - What was found
          - Why it matters
          - Attack scenario
          - Remediation
          - Learning resources
        ↓
Investigation Report
```

### 1.3 Design Philosophy

Aegis must feel like a professional modern SaaS product. Design inspiration: Apple, Linear, Stripe, Vercel, Arc.

**Must avoid:**
- Hacker terminal aesthetic
- Matrix green color scheme
- Excessive neon / dark hacker vibes
- Kali Linux-style UI
- Gratuitous animations in the application

**Must have:**
- Clean, high-information-density UI
- Fast, responsive interactions
- Clear visual hierarchy
- Professional typography and color
- Cinematic landing page (marketing)
- Practical, focused application UI

---

## 2. Target Users

### Primary Users

| User Type                 | Needs                                                  |
|---------------------------|--------------------------------------------------------|
| Cybersecurity students    | Learn by doing, understand findings, get explanations  |
| Security researchers      | Run real tools, get normalized output, document findings |
| Developers (appsec)       | Scan their own apps, understand vulnerabilities         |
| Junior penetration testers | Use professional tools with AI-guided understanding    |
| Security professionals    | Efficient investigation workflow, exportable reports   |

### Non-Goals (V1)

- Enterprise team collaboration
- Managed/cloud scanning infrastructure
- Mobile application scanning
- API security assessment (deep)
- AWS/cloud infrastructure assessment

---

## 3. Product Areas

### 3.1 Landing Page

**Purpose:** Marketing, storytelling, first impression.

**Requirements:**
- Cinematic, scroll-driven experience
- Visualize the investigation concept (target → workflow → intelligence)
- Globe / attack-surface visualization that evolves with scroll
- Clear CTA to sign up / sign in
- Does NOT impact dashboard performance or complexity

**Status:** ✅ Implemented (static, frontend only)

---

### 3.2 Authentication

**Purpose:** Secure, scoped user access.

**Requirements:**
- User registration with name, email, password
- Email uniqueness enforced
- Password hashing (bcrypt) — no plaintext storage
- JWT-based authentication (7-day expiry by default)
- Protected routes require valid JWT
- Users can only access their own data
- `/users/me` endpoint for session validation
- Frontend login and register forms
- JWT stored in localStorage
- Auto-redirect on 401

**Status:** 🔄 In Progress
- ✅ Backend: register, login, JWT, bcrypt, protected endpoint
- ✅ Frontend: login page connected to real API, register page exists
- ⏳ Frontend: route protection middleware, auth context, logout

---

### 3.3 Dashboard

**Purpose:** Mission control — overview of all user activity.

**Requirements:**
- Show user's projects
- Show recent investigations
- Show recent findings (severity breakdown)
- Security posture indicator
- Quick actions (start new investigation)
- Link to reports

**Status:** ✅ Frontend UI implemented (mock data), ⏳ not connected to backend

---

### 3.4 Projects

**Purpose:** Organize security work into named projects.

**Requirements:**
- Create / read / update / delete projects
- Each project has: name, description, target(s), timestamps
- Project belongs to a user — strict ownership enforcement
- A project can contain multiple investigations
- Project list and detail views

**Status:** ✅ ORM model and DB table defined, ⏳ CRUD API endpoints not yet built (M4)

---

### 3.5 Investigations

**Purpose:** Represent a security assessment run against a target.

**Requirements:**
- An investigation belongs to a project
- Target: domain, IP, or URL
- Scan profile: defines which tools run (e.g., Quick, Standard, Deep)
- Status lifecycle: `pending → running → completed | failed`
- Timestamps: created, started, completed, duration
- Results: technologies discovered, attack surface, tool outputs
- Findings linked to investigation
- AI analysis linked to investigation
- Timeline view of events
- Investigation detail page

**Status:** ✅ ORM model defined, ✅ frontend detail page (mock), ⏳ CRUD API not built (M4), ⏳ engine not connected (M5)

---

### 3.6 Security Engine

**Purpose:** Execute real security tools against targets.

**Requirements:**
- Modular design — each scanner has a clean, consistent interface
- Tool adapters: Nmap, WhatWeb, Gobuster, Nuclei (V1)
- No shell injection — tools executed via subprocess with controlled arguments
- Each tool's output is parsed and normalized into Aegis's internal data model
- Scan execution is backend-controlled (not triggered directly by user input)
- Results stored as Findings in the database
- Support for adding new tools without rewriting core engine

**V1 Tools:**
| Tool       | Purpose                        |
|------------|--------------------------------|
| Nmap       | Port scanning, service detection |
| WhatWeb    | Technology fingerprinting      |
| Gobuster   | Content/directory discovery    |
| Nuclei     | Vulnerability template scanning |

**Future Tools:** ffuf, Burp Suite, SQLMap, Nikto, AWS scanner

**Status:** ⏳ Not implemented (M5)

---

### 3.7 AI Intelligence

**Purpose:** Transform raw tool output into understandable security intelligence.

**Requirements:**
- Use local Ollama instance
- Model configurable via `OLLAMA_MODEL` environment variable
- AI must only analyze actual collected evidence — no invented findings
- For each significant finding, AI generates:
  - What was discovered
  - Why it matters
  - Potential impact
  - Attack scenario
  - Real-world context
  - Remediation advice
  - Learning resources / next steps
- AI responses stored and linked to findings
- AI must not be a black box — responses must be attributable to real evidence

**Status:** ⏳ Not implemented (M6). Config (`OLLAMA_BASE_URL`, `OLLAMA_MODEL`) is in place.

---

### 3.8 Case / Finding Page

**Purpose:** Tell the complete story of a single vulnerability.

**Requirements:**
- Dedicated page per finding
- Structured as a narrative:
  - Finding summary
  - Evidence (raw tool output)
  - Why it matters
  - Attack scenario
  - Real-world example
  - Remediation steps
  - Learning resources
- Severity badge (Critical / High / Medium / Low / Info)
- Link back to investigation

**Status:** ✅ Frontend page exists (mock), ⏳ not connected to real findings

---

### 3.9 Reports

**Purpose:** Generate professional security reports from investigations.

**Requirements:**
- Report is generated from an investigation's findings + AI analysis
- Sections:
  - Executive Summary
  - Security Posture
  - Technology Profile
  - Attack Surface
  - Findings (with severity, evidence, recommendations)
  - Learning Resources
  - Next Steps
  - Appendix
- Export formats: PDF, HTML, Markdown (future)

**Status:** ✅ Frontend report page (mock), ⏳ report generation not implemented (M7)

---

## 4. Non-Functional Requirements

### 4.1 Security

| Requirement                                    | Status         |
|------------------------------------------------|----------------|
| Passwords hashed with bcrypt                   | ✅ Implemented |
| No plaintext secrets in code                   | ⚠️ Dev secret in config.py — must override in prod |
| JWT-protected endpoints                        | ✅ Implemented |
| User data scoping (own projects only)          | ⏳ M4          |
| No arbitrary command execution via user input  | ⏳ M5 (engine design) |
| Input validation                               | ✅ Pydantic + email-validator |
| CORS restricted in production                  | ⚠️ Currently `*` |

### 4.2 Architecture

| Requirement                           | Status         |
|---------------------------------------|----------------|
| SQLite for MVP                        | ✅ Implemented |
| PostgreSQL-compatible ORM             | ✅ SQLAlchemy supports both |
| Environment-based configuration       | ✅ pydantic-settings |
| Modular security engine               | ⏳ M5          |
| Docker support                        | ⏳ M9          |

### 4.3 Performance

- Backend API responses: < 200ms for non-scan endpoints
- Scan operations run asynchronously (background tasks or queuing — M5)
- Frontend: no unnecessary re-renders, fast page transitions

### 4.4 Usability

- All investigation pages readable without security expertise
- AI explanations written in plain English
- Error states are clear and actionable
- Loading states shown during scans

---

## 5. Technical Constraints

- Security tools must be installed on the host or container
- AI requires local Ollama — no external AI API calls by default
- SQLite cannot support concurrent writes at high load — acceptable for MVP/single-user
- No team/multi-user collaboration in V1

---

## 6. Out of Scope (V1)

- Team workspaces
- Cloud infrastructure scanning
- Burp Suite integration
- Scheduled/automated scans
- Webhooks or alerting
- Mobile app
- Enterprise SSO
- Report templates / custom branding
