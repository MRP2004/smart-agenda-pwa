# Smart Agenda PWA (Students + Teachers)

A complete mobile-first progressive web app with a React frontend and FastAPI backend for personal calendar/event/task planning.

## Project structure

```
.
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── auth.py
│       ├── database.py
│       ├── main.py
│       ├── models.py
│       ├── schemas.py
│       └── routers/
│           ├── auth.py
│           ├── events.py
│           ├── reminders.py
│           └── tasks.py
└── frontend/
    ├── index.html
    ├── package.json
    ├── public/
    │   ├── icon-192.png
    │   ├── icon-512.png
    │   ├── manifest.json
    │   └── service-worker.js
    └── src/
        ├── api.js
        ├── App.jsx
        ├── main.jsx
        ├── styles.css
        └── components/
            ├── AuthPanel.jsx
            ├── CalendarBoard.jsx
            ├── EventQuickAdd.jsx
            └── TaskPanel.jsx
```

## Features delivered

- **PWA-ready frontend**: manifest + service worker, installable on mobile/desktop.
- **Mobile-first UX**: responsive cards, quick-add event form, category colors.
- **Calendar views**: day, week, month, upcoming 7-day list using FullCalendar list view.
- **Event CRUD model** with recurrence fields and auto-color by category.
- **Task management** with priority, notes, and optional linked event.
- **Reminder API** for configurable reminder minutes + daily summary flag.
- **Search/filter** support by keyword, category, and dates (backend query params).
- **Authentication**: register + login with JWT token and per-user data isolation.
- **PDF export**: day/week/month export buttons using jsPDF.

## Backend setup (FastAPI + SQLite)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API URL: `http://localhost:8000`

### REST API overview

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/health`
- `POST/GET/PUT/DELETE /api/events`
- `POST/GET/PUT/DELETE /api/tasks`
- `POST/GET/PUT/DELETE /api/reminders`

## Frontend setup (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

Optional environment variable:

```bash
VITE_API_URL=http://localhost:8000
```

## Push notifications notes

- Service worker is registered in `src/main.jsx`.
- `push` events are handled in `public/service-worker.js`.
- Backend reminder entities are available; web push delivery can be wired to VAPID in production.
- Daily summary concept is represented through `periodicsync` event handling and `daily_summary` reminder field.

## SQLite schema relationships

- `users` 1-to-many `events`
- `users` 1-to-many `tasks`
- `users` 1-to-many `reminders`
- `events` 1-to-many `tasks` (optional task linkage)
- `reminders` optional links to `events` or `tasks`

## Production hardening suggestions

- Move secrets/JWT config to environment variables.
- Add Alembic migrations.
- Add real web push subscriptions and background scheduler.
- Add refresh tokens and secure cookie auth.
- Add automated API/frontend tests in CI.
