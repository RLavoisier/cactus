import os
import sys

path='/var/www/cactus'

if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'cactus.settings.prod'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
