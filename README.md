# LMS Project

Comprehensive full-stack Learning Management System (LMS) project containing a Django REST Framework backend (`lms_backend`) and a React + TypeScript frontend (`lms_frontend`). This README covers both sides, setup, debugging steps, API reference, recent fixes, and developer guidance.

## Table of Contents
- Overview
- Repository layout
- Quick status (recent changes)
- Prerequisites
- Backend: setup & run
- Frontend: setup & run
- Authentication & tokens
- API reference (used by frontend)
- Frontend details & important files
- Debugging & troubleshooting
- Change log
- Testing
- Deployment
- Contributing
- License

## Overview
This project implements an LMS with role-based access (student, teacher, admin). Students can enroll and view lessons for courses they are enrolled in; teachers manage their own courses and lessons; admins have full access. The backend exposes a JSON API and the frontend consumes it using JWT authentication.

## Repository layout
- `lms_backend/` — Django backend (APIs, models, migrations, management commands)
- `lms_frontend/` — React + TypeScript frontend
- `README.md` — this file (project-level)
- Other helper scripts: `populate_db.py`, `seed_lessons.py`, etc.

## Quick status (recent, important)
- Backend: `lessons/urls.py` router updated so the LessonViewSet is reachable at `GET /api/lessons/` (router.register changed to `r""`).
- Backend: `lessons/views.py` has temporary debug prints in `get_queryset()` to help trace why a user might see zero lessons.
- Frontend: `src/services/api.ts` includes Axios interceptors to attach `accessToken` and refresh on 401, with logging.
- Frontend: `src/pages/Profile.tsx` updated to be robust to different `/api/lessons/` response shapes (array, paginated object, or empty) and to group lessons by course.
 - Frontend: Added Logout buttons to Teacher and Admin dashboards; removed Home button references.
 - Frontend: Introduced shared `.button` styles in `src/index.css` to unify buttons across pages.
 - Frontend: Password visibility toggle planned as an icon-based, accessible component (to be finalized next).

## Prerequisites
- Python 3.8+
- Node.js (16+ recommended) and npm
- Windows PowerShell examples are provided for local development

## Backend — Setup & Run (Windows PowerShell)
1. Create and activate a virtual environment:
```powershell
cd c:\Users\gph19\lms_backend
python -m venv .venv
.venv\Scripts\Activate.ps1
```
2. Install dependencies:
```powershell
pip install -r requirements.txt
```
3. Apply migrations (and optional seed):
```powershell
python manage.py migrate
python populate_db.py   # optional: populate sample data
```
4. Run the development server:
```powershell
python manage.py runserver
```
The API base is `http://127.0.0.1:8000/api/`.

## Frontend — Setup & Run (Windows PowerShell)
1. Install and start the frontend dev server:
```powershell
cd c:\Users\gph19\lms_backend\lms_frontend
npm install
npm start
```
2. (Optional) Set API base URL with environment variable:
```powershell
$env:REACT_APP_API_BASE_URL="http://127.0.0.1:8000/api"
npm start
```
Or create an `.env` file in `lms_frontend/` with:
```
REACT_APP_API_BASE_URL=http://127.0.0.1:8000/api
```

## Authentication & Tokens (frontend behavior)
- Tokens stored in `localStorage`:
  - `accessToken`: access token used in `Authorization` header
  - `refreshToken`: used to obtain a new `accessToken` when needed
- `src/services/api.ts`:
  - Request interceptor attaches `Authorization: Bearer <accessToken>` when present.
  - Response interceptor attempts to refresh the token on 401 and retry the original request.
  - If refresh fails, tokens are cleared and user is redirected to `/login`.

## API Reference (endpoints frontend uses)
- Authentication: `POST /api/accounts/login/` (or token endpoints)
- Tokens: `POST /api/token/`, `POST /api/token/refresh/`
- Courses: `GET /api/courses/` (list), `GET /api/courses/{id}/` (detail)
- Enrollments: `GET /api/enrollments/my-enrollments/`, `POST /api/enrollments/courses/{id}/enroll/`
- Lessons: `GET /api/lessons/` (list), `GET /api/lessons/{id}/` (detail), `POST /api/lessons/progress/`

