import os
import sys

path='/var/www/cactus'

if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'cactus.settings.prod'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
