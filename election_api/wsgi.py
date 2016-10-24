"""
WSGI config for election_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
import dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "election_api.settings")
dotenv.read_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

application = get_wsgi_application()
