import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
# WhiteNoise serve static directly on Vercel serverless (fallback if middleware misses)
try:
    from whitenoise import WhiteNoise
    from pathlib import Path
    from django.conf import settings
    # root is STATIC_ROOT, prefix is STATIC_URL
    app = WhiteNoise(app, root=str(settings.STATIC_ROOT), prefix=settings.STATIC_URL)
except Exception:
    pass
# Vercel expects `app` or `handler`
application = app
handler = app
