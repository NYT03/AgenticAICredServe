# System Architecture & Auditability

## Architecture

User → Frontend → FastAPI → AI Extractor → Verification Engine → Database
↓
Collections Agent → Logs → Human Escalation

## Proof Logs

We store:

- Input document hash
- Extracted JSON
- Verification result
- Retry attempts
- Agent state transitions
- Voice call transcripts
- Human escalation reason

## Prompt Injection Prevention

- Input sanitization
- Fixed JSON schema output
- No system prompt exposure
- Role-based prompt templates

## Data Leakage Prevention

- Mask account numbers
- Encrypt logs
- Store only required fields
- Access control for logs

## Human-in-the-loop

If:

- Verification fails twice
- User disputes payment
- AI confidence low

→ Case routed to human officer.