> Note: The frontend expects the LessonViewSet to be reachable at `/api/lessons/`. Ensure the backend router for lessons is registered at the empty prefix (see `lessons/urls.py`).

## Frontend — Important files & recent changes
- `src/services/api.ts`: Axios instance with request/response interceptors and console logs for token attachment and refresh attempts.
- `src/auth/AuthContext.tsx`: Provides login/logout and the current user context.
- `src/pages/Profile.tsx`: Fetches courses, enrollments, lessons. Recent improvements:
  - Handles `res.data` whether it's an array, paginated (object with `results`) or empty.
  - Logs `res.data`, `courseIds`, `lessonsArray`, and grouped lessons for easier debugging.
  - Groups lessons by course id into `courseLessons` state.
- `src/pages/LessonDetail.tsx`: Renders lesson content (server-rendered HTML endpoint for lesson detail exists as well).
 - `src/index.css`: Shared `.button` class added for consistent theming and focus/hover states.
 - `src/pages/TeacherDashboard.tsx` and `src/pages/AdminDashboard.tsx`: Logout button added in header; Home button removed.
 - Planned: `src/components/PasswordField.tsx` with icon toggle (`Eye`/`EyeOff`) to provide accessible, type-safe show/hide password control.

## Debugging & Troubleshooting (step-by-step)
If a student sees "No lessons available" while the DB lists lessons:

1. Confirm backend route mapping:
   - `c:\Users\gph19\lms_backend\lessons\urls.py` should register the LessonViewSet with `router.register(r"", LessonViewSet, basename="lesson")` so that `/api/lessons/` is routed properly.

2. Check Django server logs (terminal running `python manage.py runserver`):
   - `lessons/views.py` includes debug prints in `get_queryset()` that show the username, role, and the number of lessons filtered for the user. Look for lines like:
     - `DEBUG: User in LessonViewSet get_queryset: <username>, ID: <id>, Role: <role>`
     - `DEBUG: Student queryset contains X lessons.`

3. Browser DevTools (Profile page tab):
   - Network tab: locate `GET /api/lessons/` and inspect the Response tab. Is it an array? An object with `results`? Empty?
   - Console tab: look for console logs produced by `Profile.tsx`: `res.data:`, `courseIds:`, `lessonsArray:`, `Grouped lessons by course:`.

4. Token verification:
   - In DevTools > Application > Local Storage, confirm `accessToken` and `refreshToken` are present.
   - Check console logs from `src/services/api.ts` for token presence and refresh attempts.

5. If backend returns no lessons but DB has lessons:
   - Verify the user in request matches enrollments in DB.
   - Verify `get_queryset()` filter `course__enrollments__student=user` matches your Enrollment model.

## Change Log (recent & relevant)
- Backend:
  - `lessons/urls.py`: router.register changed to `r""` so `/api/lessons/` routes to LessonViewSet.
  - `lessons/views.py`: added debug prints in `get_queryset()` to aid troubleshooting.
- Frontend:
  - `src/services/api.ts`: added logging and robust token refresh handling.
  - `src/pages/Profile.tsx`: handle different response shapes from `/api/lessons/` to avoid runtime errors and added grouping/logging.

## Testing
- Backend tests (Django):
```powershell
cd c:\Users\gph19\lms_backend
.venv\Scripts\Activate.ps1
python manage.py test
```
- Frontend tests (if configured):
```powershell
cd c:\Users\gph19\lms_backend\lms_frontend
npm test
```

## Deployment (brief)
- Use PostgreSQL in production; configure `DATABASES` in `settings.py`.
- Set `DEBUG=False`, provide `SECRET_KEY` and `ALLOWED_HOSTS`.
- Serve static files with WhiteNoise or a dedicated CDN.

## Contributing
- Use feature branches and open PRs with clear descriptions and tests.
- Keep the frontend-backend contract stable — coordinate endpoint or payload shape changes across both sides.

## License
This project is for educational purposes. No specific license applied.