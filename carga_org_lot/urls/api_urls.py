"""
Carga Org/Lot - API URLs
========================

Endpoints REST para consumo do Next.js.

Prefixo base: /api/v1/carga/

Estrutura:
- ViewSets (CRUD completo) -> router DRF
- Funções (@api_view) -> path() manual
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ..views import (
    # Funções de view
    user_permissions,
    dashboard_stats,
    search_orgao,
    
    # ViewSets
    UserManagementViewSet,
    StatusProgressoViewSet,
    StatusCargaViewSet,
    TipoCargaViewSet,
    StatusTokenEnvioCargaViewSet,
    PatriarcaViewSet,
    OrganogramaVersaoViewSet,
    OrgaoUnidadeViewSet,
    LotacaoVersaoViewSet,
    CargaPatriarcaViewSet,
    TokenEnvioCargaViewSet,
)


app_name = 'carga_org_lot_api'


# =============================================================================
# ROUTER DRF - ViewSets (CRUD automático)
# =============================================================================

router = DefaultRouter()

# Gerenciamento de usuários
router.register(
    r'users',
    UserManagementViewSet,
    basename='users'
)

# Modelos principais
router.register(
    r'patriarcas',
    PatriarcaViewSet,
    basename='patriarcas'
)

router.register(
    r'organogramas',
    OrganogramaVersaoViewSet,
    basename='organogramas'
)

router.register(
    r'orgaos',
    OrgaoUnidadeViewSet,
    basename='orgaos'
)

router.register(
    r'lotacoes',
    LotacaoVersaoViewSet,
    basename='lotacoes'
)

router.register(
    r'cargas',
    CargaPatriarcaViewSet,
    basename='cargas'
)

router.register(
    r'tokens',
    TokenEnvioCargaViewSet,
    basename='tokens'
)

# Tabelas auxiliares (read-only)
router.register(
    r'status-progresso',
    StatusProgressoViewSet,
    basename='status-progresso'
)

router.register(
    r'status-carga',
    StatusCargaViewSet,
    basename='status-carga'
)

router.register(
    r'tipos-carga',
    TipoCargaViewSet,
    basename='tipos-carga'
)

router.register(
    r'status-token',
    StatusTokenEnvioCargaViewSet,
    basename='status-token'
)


# =============================================================================
# URL PATTERNS - Funções e ViewSets
# =============================================================================

urlpatterns = [
    # =========================================================================
    # ENDPOINTS DE FUNÇÃO (@api_view)
    # =========================================================================
    
    # Permissões do usuário (para Next.js)
    path(
        'permissions/',
        user_permissions,
        name='user-permissions'
    ),
    
    # Dashboard e estatísticas
    path(
        'dashboard/',
        dashboard_stats,
        name='dashboard-stats'
    ),
    
    # Busca rápida (autocomplete)
    path(
        'search/orgao/',
        search_orgao,
        name='search-orgao'
    ),
    
    # =========================================================================
    # VIEWSETS (DRF Router)
    # =========================================================================
    # Inclui todas as rotas dos ViewSets registrados no router:
    # - GET    /patriarcas/           -> list
    # - POST   /patriarcas/           -> create
    # - GET    /patriarcas/{id}/      -> retrieve
    # - PUT    /patriarcas/{id}/      -> update
    # - PATCH  /patriarcas/{id}/      -> partial_update
    # - DELETE /patriarcas/{id}/      -> destroy
    # - GET    /patriarcas/list_light/ -> custom action
    # - etc...
    path('', include(router.urls)),
]


# =============================================================================
# DOCUMENTAÇÃO DAS ROTAS
# =============================================================================
"""
Endpoints disponíveis após /api/v1/carga/:

1. PERMISSÕES
   GET /permissions/

2. DASHBOARD
   GET /dashboard/
   GET /search/orgao/

3. USUÁRIOS
   GET    /users/
   GET    /users/{email}/
   POST   /users/sync_user/
   GET    /users/list_users/

4. PATRIARCAS
   GET    /patriarcas/
   POST   /patriarcas/
   GET    /patriarcas/{id}/
   PUT    /patriarcas/{id}/
   PATCH  /patriarcas/{id}/
   DELETE /patriarcas/{id}/
   GET    /patriarcas/list_light/
   GET    /patriarcas/{id}/organogramas/
   GET    /patriarcas/{id}/lotacoes/
   GET    /patriarcas/{id}/estatisticas/

5. ORGANOGRAMAS
   GET    /organogramas/
   POST   /organogramas/
   GET    /organogramas/{id}/
   PUT    /organogramas/{id}/
   PATCH  /organogramas/{id}/
   DELETE /organogramas/{id}/
   POST   /organogramas/{id}/ativar/
   GET    /organogramas/{id}/orgaos/
   GET    /organogramas/{id}/hierarquia/
   GET    /organogramas/{id}/json_envio/

6. ÓRGÃOS/UNIDADES
   GET    /orgaos/
   POST   /orgaos/
   GET    /orgaos/{id}/
   PUT    /orgaos/{id}/
   PATCH  /orgaos/{id}/
   DELETE /orgaos/{id}/

7. LOTAÇÕES
   GET    /lotacoes/
   POST   /lotacoes/
   GET    /lotacoes/{id}/
   PUT    /lotacoes/{id}/
   PATCH  /lotacoes/{id}/
   DELETE /lotacoes/{id}/
   POST   /lotacoes/{id}/ativar/
   GET    /lotacoes/{id}/registros/
   GET    /lotacoes/{id}/inconsistencias/
   GET    /lotacoes/{id}/estatisticas/

8. CARGAS
   GET    /cargas/
   POST   /cargas/
   GET    /cargas/{id}/
   PUT    /cargas/{id}/
   PATCH  /cargas/{id}/
   DELETE /cargas/{id}/
   GET    /cargas/{id}/timeline/

9. TOKENS
   GET    /tokens/
   POST   /tokens/
   GET    /tokens/{id}/
   PUT    /tokens/{id}/
   PATCH  /tokens/{id}/
   DELETE /tokens/{id}/

10. TABELAS AUXILIARES (read-only)
    GET /status-progresso/
    GET /status-progresso/{id}/
    GET /status-carga/
    GET /status-carga/{id}/
    GET /tipos-carga/
    GET /tipos-carga/{id}/
    GET /status-token/
    GET /status-token/{id}/


Query Params Comuns:
- patriarca={id}       - Filtro por patriarca
- ativos=true          - Apenas ativos
- status={id}          - Por status
- q={termo}            - Busca textual
- page={n}             - Página
- page_size={n}        - Tamanho da página
- ordering={field}     - Ordenação


Autenticação:
- Header: Authorization: Token {token}
- Ou session cookie (para navegador)


Permissões:
- Verificadas automaticamente via HasCargaOrgLotPermission
- Operações sensíveis requerem IsCoordenadorOrAbove ou IsGestor
"""
