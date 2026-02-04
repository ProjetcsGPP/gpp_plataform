"""
URLs do módulo Carga Org/Lot - Web Views (Django Templates)

Este arquivo centraliza as rotas web tradicionais.
Para APIs REST, veja api_urls.py no mesmo diretório.
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
    path('patriarcas/novo/', web_views.patriarca_create, name='patriarca_create'),
    path('patriarcas/<int:pk>/', web_views.patriarca_detail, name='patriarca_detail'),
    path('patriarcas/<int:pk>/editar/', web_views.patriarca_update, name='patriarca_update'),
    path('patriarcas/<int:pk>/selecionar/', web_views.patriarca_select, name='patriarca_select'),
    path('patriarcas/<int:pk>/reset/', web_views.patriarca_reset, name='patriarca_reset'),
    
    # ========================================
    # ORGANOGRAMA - UPLOAD E PROCESSAMENTO
    # ========================================
    path('organograma/upload/', web_views.organograma_upload, name='organograma_upload'),
    path('organograma/processar/', web_views.organograma_processar, name='organograma_processar'),
    path('organograma/validar/', web_views.organograma_validar, name='organograma_validar'),
    
    # ========================================
    # ORGANOGRAMA - EDIÇÃO VISUAL (REACTFLOW)
    # ========================================
    path('organograma/editar/', web_views.organograma_edit, name='organograma_edit'),
    path('organograma/editar/salvar/', web_views.organograma_save, name='organograma_save'),
    path('organograma/editar/json/', web_views.organograma_json_get, name='organograma_json_get'),
    path('organograma/editar/organizar/', web_views.organograma_organizar, name='organograma_organizar'),
    path('organograma/visualizar/', web_views.organograma_visualizar, name='organograma_visualizar'),
    
    # ========================================
    # LOTAÇÃO
    # ========================================
    path('lotacao/upload/', web_views.lotacao_upload, name='lotacao_upload'),
    path('lotacao/processar/', web_views.lotacao_processar, name='lotacao_processar'),
    path('lotacao/validar/', web_views.lotacao_validar, name='lotacao_validar'),
    path('lotacao/gerar-json/', web_views.lotacao_gerar_json, name='lotacao_gerar_json'),
    
    # ========================================
    # CARGA - ENVIO E MONITORAMENTO
    # ========================================
    path('carga/enviar/', web_views.carga_enviar, name='carga_enviar'),
    path('carga/iniciar/<int:patriarca_id>/', web_views.carga_iniciar, name='carga_iniciar'),
    path('carga/monitorar/<uuid:guid>/', web_views.carga_monitorar, name='carga_monitorar'),
    path('carga/status/', web_views.carga_status, name='carga_status'),
    path('carga/status/verificar/<uuid:guid>/', web_views.carga_verificar, name='carga_verificar'),
    path('carga/detalhes/<int:carga_id>/', web_views.carga_detail, name='carga_detail'),
    
    # ========================================
    # UPLOAD GENÉRICO
    # ========================================
    path('upload/local/', web_views.upload_local, name='upload_local'),
    path('upload/google-drive/', web_views.upload_google_drive, name='upload_google_drive'),
]
