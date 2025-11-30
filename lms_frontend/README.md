
# LMS Frontend

Focused frontend README for the React + TypeScript app located at `lms_frontend/`.

This file explains how to run, test, and debug the frontend locally and documents the API contract and token behavior the app relies on.

## Quick Start (Windows PowerShell)

1. Install dependencies and start the dev server:
```powershell
cd c:\Users\gph19\lms_backend\lms_frontend
npm install
npm start
```

2. Configure API base URL (optional — defaults to `http://127.0.0.1:8000/api`):
```powershell
$env:REACT_APP_API_BASE_URL="http://127.0.0.1:8000/api"
npm start
```
Or create an `.env` file in `lms_frontend/` with:
```
REACT_APP_API_BASE_URL=http://127.0.0.1:8000/api
```

## Build & Test

- Build for production:
```powershell
npm run build
```

- Run tests (if present):
```powershell
npm test
```

## Token storage & API behavior

- Tokens used by the frontend are stored in `localStorage` with these keys:
  - `accessToken` — short-lived JWT access token attached to `Authorization: Bearer <token>` on requests.
  - `refreshToken` — used to obtain a fresh `accessToken` when a 401 response occurs.

- `src/services/api.ts` behavior:
  - A request interceptor attaches `Authorization: Bearer <accessToken>` when present.
  - A response interceptor tries to refresh the `accessToken` using the `refreshToken` when a 401 is received, then retries the original request once.
  - If refresh fails, tokens are cleared and the app navigates to `/login`.

## API endpoints the frontend uses (summary)
- `GET /courses/` — list courses
- `GET /courses/{id}/` — course detail
- `GET /enrollments/my-enrollments/` — user's enrollments
- `POST /enrollments/course/{course_id}/enroll/` — enroll in course
- `GET /lessons/` — list lessons (filtered by user role/enrollment)
- `GET /lessons/{id}/` — lesson detail
- `POST /lessons/progress/` — update lesson progress

> Full endpoints include the `/api/` prefix configured via `REACT_APP_API_BASE_URL`.

## Key frontend files
- `src/services/api.ts` — Axios instance, request/response interceptors, token refresh logic.
- `src/auth/AuthContext.tsx` — Auth provider exposing login/logout and authenticated user info.
- `src/pages/Profile.tsx` — Fetches and displays user's courses, enrollments, and lessons. Logs useful debug info when enabled.
- `src/pages/LessonDetail.tsx` — Renders lesson content.

## Debugging checklist (when lessons do not appear)

1. Confirm backend route mapping:
	- Ensure `GET /api/lessons/` resolves to the LessonViewSet on the backend (check `lms_backend/lessons/urls.py`). The frontend expects `/api/lessons/`.

2. Check browser DevTools (Profile page):
	- Network tab: Find `GET /api/lessons/` and open Response. Possible shapes:
	  - An array of lesson objects (e.g. `[{...}, {...}]`).
	  - An object with a `results` array (paginated, e.g. `{count: X, results: [...]}`).
	  - Empty object or `[]`.
	- Console tab: Look for logs added in `Profile.tsx`:
	  - `res.data:` — raw payload from the API
	  - `courseIds:` — course ids we requested lessons for
	  - `lessonsArray:` — normalized array of lessons used by the UI
	  - `Grouped lessons by course:` — mapping of courseId → lessons

3. Verify tokens:
	- In DevTools → Application → Local Storage: ensure `accessToken` and `refreshToken` exist for the app's origin.
	- Check network request headers for `Authorization: Bearer <token>`.

4. Check the Django server terminal logs:
	- If `lessons/views.py` includes debug prints, look for lines like `DEBUG: Student queryset contains X lessons.` and confirm the user matches the DB enrollments.

5. Common causes and fixes:
	- Route mismatch: backend's `lessons` router not registered at the prefix expected by frontend.
	- Token/refresh failure: expired `refreshToken` or refresh endpoint not reachable.
	- Response shape change: frontend expects an array but receives a paginated object — `Profile.tsx` now normalizes these shapes.

## Recommended development steps
- Add any API shape changes to the frontend immediately (or add compatibility code). `Profile.tsx` already guards against paginated vs array responses.
- Keep auth and API behavior covered with tests if possible.

## Change log (frontend-focused)
- Added robust handling in `src/pages/Profile.tsx` to support array or paginated lesson responses and to group lessons by course id.
- `src/services/api.ts` includes token refresh retry logic and logging.

## Next tasks you may want me to do
- Add more examples showing expected lesson JSON shape.
- Add a small smoke-test script to verify `GET /api/lessons/` returns a non-empty payload for an enrolled test user.
- Create a short `CONTRIBUTING.md` with local dev conventions.
