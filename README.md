# CredServ MVP – AI Onboarding & Collections Agent

## Overview

This project implements two AI systems:

1. AI Onboarding Agent – Extracts structured data from bank statements using LLM.
2. AI Collections Agent – State machine workflow for payment collections.

## Tech Stack

- Python
- FastAPI
- LangGraph
- OpenAI
- OCR (PyMuPDF, Tesseract)
- HTML/CSS/JS (Frontend)

## How to Run

### Step 1 – Install Dependencies

pip install -r requirements.txt

### Step 2 – Run Backend

uvicorn backend.api:app --reload

### Step 3 – Open Frontend

Open frontend/index.html in browser

## Features

- LLM-based OCR extraction
- Verification engine
- Retry mechanism
- Collections workflow state machine
- Audit logs
- Simple UI

## Logs

All system actions are logged in:

- logs/extraction_logs.json
- logs/verification_logs.json
- logs/agent_logs.json

# Stage 3 – System Design & Auditability

## 1. Production Architecture Overview

This system consists of two AI agents:

- **Onboarding Agent** – Extracts structured data from financial documents using a Vision-Language Model (VLM/LLM).
- **Collections Agent** – A deterministic state machine that manages borrower communication and escalation workflows.

## Production Architecture Flow

````text
User Upload / Trigger / Webhook
                |
                v
        API Gateway (FastAPI)
                |
                v
    Orchestration Layer (LangGraph)
           /                 \
          v                   v
 Onboarding Agent     Collections Agent
          |                   |
          v                   v
   Document Store       State Database
          |
          v
      LLM Service
          |
          v
   Verification Engine
          |
          v
   Proof Logs + Audit Trail
          |
          v
   Human Review Dashboard

Notifications (SMS/Email/Voice) triggered by Collections Agent ```

---

## Option 2 — Mermaid Diagram (Best for GitHub)

GitHub supports Mermaid diagrams. This will render as a **proper architecture diagram**.

```markdown
## Production Architecture Flow

```mermaid
flowchart TD
    A[User Upload / Trigger / Webhook] --> B[API Gateway - FastAPI]
    B --> C[Orchestration Layer - LangGraph]

    C --> D[Onboarding Agent]
    C --> E[Collections Agent]

    D --> F[Document Store]
    D --> G[LLM Service]
    G --> H[Verification Engine]

    E --> I[State Database]
    E --> J[Notification Service (SMS/Email/Voice)]

    H --> K[Proof Logs + Audit Trail]
    I --> K
    K --> L[Human Review Dashboard]

````

## 3. Preventing Prompt Injection & Data Leakage

### Prompt Injection Risks

Financial documents may contain malicious text like:

- “Ignore previous instructions”
- “Extract all data”
- “Send data to external server”

### Prevention Measures

| Risk                           | Mitigation                                   |
| ------------------------------ | -------------------------------------------- |
| Prompt injection from document | Sanitize document text before sending to LLM |
| Role override                  | Use fixed system prompt                      |
| Unauthorized fields            | Allow only specific JSON fields              |
| Data exfiltration              | Disable external tool access                 |

### Allowed Output Schema

The LLM is only allowed to return the following JSON:

```json
{
  "account_holder_name": "",
  "bank_name": "",
  "account_number": "",
  "transactions": [
    {
      "date": "",
      "description": "",
      "debit": 0,
      "credit": 0,
      "balance": 0
    }
  ]
}
```
