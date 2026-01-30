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

# Permissões (NOVO - Fase 3/4)
from .permissions_api import user_permissions

# Gerenciamento de Usuários (NOVO - Fase 3/4)
from .users_api import UserManagementViewSet

# ViewSets principais
from .patriarca_api import PatriarcaViewSet
from .organograma_api import OrganogramaVersaoViewSet
from .lotacao_api import LotacaoVersaoViewSet
from .carga_api import CargaPatriarcaViewSet

# ViewSets novos
from .lotacao_json_api import LotacaoJsonOrgaoViewSet
from .token_api import TokenEnvioCargaViewSet

# ViewSets auxiliares (read-only) - TODOS estão em token_api.py
from .token_api import (
    StatusProgressoViewSet,
    StatusCargaViewSet,
    TipoCargaViewSet,
    StatusTokenEnvioCargaViewSet,
)

# NOTA: OrgaoUnidadeViewSet será criado quando necessário
# Por enquanto, os órgãos são acessados via OrganogramaVersaoViewSet

__all__ = [
    # Dashboard e utilitários
    'dashboard_stats',
    'search_orgao',
    'upload_organograma',
    'upload_lotacao',
    
    # Permissões (NOVO)
    'user_permissions',
    
    # Gerenciamento (NOVO)
    'UserManagementViewSet',
    
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
