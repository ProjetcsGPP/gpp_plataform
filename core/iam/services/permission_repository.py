"""Permission Repository

Provides cached permission queries to optimize authorization checks.
"""

from typing import List, Optional, Set
from django.core.cache import cache
from django.contrib.auth.models import Permission
from ..models import UserRole, RolePermission, Aplicacao


class PermissionRepository:
    """Repository for permission queries with caching"""
    
    # Cache TTL in seconds (5 minutes)
    CACHE_TTL = 300
    
    @staticmethod
    def get_permissions(user_id: int, app_code: str) -> List[str]:
        """Get user permissions with caching
        
        Cache key format: 'user_perms:{user_id}:{app_code}'
        
        Args:
            user_id: User ID
            app_code: Application code
            
        Returns:
            List of permission codenames
            
        Example:
            >>> perms = PermissionRepository.get_permissions(1, 'ACOES_PNGI')
            >>> # ['view_eixo', 'add_eixo', 'change_eixo', ...]
        """
        cache_key = f'user_perms:{user_id}:{app_code}'
        
        # Try cache first
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        
        # Query database
        permissions = PermissionRepository._query_permissions(user_id, app_code)
        
        # Save to cache
        cache.set(cache_key, permissions, PermissionRepository.CACHE_TTL)
        
        return permissions
    
    @staticmethod
    def get_permissions_batch(
        user_id: int,
        app_codes: List[str]
    ) -> dict[str, List[str]]:
        """Get permissions for multiple applications at once
        
        Args:
            user_id: User ID
            app_codes: List of application codes
            
        Returns:
            Dict mapping app codes to permission lists
            
        Example:
            >>> perms = PermissionRepository.get_permissions_batch(
            >>>     1, ['ACOES_PNGI', 'CARGA_ORG_LOT']
            >>> )
            >>> # {
            >>> #   'ACOES_PNGI': ['view_eixo', 'add_eixo', ...],
            >>> #   'CARGA_ORG_LOT': ['view_lotacao', ...]
            >>> # }
        """
        result = {}
        for app_code in app_codes:
            result[app_code] = PermissionRepository.get_permissions(
                user_id, app_code
            )
        return result
    
    @staticmethod
    def _query_permissions(user_id: int, app_code: str) -> List[str]:
        """Execute actual database query for permissions"""
        try:
            app = Aplicacao.objects.get(codigointerno=app_code)
        except Aplicacao.DoesNotExist:
            return []
        
        # Get user's roles in this application
        user_roles = UserRole.objects.filter(
            user_id=user_id,
            aplicacao=app
        ).values_list('role', flat=True)
        
        if not user_roles:
            return []
        
        # Get permission IDs for these roles
        permission_ids = RolePermission.objects.filter(
            role__in=user_roles
        ).values_list('permission_id', flat=True)
        
        if not permission_ids:
            return []
        
        # Get permission codenames
        return list(
            Permission.objects.filter(
                id__in=permission_ids
            ).values_list('codename', flat=True)
        )
    
    @staticmethod
    def invalidate_user_cache(
        user_id: int,
        app_code: Optional[str] = None
    ) -> None:
        """Invalidate permission cache for a user
        
        Args:
            user_id: User ID
            app_code: Application code (invalidates all if None)
            
        Example:
            >>> # After changing user roles
            >>> PermissionRepository.invalidate_user_cache(1, 'ACOES_PNGI')
            >>> 
            >>> # Invalidate all applications
            >>> PermissionRepository.invalidate_user_cache(1)
        """
        if app_code:
            cache_key = f'user_perms:{user_id}:{app_code}'
            cache.delete(cache_key)
        else:
            # Invalidate for all applications
            apps = Aplicacao.objects.values_list('codigointerno', flat=True)
            for app in apps:
                cache_key = f'user_perms:{user_id}:{app}'
                cache.delete(cache_key)
    
    @staticmethod
    def invalidate_role_cache(role_id: int) -> None:
        """Invalidate cache for all users with a specific role
        
        Use this when role permissions are changed.
        
        Args:
            role_id: Role ID
            
        Example:
            >>> # After changing permissions for GESTOR_PNGI role
            >>> PermissionRepository.invalidate_role_cache(1)
        """
        # Get all users with this role
        user_ids = UserRole.objects.filter(
            role_id=role_id
        ).values_list('user_id', flat=True).distinct()
        
        # Get the application for this role
        try:
            from ..models import Role
            role = Role.objects.select_related('aplicacao').get(id=role_id)
            app_code = role.aplicacao.codigointerno
            
            # Invalidate cache for each user
            for user_id in user_ids:
                PermissionRepository.invalidate_user_cache(user_id, app_code)
        except Role.DoesNotExist:
            pass
    
    @staticmethod
    def preload_permissions(
        user_id: int,
        app_codes: List[str]
    ) -> None:
        """Preload permissions into cache
        
        Useful for warming up cache on user login.
        
        Args:
            user_id: User ID
            app_codes: List of application codes to preload
            
        Example:
            >>> # On user login
            >>> PermissionRepository.preload_permissions(
            >>>     user.id, ['ACOES_PNGI', 'CARGA_ORG_LOT']
            >>> )
        """
        for app_code in app_codes:
            PermissionRepository.get_permissions(user_id, app_code)