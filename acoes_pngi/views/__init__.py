"""
Views Package - Exports de todas as views (API e Web).
Padronização completa seguindo estrutura de carga_org_lot.

Estrutura:
- api_views/: Módulos especializados de API ViewSets
- web_views/: Módulos especializados de Class-Based Views Web
- api_views.py: Arquivo de compatibilidade para imports diretos
- web_views.py: Arquivo de compatibilidade para imports diretos
"""

# Importa todas as API views
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

# Importa todas as Web views
from .web_views import (
    # Core
    EixoListView, EixoDetailView, EixoCreateView, EixoUpdateView, EixoDeleteView,
    SituacaoAcaoListView, SituacaoAcaoDetailView, SituacaoAcaoCreateView,
    SituacaoAcaoUpdateView, SituacaoAcaoDeleteView,
    VigenciaPNGIListView, VigenciaPNGIDetailView, VigenciaPNGICreateView,
    VigenciaPNGIUpdateView, VigenciaPNGIDeleteView,
    TipoEntraveAlertaListView, TipoEntraveAlertaDetailView, TipoEntraveAlertaCreateView,
    TipoEntraveAlertaUpdateView, TipoEntraveAlertaDeleteView,
    
    # Acoes
    AcoesListView, AcoesDetailView, AcoesCreateView, AcoesUpdateView, AcoesDeleteView,
    AcaoPrazoListView, AcaoPrazoDetailView, AcaoPrazoCreateView,
    AcaoPrazoUpdateView, AcaoPrazoDeleteView,
    AcaoDestaqueListView, AcaoDestaqueDetailView, AcaoDestaqueCreateView,
    AcaoDestaqueUpdateView, AcaoDestaqueDeleteView,
    
    # Alinhamento
    TipoAnotacaoAlinhamentoListView, TipoAnotacaoAlinhamentoDetailView,
    TipoAnotacaoAlinhamentoCreateView, TipoAnotacaoAlinhamentoUpdateView,
    TipoAnotacaoAlinhamentoDeleteView,
    AcaoAnotacaoAlinhamentoListView, AcaoAnotacaoAlinhamentoDetailView,
    AcaoAnotacaoAlinhamentoCreateView, AcaoAnotacaoAlinhamentoUpdateView,
    AcaoAnotacaoAlinhamentoDeleteView,
    
    # Responsavel
    UsuarioResponsavelListView, UsuarioResponsavelDetailView,
    UsuarioResponsavelCreateView, UsuarioResponsavelUpdateView,
    UsuarioResponsavelDeleteView,
    RelacaoAcaoUsuarioResponsavelListView, RelacaoAcaoUsuarioResponsavelDetailView,
    RelacaoAcaoUsuarioResponsavelCreateView, RelacaoAcaoUsuarioResponsavelUpdateView,
    RelacaoAcaoUsuarioResponsavelDeleteView,
)


__all__ = [
    # API Auth
    'portal_auth',
    'UserManagementViewSet',
    'get_app_code',
    
    # API Core
    'EixoViewSet',
    'SituacaoAcaoViewSet',
    'VigenciaPNGIViewSet',
    'TipoEntraveAlertaViewSet',
    
    # API Acoes
    'AcoesViewSet',
    'AcaoPrazoViewSet',
    'AcaoDestaqueViewSet',
    
    # API Alinhamento
    'TipoAnotacaoAlinhamentoViewSet',
    'AcaoAnotacaoAlinhamentoViewSet',
    
    # API Responsavel
    'UsuarioResponsavelViewSet',
    'RelacaoAcaoUsuarioResponsavelViewSet',
    
    # Web Core
    'EixoListView', 'EixoDetailView', 'EixoCreateView', 'EixoUpdateView', 'EixoDeleteView',
    'SituacaoAcaoListView', 'SituacaoAcaoDetailView', 'SituacaoAcaoCreateView',
    'SituacaoAcaoUpdateView', 'SituacaoAcaoDeleteView',
    'VigenciaPNGIListView', 'VigenciaPNGIDetailView', 'VigenciaPNGICreateView',
    'VigenciaPNGIUpdateView', 'VigenciaPNGIDeleteView',
    'TipoEntraveAlertaListView', 'TipoEntraveAlertaDetailView', 'TipoEntraveAlertaCreateView',
    'TipoEntraveAlertaUpdateView', 'TipoEntraveAlertaDeleteView',
    
    # Web Acoes
    'AcoesListView', 'AcoesDetailView', 'AcoesCreateView', 'AcoesUpdateView', 'AcoesDeleteView',
    'AcaoPrazoListView', 'AcaoPrazoDetailView', 'AcaoPrazoCreateView',
    'AcaoPrazoUpdateView', 'AcaoPrazoDeleteView',
    'AcaoDestaqueListView', 'AcaoDestaqueDetailView', 'AcaoDestaqueCreateView',
    'AcaoDestaqueUpdateView', 'AcaoDestaqueDeleteView',
    
    # Web Alinhamento
    'TipoAnotacaoAlinhamentoListView', 'TipoAnotacaoAlinhamentoDetailView',
    'TipoAnotacaoAlinhamentoCreateView', 'TipoAnotacaoAlinhamentoUpdateView',
    'TipoAnotacaoAlinhamentoDeleteView',
    'AcaoAnotacaoAlinhamentoListView', 'AcaoAnotacaoAlinhamentoDetailView',
    'AcaoAnotacaoAlinhamentoCreateView', 'AcaoAnotacaoAlinhamentoUpdateView',
    'AcaoAnotacaoAlinhamentoDeleteView',
    
    # Web Responsavel
    'UsuarioResponsavelListView', 'UsuarioResponsavelDetailView',
    'UsuarioResponsavelCreateView', 'UsuarioResponsavelUpdateView',
    'UsuarioResponsavelDeleteView',
    'RelacaoAcaoUsuarioResponsavelListView', 'RelacaoAcaoUsuarioResponsavelDetailView',
    'RelacaoAcaoUsuarioResponsavelCreateView', 'RelacaoAcaoUsuarioResponsavelUpdateView',
    'RelacaoAcaoUsuarioResponsavelDeleteView',
]
