from .base import *

DEBUG = False
ALLOWED_HOSTS = ['www.cfa-epure.com',]

EMAIL_HOST = 'smtp.cfa-epure.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'no_reply@cfa-epure.com'
EMAIL_HOST_PASSWORD = 'imRp4%04'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 30
EMAIL_SSL_KEYFILE = None
EMAIL_SSL_CERTFILE = None

EXTRA_DOMAIN_PATH = "cactus/"