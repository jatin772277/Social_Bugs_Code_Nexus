# CodeNexus — Pre-Publication Brand Governance Platform

**Team:** Social Bugs | **Hackathon:** CodeNexus India 2026 | **Round:** 2

## What It Does

A review desk that sits between content creation and publishing. Creators upload drafts → platform checks against the organisation's own brand guidelines using rule-based checks and grounded AI → evidence-locked findings (each citing the exact guideline clause) → creators accept/dispute/dismiss → manager or reviewer approves → locked record with audit trail.

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS |
| Backend | Python 3.11 + FastAPI + SQLAlchemy |
| Database | PostgreSQL 16 |
| AI | Google Gemini API (`gemini-3.8-flash`) via `google-genai` SDK |
| Auth | JWT (python-jose) + bcrypt |

## Running Locally

### Prerequisites
- Python 3.11+
- Node 18+
- PostgreSQL 16 running (or Docker)
- Gemini API key

### Backend

```bash
cd backend
cp .env.example .env
# Edit .env — add your GEMINI_API_KEY
pip install -r requirements.txt
python seed.py          # creates tables + demo data
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at http://localhost:5173 | API at http://localhost:8000

### Docker (full stack)

```bash
cp backend/.env.example .env
# Edit .env
docker compose up --build
```

Then visit http://localhost:5173

## Demo Accounts (after seeding)

| Email | Password | Role |
|---|---|---|
| admin@codenexus.demo | admin123 | Admin |
| manager@codenexus.demo | manager123 | Brand Manager |
| creator@codenexus.demo | creator123 | Content Creator |
| reviewer@codenexus.demo | reviewer123 | Legal Reviewer |

## Features Shipped (Round 2)

- JWT authentication with 4 roles (creator / manager / reviewer / admin)
- Workspace management with multi-workspace support
- Guideline import with automatic clause splitting and category inference
- Terminology rules (banned / preferred terms)
- Approved facts store with source citations
- **Rule-based checks** — banned term detection with exact location
- **AI-grounded review** — Gemini checks content against retrieved clauses, returns structured JSON
- **Evidence verification** — findings dropped if the quoted content or clause cannot be confirmed in source
- Accept / dispute / dismiss workflow with dispute reason capture
- Clause dispute/dismiss counters for future clarity insights
- Manager/reviewer approval step with note and decision record
- Comment threads per draft
- Insights dashboard (findings by category/severity, unclear clauses)
- Pre-loaded sample brand kit + 4 demo users

## Round 3 Improvements (pre-committed)

1. **Word/PDF/Image file upload and parsing** — Position-aware highlights; image palette + contrast + alt-text checks
2. **Full revision history with diff view** — Every content revision stored; before/after comparison shown to approver
3. **Guideline clarity insights with AI rewrite suggestions** — Disputed/dismissed clauses flagged; Gemini suggests clearer rewrites for the guideline owner

## API Docs

With backend running: http://localhost:8000/docs

## Repository

All code is in this repository. No code was generated and hidden — all logic is in `backend/app/` and `frontend/src/`.

External services used:
- Google Gemini API (`gemini-3.8-flash`) for grounded content review
- PostgreSQL for all data storage

## Team

| Name | Role |
|---|---|
| Jatin Baghel | Backend and AI pipeline lead |
| Dushyant | Frontend and workflow lead |
| Vishal Thombre | Rules, formats and accessibility |
| Ricky Mukherjee | Data, insights, testing and documentation |

