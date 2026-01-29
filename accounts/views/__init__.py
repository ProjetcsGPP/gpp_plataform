# accounts/views/__init__.py
"""
Views do aplicativo accounts

Organização:
- role_views.py: Gestão de seleção e troca de papéis/perfis
- api_views.py: Views para API REST
- web_views.py: Views tradicionais (templates)
"""

# Importa funções de role_views
from .role_views import (
    select_role,
    set_active_role,
    switch_role,
)

# Exporta para uso externo
__all__ = [
    'select_role',
    'set_active_role', 
    'switch_role',
]
