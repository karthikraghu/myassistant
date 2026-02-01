# Personal Executive Assistant Agent

Python + Next.js AI agent using Gemini LLM to aggregate Gmail and Calendar data.

## Structure

```
├── src/                    # Python backend
│   ├── main.py             # Entry point
│   ├── core/               # LLM + prompts
│   ├── tools/              # Gmail, Calendar API wrappers
│   └── utils/              # OAuth handler
│
└── frontend/               # Next.js app
    └── src/
        ├── app/            # Pages + API routes
        └── components/     # Chat UI components
```

## Backend Setup

```bash
python -m venv venv
.\venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

1. Add `credentials.json` from Google Cloud Console
2. Copy `.env.example` to `.env`, set `GEMINI_API_KEY`
3. Run: `python src/main.py`

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Copy `frontend/.env.example` to `frontend/.env.local`

## Required Scopes

- `gmail.readonly`
- `calendar.readonly`
