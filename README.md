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