for .settings import *
STATIC_ROOT = 'staticfiles'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARD_PROTO', 'https')
ALLOWED_HOSTS = ['*']
DEBUG = False