"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from core.settings import BASE_DIR

env_path = os.path.join(BASE_DIR, '.env')
print(BASE_DIR)
print(env_path)
load_dotenv(dotenv_path=env_path)


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.production')

application = get_wsgi_application()
