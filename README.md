# 🛡️ Aegis (Amnya AI)

> **Know Your Attack Surface. Before Attackers Do.**

Aegis is a cybersecurity investigation platform that helps users assess the security of websites using common security tools and AI.

The idea is simple: instead of having to run different tools separately and then figure out what all the output means, Aegis puts the process into one investigation workflow. It collects the results, keeps track of what was checked, and uses a local LLM to explain the findings in simpler terms.

The goal is to make security testing easier to understand without hiding the technical details.

---

## What Aegis Does

A typical investigation goes through a few stages:

* Website reconnaissance
* Technology detection
* Content and directory discovery
* Vulnerability scanning
* Evidence collection
* AI-assisted analysis
* Report generation

The results are shown through a dashboard where you can follow the investigation and review individual findings.

---

## Investigation Flow

```text
Create Project
      ↓
Add Target
      ↓
Choose Investigation Profile
      ↓
Start Investigation
      ↓
Reconnaissance
      ↓
Technology Detection
      ↓
Content Discovery
      ↓
Vulnerability Assessment
      ↓
Evidence Collection
      ↓
AI Analysis
      ↓
Generate Report
```

---

## Features

### 🔎 Website Investigations

Create an investigation for a website and run a predefined set of security checks against it.

### 📡 Reconnaissance

Collect basic information about the target using tools such as Nmap and WhatWeb.

### 🧩 Technology Fingerprinting

Identify technologies, frameworks, servers and other components that are exposed by the target.

### 📂 Content Discovery

Find publicly accessible directories and files using Gobuster.

### 🛡️ Vulnerability Scanning

Use Nuclei to check the target against known vulnerability and security templates.

### 🤖 AI Intelligence

A local LLM is used to explain security findings, provide context and make the scanner output easier to understand.

Aegis does not replace the underlying security tools. It works on top of them and helps interpret their results.

### 📚 Learning Mode

Learning Mode is aimed at students who want to understand security findings rather than just see a vulnerability name.

For example, instead of only showing:

```text
Missing Security Header
```

Aegis can explain what the header does, why it matters and what should normally be done to fix the issue.

### 📊 Investigation Timeline

Each investigation has a timeline showing what Aegis is currently doing and what has already been completed.

### 📄 Security Reports

Investigation results can be compiled into a structured security report containing the target information, findings, evidence and recommendations.

### 🗂️ Investigation History

Previous investigations are stored so users can return to them and compare results later.

---

# 🛠️ Tech Stack

## Frontend

* Next.js
* TypeScript
* Tailwind CSS
* Framer Motion

## Backend

* FastAPI
* Python

## Database

* SQLite

SQLite is being used for the first version to keep the setup simple. The database layer is designed so that it can be replaced with PostgreSQL later if needed.

## AI

* Ollama
* Local LLM

Running the model locally keeps the AI portion of the project independent from a paid API during development.

## Security Tools

### Version 1

* Nmap
* WhatWeb
* Gobuster
* Nuclei

### Planned

**Version 2**

* Burp Suite
* ffuf

**Version 3**

* SQLMap
* Nikto

**Version 4**

* AWS security assessment tools

---

# 📁 Project Structure

```text
Aegis/
│
├── README.md
│
├── docs/
│   ├── PRD.md
│   │
│   ├── SSD/
│   │   ├── SSD_1_System_Architecture.md
│   │   ├── SSD_2_Backend.md
│   │   ├── SSD_3_Security_Engine.md
│   │   ├── SSD_4_Database.md
│   │   └── SSD_5_AI_Report.md
│   │
│   └── UI/
│       ├── Landing.md
│       ├── Dashboard.md
│       ├── Investigation.md
│       ├── Case.md
│       └── Report.md
│
├── frontend/
│
└── backend/
```

---

# 🎯 Version 1

The first version is focused on website security assessments.

### Included

* User authentication
* Project management
* Website investigations
* Investigation profiles
* Investigation timeline
* Security tool integration
* AI-assisted explanations
* Learning Mode
* Security reports
* Investigation history

### Not Included Yet

* Cloud security assessments
* API security testing
* Team collaboration
* Mobile application
* Enterprise features

These can be added later once the core investigation workflow is stable.

---

# 🚧 Development Roadmap

## Phase 1 — Documentation

Set up the basic project documentation and define the architecture before implementation.

* Product requirements
* System architecture
* Backend design
* Database design
* Security engine design
* AI/reporting design
* UI specifications

## Phase 2 — Core Platform

Build the application around the investigation workflow.

* Authentication
* Dashboard
* Projects
* Targets
* Investigation creation
* Investigation status tracking
* Investigation history

## Phase 3 — Security Engine

Integrate the initial security tools.

* Nmap
* WhatWeb
* Gobuster
* Nuclei
* Tool execution management
* Result parsing
* Evidence storage

## Phase 4 — AI

Add the local AI layer.

* Finding explanations
* Security recommendations
* Learning Mode
* Investigation summaries
* Report generation

## Phase 5 — Polish & Deployment

Once the core functionality works:

* Improve the UI
* Add animations where they actually help
* Responsive design
* Testing
* Error handling
* Security hardening
* Deployment

---

# ⚠️ Responsible Use

Aegis is intended for security testing on systems that you own or have explicit permission to assess.

Do not use it to scan or test websites, servers, or infrastructure without authorization.

The project is being developed primarily for learning, research and authorized security assessments.

---

# 🤝 Contributing

Aegis is being built as a modular project, so new security tools and features can be added without rewriting the entire application.

If you want to contribute, check the documentation in `docs/` first, especially the system design documents, before making architectural changes.

---

# 📜 License

This project is licensed under the MIT License.

---

## Why Aegis?

Most security tools are good at finding things. The difficult part, especially when you're learning, is understanding what those findings actually mean.

Aegis is an attempt to put the investigation process into one place — run the tools, collect the results, understand the findings, and turn them into something useful.

The long-term goal is to build a platform that can grow from a simple website assessment tool into a broader cybersecurity investigation platform.
