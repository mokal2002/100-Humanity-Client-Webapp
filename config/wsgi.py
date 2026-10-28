"""
WSGI config for 100% HUMANITY project.
Exposes both `application` (standard WSGI) and `app` (for Vercel Python runtime).
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
app = application
