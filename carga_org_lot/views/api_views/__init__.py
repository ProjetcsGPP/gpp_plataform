"""
API Views - REST Framework ViewSets
Centraliza imports para compatibilidade retroativa.
"""

from .dashboard_api import *
from .patriarca_api import *
from .organograma_api import *
from .lotacao_api import *
from .carga_api import *

__all__ = [
    # Dashboard
    'dashboard_stats',
    'search_orgao',
    'upload_organograma',
    'upload_lotacao',
    
    # ViewSets
    'PatriarcaViewSet',
    'OrganogramaVersaoViewSet',
    'LotacaoVersaoViewSet',
    'CargaPatriarcaViewSet',
]
