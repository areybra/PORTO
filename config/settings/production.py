from .base import *  # noqa: F403, F401
import os

try:
    import dj_database_url  # noqa: F401
except ImportError:
    dj_database_url = None

DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if os.getenv("DJANGO_ALLOWED_HOSTS") else ["*"]
# Vercel adds VERCEL_URL automatically
if os.getenv("VERCEL_URL"):
    ALLOWED_HOSTS.append(os.getenv("VERCEL_URL"))
    ALLOWED_HOSTS.append(f".vercel.app")
CSRF_TRUSTED_ORIGINS = []
for h in ALLOWED_HOSTS:
    if h != "*" and h:
        if not h.startswith("http"):
            CSRF_TRUSTED_ORIGINS.append(f"https://{h}")
            CSRF_TRUSTED_ORIGINS.append(f"https://{h.lstrip('.')}")
# also add SITE_URL host
site_host = os.getenv("SITE_URL", "")
if site_host:
    try:
        from urllib.parse import urlparse
        host = urlparse(site_host).netloc
        if host and f"https://{host}" not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(f"https://{host}")
    except Exception:
        pass

# ── Database: Railway DATABASE_URL / MYSQL_URL → dj-database-url, else fallback to MYSQL_* / sqlite ──
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("MYSQL_URL") or os.getenv("MYSQL_PUBLIC_URL") or os.getenv("RAILWAY_MYSQL_URL")
if DATABASE_URL and dj_database_url:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=False)}
    # Railway MySQL sometimes needs charset
    DATABASES["default"].setdefault("OPTIONS", {})
    DATABASES["default"]["OPTIONS"].setdefault("charset", "utf8mb4")
elif DATABASE_URL and not dj_database_url:
    # fallback manual parse for mysql://
    from urllib.parse import urlparse
    u = urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": u.path.lstrip("/"),
            "USER": u.username or "",
            "PASSWORD": u.password or "",
            "HOST": u.hostname or "127.0.0.1",
            "PORT": str(u.port or 3306),
            "OPTIONS": {"charset": "utf8mb4", "init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("MYSQL_DATABASE", "areybra_porto"),
            "USER": os.getenv("MYSQL_USER", "root"),
            "PASSWORD": os.getenv("MYSQL_PASSWORD", ""),
            "HOST": os.getenv("MYSQL_HOST", "127.0.0.1"),
            "PORT": os.getenv("MYSQL_PORT", "3306"),
            "OPTIONS": {"charset": "utf8mb4", "init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
        }
    }
    # if no mysql env at all on Vercel without DB, fallback to sqlite to avoid crash (read-only)
    if not os.getenv("MYSQL_DATABASE") and not os.getenv("MYSQL_HOST") and os.getenv("VERCEL"):
        DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}  # noqa: F405

# Security hardening
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False") == "True" and not DEBUG

STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa: F405
MEDIA_ROOT = BASE_DIR / "media"  # noqa: F405
# Vercel: static served by whitenoise, no need for extra config
WHITENOISE_AUTOREFRESH = DEBUG

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")

# SEO
SITE_URL = os.getenv("SITE_URL", "https://areybra.vercel.app").rstrip("/")  # noqa: F405
