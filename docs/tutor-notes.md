# Tutor Notes / Marking Guide

Welcome, and thank you for reviewing this LMS project.

This document is a quick guide to the repository layout, how to run the project, and where to find the key design artefacts (wireframes, flow chart, screenshots).

## Repository and main entry points

- GitHub repository:  
  https://github.com/GlennHuckett82/LMS-project
- Main project README (high-level overview, setup, testing, and validation):  
  [README.md](../README.md)

### Backend (Django REST Framework API)

- Location: [lms_backend](../lms_backend)
- Entry point: [manage.py](../manage.py)
- Core settings: [lms_backend/settings.py](../lms_backend/settings.py)
- Main apps:
  - [accounts](../accounts)
  - [courses](../courses)
  - [lessons](../lessons)
  - [enrollments](../enrollments)
  - [quizzes](../quizzes)

The backend exposes a JSON API used by the React frontend and implements role-based access for students, teachers, and admins.

### Frontend (React + TypeScript)

- Location: [lms_frontend](../lms_frontend)
- Frontend-specific README (quick start, tests, API contract):  
  [lms_frontend/README.md](../lms_frontend/README.md)

The frontend is a single-page application that communicates with the Django API using JWT authentication.

## How to run the project locally (summary)

Full, copy-paste commands (Windows PowerShell) are in the root [README.md](../README.md). This is a concise summary:

### Backend

From the repository root:

1. Create and activate a virtual environment, then install dependencies:
   - See "Backend — Setup & Run" in [README.md](../README.md) for exact commands.
2. Apply migrations and (optionally) seed demo data.
3. Run the development server:
   - `python manage.py runserver`
4. API base URL: `http://127.0.0.1:8000/api/`

### Frontend

From the frontend folder:

1. Change into the frontend directory:
   - `cd lms_frontend`
2. Install dependencies and start the dev server:
   - `npm install`
   - `npm start`
3. The frontend is configured to talk to the backend at `http://127.0.0.1:8000/api` by default. This can be overridden via the `REACT_APP_API_BASE_URL` environment variable (documented in [lms_frontend/README.md](../lms_frontend/README.md)).

## Design work (wireframes, flow chart, screenshots)

All design artefacts are located under the `docs` and `wireframes_static` folders.

### Figma prototype (wireframes and user flow)

- Interactive Figma prototype showing desktop wireframes and a user-flow diagram is linked in the main README under “Design & UX (screenshots & wireframes)”:  
  [README.md#design--ux-screenshots--wireframes](../README.md#design--ux-screenshots--wireframes)

### PNG wireframes and flow chart

- Folder: [docs/wireframes](docs/wireframes)
- Contents:
  - PNG screenshots of the six main desktop wireframe screens (home, login, register, dashboard, lessons, quizzes).
  - A PNG of the user-flow chart.
  - A short description of each image in [docs/wireframes/README.md](docs/wireframes/README.md).

### Static HTML/CSS wireframes

- Folder: [wireframes_static](../wireframes_static)
- Contains the source HTML and CSS for the six desktop wireframe screens.

### Real UI screenshots

- Folder: [docs/screenshots](docs/screenshots)
- Contains screenshots of the implemented UI, including:
  - Profile page (desktop and mobile)
  - Teacher Dashboard (desktop and mobile)
  - Admin Dashboard (desktop and mobile)
  - Home page views

These screenshots illustrate how the final implementation aligns with the original wireframes and user flow.

## Testing and validation

The latest testing and validation details (backend tests, frontend tests, TypeScript check, production build, HTML/CSS validation) are documented in:

- “Testing” and “Validation” sections of the root [README.md](../README.md)

In brief:

- Django tests (`python manage.py test`) pass.
- Frontend tests (`npm test`), TypeScript check (`npx tsc --noEmit`), and production build (`npm run build`) have been run successfully.
- Key HTML and CSS files have been validated with the W3C Nu HTML checker and CSS validator.

## Notes for assessment

- The main starting point for understanding the project is the root [README.md](../README.md).
- For a quick mental model of the user journey, the Figma prototype link and the PNGs in [docs/wireframes](docs/wireframes) are helpful.
- For seeing the implemented UI in context, the screenshots in [docs/screenshots](docs/screenshots) provide desktop and mobile views.

If you have any questions about specific features (for example, role-based access control, enrollment logic, or lesson/quiz handling), I am happy to clarify or point you to the relevant files.
