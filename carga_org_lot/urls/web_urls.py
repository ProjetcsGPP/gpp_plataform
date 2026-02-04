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

app_name = 'carga_org_lot'

urlpatterns = [
    # ============================================
    # AUTENTICAÇÃO
    # ============================================
    path('', RedirectView.as_view(pattern_name='carga_org_lot:login'), name='home'),
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
    path('patriarcas/<int:patriarca_id>/', patriarca_detail, name='patriarca_detail'),
    
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
