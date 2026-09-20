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

# ── Database: Supabase PostgreSQL via DATABASE_URL ──
# Supabase gives: postgresql://postgres.[ref]:[PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres?pgbouncer=true
# or direct: postgresql://postgres:[PASSWORD]@db.[ref].supabase.co:5432/postgres
# Supports DATABASE_URL, POSTGRES_URL, SUPABASE_DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or os.getenv("SUPABASE_DATABASE_URL") or os.getenv("POSTGRES_PRISMA_URL")
if DATABASE_URL and dj_database_url:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)}
elif DATABASE_URL and not dj_database_url:
    # fallback manual parse for postgres://
    from urllib.parse import urlparse
    u = urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": u.path.lstrip("/").split("?")[0],
            "USER": u.username or "",
            "PASSWORD": u.password or "",
            "HOST": u.hostname or "127.0.0.1",
            "PORT": str(u.port or 5432),
        }
    }
else:
    # Fallback individual POSTGRES_* vars (Supabase dashboard)
    if os.getenv("POSTGRES_HOST") or os.getenv("SUPABASE_HOST"):
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": os.getenv("POSTGRES_DATABASE", os.getenv("POSTGRES_DB", "postgres")),
                "USER": os.getenv("POSTGRES_USER", "postgres"),
                "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
                "HOST": os.getenv("POSTGRES_HOST", os.getenv("SUPABASE_HOST", "127.0.0.1")),
                "PORT": os.getenv("POSTGRES_PORT", "5432"),
            }
        }
    else:
        # Vercel build without DB env → sqlite fallback to avoid crash during collectstatic
        DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}  # noqa: F405
        if os.getenv("VERCEL") and not os.getenv("DATABASE_URL"):
            pass  # keep sqlite for build

# Security hardening
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False") == "True" and not DEBUG

STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa: F405
MEDIA_ROOT = BASE_DIR / "media"  # noqa: F405
WHITENOISE_AUTOREFRESH = DEBUG

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")

# SEO
SITE_URL = os.getenv("SITE_URL", "https://areybra.vercel.app").rstrip("/")  # noqa: F405
