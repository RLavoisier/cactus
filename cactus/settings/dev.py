from .base import *

# A utiliser en mode test
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 'cactus.test.tg@gmail.com'
#EMAIL_HOST_PASSWORD = 'toto1234toto1234'
#EMAIL_USE_TLS = True
#EMAIL_USE_SSL = False
#EMAIL_TIMEOUT = 30
#EMAIL_SSL_KEYFILE = None
#EMAIL_SSL_CERTFILE = None

EMAIL_HOST = 'smtp.cfa-epure.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'no_reply@cfa-epure.com'
EMAIL_HOST_PASSWORD = 'imRp4%04'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 30
EMAIL_SSL_KEYFILE = None
EMAIL_SSL_CERTFILE = None

DEBUG = True
