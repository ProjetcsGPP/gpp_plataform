"""
URLs da API REST de Ações PNGI
Inclui endpoints de dados + novos endpoints de contexto

Exemplos:
- GET /api/v1/acoes_pngi/acoes/
- POST /api/v1/acoes_pngi/acoes/
- GET /api/v1/acoes_pngi/context/app/
- GET /api/v1/acoes_pngi/context/permissions/
- GET /api/v1/acoes_pngi/context/models/
- GET /api/v1/acoes_pngi/context/full/
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importar TODAS as views da API
from ..views.api_views import (
    portal_auth,
    user_permissions,
    UserManagementViewSet,
    EixoViewSet,
    SituacaoAcaoViewSet,
    VigenciaPNGIViewSet,
    TipoEntraveAlertaViewSet,
    AcoesViewSet,
    AcaoPrazoViewSet,
    AcaoDestaqueViewSet,
    TipoAnotacaoAlinhamentoViewSet,
    AcaoAnotacaoAlinhamentoViewSet,
    UsuarioResponsavelViewSet,
    RelacaoAcaoUsuarioResponsavelViewSet,
)

# Importar views de contexto
from ..views.context_api_views import (
    app_context_api,
    user_permissions_api,
    models_info_api,
    full_context_api,
)

app_name = 'acoes_pngi_api'

# Registra ViewSets no Router
router = DefaultRouter()

# Usuários e autenticação
router.register(r'users', UserManagementViewSet, basename='user-management')

# Entidades Core
router.register(r'eixos', EixoViewSet, basename='eixo')
router.register(r'situacoes', SituacaoAcaoViewSet, basename='situacaoacao')
router.register(r'vigencias', VigenciaPNGIViewSet, basename='vigenciapngi')
router.register(r'tipos-entrave-alerta', TipoEntraveAlertaViewSet, basename='tipoentravealerta')

# Ações PNGI
router.register(r'acoes', AcoesViewSet, basename='acoes')
router.register(r'acoes-prazo', AcaoPrazoViewSet, basename='acaoprazo')
router.register(r'acoes-destaque', AcaoDestaqueViewSet, basename='acaodestaque')

# Alinhamento
router.register(r'tipos-anotacao-alinhamento', TipoAnotacaoAlinhamentoViewSet, basename='tipoanotacaoalinhamento')
router.register(r'acoes-anotacao-alinhamento', AcaoAnotacaoAlinhamentoViewSet, basename='acaoanotacaoalinhamento')

# Responsáveis
router.register(r'usuarios-responsaveis', UsuarioResponsavelViewSet, basename='usuarioresponsavel')
router.register(r'relacoes-acao-responsavel', RelacaoAcaoUsuarioResponsavelViewSet, basename='relacaoacaousuarioresponsavel')

urlpatterns = [
    # ===== AUTENTICAÇÃO =====
    path('auth/portal/', portal_auth, name='portal-auth'),
    path('permissions/', user_permissions, name='user-permissions'),
    
    # ===== CONTEXTO PARA NEXT.JS =====
    path('context/app/', app_context_api, name='app-context'),
    path('context/permissions/', user_permissions_api, name='context-permissions'),
    path('context/models/', models_info_api, name='models-info'),
    path('context/full/', full_context_api, name='full-context'),
    
    # ===== VIEWSETS (Router) =====
    path('', include(router.urls)),
]
