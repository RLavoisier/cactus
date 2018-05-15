from .base import *

DEBUG = False
ALLOWED_HOSTS = ['www.cfa-epure.com',]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'cactus.test.tg@gmail.com'
EMAIL_HOST_PASSWORD = 'toto1234toto1234'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 30
EMAIL_SSL_KEYFILE = None
EMAIL_SSL_CERTFILE = None