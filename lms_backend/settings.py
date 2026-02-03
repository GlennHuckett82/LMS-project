"""Django settings for lms_backend project."""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# In production (Render) this comes from the SECRET_KEY env var
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-934e^9_8*mbbjyban@bpbdpl0qm4477!xtu@24q+$dw_+0_ke7',
)

# DEBUG is controlled via an environment variable (DEBUG="True" or "False")
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# Always allow local addresses; also allow the Render hostname if present
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_host:
    ALLOWED_HOSTS.append(render_host)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'courses',
    'enrollments',
    'lessons',
    'quizzes',
    'rest_framework',
    'rest_framework_simplejwt',
    # ✅ Added for CORS
    'corsheaders',
]

MIDDLEWARE = [
    # ✅ Added for CORS (must be at the very top)
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lms_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lms_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Use WhiteNoise's default static file handling without manifest hashing.
# This avoids missing-manifest issues on Render where collectstatic is not run.
# If you later add a collectstatic step to your build, you can switch back to
# 'whitenoise.storage.CompressedManifestStaticFilesStorage'.
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',
        'anon': '200/day',
    }
}

# ✅ Allow frontend at localhost:3000 and Netlify
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://lms-project-frontend.netlify.app",
]