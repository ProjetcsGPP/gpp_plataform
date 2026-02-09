"""
URL Configuration para API do Ações PNGI.
Registra todos os ViewSets no router do DRF.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ..views.api_views import (
    portal_auth,
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
    RelacaoAcaoUsuarioResponsavelViewSet
)

app_name = 'acoes_pngi_api'

router = DefaultRouter()

# Rotas de gerenciamento de usuários
router.register(r'users', UserManagementViewSet, basename='users')

# Rotas dos modelos PNGI
router.register(r'eixos', EixoViewSet, basename='eixo')
router.register(r'situacoes', SituacaoAcaoViewSet, basename='situacaoacao')
router.register(r'vigencias', VigenciaPNGIViewSet, basename='vigenciapngi')
router.register(r'tipos-entrave-alerta', TipoEntraveAlertaViewSet, basename='tipoentravealerta')
router.register(r'acoes', AcoesViewSet, basename='acoes')
router.register(r'acoes-prazo', AcaoPrazoViewSet, basename='acaoprazo')
router.register(r'acoes-destaque', AcaoDestaqueViewSet, basename='acaodestaque')
router.register(r'tipos-anotacao-alinhamento', TipoAnotacaoAlinhamentoViewSet, basename='tipoanotacaoalinhamento')
router.register(r'acoes-anotacao-alinhamento', AcaoAnotacaoAlinhamentoViewSet, basename='acaoanotacaoalinhamento')
router.register(r'usuarios-responsaveis', UsuarioResponsavelViewSet, basename='usuarioresponsavel')
router.register(r'relacoes-acao-responsavel', RelacaoAcaoUsuarioResponsavelViewSet, basename='relacaoacaousuarioresponsavel')

urlpatterns = [
    # Autenticação via portal
    path('auth/portal/', portal_auth, name='portal_auth'),
    
    # Rotas do router
    path('', include(router.urls)),
]
