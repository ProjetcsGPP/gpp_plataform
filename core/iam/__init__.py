"""Core IAM (Identity and Access Management) module

This module provides centralized authentication and authorization services
for the GPP Platform. It's designed to be a service-oriented architecture
that can eventually be extracted as an independent microservice.

Public API:
    Services:
        - TokenService: JWT generation and validation
        - AuthorizationService: Permission checking
        - RoleResolver: Role management
        - PermissionRepository: Permission queries with cache
    
    Interfaces:
        - Decorators: @require_permission, @require_role
        - Permissions: HasAppPermission, RequireRole (DRF)
        - Middleware: IAMContextMiddleware

Usage:
    # In domain apps
    from core.iam.services import AuthorizationService
    from core.iam.interfaces.permissions import HasAppPermission
    
    # Check permission
    if AuthorizationService.user_has_permission(user, 'ACOES_PNGI', 'add_eixo'):
        # do something
"""

__version__ = '1.0.0'
__all__ = [
    'services',
    'interfaces',
    'models',
]