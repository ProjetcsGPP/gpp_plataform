# gpp_plataform/settings_test.py
from .settings import *
import os
from decouple import config

# Usar PostgreSQL para testes (igual ao ambiente real)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='gpp_plataform'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'TEST': {
            # Nome do banco de teste (será criado automaticamente)
            'NAME': 'test_gpp_plataform',
            # Charset
            'CHARSET': 'UTF8',
        },
    }
}

# Acelerar testes
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Desabilitar debug em testes
DEBUG = False
TEMPLATE_DEBUG = False

# Logging mínimo
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Test Runner customizado
TEST_RUNNER = 'common.test_runner.CustomTestRunner'