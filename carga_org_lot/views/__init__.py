"""
Carga Org/Lot Views
===================

Centraliza todos os imports de views (web e API) para manter compatibilidade retroativa.
Após a refatoração, o código existente que importa de `carga_org_lot.views` continua funcionando.

Exemplo:
    from carga_org_lot.views import carga_login, PatriarcaViewSet
"""

# ============================================
# API VIEWS (REST Framework ViewSets)
# ============================================
from .api_views import (  # Funções de view; ViewSets Principais; ViewSets Novos; ViewSets Auxiliares (Read-Only)
    CargaPatriarcaViewSet,
    LotacaoJsonOrgaoViewSet,
    LotacaoVersaoViewSet,
    OrganogramaVersaoViewSet,
    PatriarcaViewSet,
    StatusCargaViewSet,
    StatusProgressoViewSet,
    StatusTokenEnvioCargaViewSet,
    TipoCargaViewSet,
    TokenEnvioCargaViewSet,
    UserManagementViewSet,
    dashboard_stats,
    search_orgao,
    user_permissions,
)
from .web_views.ajax_views import search_orgao_ajax

# ============================================
# WEB VIEWS (Django Template Views)
# ============================================
from .web_views.auth_views import carga_login, carga_logout, carga_org_lot_required
from .web_views.carga_views import carga_detail, carga_list
from .web_views.dashboard_views import carga_dashboard
from .web_views.lotacao_views import (
    lotacao_detail,
    lotacao_inconsistencias,
    lotacao_list,
)
from .web_views.organograma_views import (
    organograma_detail,
    organograma_hierarquia_json,
    organograma_list,
)
from .web_views.patriarca_views import patriarca_detail, patriarca_list
from .web_views.upload_views import (
    upload_lotacao_handler,
    upload_organograma_handler,
    upload_page,
)

# ============================================
# EXPORTS
# ============================================
__all__ = [
    # Auth & Decorators
    "carga_login",
    "carga_logout",
    "carga_org_lot_required",
    # Dashboard Web
    "carga_dashboard",
    # Patriarca Web
    "patriarca_list",
    "patriarca_detail",
    # Organograma Web
    "organograma_list",
    "organograma_detail",
    "organograma_hierarquia_json",
    # Lotação Web
    "lotacao_list",
    "lotacao_detail",
    "lotacao_inconsistencias",
    # Carga Web
    "carga_list",
    "carga_detail",
    # Upload Web
    "upload_page",
    "upload_organograma_handler",
    "upload_lotacao_handler",
    # AJAX
    "search_orgao_ajax",
    # API Functions
    "user_permissions",
    "dashboard_stats",
    "search_orgao",
    # API ViewSets Principais
    "UserManagementViewSet",
    "PatriarcaViewSet",
    "OrganogramaVersaoViewSet",
    "LotacaoVersaoViewSet",
    "CargaPatriarcaViewSet",
    # API ViewSets Novos
    "LotacaoJsonOrgaoViewSet",
    "TokenEnvioCargaViewSet",
    # API ViewSets Auxiliares (Read-Only)
    "StatusProgressoViewSet",
    "StatusCargaViewSet",
    "TipoCargaViewSet",
    "StatusTokenEnvioCargaViewSet",
]
