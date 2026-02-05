"""
URLs Web (Django templates) para a aplicação Carga Org/Lot.
Prefixo aplicado em gpp_platform/urls.py: /carga_org_lot/

Este arquivo contém as rotas para as views web (páginas HTML renderizadas pelo Django).
Para APIs REST (consumidas pelo Next.js), veja api_urls.py.
"""

from django.urls import path
from django.views.generic import RedirectView
from ..views.web_views import (
    # Autenticação
    carga_login,
    carga_logout,
    
    # Dashboard
    carga_dashboard,
    
    # Patriarcas
    patriarca_list,
    patriarca_detail,
    patriarca_create,
    patriarca_update,
    patriarca_select,
    patriarca_reset,
    
    # Organogramas
    organograma_list,
    organograma_detail,
    organograma_hierarquia_json,
    
    # Lotações
    lotacao_list,
    lotacao_detail,
    lotacao_inconsistencias,
    
    # Cargas
    carga_list,
    carga_detail,
    
    # Upload
    upload_page,
    upload_organograma_handler,
    upload_lotacao_handler,
    
    # AJAX
    search_orgao_ajax,
)

app_name = 'carga_org_lot_web'  # ✅ Namespace para views web (Django templates)

urlpatterns = [
    # ============================================
    # AUTENTICAÇÃO
    # ============================================
    path('', RedirectView.as_view(pattern_name='carga_org_lot_web:login'), name='home'),
    path('login/', carga_login, name='login'),
    path('logout/', carga_logout, name='logout'),
    
    # ============================================
    # DASHBOARD
    # ============================================
    path('dashboard/', carga_dashboard, name='dashboard'),
    
    # ============================================
    # PATRIARCAS
    # ============================================
    path('patriarcas/', patriarca_list, name='patriarca_list'),
    path('patriarcas/novo/', patriarca_create, name='patriarca_create'),
    path('patriarcas/<int:pk>/', patriarca_detail, name='patriarca_detail'),
    path('patriarcas/<int:pk>/editar/', patriarca_update, name='patriarca_update'),
    path('patriarcas/<int:pk>/selecionar/', patriarca_select, name='patriarca_select'),
    path('patriarcas/<int:pk>/reset/', patriarca_reset, name='patriarca_reset'),
    
    # ============================================
    # ORGANOGRAMAS
    # ============================================
    path('organogramas/', organograma_list, name='organograma_list'),
    path('organogramas/<int:organograma_id>/', organograma_detail, name='organograma_detail'),
    path('organogramas/<int:organograma_id>/hierarquia/json/', organograma_hierarquia_json, name='organograma_hierarquia_json'),
    
    # ============================================
    # LOTAÇÕES
    # ============================================
    path('lotacoes/', lotacao_list, name='lotacao_list'),
    path('lotacoes/<int:lotacao_versao_id>/', lotacao_detail, name='lotacao_detail'),
    path('lotacoes/<int:lotacao_versao_id>/inconsistencias/', lotacao_inconsistencias, name='lotacao_inconsistencias'),
    
    # ============================================
    # CARGAS
    # ============================================
    path('cargas/', carga_list, name='carga_list'),
    path('cargas/<int:carga_id>/', carga_detail, name='carga_detail'),
    
    # ============================================
    # UPLOAD
    # ============================================
    path('upload/', upload_page, name='upload'),
    path('upload/organograma/', upload_organograma_handler, name='upload_organograma'),
    path('upload/lotacao/', upload_lotacao_handler, name='upload_lotacao'),
    
    # ============================================
    # AJAX / AUTOCOMPLETE
    # ============================================
    path('ajax/search-orgao/', search_orgao_ajax, name='search_orgao_ajax'),
]
