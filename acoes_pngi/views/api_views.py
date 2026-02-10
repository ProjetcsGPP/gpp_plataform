"""
API Views do Ações PNGI.

ARQUIVO DE COMPATIBILIDADE - Importa de api_views/ modular.
Toda implementação agora está em módulos especializados dentro de api_views/.

Estrutura modular:
- api_views/auth_views.py: Autenticação e gerenciamento de usuários
- api_views/core_views.py: Entidades core (Eixo, Situação, Vigência, Tipo Entrave)
- api_views/acoes_views.py: Ações, Prazos e Destaques
- api_views/alinhamento_views.py: Anotações de alinhamento
- api_views/responsavel_views.py: Usuários responsáveis

Todos os imports diretos deste arquivo continuam funcionando para manter compatibilidade.
"""

# Importa tudo dos módulos especializados
from .api_views import *  # noqa: F401, F403

# Mantém compatibilidade com imports específicos
from .api_views import (
    # Auth
    portal_auth,
    UserManagementViewSet,
    get_app_code,
    
    # Core
    EixoViewSet,
    SituacaoAcaoViewSet,
    VigenciaPNGIViewSet,
    TipoEntraveAlertaViewSet,
    
    # Acoes
    AcoesViewSet,
    AcaoPrazoViewSet,
    AcaoDestaqueViewSet,
    
    # Alinhamento
    TipoAnotacaoAlinhamentoViewSet,
    AcaoAnotacaoAlinhamentoViewSet,
    
    # Responsavel
    UsuarioResponsavelViewSet,
    RelacaoAcaoUsuarioResponsavelViewSet,
)

__all__ = [
    # Auth
    'portal_auth',
    'UserManagementViewSet',
    'get_app_code',
    
    # Core
    'EixoViewSet',
    'SituacaoAcaoViewSet',
    'VigenciaPNGIViewSet',
    'TipoEntraveAlertaViewSet',
    
    # Acoes
    'AcoesViewSet',
    'AcaoPrazoViewSet',
    'AcaoDestaqueViewSet',
    
    # Alinhamento
    'TipoAnotacaoAlinhamentoViewSet',
    'AcaoAnotacaoAlinhamentoViewSet',
    
    # Responsavel
    'UsuarioResponsavelViewSet',
    'RelacaoAcaoUsuarioResponsavelViewSet',
]
