"""
Carga Org/Lot URLs

Este __init__.py resolve o conflito entre:
- carga_org_lot/urls/ (pasta com api_urls.py e web_urls.py)
- carga_org_lot/urls.py (arquivo principal com rotas web modernas)

Quando Django faz include('carga_org_lot.urls'), ele encontra esta pasta.
Por isso, importamos as rotas do arquivo urls.py da raiz.
"""

# Importa urlpatterns e app_name do arquivo urls.py na raiz do módulo
from ..urls import urlpatterns, app_name

__all__ = ['urlpatterns', 'app_name']
