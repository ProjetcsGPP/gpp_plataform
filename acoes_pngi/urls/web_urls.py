"""
URLs Web (Django templates) para a aplicação Ações PNGI.
🚀 MIGRAÇÃO COMPLETA: AuthorizationService + Class-Based Views
Prefixo: /acoes-pngi/
"""

from django.urls import path

# Autenticação (mantida como FBV)
from ..views.web_views import (
    acoes_pngi_login,
    acoes_pngi_dashboard,
    acoes_pngi_logout,
)

# TODAS as CBV com AuthorizationService
from ..views.web_views_cbv import (
    # Configurações Nível 1 (GESTOR)
    SituacaoAcaoListView, SituacaoAcaoCreateView, SituacaoAcaoUpdateView, SituacaoAcaoDeleteView,
    TipoEntraveAlertaListView, TipoEntraveAlertaCreateView, TipoEntraveAlertaUpdateView, TipoEntraveAlertaDeleteView,
    
    # Configurações Nível 2 (GESTOR + COORDENADOR)
    EixoListView, EixoCreateView, EixoUpdateView, EixoDeleteView,
    VigenciaListView, VigenciaCreateView, VigenciaUpdateView, VigenciaDeleteView,
    TipoAnotacaoAlinhamentoListView, TipoAnotacaoAlinhamentoCreateView, TipoAnotacaoAlinhamentoUpdateView, TipoAnotacaoAlinhamentoDeleteView,
    
    # Operações (GESTOR + COORDENADOR + OPERADOR)
    AcoesListView, AcoesCreateView, AcoesUpdateView, AcoesDeleteView,
    AcaoPrazoListView, AcaoPrazoCreateView, AcaoPrazoUpdateView, AcaoPrazoDeleteView,
    AcaoDestaqueListView, AcaoDestaqueCreateView, AcaoDestaqueUpdateView, AcaoDestaqueDeleteView,
    AcaoAnotacaoAlinhamentoListView, AcaoAnotacaoAlinhamentoCreateView, AcaoAnotacaoAlinhamentoUpdateView, AcaoAnotacaoAlinhamentoDeleteView,
    UsuarioResponsavelListView, UsuarioResponsavelCreateView, UsuarioResponsavelUpdateView, UsuarioResponsavelDeleteView,
    RelacaoAcaoUsuarioResponsavelListView, RelacaoAcaoUsuarioResponsavelCreateView, RelacaoAcaoUsuarioResponsavelDeleteView,
    
    # Vistas especiais
    AcoesCompletasListView, AcoesPorResponsavelListView,
)

app_name = 'acoes_pngi_web'

