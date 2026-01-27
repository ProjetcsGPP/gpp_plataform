"""
Carga Org/Lot Views
===================

Centraliza todos os imports de views (web e API) para manter compatibilidade retroativa.
Após a refatoração, o código existente que importa de `carga_org_lot.views` continua funcionando.

Exemplo:
    from carga_org_lot.views import carga_login, PatriarcaViewSet
"""

# ============================================
# WEB VIEWS (Django Template Views)
# ============================================
from .web_views.auth_views import (
    carga_login,
    carga_logout,
    carga_org_lot_required,
)
from .web_views.dashboard_views import carga_dashboard
from .web_views.patriarca_views import (
    patriarca_list,
    patriarca_detail,
)
from .web_views.organograma_views import (
    organograma_list,
    organograma_detail,
    organograma_hierarquia_json,
)
from .web_views.lotacao_views import (
    lotacao_list,
    lotacao_detail,
    lotacao_inconsistencias,
)
from .web_views.carga_views import (
    carga_list,
    carga_detail,
)
from .web_views.upload_views import (
    upload_page,
    upload_organograma_handler,
    upload_lotacao_handler,
)
from .web_views.ajax_views import search_orgao_ajax

# ============================================
# API VIEWS (REST Framework ViewSets)
# ============================================
from .api_views.dashboard_api import (
    dashboard_stats,
    search_orgao,
    upload_organograma,
    upload_lotacao,
)
from .api_views.patriarca_api import PatriarcaViewSet
from .api_views.organograma_api import OrganogramaVersaoViewSet
from .api_views.lotacao_api import LotacaoVersaoViewSet
from .api_views.carga_api import CargaPatriarcaViewSet


# ============================================
# EXPORTS
# ============================================
__all__ = [
    # Auth & Decorators
    'carga_login',
    'carga_logout',
    'carga_org_lot_required',
    
    # Dashboard
    'carga_dashboard',
    
    # Patriarca
    'patriarca_list',
    'patriarca_detail',
    
    # Organograma
    'organograma_list',
    'organograma_detail',
    'organograma_hierarquia_json',
    
    # Lotação
    'lotacao_list',
    'lotacao_detail',
    'lotacao_inconsistencias',
    
    # Carga
    'carga_list',
    'carga_detail',
    
    # Upload
    'upload_page',
    'upload_organograma_handler',
    'upload_lotacao_handler',
    
    # AJAX
    'search_orgao_ajax',
    
    # API Dashboard
    'dashboard_stats',
    'search_orgao',
    'upload_organograma',
    'upload_lotacao',
    
    # API ViewSets
    'PatriarcaViewSet',
    'OrganogramaVersaoViewSet',
    'LotacaoVersaoViewSet',
    'CargaPatriarcaViewSet',
]
