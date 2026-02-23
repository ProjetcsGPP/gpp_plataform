"""Authorization Service

Centralized permission checking logic.
All authorization decisions must go through this service.
"""

from typing import List, Optional
from django.contrib.auth.models import Permission
from ..models import User, UserRole, RolePermission, Aplicacao


class AuthorizationService:
    """Service for authorization decisions"""
    
    @staticmethod
    def user_has_permission(
        user: User,
        app_code: str,
        permission_codename: str
    ) -> bool:
        """Check if user has specific permission in an application
        
        Args:
            user: User instance
            app_code: Application code (e.g., 'ACOES_PNGI')
            permission_codename: Permission codename (e.g., 'add_eixo')
            
        Returns:
            True if user has the permission
            
        Example:
            >>> has_perm = AuthorizationService.user_has_permission(
            >>>     request.user, 'ACOES_PNGI', 'add_eixo'
            >>> )
            >>> if has_perm:
            >>>     # Allow action
        """
        if not user or not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True
        
        permissions = AuthorizationService.get_user_permissions(user, app_code)
        return permission_codename in permissions
    
    @staticmethod
    def user_has_any_permission(
        user: User,
        app_code: str,
        permission_codenames: List[str]
    ) -> bool:
        """Check if user has ANY of the listed permissions
        
        Args:
            user: User instance
            app_code: Application code
            permission_codenames: List of permission codenames
            
        Returns:
            True if user has at least one permission
        """
        if not user or not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True
        
        permissions = AuthorizationService.get_user_permissions(user, app_code)
        return any(perm in permissions for perm in permission_codenames)
    
    @staticmethod
    def user_has_all_permissions(
        user: User,
        app_code: str,
        permission_codenames: List[str]
    ) -> bool:
        """Check if user has ALL listed permissions
        
        Args:
            user: User instance
            app_code: Application code
            permission_codenames: List of permission codenames
            
        Returns:
            True if user has all permissions
        """
        if not user or not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True
        
        permissions = AuthorizationService.get_user_permissions(user, app_code)
        return all(perm in permissions for perm in permission_codenames)
    
    @staticmethod
    def get_user_permissions(user: User, app_code: str) -> List[str]:
        """Get list of permission codenames for user in application
        
        Uses PermissionRepository for caching.
        
        Args:
            user: User instance
            app_code: Application code
            
        Returns:
            List of permission codenames
        """
        from .permission_repository import PermissionRepository
        return PermissionRepository.get_permissions(user.id, app_code)
    
    @staticmethod
    def user_has_role(
        user: User,
        app_code: str,
        role_code: str
    ) -> bool:
        """Check if user has specific role
        
        Args:
            user: User instance
            app_code: Application code
            role_code: Role code (e.g., 'GESTOR_PNGI')
            
        Returns:
            True if user has the role
            
        Example:
            >>> is_gestor = AuthorizationService.user_has_role(
            >>>     request.user, 'ACOES_PNGI', 'GESTOR_PNGI'
            >>> )
        """
        if not user or not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True
        
        return UserRole.objects.filter(
            user=user,
            aplicacao__codigointerno=app_code,
            role__codigoperfil=role_code
        ).exists()
    
    @staticmethod
    def user_has_any_role(
        user: User,
        app_code: str,
        role_codes: List[str]
    ) -> bool:
        """Check if user has any of the listed roles
        
        Args:
            user: User instance
            app_code: Application code
            role_codes: List of role codes
            
        Returns:
            True if user has at least one role
            
        Example:
            >>> can_manage = AuthorizationService.user_has_any_role(
            >>>     request.user, 
            >>>     'ACOES_PNGI', 
            >>>     ['GESTOR_PNGI', 'COORDENADOR_PNGI']
            >>> )
        """
        if not user or not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True
        
        return UserRole.objects.filter(
            user=user,
            aplicacao__codigointerno=app_code,
            role__codigoperfil__in=role_codes
        ).exists()
    
    @staticmethod
    def user_has_attribute(
        user: User,
        app_code: str,
        key: str,
        value: Optional[str] = None
    ) -> bool:
        """Check user ABAC attribute
        
        Args:
            user: User instance
            app_code: Application code
            key: Attribute key
            value: Attribute value (optional, checks existence if None)
            
        Returns:
            True if user has the attribute
            
        Example:
            >>> can_upload = AuthorizationService.user_has_attribute(
            >>>     request.user, 'ACOES_PNGI', 'can_upload', 'true'
            >>> )
        """
        from ..models import Attribute
        
        if not user or not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True
        
        query = Attribute.objects.filter(
            user=user,
            aplicacao__codigointerno=app_code,
            key=key
        )
        
        if value is not None:
            query = query.filter(value=value)
        
        return query.exists()