from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.api_views import (
    EixoViewSet,
    SituacaoAcaoViewSet,
    VigenciaPNGIViewSet,
    UserManagementViewSet,
    portal_auth,
)


# Configuração do router para ViewSets
router = DefaultRouter()
router.register(r'eixos', EixoViewSet, basename='eixo')
router.register(r'situacoes', SituacaoAcaoViewSet, basename='situacao')
router.register(r'vigencias', VigenciaPNGIViewSet, basename='vigencia')
router.register(r'users', UserManagementViewSet, basename='user')

app_name = 'acoes_pngi_api'  # ← MUDOU: namespace específico para API

urlpatterns = [
    # Autenticação via portal
    path('auth/portal/', portal_auth, name='portal-auth'),
    
    # Rotas do router (ViewSets)
    path('', include(router.urls)),
]
