# Grid Quiz — Team 2 Semester Project

Grid Quiz is a Jeopardy inspired quiz game with a Django REST backend and a Vite + React frontend. This repository contains the API and admin backend (meant for Railway hosting) and a modern frontend (meant for Vercel hosting).

**Quick overview**
- A grid-based quiz game with persistent leaderboards, user accounts, and admin tools.
- Backend: Django + Django REST Framework, SQLite (dev). See `backend/`.
- Frontend: React + Vite. See `frontend/`.

**Repository structure**
- `backend/`: Django project, REST API, admin, migrations, and deployment notes.
- `frontend/`: Vite + React app, API client, and deployment notes for Vercel.

Getting started (development)

1. Backend (On Windows)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/` (and DRF browsable API under `/api/`).

2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the development server (Vite) URL shown in the terminal.

Configuration & environment
- Backend env and deployment notes: see `backend/DEPLOY.md`.
- Frontend deployment notes: see `frontend/DEPLOY_VERCEL.md`.
- Database: `backend/db.sqlite3` is used for local development. Use a production DB for deployments.

Key files
- API client used by the frontend: `frontend/src/api/client.js`
- Django app with game logic: `backend/gridquiz/quickstart/` (models, views, serializers)

Deployment
- This project has deployment instructions for Railway (backend) and Vercel (frontend). See `backend/DEPLOY.md` and `frontend/DEPLOY_VERCEL.md`.
