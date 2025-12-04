"""
WSGI config for clothshop project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothshop.settings')

application = get_wsgi_application()
