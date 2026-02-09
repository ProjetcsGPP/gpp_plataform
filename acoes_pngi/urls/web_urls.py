"""
URL Configuration para interface web do Ações PNGI.
Definido rotas para todas as views web.
"""

from django.urls import path

from ..views.web_views import (
    # Eixo
    EixoListView, EixoDetailView, EixoCreateView, 
    EixoUpdateView, EixoDeleteView,
    # SituacaoAcao
    SituacaoAcaoListView, SituacaoAcaoDetailView, SituacaoAcaoCreateView,
    SituacaoAcaoUpdateView, SituacaoAcaoDeleteView,
    # VigenciaPNGI
    VigenciaPNGIListView, VigenciaPNGIDetailView, VigenciaPNGICreateView,
    VigenciaPNGIUpdateView, VigenciaPNGIDeleteView,
    # TipoEntraveAlerta
    TipoEntraveAlertaListView, TipoEntraveAlertaDetailView, TipoEntraveAlertaCreateView,
    TipoEntraveAlertaUpdateView, TipoEntraveAlertaDeleteView,
    # Acoes
    AcoesListView, AcoesDetailView, AcoesCreateView,
    AcoesUpdateView, AcoesDeleteView,
    # AcaoPrazo
    AcaoPrazoListView, AcaoPrazoDetailView, AcaoPrazoCreateView,
    AcaoPrazoUpdateView, AcaoPrazoDeleteView,
    # AcaoDestaque
    AcaoDestaqueListView, AcaoDestaqueDetailView, AcaoDestaqueCreateView,
    AcaoDestaqueUpdateView, AcaoDestaqueDeleteView,
    # TipoAnotacaoAlinhamento
    TipoAnotacaoAlinhamentoListView, TipoAnotacaoAlinhamentoDetailView,
    TipoAnotacaoAlinhamentoCreateView, TipoAnotacaoAlinhamentoUpdateView,
    TipoAnotacaoAlinhamentoDeleteView,
    # AcaoAnotacaoAlinhamento
    AcaoAnotacaoAlinhamentoListView, AcaoAnotacaoAlinhamentoDetailView,
    AcaoAnotacaoAlinhamentoCreateView, AcaoAnotacaoAlinhamentoUpdateView,
    AcaoAnotacaoAlinhamentoDeleteView,
    # UsuarioResponsavel
    UsuarioResponsavelListView, UsuarioResponsavelDetailView,
    UsuarioResponsavelCreateView, UsuarioResponsavelUpdateView,
    UsuarioResponsavelDeleteView,
    # RelacaoAcaoUsuarioResponsavel
    RelacaoAcaoUsuarioResponsavelListView, RelacaoAcaoUsuarioResponsavelDetailView,
    RelacaoAcaoUsuarioResponsavelCreateView, RelacaoAcaoUsuarioResponsavelUpdateView,
    RelacaoAcaoUsuarioResponsavelDeleteView,
)

app_name = 'acoes_pngi'

