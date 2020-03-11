"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from core.settings import BASE_DIR

load_dotenv(dotenv_path='../.env')

print(BASE_DIR)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.production')

application = get_wsgi_application()
