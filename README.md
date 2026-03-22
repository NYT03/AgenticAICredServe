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

### Production Architecture Flow

User Upload / Trigger / Webhook
│
▼
API Gateway (FastAPI)
│
▼
Orchestration Layer (LangGraph)
│ │
│ │
▼ ▼
Onboarding Agent Collections Agent
│ │
▼ ▼
Document Store State Database
│ │
▼ ▼
LLM Service Notification Service (SMS/Email/Voice)
│
▼
Verification Engine
│
▼
Proof Logs + Audit Trail
│
▼
Human Review Dashboard

---

## 2. Proof Logs Strategy (Auditability)

In financial systems, every AI decision must be traceable and auditable. The system will automatically generate **Proof Logs** for every action taken by the AI agents.

### Each Proof Log Entry Stores:

| Field               | Description                                |
| ------------------- | ------------------------------------------ |
| timestamp           | When the action occurred                   |
| agent_name          | Onboarding Agent / Collections Agent       |
| triggered_by        | User / System / Webhook                    |
| input_data_hash     | Hash of uploaded document or borrower data |
| prompt_version      | Version of the LLM prompt                  |
| llm_response        | Raw LLM output                             |
| verification_result | PASS / FAIL                                |
| state_transition    | Previous → New State                       |
| human_handoff       | Yes / No                                   |
| final_decision      | Approved / Retry / Escalated               |

### Storage Strategy

- Logs stored in **append-only storage** (JSONL / Database).
- Each log entry is **hash-chained** with the previous log to prevent tampering.
- This allows regulators to **replay the decision process** using:
  - Input data
  - Prompt used
  - LLM output
  - Verification result
  - Final decision

This ensures full auditability and compliance with financial regulations.

---

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
