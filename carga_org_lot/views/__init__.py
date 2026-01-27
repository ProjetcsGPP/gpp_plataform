"""
Views do módulo carga_org_lot
Centraliza todos os imports para manter compatibilidade retroativa
"""

# ================================
# Web Views (Django Templates)
# ================================
from .web_views.auth_views import *
from .web_views.dashboard_views import *
from .web_views.patriarca_views import *
from .web_views.organograma_views import *
from .web_views.lotacao_views import *
from .web_views.carga_views import *
from .web_views.upload_views import *
from .web_views.ajax_views import *

# ================================
# API Views (REST Framework)
# ================================
from .api_views.patriarca_api import *
from .api_views.organograma_api import *
from .api_views.lotacao_api import *
from .api_views.carga_api import *

__all__ = [
    # Web Views
    # TODO: Adicionar nomes das classes/funções
    
    # API Views
    # TODO: Adicionar nomes dos ViewSets
]
