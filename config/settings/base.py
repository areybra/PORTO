import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-8_(p&5rzr(3cl@9%nn2vwb615+-s*1r61&z4fs5ua$yj^&cf1*")

DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",") if os.getenv("DJANGO_ALLOWED_HOSTS") else ["*"]

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "apps.core",
    "apps.portfolio",
    "apps.blog",
    "apps.contact",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
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
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_profile",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Default sqlite - overridden by development/production
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "id"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# SEO / GEO
SITE_URL = os.getenv("SITE_URL", "https://areybra.vercel.app").rstrip("/")
SITE_NAME = "AREYBRA"
SITE_BRAND_ALIASES = ["Areybra", "Areta Y. Radjawali", "Areta Ybei Radjawali", "Areta Radjawali", "AREYBRA Studio"]
DEFAULT_META_DESCRIPTION = "Portofolio Areta Y. Radjawali (Areybra / Areta Ybei Radjawali) — Junior Web Developer, SMK Nurul Jadid RPL. Spesialis Django, Tailwind, MySQL, Linux, Cyber Security & Data Analyst. Jakarta, Indonesia."
DEFAULT_META_KEYWORDS = "Areta Y Radjawali, Areta Ybei Radjawali, Areybra, AREYBRA, Areta Radjawali, Junior Web Developer, Django Developer, SMK Nurul Jadid, Portfolio Django, Tailwind, MySQL, Cyber Security"
DEFAULT_OG_IMAGE = os.getenv("DEFAULT_OG_IMAGE", "https://lh3.googleusercontent.com/aida/AEtjO1UEoiyjmRKUBIc9t_Fndn02qah9zD4YxMOclwvCsw3RgF04tBa7qBJtB3e-J04xQLKcvUDjFs3W9OGpRH2ONio9YqP3AFOlbnf_VADprquwDe9nBnqaSBN4w2LlKcPBqpkEODL3pzu4GkgxG44ucGQRBvUR2HQGWMBjGgDsHFLRA1U1NAfAjAKRmAirn9ZaUcwEP-OH1rfpqF-1S_JV3Za18csDTh8B6C7BX43cPLUS05jJpemociIHRQPo")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# WhatsApp redirect
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "6282142961010")

# Jazzmin
JAZZMIN_SETTINGS = {
    "site_title": "AREYBRA Admin",
    "site_header": "AREYBRA Studio",
    "site_brand": "AREYBRA",
    "welcome_sign": "Dashboard Portofolio — Areta Y. Radjawali",
    "copyright": "AREYBRA Studio © 2025",
    "site_logo": None,
    "login_logo": None,
    "site_icon": None,
    "search_model": ["portfolio.Project", "blog.Post", "contact.ContactMessage"],
    "topmenu_links": [
        {"name": "Lihat Situs", "url": "/", "new_window": True},
        {"model": "auth.User"},
    ],
    "usermenu_links": [
        {"name": "Lihat Situs", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": False,
    "order_with_respect_to": ["core", "portfolio", "blog", "contact", "auth"],
    "icons": {
        "core.SiteProfile": "fas fa-id-card",
        "core.SocialLink": "fas fa-link",
        "core.Service": "fas fa-concierge-bell",
        "core.FAQ": "fas fa-question-circle",
        "portfolio.Category": "fas fa-folder",
        "portfolio.Technology": "fas fa-code",
        "portfolio.Project": "fas fa-layer-group",
        "blog.Category": "fas fa-tag",
        "blog.Post": "fas fa-pen-nib",
        "contact.ContactMessage": "fas fa-envelope",
        "auth.User": "fas fa-user",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": True,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "flatly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

# Email (dev console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
