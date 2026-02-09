# Personal Executive Assistant

AI-powered personal assistant using **LangChain + Gemini** 

## Quick Start

### Backend
```powershell
cd backend
.\venv\Scripts\activate
python src\server.py
```

### Frontend
```powershell
cd frontend
npm run dev
```

Open `http://localhost:3000`

---

## Project Structure

```
personal-assistant-agent/
├── backend/                    # Python API
│   ├── .env                    # GEMINI_API_KEY
│   ├── requirements.txt
│   ├── venv/
│   ├── secrets/                # OAuth credentials (gitignored)
│   │   ├── credentials.json
│   │   └── token.json
│   └── src/
│       ├── server.py           # FastAPI entry point
│       ├── core/
│       │   ├── agent.py        # LangChain ReAct agent
│       │   └── prompts.py
│       ├── tools/
│       │   ├── __init__.py     # Clean exports
│       │   ├── gmail.py
│       │   └── calendar.py
│       └── utils/
│           └── auth.py         # Google OAuth
│
├── frontend/                   # Next.js UI
│   ├── .env.local              # BACKEND_URL
│   └── src/app/
│
└── .gitignore
```

---

