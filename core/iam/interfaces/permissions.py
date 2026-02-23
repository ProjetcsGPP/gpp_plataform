"""DRF Permission Classes

Django REST Framework permission classes that use IAM services
for authorization decisions.
"""

from typing import List, Optional
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView
from ..services.authorization_service import AuthorizationService


class HasAppPermission(BasePermission):
    """Generic permission class based on Django permissions
    
    Automatically maps HTTP methods to Django permission actions:
    - GET/HEAD/OPTIONS → view_{model}
    - POST → add_{model}
    - PUT/PATCH → change_{model}
    - DELETE → delete_{model}
    
    Usage in ViewSet:
        >>> class EixoViewSet(ModelViewSet):
        >>>     permission_classes = [HasAppPermission]
        >>>     app_code = 'ACOES_PNGI'
        >>>     queryset = Eixo.objects.all()
        >>>     serializer_class = EixoSerializer
    
    The permission will automatically check:
    - GET → user_has_permission(user, 'ACOES_PNGI', 'view_eixo')
    - POST → user_has_permission(user, 'ACOES_PNGI', 'add_eixo')
    - etc.
    """
    
    permission_map = {
        'GET': 'view',
        'HEAD': 'view',
        'OPTIONS': 'view',
        'POST': 'add',
        'PUT': 'change',
        'PATCH': 'change',
        'DELETE': 'delete',
    }
    
    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check if user has permission for this request"""
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Superuser always has access
        if request.user.is_superuser:
            return True
        
        # Get app_code from view
        app_code = getattr(view, 'app_code', None)
        if not app_code:
            # Fallback: try to infer from view class name or raise error
            return False
        
        # Get model name from queryset
        if hasattr(view, 'queryset') and view.queryset is not None:
            model_name = view.queryset.model._meta.model_name
        else:
            return False
        
        # Map HTTP method to permission action
        action = self.permission_map.get(request.method, 'view')
        perm_codename = f'{action}_{model_name}'
        
        # Check permission using AuthorizationService
        return AuthorizationService.user_has_permission(
            request.user, app_code, perm_codename
        )
    
    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj
    ) -> bool:
        """Object-level permission check
        
        By default, uses same logic as has_permission.
        Override in subclass for object-specific rules.
        """
        return self.has_permission(request, view)


class RequireRole(BasePermission):
    """Permission class requiring specific roles
    
    Usage in ViewSet:
        >>> class ConfigViewSet(ModelViewSet):
        >>>     permission_classes = [RequireRole]
        >>>     app_code = 'ACOES_PNGI'
        >>>     required_roles = ['GESTOR_PNGI', 'COORDENADOR_PNGI']
        >>>     ...
    
    For read-only access with different write roles:
        >>> class EixoViewSet(ModelViewSet):
        >>>     permission_classes = [RequireRole]
        >>>     app_code = 'ACOES_PNGI'
        >>>     required_roles_read = ['GESTOR_PNGI', 'COORDENADOR_PNGI', 'OPERADOR_ACAO', 'CONSULTOR_PNGI']
        >>>     required_roles_write = ['GESTOR_PNGI', 'COORDENADOR_PNGI']
    """
    
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
    
    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check if user has required role"""
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        app_code = getattr(view, 'app_code', None)
        if not app_code:
            return False
        
        # Check if view has different roles for read/write
        if request.method in self.SAFE_METHODS:
            required_roles = getattr(
                view, 'required_roles_read',
                getattr(view, 'required_roles', [])
            )
        else:
            required_roles = getattr(
                view, 'required_roles_write',
                getattr(view, 'required_roles', [])
            )
        
        if not required_roles:
            return False
        
        return AuthorizationService.user_has_any_role(
            request.user, app_code, required_roles
        )


class RequireAnyRole(BasePermission):
    """Alias for RequireRole (semantic clarity)
    
    Usage:
        >>> class MyViewSet(ModelViewSet):
        >>>     permission_classes = [RequireAnyRole]
        >>>     app_code = 'ACOES_PNGI'
        >>>     required_roles = ['GESTOR_PNGI', 'COORDENADOR_PNGI']
    """
    
    def has_permission(self, request: Request, view: APIView) -> bool:
        return RequireRole().has_permission(request, view)


class RequireAttribute(BasePermission):
    """Permission class requiring specific ABAC attribute
    
    Usage in ViewSet:
        >>> class UploadViewSet(GenericViewSet):
        >>>     permission_classes = [RequireAttribute]
        >>>     app_code = 'ACOES_PNGI'
        >>>     required_attribute_key = 'can_upload'
        >>>     required_attribute_value = 'true'
        >>>     ...
    
    Or check only key existence:
        >>> class BetaFeatureViewSet(GenericViewSet):
        >>>     permission_classes = [RequireAttribute]
        >>>     app_code = 'ACOES_PNGI'
        >>>     required_attribute_key = 'beta_access'
        >>>     # No required_attribute_value = checks only if key exists
    """
    
    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check if user has required attribute"""
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        app_code = getattr(view, 'app_code', None)
        attr_key = getattr(view, 'required_attribute_key', None)
        
        if not app_code or not attr_key:
            return False
        
        attr_value = getattr(view, 'required_attribute_value', None)
        
        return AuthorizationService.user_has_attribute(
            request.user, app_code, attr_key, attr_value
        )


class IsReadOnly(BasePermission):
    """Allow only safe methods (GET, HEAD, OPTIONS)
    
    Useful for combining with other permissions:
        >>> permission_classes = [IsAuthenticated, IsReadOnly | HasAppPermission]
    """
    
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
    
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.method in self.SAFE_METHODS