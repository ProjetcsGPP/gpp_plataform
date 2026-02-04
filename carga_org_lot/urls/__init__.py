"""
URLs do módulo Carga Org/Lot - Web Views (Django Templates)

Este arquivo centraliza as rotas web tradicionais.
Para APIs REST, veja api_urls.py no mesmo diretório.

NOTA: Este arquivo contém apenas rotas para views que EXISTEM.
Views faltantes precisam ser implementadas nos arquivos individuais.
"""

from django.urls import path
from ..views import web_views

app_name = 'carga_org_lot'

urlpatterns = [
    # ========================================
    # DASHBOARD
    # ========================================
    path('', web_views.carga_dashboard, name='dashboard'),
    
    # ========================================
    # PATRIARCAS
    # ========================================
    path('patriarcas/', web_views.patriarca_list, name='patriarca_list'),
    path('patriarcas/<int:patriarca_id>/', web_views.patriarca_detail, name='patriarca_detail'),
    # NOTA: Rotas abaixo ESTÃO NO ARQUIVO patriarca_views.py MAS NÃO EM __all__
    # Precisam ser adicionadas ao __init__.py do web_views
    # path('patriarcas/novo/', web_views.patriarca_create, name='patriarca_create'),
    # path('patriarcas/<int:pk>/editar/', web_views.patriarca_update, name='patriarca_update'),
    # path('patriarcas/<int:pk>/selecionar/', web_views.patriarca_select, name='patriarca_select'),
    # path('patriarcas/<int:pk>/reset/', web_views.patriarca_reset, name='patriarca_reset'),
    
    # ========================================
    # ORGANOGRAMA
    # ========================================
    path('organogramas/', web_views.organograma_list, name='organograma_list'),
    path('organogramas/<int:organograma_id>/', web_views.organograma_detail, name='organograma_detail'),
    path('organogramas/<int:organograma_id>/hierarquia/json/', web_views.organograma_hierarquia_json, name='organograma_hierarquia_json'),
    # NOTA: Views de upload/processamento NÃO ESTÃO IMPLEMENTADAS em web_views
    # Precisam ser criadas em organograma_views.py e exportadas
    
    # ========================================
    # LOTAÇÃO
    # ========================================
    path('lotacoes/', web_views.lotacao_list, name='lotacao_list'),
    path('lotacoes/<int:lotacao_versao_id>/', web_views.lotacao_detail, name='lotacao_detail'),
    path('lotacoes/<int:lotacao_versao_id>/inconsistencias/', web_views.lotacao_inconsistencias, name='lotacao_inconsistencias'),
    # NOTA: Views de upload/processamento NÃO ESTÃO IMPLEMENTADAS em web_views
    
    # ========================================
    # CARGAS
    # ========================================
    path('cargas/', web_views.carga_list, name='carga_list'),
    path('cargas/<int:carga_id>/', web_views.carga_detail, name='carga_detail'),
    # NOTA: Views de envio/monitoramento NÃO ESTÃO IMPLEMENTADAS em web_views
    
    # ========================================
    # UPLOAD
    # ========================================
    path('upload/', web_views.upload_page, name='upload'),
    path('upload/organograma/', web_views.upload_organograma_handler, name='upload_organograma'),
    path('upload/lotacao/', web_views.upload_lotacao_handler, name='upload_lotacao'),
    
    # ========================================
    # AJAX / AUTOCOMPLETE
    # ========================================
    path('ajax/search-orgao/', web_views.search_orgao_ajax, name='search_orgao_ajax'),
]
