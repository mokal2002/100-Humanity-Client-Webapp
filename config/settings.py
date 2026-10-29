"""
Django settings for 100% HUMANITY monolithic web application.
Configured for zero-cost local development (SQLite) and production deployment
(Neon PostgreSQL + WhiteNoise + Cloudinary + strict security headers).
"""
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# CORE SECURITY & ENVIRONMENT SETTINGS
# ==============================================================================
DEBUG = os.environ.get("DEBUG", "False").strip().lower() in ("true", "1", "yes")

SECRET_KEY = os.environ.get("SECRET_KEY", "").strip()
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-dev-only-key-for-100-humanity-local-testing-do-not-use-in-prod"
    else:
        raise ValueError("CRITICAL: SECRET_KEY environment variable must be set when DEBUG=False.")

raw_hosts = os.environ.get(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost,testserver,.onrender.com,.vercel.app,.pythonanywhere.com"
)
ALLOWED_HOSTS = [h.strip() for h in raw_hosts.split(",") if h.strip()]

raw_csrf = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [u.strip() for u in raw_csrf.split(",") if u.strip()]

# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # 100% HUMANITY Applications
    "apps.core.apps.CoreConfig",
    "apps.education.apps.EducationConfig",
    "apps.events.apps.EventsConfig",
    "apps.gallery.apps.GalleryConfig",
    "apps.videos.apps.VideosConfig",
    "apps.articles.apps.ArticlesConfig",
    "apps.contact.apps.ContactConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
]

# Enable WhiteNoise if installed for zero-cost static file serving in production
try:
    import whitenoise  # noqa: F401
    MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")
    WHITENOISE_AVAILABLE = True
except ImportError:
    WHITENOISE_AVAILABLE = False

MIDDLEWARE += [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "apps.core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ==============================================================================
# DATABASE CONFIGURATION (SQLite locally, Free PostgreSQL via DATABASE_URL in prod)
# ==============================================================================
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {
            "default": dj_database_url.parse(
                DATABASE_URL,
                conn_max_age=600,
                ssl_require=not DEBUG,
            )
        }
    except ImportError:
        raise ImportError(
            "dj-database-url is required when DATABASE_URL is set. "
            "Run `pip install dj-database-url psycopg2-binary`."
        )
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==============================================================================
# INTERNATIONALIZATION (English, Marathi, Hindi)
# ==============================================================================
LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", _("English")),
    ("mr", _("Marathi (मराठी)")),
    ("hi", _("Hindi (हिन्दी)")),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

if WHITENOISE_AVAILABLE and not DEBUG:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }
    WHITENOISE_MANIFEST_STRICT = False

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Maximum upload size: 5 MB per image to stay well within free Cloudinary limits
DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024  # 20 MB total form payload
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024   # 5 MB per file
MAX_IMAGE_UPLOAD_BYTES = 5 * 1024 * 1024        # 5 MB validation limit
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_IMAGE_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}

# ==============================================================================
# CLOUDINARY CONFIGURATION (Official Python SDK)
# ==============================================================================
CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME", "").strip()
CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY", "").strip()
CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET", "").strip()
CLOUDINARY_FOLDER = os.environ.get("CLOUDINARY_FOLDER", "100_humanity").strip()

CLOUDINARY_CONFIGURED = bool(
    CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET
)

if CLOUDINARY_CONFIGURED:
    try:
        import cloudinary
        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET,
            secure=True,
        )
    except ImportError:
        CLOUDINARY_CONFIGURED = False

# ==============================================================================
# SITE IDENTITY DEFAULTS
# ==============================================================================
DEFAULT_SITE_NAME = os.environ.get("SITE_NAME", "100% HUMANITY")
DEFAULT_CONTACT_PERSON = os.environ.get("CONTACT_PERSON", "Arvind Betkar")
DEFAULT_CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "arvindbet12@gmail.com")
DEFAULT_CONTACT_PHONE = os.environ.get("CONTACT_PHONE", "8983087210")
DEFAULT_YOUTUBE_CHANNEL_NAME = os.environ.get("YOUTUBE_CHANNEL_NAME", "100% HUMANITY")
DEFAULT_YOUTUBE_CHANNEL_URL = os.environ.get("YOUTUBE_CHANNEL_URL", "")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================================================================
# PRODUCTION SECURITY HARDENING (Active when DEBUG=False)
# ==============================================================================
if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True").lower() in ("true", "1")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
