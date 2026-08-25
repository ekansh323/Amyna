#  Aegis (Amyna AI)

> AI-assisted website security investigation platform.

Aegis combines common security tools into a single workflow and uses a local LLM to explain the results in plain English. Instead of jumping between different terminal outputs, you get one investigation with findings, evidence, and a report.

> **Only use Aegis on systems you own or have permission to test.**

## Features

- Website reconnaissance
- Technology fingerprinting
- Directory discovery
- Vulnerability scanning
- AI explanations (Ollama)
- Investigation timeline
- Security reports
- Learning Mode

## Workflow

```text
Create Project
      ↓
Add Target
      ↓
Run Investigation
      ↓
Recon → Fingerprinting → Discovery → Scan
      ↓
AI Analysis
      ↓
Report
```

## Tech Stack

| Frontend | Backend | Database | AI |
|----------|---------|----------|----|
| Next.js | FastAPI | SQLite | Ollama |

### Security Tools (v1)

- Nmap
- WhatWeb
- Gobuster
- Nuclei

