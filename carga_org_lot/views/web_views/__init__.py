"""
Web Views - Django Template Views
Centraliza imports para compatibilidade retroativa.
"""

from .auth_views import *
from .dashboard_views import *
from .patriarca_views import *
from .organograma_views import *
from .lotacao_views import *
from .carga_views import *
from .upload_views import *
from .ajax_views import *

__all__ = [
    # Auth
    'carga_login',
    'carga_logout',
    'carga_org_lot_required',
    
    # Dashboard
    'carga_dashboard',
    
    # Patriarca
    'patriarca_list',
    'patriarca_detail',
    'patriarca_create',      # ← ADICIONADO
    'patriarca_update',      # ← ADICIONADO
    'patriarca_select',      # ← ADICIONADO
    'patriarca_reset',       # ← ADICIONADO
    
    # Organograma
    'organograma_list',
    'organograma_detail',
    'organograma_hierarquia_json',
    
    # Lotação
    'lotacao_list',
    'lotacao_detail',
    'lotacao_inconsistencias',
    
    # Carga
    'carga_list',
    'carga_detail',
    
    # Upload
    'upload_page',
    'upload_organograma_handler',
    'upload_lotacao_handler',
    
    # AJAX
    'search_orgao_ajax',
]
