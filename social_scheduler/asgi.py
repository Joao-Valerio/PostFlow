"""
ASGI config for social_scheduler project.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_scheduler.settings")

application = get_asgi_application()
