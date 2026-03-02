"""IAM Middleware

Middleware for injecting IAM context into requests.
"""

from typing import Callable
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from ..services.role_resolver import RoleResolver
from ..services.authorization_service import AuthorizationService


class IAMContextMiddleware(MiddlewareMixin):
    """Middleware that adds IAM context to request object
    
    Adds the following attributes to request:
    - request.user_roles: Dict of roles by application
    - request.active_role: Active role for current app (if in session)
    - request.user_permissions: Helper method to check permissions
    
    Installation in settings.py:
        MIDDLEWARE = [
            ...,
            'core.iam.interfaces.middleware.IAMContextMiddleware',
            ...,
        ]
    
    Usage in views:
        >>> def my_view(request):
        >>>     # Access user roles
        >>>     roles = request.user_roles.get('ACOES_PNGI', [])
        >>>     
        >>>     # Check permission
        >>>     if request.user_has_permission('ACOES_PNGI', 'add_eixo'):
        >>>         ...
    """
    
    def process_request(self, request: HttpRequest) -> None:
        """Add IAM context to request"""
        if not request.user or not request.user.is_authenticated:
            request.user_roles = {}
            request.active_role = None
            return
        
        # Add all user roles
        request.user_roles = RoleResolver.get_all_user_roles(request.user)
        
        # Try to get active role from session
        # (application-specific, view should specify app_code)
        request.active_role = None
        
        # Add helper method for permission checking
        def user_has_permission(app_code: str, permission_codename: str) -> bool:
            """Helper method attached to request"""
            return AuthorizationService.user_has_permission(
                request.user, app_code, permission_codename
            )
        
        request.user_has_permission = user_has_permission
        
        # Add helper method for role checking
        def user_has_role(app_code: str, role_code: str) -> bool:
            """Helper method attached to request"""
            return AuthorizationService.user_has_role(
                request.user, app_code, role_code
            )
        
        request.user_has_role = user_has_role


class ActiveRoleMiddleware(MiddlewareMixin):
    """Middleware that resolves active role for specific application
    
    This middleware should be configured per-application URL pattern.
    It sets request.active_role based on session data.
    
    Example with separate settings per app:
        # In acoes_pngi/middleware.py
        class AcoesPNGIRoleMiddleware(ActiveRoleMiddleware):
            app_code = 'ACOES_PNGI'
    
    Or configure in URLs:
        # In acoes_pngi/urls.py (if Django supports per-URL middleware)
        urlpatterns = [
            path('acoes/', include('acoes_pngi.urls')),
        ]
    """
    
    # Override this in subclass or set in settings
    app_code: str = None
    
    def process_request(self, request: HttpRequest) -> None:
        """Resolve active role for application"""
        if not request.user or not request.user.is_authenticated:
            return
        
        if not self.app_code:
            return
        
        # Get active role from session
        active_role = RoleResolver.get_active_role(
            request.user,
            self.app_code,
            request.session
        )
        
        request.active_role = active_role
        request.active_app_code = self.app_code