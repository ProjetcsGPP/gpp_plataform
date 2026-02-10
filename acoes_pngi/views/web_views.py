"""
Web Views do Ações PNGI.

ARQUIVO DE COMPATIBILIDADE - Importa de web_views/ modular.
Toda implementação agora está em módulos especializados dentro de web_views/.

Estrutura modular:
- web_views/core_web_views.py: Eixo, Situação, Vigência, Tipo Entrave
- web_views/acoes_web_views.py: Ações, Prazos e Destaques
- web_views/alinhamento_web_views.py: Anotações de alinhamento
- web_views/responsavel_web_views.py: Usuários responsáveis

Todos os imports diretos deste arquivo continuam funcionando para manter compatibilidade.
"""

# Importa tudo dos módulos especializados
from .web_views import *  # noqa: F401, F403

# Mantém compatibilidade com imports específicos
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
