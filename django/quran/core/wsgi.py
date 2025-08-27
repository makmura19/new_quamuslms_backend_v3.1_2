import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app_name = "New QuamusLMS API - base"

try:
    application = get_wsgi_application()
except Exception as e:
    raise
