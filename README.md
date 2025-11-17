# LMS Backend

A Django REST Framework (DRF) backend for a Learning Management System (LMS). This API supports user authentication, course management, lesson delivery, and student enrollments with role-based access control.

## Overview

The LMS allows users to register with roles (student, teacher, admin). Students can browse and enroll in courses, teachers can create and manage their courses and lessons, and admins have full access. The system uses JWT for authentication and includes pagination, throttling, and comprehensive permissions.

### Key Features
- **User Roles**: Student, Teacher, Admin with specific permissions.
- **Courses**: CRUD operations with teacher ownership.
- **Lessons**: Ordered lessons per course, accessible based on enrollment.
- **Enrollments**: Students enroll in courses; teachers/admins view rosters.
- **Authentication**: JWT token-based login.
- **Security**: Role-based permissions, throttling (1000/day user, 200/day anon).
- **Testing**: Full test suite for all endpoints.

### Tech Stack
- **Backend**: Django 5.2, Django REST Framework 3.16
- **Database**: SQLite
- **Authentication**: Simple JWT
- **Testing**: Django's test framework
- **Other**: Faker for data population

## Setup Instructions

### Prerequisites
- Python 3.8+
- Git

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/GlennHuckett82/LMS-project.git
   cd lms_backend
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # On Windows PowerShell
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. (Optional) Populate with sample data:
   ```
   python populate_db.py
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```
   The API will be available at `http://127.0.0.1:8000/`.

### Environment Variables
- `SECRET_KEY`: Set in `lms_backend/settings.py` (change for production).
- `DEBUG`: Set to `False` for production.
- `ALLOWED_HOSTS`: Configure for deployment.

## API Endpoints

Base URL: `http://127.0.0.1:8000/api/`

### Authentication
- `POST /api/token/`: Obtain JWT token (username, password).
- `POST /api/token/refresh/`: Refresh JWT token.
- `POST /api/token/verify/`: Verify JWT token.

### Accounts
- `POST /api/accounts/register/`: Register a new user (fields: username, email, password, role).
- Requires authentication for some operations, but registration is open.

### Courses
- `GET /api/courses/`: List all courses (public).
- `POST /api/courses/`: Create a course (teachers/admins only; teacher auto-assigned or specified by admin).
- `GET /api/courses/{id}/`: Retrieve a course (public).
- `PUT/PATCH /api/courses/{id}/`: Update a course (owner teacher or admin).
- `DELETE /api/courses/{id}/`: Delete a course (owner teacher or admin).

### Lessons
- `GET /api/lessons/`: List lessons (filtered by user role/enrollment).
- `POST /api/lessons/`: Create a lesson (course teacher or admin).
- `GET /api/lessons/{id}/`: Retrieve a lesson (enrolled students, teacher, admin).
- `PUT/PATCH /api/lessons/{id}/`: Update a lesson (course teacher or admin).
- `DELETE /api/lessons/{id}/`: Delete a lesson (course teacher or admin).

### Enrollments
- `POST /api/enrollments/course/{course_id}/enroll/`: Enroll in a course (students only).
- `GET /api/enrollments/my-enrollments/`: List student's enrollments (authenticated user).
- `GET /api/enrollments/course/{course_id}/roster/`: View course roster (course teacher or admin).

### Permissions
- **Anonymous**: Read courses/lessons.
- **Students**: Enroll, view enrolled content.
- **Teachers**: Manage own courses/lessons.
- **Admins**: Full access.

## Testing

Run the full test suite:
```
python manage.py test
```

Tests cover:
- User registration and roles.
- Course CRUD and permissions.
- Lesson access and management.
- Enrollment logic and rosters.

All 33 tests should pass.

## Deployment

### Heroku/Netlify
1. Set up a Heroku app or Netlify site.
2. Configure environment variables (SECRET_KEY, DEBUG=False, ALLOWED_HOSTS).
3. Use PostgreSQL for production (update DATABASES in settings.py).
4. Deploy via Git push or build process.
5. Run migrations on deployment.

### Local Production
- Use a WSGI server like Gunicorn.
- Serve static files with WhiteNoise or a CDN.
- Enable HTTPS.

## Contributing
- Follow Django best practices.
- Write tests for new features.
- Use Git for version control with descriptive commits.

## License
This project is for educational purposes. No specific license applied.