urlpatterns = [
    # =========================================================================
    # AUTENTICAÇÃO (mantida)
    # =========================================================================
    path('', acoes_pngi_login, name='home'),
    path('login/', acoes_pngi_login, name='login'),
    path('logout/', acoes_pngi_logout, name='logout'),
    path('dashboard/', acoes_pngi_dashboard, name='dashboard'),
    
    # =========================================================================
    # CONFIGURAÇÕES - NÍVEL 1 (APENAS GESTOR)
    # =========================================================================
    path('situacoes/', SituacaoAcaoListView.as_view(), name='situacoes_list'),
    path('situacoes/criar/', SituacaoAcaoCreateView.as_view(), name='situacao_create'),
    path('situacoes/<int:pk>/editar/', SituacaoAcaoUpdateView.as_view(), name='situacao_update'),
    path('situacoes/<int:pk>/deletar/', SituacaoAcaoDeleteView.as_view(), name='situacao_delete'),
    
    path('tipos-entrave/', TipoEntraveAlertaListView.as_view(), name='tipos_entrave_list'),
    path('tipos-entrave/criar/', TipoEntraveAlertaCreateView.as_view(), name='tipo_entrave_create'),
    path('tipos-entrave/<int:pk>/editar/', TipoEntraveAlertaUpdateView.as_view(), name='tipo_entrave_update'),
    path('tipos-entrave/<int:pk>/deletar/', TipoEntraveAlertaDeleteView.as_view(), name='tipo_entrave_delete'),
    
    # =========================================================================
    # CONFIGURAÇÕES - NÍVEL 2 (GESTOR + COORDENADOR)
    # =========================================================================
    path('eixos/', EixoListView.as_view(), name='eixos_list'),
    path('eixos/criar/', EixoCreateView.as_view(), name='eixo_create'),
    path('eixos/<int:pk>/editar/', EixoUpdateView.as_view(), name='eixo_update'),
    path('eixos/<int:pk>/deletar/', EixoDeleteView.as_view(), name='eixo_delete'),
    
    path('vigencias/', VigenciaListView.as_view(), name='vigencias_list'),
    path('vigencias/criar/', VigenciaCreateView.as_view(), name='vigencia_create'),
    path('vigencias/<int:pk>/editar/', VigenciaUpdateView.as_view(), name='vigencia_update'),
    path('vigencias/<int:pk>/deletar/', VigenciaDeleteView.as_view(), name='vigencia_delete'),
    
    path('tipos-anotacao/', TipoAnotacaoAlinhamentoListView.as_view(), name='tipos_anotacao_list'),
    path('tipos-anotacao/criar/', TipoAnotacaoAlinhamentoCreateView.as_view(), name='tipo_anotacao_create'),
    path('tipos-anotacao/<int:pk>/editar/', TipoAnotacaoAlinhamentoUpdateView.as_view(), name='tipo_anotacao_update'),
    path('tipos-anotacao/<int:pk>/deletar/', TipoAnotacaoAlinhamentoDeleteView.as_view(), name='tipo_anotacao_delete'),
    
    # =========================================================================
    # OPERAÇÕES (GESTOR + COORDENADOR + OPERADOR)
    # =========================================================================
    path('acoes/', AcoesListView.as_view(), name='acoes_list'),
    path('acoes/criar/', AcoesCreateView.as_view(), name='acao_create'),
    path('acoes/<int:pk>/editar/', AcoesUpdateView.as_view(), name='acao_update'),
    path('acoes/<int:pk>/deletar/', AcoesDeleteView.as_view(), name='acao_delete'),
    
    path('prazos/', AcaoPrazoListView.as_view(), name='prazos_list'),
    path('prazos/criar/', AcaoPrazoCreateView.as_view(), name='prazo_create'),
    path('prazos/<int:pk>/editar/', AcaoPrazoUpdateView.as_view(), name='prazo_update'),
    path('prazos/<int:pk>/deletar/', AcaoPrazoDeleteView.as_view(), name='prazo_delete'),
    
    path('acoes/<int:acao_id>/prazos/', AcaoPrazoListView.as_view(), name='acao_prazos_list'),
    
    path('destaques/', AcaoDestaqueListView.as_view(), name='destaques_list'),
    path('destaques/criar/', AcaoDestaqueCreateView.as_view(), name='destaque_create'),
    path('destaques/<int:pk>/editar/', AcaoDestaqueUpdateView.as_view(), name='destaque_update'),
    path('destaques/<int:pk>/deletar/', AcaoDestaqueDeleteView.as_view(), name='destaque_delete'),
    
    path('anotacoes/', AcaoAnotacaoAlinhamentoListView.as_view(), name='anotacoes_list'),
    path('anotacoes/criar/', AcaoAnotacaoAlinhamentoCreateView.as_view(), name='anotacao_create'),
    path('anotacoes/<int:pk>/editar/', AcaoAnotacaoAlinhamentoUpdateView.as_view(), name='anotacao_update'),
    path('anotacoes/<int:pk>/deletar/', AcaoAnotacaoAlinhamentoDeleteView.as_view(), name='anotacao_delete'),
    
    path('responsaveis/', UsuarioResponsavelListView.as_view(), name='responsaveis_list'),
    path('responsaveis/criar/', UsuarioResponsavelCreateView.as_view(), name='responsavel_create'),
    path('responsaveis/<int:pk>/editar/', UsuarioResponsavelUpdateView.as_view(), name='responsavel_update'),
    path('responsaveis/<int:pk>/deletar/', UsuarioResponsavelDeleteView.as_view(), name='responsavel_delete'),
    
    path('relacoes/', RelacaoAcaoUsuarioResponsavelListView.as_view(), name='relacoes_list'),
    path('relacoes/criar/', RelacaoAcaoUsuarioResponsavelCreateView.as_view(), name='relacao_create'),
    path('relacoes/<int:pk>/deletar/', RelacaoAcaoUsuarioResponsavelDeleteView.as_view(), name='relacao_delete'),
    
    # =========================================================================
    # VISTAS ESPECIAIS
    # =========================================================================
    path('acoes/completas/', AcoesCompletasListView.as_view(), name='acoes_completa_list'),
    path('acoes/por-responsavel/', AcoesPorResponsavelListView.as_view(), name='acoes_por_responsavel'),
    
    # acoes_pngi/urls/web_urls.py
    path('acoes/completa/', AcoesCompletasListView.as_view(), name='acoes_completa_list'),
    
    path('acoes/completas/', AcoesCompletasListView.as_view(), name='acoes_completa_list'),
    path('acoes/por-responsavel/', AcoesPorResponsavelListView.as_view(), name='acoes_por_responsavel'),
]
