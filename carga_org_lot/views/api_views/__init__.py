"""
API Views - REST Framework ViewSets e Funções
Centraliza imports para compatibilidade retroativa.
"""

# Dashboard e utilitários
from .dashboard_api import (
    dashboard_stats,
    search_orgao,
    upload_organograma,
    upload_lotacao,
)

# ViewSets principais
from .patriarca_api import PatriarcaViewSet
from .organograma_api import OrganogramaVersaoViewSet
from .lotacao_api import LotacaoVersaoViewSet
from .carga_api import CargaPatriarcaViewSet

# ViewSets novos
from .lotacao_json_api import LotacaoJsonOrgaoViewSet
from .token_api import TokenEnvioCargaViewSet

# ViewSets auxiliares (read-only)
from .patriarca_api import (
    StatusProgressoViewSet,
)
from .carga_api import (
    StatusCargaViewSet,
    TipoCargaViewSet,
)
from .token_api import (
    StatusTokenEnvioCargaViewSet,
)

__all__ = [
    # Dashboard e utilitários
    'dashboard_stats',
    'search_orgao',
    'upload_organograma',
    'upload_lotacao',
    
    # ViewSets Principais
    'PatriarcaViewSet',
    'OrganogramaVersaoViewSet',
    'LotacaoVersaoViewSet',
    'CargaPatriarcaViewSet',
    
    # ViewSets Novos
    'LotacaoJsonOrgaoViewSet',
    'TokenEnvioCargaViewSet',
    
    # ViewSets Auxiliares (Read-Only)
    'StatusProgressoViewSet',
    'StatusCargaViewSet',
    'TipoCargaViewSet',
    'StatusTokenEnvioCargaViewSet',
]
