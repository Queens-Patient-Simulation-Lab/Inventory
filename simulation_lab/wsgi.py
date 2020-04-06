"""
WSGI config for simulation_lab project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simulation_lab.settings')

application = get_wsgi_application()

# Heroku can't presist the search index so it must be manually rebuilt at startup
if settings.ON_HEROKU:
    call_command("update_index", remove=True)