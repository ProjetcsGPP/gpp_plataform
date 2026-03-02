"""
Configuração pytest para testes Django do TokenService.
"""

import os
import django
from pytest import fixture

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gpp_plataform.settings")
django.setup()


@fixture(autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    """Configuração automática do banco para todos os testes."""
    pass


@fixture(autouse=True)
def clear_cache():
    """Limpa cache antes de cada teste."""
    from django.core.cache import cache
    cache.clear()
