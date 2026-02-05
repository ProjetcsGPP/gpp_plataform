"""
URLs da API REST de Ações PNGI
Inclui endpoints de dados + novos endpoints de contexto

Exemplos:
- GET /api/v1/acoes_pngi/eixos/
- POST /api/v1/acoes_pngi/eixos/
- GET /api/v1/acoes_pngi/context/app/
- GET /api/v1/acoes_pngi/context/permissions/
- GET /api/v1/acoes_pngi/context/models/
- GET /api/v1/acoes_pngi/context/full/
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.api_views import (
    portal_auth,
    user_permissions,
    UserManagementViewSet,
    EixoViewSet,
    SituacaoAcaoViewSet,
    VigenciaPNGIViewSet,
)
from ..views.context_api_views import (
    app_context_api,
    user_permissions_api,
    models_info_api,
    full_context_api,
)

app_name = 'acoes_pngi_api'

# Registra ViewSets
router = DefaultRouter()
router.register(r'users', UserManagementViewSet, basename='user-management')
router.register(r'eixos', EixoViewSet, basename='eixo')
router.register(r'situacoes', SituacaoAcaoViewSet, basename='situacaoacao')
router.register(r'vigencias', VigenciaPNGIViewSet, basename='vigenciapngi')

urlpatterns = [
    # ===== AUTENTICAÇÃO =====
    path('auth/portal/', portal_auth, name='portal-auth'),
    path('permissions/', user_permissions, name='user-permissions'),
    
    # ===== CONTEXTO PARA NEXT.JS =====
    path('context/app/', app_context_api, name='app-context'),
    path('context/permissions/', user_permissions_api, name='context-permissions'),
    path('context/models/', models_info_api, name='models-info'),
    path('context/full/', full_context_api, name='full-context'),
    
    # ===== VIEWSETS =====
    path('', include(router.urls)),
]
