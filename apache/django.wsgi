import os
import sys

site_path = '/var/journalx'
if site_path not in sys.path:
    sys.path.append(site_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'journalx.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
