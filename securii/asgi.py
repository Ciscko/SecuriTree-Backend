"""
ASGI config for securii project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'securii.settings')

application = get_asgi_application()

from dotenv import load_dotenv
# loads the configs from .env
load_dotenv() 
from django.contrib.auth.models import User
users = User.objects.filter(is_superuser=True)

if not users[0]:
    User.objects.create_superuser(last_name=str(os.getenv('SUPERUSER_LAST_NAME')), first_name=str(os.getenv('SUPERUSER_FIRST_NAME')), username=str(os.getenv('SUPERUSER_USERNAME')), email=str(os.getenv('SUPERUSER_EMAIL')), password=str(os.getenv('SUPERUSER_PASSWORD')), is_active=True, is_staff=True)
else:
    user = users[0]
    user.first_name = str(os.getenv('SUPERUSER_FIRST_NAME'))
    user.last_name = str(os.getenv('SUPERUSER_LAST_NAME'))
    user.username = str(os.getenv('SUPERUSER_USERNAME'))
    user.email = str(os.getenv('SUPERUSER_EMAIL'))
    user.save()
    user.set_password(str(os.getenv('SUPERUSER_PASSWORD'))) 
    user.save()
