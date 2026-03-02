"""IAM Interface Layer

Public interfaces for consuming IAM services in domain applications.
Provides decorators, permissions, and middleware that abstract the
underlying IAM logic.

Usage:
    # Web Views
    from core.iam.interfaces.decorators import require_permission
    
    @require_permission('ACOES_PNGI', 'add_eixo')
    def create_eixo(request):
        ...
    
    # API Views
    from core.iam.interfaces.permissions import HasAppPermission
    
    class EixoViewSet(ModelViewSet):
        permission_classes = [HasAppPermission]
        app_code = 'ACOES_PNGI'
"""

from .decorators import (
    require_permission,
    require_any_permission,
    require_all_permissions,
    require_role,
    require_any_role,
)

from .permissions import (
    HasAppPermission,
    RequireRole,
    RequireAnyRole,
    RequireAttribute,
)

__all__ = [
    # Decorators
    'require_permission',
    'require_any_permission',
    'require_all_permissions',
    'require_role',
    'require_any_role',
    # DRF Permissions
    'HasAppPermission',
    'RequireRole',
    'RequireAnyRole',
    'RequireAttribute',
]