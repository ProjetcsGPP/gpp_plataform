"""
API Views Package - Exports de todos os ViewSets e endpoints modulares.
Padronização seguindo estrutura de carga_org_lot.
"""

# Auth Views
from .auth_views import (
    portal_auth,
    UserManagementViewSet,
    get_app_code
)

# Core Views
from .core_views import (
    EixoViewSet,
    SituacaoAcaoViewSet,
    VigenciaPNGIViewSet,
    TipoEntraveAlertaViewSet
)

# Acoes Views
from .acoes_views import (
    AcoesViewSet,
    AcaoPrazoViewSet,
    AcaoDestaqueViewSet
)

# Alinhamento Views
from .alinhamento_views import (
    TipoAnotacaoAlinhamentoViewSet,
    AcaoAnotacaoAlinhamentoViewSet
)

# Responsavel Views
from .responsavel_views import (
    UsuarioResponsavelViewSet,
    RelacaoAcaoUsuarioResponsavelViewSet
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
