"""
Web Views Package - Exports de todas as Class-Based Views modulares.
Padronização seguindo estrutura de carga_org_lot.
"""

# Core Web Views
from .core_web_views import (
    EixoListView, EixoDetailView, EixoCreateView, EixoUpdateView, EixoDeleteView,
    SituacaoAcaoListView, SituacaoAcaoDetailView, SituacaoAcaoCreateView,
    SituacaoAcaoUpdateView, SituacaoAcaoDeleteView,
    VigenciaPNGIListView, VigenciaPNGIDetailView, VigenciaPNGICreateView,
    VigenciaPNGIUpdateView, VigenciaPNGIDeleteView,
    TipoEntraveAlertaListView, TipoEntraveAlertaDetailView, TipoEntraveAlertaCreateView,
    TipoEntraveAlertaUpdateView, TipoEntraveAlertaDeleteView
)

# Acoes Web Views
from .acoes_web_views import (
    AcoesListView, AcoesDetailView, AcoesCreateView, AcoesUpdateView, AcoesDeleteView,
    AcaoPrazoListView, AcaoPrazoDetailView, AcaoPrazoCreateView,
    AcaoPrazoUpdateView, AcaoPrazoDeleteView,
    AcaoDestaqueListView, AcaoDestaqueDetailView, AcaoDestaqueCreateView,
    AcaoDestaqueUpdateView, AcaoDestaqueDeleteView
)

# Alinhamento Web Views
from .alinhamento_web_views import (
    TipoAnotacaoAlinhamentoListView, TipoAnotacaoAlinhamentoDetailView,
    TipoAnotacaoAlinhamentoCreateView, TipoAnotacaoAlinhamentoUpdateView,
    TipoAnotacaoAlinhamentoDeleteView,
    AcaoAnotacaoAlinhamentoListView, AcaoAnotacaoAlinhamentoDetailView,
    AcaoAnotacaoAlinhamentoCreateView, AcaoAnotacaoAlinhamentoUpdateView,
    AcaoAnotacaoAlinhamentoDeleteView
)

# Responsavel Web Views
from .responsavel_web_views import (
    UsuarioResponsavelListView, UsuarioResponsavelDetailView,
    UsuarioResponsavelCreateView, UsuarioResponsavelUpdateView,
    UsuarioResponsavelDeleteView,
    RelacaoAcaoUsuarioResponsavelListView, RelacaoAcaoUsuarioResponsavelDetailView,
    RelacaoAcaoUsuarioResponsavelCreateView, RelacaoAcaoUsuarioResponsavelUpdateView,
    RelacaoAcaoUsuarioResponsavelDeleteView
)


__all__ = [
    # Core
    'EixoListView', 'EixoDetailView', 'EixoCreateView', 'EixoUpdateView', 'EixoDeleteView',
    'SituacaoAcaoListView', 'SituacaoAcaoDetailView', 'SituacaoAcaoCreateView',
    'SituacaoAcaoUpdateView', 'SituacaoAcaoDeleteView',
    'VigenciaPNGIListView', 'VigenciaPNGIDetailView', 'VigenciaPNGICreateView',
    'VigenciaPNGIUpdateView', 'VigenciaPNGIDeleteView',
    'TipoEntraveAlertaListView', 'TipoEntraveAlertaDetailView', 'TipoEntraveAlertaCreateView',
    'TipoEntraveAlertaUpdateView', 'TipoEntraveAlertaDeleteView',
    
    # Acoes
    'AcoesListView', 'AcoesDetailView', 'AcoesCreateView', 'AcoesUpdateView', 'AcoesDeleteView',
    'AcaoPrazoListView', 'AcaoPrazoDetailView', 'AcaoPrazoCreateView',
    'AcaoPrazoUpdateView', 'AcaoPrazoDeleteView',
    'AcaoDestaqueListView', 'AcaoDestaqueDetailView', 'AcaoDestaqueCreateView',
    'AcaoDestaqueUpdateView', 'AcaoDestaqueDeleteView',
    
    # Alinhamento
    'TipoAnotacaoAlinhamentoListView', 'TipoAnotacaoAlinhamentoDetailView',
    'TipoAnotacaoAlinhamentoCreateView', 'TipoAnotacaoAlinhamentoUpdateView',
    'TipoAnotacaoAlinhamentoDeleteView',
    'AcaoAnotacaoAlinhamentoListView', 'AcaoAnotacaoAlinhamentoDetailView',
    'AcaoAnotacaoAlinhamentoCreateView', 'AcaoAnotacaoAlinhamentoUpdateView',
    'AcaoAnotacaoAlinhamentoDeleteView',
    
    # Responsavel
    'UsuarioResponsavelListView', 'UsuarioResponsavelDetailView',
    'UsuarioResponsavelCreateView', 'UsuarioResponsavelUpdateView',
    'UsuarioResponsavelDeleteView',
    'RelacaoAcaoUsuarioResponsavelListView', 'RelacaoAcaoUsuarioResponsavelDetailView',
    'RelacaoAcaoUsuarioResponsavelCreateView', 'RelacaoAcaoUsuarioResponsavelUpdateView',
    'RelacaoAcaoUsuarioResponsavelDeleteView',
]
