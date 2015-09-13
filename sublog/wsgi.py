"""
WSGI config for sublog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""
import logging
import os

from django.core.wsgi import get_wsgi_application

from sublog import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sublog.settings")

application = get_wsgi_application()

logging.getLogger('sublog').info('----------------------')
logging.getLogger('sublog').info('server started. %s' % settings.SU_VERSION)