urlpatterns = [
    # Eixo URLs
    path('eixos/', EixoListView.as_view(), name='eixo_list'),
    path('eixos/<int:ideixo>/', EixoDetailView.as_view(), name='eixo_detail'),
    path('eixos/novo/', EixoCreateView.as_view(), name='eixo_create'),
    path('eixos/<int:ideixo>/editar/', EixoUpdateView.as_view(), name='eixo_update'),
    path('eixos/<int:ideixo>/excluir/', EixoDeleteView.as_view(), name='eixo_delete'),
    
    # SituacaoAcao URLs
    path('situacoes-acao/', SituacaoAcaoListView.as_view(), name='situacaoacao_list'),
    path('situacoes-acao/<int:idsituacaoacao>/', SituacaoAcaoDetailView.as_view(), name='situacaoacao_detail'),
    path('situacoes-acao/novo/', SituacaoAcaoCreateView.as_view(), name='situacaoacao_create'),
    path('situacoes-acao/<int:idsituacaoacao>/editar/', SituacaoAcaoUpdateView.as_view(), name='situacaoacao_update'),
    path('situacoes-acao/<int:idsituacaoacao>/excluir/', SituacaoAcaoDeleteView.as_view(), name='situacaoacao_delete'),
    
    # VigenciaPNGI URLs
    path('vigencias-pngi/', VigenciaPNGIListView.as_view(), name='vigenciapngi_list'),
    path('vigencias-pngi/<int:idvigenciapngi>/', VigenciaPNGIDetailView.as_view(), name='vigenciapngi_detail'),
    path('vigencias-pngi/novo/', VigenciaPNGICreateView.as_view(), name='vigenciapngi_create'),
    path('vigencias-pngi/<int:idvigenciapngi>/editar/', VigenciaPNGIUpdateView.as_view(), name='vigenciapngi_update'),
    path('vigencias-pngi/<int:idvigenciapngi>/excluir/', VigenciaPNGIDeleteView.as_view(), name='vigenciapngi_delete'),
    
    # TipoEntraveAlerta URLs
    path('tipos-entrave-alerta/', TipoEntraveAlertaListView.as_view(), name='tipoentravealerta_list'),
    path('tipos-entrave-alerta/<int:idtipoentravealerta>/', TipoEntraveAlertaDetailView.as_view(), name='tipoentravealerta_detail'),
    path('tipos-entrave-alerta/novo/', TipoEntraveAlertaCreateView.as_view(), name='tipoentravealerta_create'),
    path('tipos-entrave-alerta/<int:idtipoentravealerta>/editar/', TipoEntraveAlertaUpdateView.as_view(), name='tipoentravealerta_update'),
    path('tipos-entrave-alerta/<int:idtipoentravealerta>/excluir/', TipoEntraveAlertaDeleteView.as_view(), name='tipoentravealerta_delete'),
    
    # Acoes URLs
    path('acoes/', AcoesListView.as_view(), name='acoes_list'),
    path('acoes/<int:idacao>/', AcoesDetailView.as_view(), name='acoes_detail'),
    path('acoes/novo/', AcoesCreateView.as_view(), name='acoes_create'),
    path('acoes/<int:idacao>/editar/', AcoesUpdateView.as_view(), name='acoes_update'),
    path('acoes/<int:idacao>/excluir/', AcoesDeleteView.as_view(), name='acoes_delete'),
    
    # AcaoPrazo URLs
    path('acoes-prazo/', AcaoPrazoListView.as_view(), name='acaoprazo_list'),
    path('acoes-prazo/<int:idacaoprazo>/', AcaoPrazoDetailView.as_view(), name='acaoprazo_detail'),
    path('acoes-prazo/novo/', AcaoPrazoCreateView.as_view(), name='acaoprazo_create'),
    path('acoes-prazo/<int:idacaoprazo>/editar/', AcaoPrazoUpdateView.as_view(), name='acaoprazo_update'),
    path('acoes-prazo/<int:idacaoprazo>/excluir/', AcaoPrazoDeleteView.as_view(), name='acaoprazo_delete'),
    
    # AcaoDestaque URLs
    path('acoes-destaque/', AcaoDestaqueListView.as_view(), name='acaodestaque_list'),
    path('acoes-destaque/<int:idacaodestaque>/', AcaoDestaqueDetailView.as_view(), name='acaodestaque_detail'),
    path('acoes-destaque/novo/', AcaoDestaqueCreateView.as_view(), name='acaodestaque_create'),
    path('acoes-destaque/<int:idacaodestaque>/editar/', AcaoDestaqueUpdateView.as_view(), name='acaodestaque_update'),
    path('acoes-destaque/<int:idacaodestaque>/excluir/', AcaoDestaqueDeleteView.as_view(), name='acaodestaque_delete'),
    
    # TipoAnotacaoAlinhamento URLs
    path('tipos-anotacao-alinhamento/', TipoAnotacaoAlinhamentoListView.as_view(), name='tipoanotacaoalinhamento_list'),
    path('tipos-anotacao-alinhamento/<int:idtipoanotacaoalinhamento>/', TipoAnotacaoAlinhamentoDetailView.as_view(), name='tipoanotacaoalinhamento_detail'),
    path('tipos-anotacao-alinhamento/novo/', TipoAnotacaoAlinhamentoCreateView.as_view(), name='tipoanotacaoalinhamento_create'),
    path('tipos-anotacao-alinhamento/<int:idtipoanotacaoalinhamento>/editar/', TipoAnotacaoAlinhamentoUpdateView.as_view(), name='tipoanotacaoalinhamento_update'),
    path('tipos-anotacao-alinhamento/<int:idtipoanotacaoalinhamento>/excluir/', TipoAnotacaoAlinhamentoDeleteView.as_view(), name='tipoanotacaoalinhamento_delete'),
    
    # AcaoAnotacaoAlinhamento URLs
    path('acoes-anotacao-alinhamento/', AcaoAnotacaoAlinhamentoListView.as_view(), name='acaoanotacaoalinhamento_list'),
    path('acoes-anotacao-alinhamento/<int:idacaoanotacaoalinhamento>/', AcaoAnotacaoAlinhamentoDetailView.as_view(), name='acaoanotacaoalinhamento_detail'),
    path('acoes-anotacao-alinhamento/novo/', AcaoAnotacaoAlinhamentoCreateView.as_view(), name='acaoanotacaoalinhamento_create'),
    path('acoes-anotacao-alinhamento/<int:idacaoanotacaoalinhamento>/editar/', AcaoAnotacaoAlinhamentoUpdateView.as_view(), name='acaoanotacaoalinhamento_update'),
    path('acoes-anotacao-alinhamento/<int:idacaoanotacaoalinhamento>/excluir/', AcaoAnotacaoAlinhamentoDeleteView.as_view(), name='acaoanotacaoalinhamento_delete'),
    
    # UsuarioResponsavel URLs
    path('usuarios-responsaveis/', UsuarioResponsavelListView.as_view(), name='usuarioresponsavel_list'),
    path('usuarios-responsaveis/<int:idusuario>/', UsuarioResponsavelDetailView.as_view(), name='usuarioresponsavel_detail'),
    path('usuarios-responsaveis/novo/', UsuarioResponsavelCreateView.as_view(), name='usuarioresponsavel_create'),
    path('usuarios-responsaveis/<int:idusuario>/editar/', UsuarioResponsavelUpdateView.as_view(), name='usuarioresponsavel_update'),
    path('usuarios-responsaveis/<int:idusuario>/excluir/', UsuarioResponsavelDeleteView.as_view(), name='usuarioresponsavel_delete'),
    
    # RelacaoAcaoUsuarioResponsavel URLs
    path('relacoes-acao-responsavel/', RelacaoAcaoUsuarioResponsavelListView.as_view(), name='relacaoacaousuarioresponsavel_list'),
    path('relacoes-acao-responsavel/<int:idacaousuarioresponsavel>/', RelacaoAcaoUsuarioResponsavelDetailView.as_view(), name='relacaoacaousuarioresponsavel_detail'),
    path('relacoes-acao-responsavel/novo/', RelacaoAcaoUsuarioResponsavelCreateView.as_view(), name='relacaoacaousuarioresponsavel_create'),
    path('relacoes-acao-responsavel/<int:idacaousuarioresponsavel>/editar/', RelacaoAcaoUsuarioResponsavelUpdateView.as_view(), name='relacaoacaousuarioresponsavel_update'),
    path('relacoes-acao-responsavel/<int:idacaousuarioresponsavel>/excluir/', RelacaoAcaoUsuarioResponsavelDeleteView.as_view(), name='relacaoacaousuarioresponsavel_delete'),
]
