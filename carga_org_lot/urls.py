"""
URLs do módulo Carga Org/Lot
"""

from django.urls import path
from .views.web_views import (
    dashboard_views,
    patriarca_views,
    organograma_views,
    lotacao_views,
    carga_views,
    upload_views,
)

app_name = 'carga_org_lot'

urlpatterns = [
    # ========================================
    # DASHBOARD
    # ========================================
    path('', dashboard_views.dashboard_view, name='dashboard'),
    
    # ========================================
    # PATRIARCAS
    # ========================================
    path('patriarcas/', patriarca_views.patriarca_list, name='patriarca_list'),
    path('patriarcas/novo/', patriarca_views.patriarca_create, name='patriarca_create'),
    path('patriarcas/<int:pk>/', patriarca_views.patriarca_detail, name='patriarca_detail'),
    path('patriarcas/<int:pk>/editar/', patriarca_views.patriarca_update, name='patriarca_update'),
    path('patriarcas/<int:pk>/selecionar/', patriarca_views.patriarca_select, name='patriarca_select'),
    path('patriarcas/<int:pk>/reset/', patriarca_views.patriarca_reset, name='patriarca_reset'),
    
    # ========================================
    # ORGANOGRAMA - UPLOAD E PROCESSAMENTO
    # ========================================
    path('organograma/upload/', organograma_views.organograma_upload, name='organograma_upload'),
    path('organograma/processar/', organograma_views.organograma_processar, name='organograma_processar'),
    path('organograma/validar/', organograma_views.organograma_validar, name='organograma_validar'),
    
    # ========================================
    # ORGANOGRAMA - EDIÇÃO VISUAL (REACTFLOW)
    # ========================================
    path('organograma/editar/', organograma_views.organograma_edit, name='organograma_edit'),
    path('organograma/editar/salvar/', organograma_views.organograma_save, name='organograma_save'),
    path('organograma/editar/json/', organograma_views.organograma_json_get, name='organograma_json_get'),
    path('organograma/editar/organizar/', organograma_views.organograma_organizar, name='organograma_organizar'),
    path('organograma/visualizar/', organograma_views.organograma_visualizar, name='organograma_visualizar'),
    
    # ========================================
    # LOTAÇÃO
    # ========================================
    path('lotacao/upload/', lotacao_views.lotacao_upload, name='lotacao_upload'),
    path('lotacao/processar/', lotacao_views.lotacao_processar, name='lotacao_processar'),
    path('lotacao/validar/', lotacao_views.lotacao_validar, name='lotacao_validar'),
    path('lotacao/gerar-json/', lotacao_views.lotacao_gerar_json, name='lotacao_gerar_json'),
    
    # ========================================
    # CARGA - ENVIO E MONITORAMENTO
    # ========================================
    path('carga/enviar/', carga_views.carga_enviar, name='carga_enviar'),
    path('carga/iniciar/<int:patriarca_id>/', carga_views.carga_iniciar, name='carga_iniciar'),
    path('carga/monitorar/<uuid:guid>/', carga_views.carga_monitorar, name='carga_monitorar'),
    path('carga/status/', carga_views.carga_status, name='carga_status'),
    path('carga/status/verificar/<uuid:guid>/', carga_views.carga_verificar, name='carga_verificar'),
    path('carga/detalhes/<int:carga_id>/', carga_views.carga_detail, name='carga_detail'),
    
    # ========================================
    # UPLOAD GENÉRICO
    # ========================================
    path('upload/local/', upload_views.upload_local, name='upload_local'),
    path('upload/google-drive/', upload_views.upload_google_drive, name='upload_google_drive'),
]
