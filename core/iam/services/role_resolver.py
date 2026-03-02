"""Role Resolver Service

Manages role resolution and active role selection.
"""

from typing import List, Dict, Any, Optional
from ..models import User, UserRole, Aplicacao


class RoleResolver:
    """Service for role resolution and management"""
    
    @staticmethod
    def get_user_roles_for_app(
        user: User,
        app_code: str
    ) -> List[Dict[str, Any]]:
        """Get all roles a user has in an application
        
        Args:
            user: User instance
            app_code: Application code
            
        Returns:
            List of role information dicts
            
        Example:
            >>> roles = RoleResolver.get_user_roles_for_app(
            >>>     request.user, 'ACOES_PNGI'
            >>> )
            >>> # roles = [
            >>> #   {'id': 1, 'code': 'GESTOR_PNGI', 'name': 'Gestor'},
            >>> #   {'id': 2, 'code': 'COORDENADOR_PNGI', 'name': 'Coordenador'}
            >>> # ]
        """
        user_roles = UserRole.objects.filter(
            user=user,
            aplicacao__codigointerno=app_code
        ).select_related('role', 'aplicacao')
        
        return [
            {
                'id': ur.role.id,
                'code': ur.role.codigoperfil,
                'name': ur.role.nomeperfil,
                'application_code': ur.aplicacao.codigointerno,
                'application_name': ur.aplicacao.nomeaplicacao,
            }
            for ur in user_roles
        ]
    
    @staticmethod
    def get_all_user_roles(user: User) -> Dict[str, List[Dict[str, Any]]]:
        """Get all roles for a user across all applications
        
        Args:
            user: User instance
            
        Returns:
            Dict mapping application codes to role lists
            
        Example:
            >>> all_roles = RoleResolver.get_all_user_roles(request.user)
            >>> # {
            >>> #   'ACOES_PNGI': [{'id': 1, 'code': 'GESTOR_PNGI', ...}],
            >>> #   'CARGA_ORG_LOT': [{'id': 5, 'code': 'ADMIN_ORG', ...}]
            >>> # }
        """
        user_roles = UserRole.objects.filter(
            user=user
        ).select_related('role', 'aplicacao')
        
        roles_by_app: Dict[str, List[Dict[str, Any]]] = {}
        
        for ur in user_roles:
            app_code = ur.aplicacao.codigointerno
            if app_code not in roles_by_app:
                roles_by_app[app_code] = []
            
            roles_by_app[app_code].append({
                'id': ur.role.id,
                'code': ur.role.codigoperfil,
                'name': ur.role.nomeperfil,
                'application_code': ur.aplicacao.codigointerno,
                'application_name': ur.aplicacao.nomeaplicacao,
            })
        
        return roles_by_app
    
    @staticmethod
    def get_active_role(
        user: User,
        app_code: str,
        session_data: Optional[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """Get active role for user in application
        
        For web sessions, checks session_data for saved active role.
        For APIs, returns first available role (or use header/query param).
        
        Args:
            user: User instance
            app_code: Application code
            session_data: Session dict (for web views)
            
        Returns:
            Active role dict or None
            
        Example:
            >>> # In web view
            >>> active_role = RoleResolver.get_active_role(
            >>>     request.user, 'ACOES_PNGI', request.session
            >>> )
            >>> 
            >>> # In API view
            >>> active_role = RoleResolver.get_active_role(
            >>>     request.user, 'ACOES_PNGI'
            >>> )
        """
        session_key = f'active_role_{app_code}'
        
        # Try to get from session
        if session_data and session_key in session_data:
            role_id = session_data[session_key]
            try:
                user_role = UserRole.objects.select_related(
                    'role', 'aplicacao'
                ).get(
                    user=user,
                    aplicacao__codigointerno=app_code,
                    role_id=role_id
                )
                return {
                    'id': user_role.role.id,
                    'code': user_role.role.codigoperfil,
                    'name': user_role.role.nomeperfil,
                    'application_code': user_role.aplicacao.codigointerno,
                }
            except UserRole.DoesNotExist:
                pass
        
        # Fallback: return first available role
        roles = RoleResolver.get_user_roles_for_app(user, app_code)
        return roles[0] if roles else None
    
    @staticmethod
    def set_active_role(
        user: User,
        app_code: str,
        role_id: int,
        session_data: Dict
    ) -> None:
        """Set active role in session
        
        Args:
            user: User instance
            app_code: Application code
            role_id: Role ID to activate
            session_data: Session dict to update
            
        Raises:
            ValueError: If user doesn't have the specified role
            
        Example:
            >>> try:
            >>>     RoleResolver.set_active_role(
            >>>         request.user, 'ACOES_PNGI', 1, request.session
            >>>     )
            >>> except ValueError:
            >>>     # Handle invalid role
        """
        # Validate that user has this role
        if not UserRole.objects.filter(
            user=user,
            aplicacao__codigointerno=app_code,
            role_id=role_id
        ).exists():
            raise ValueError(
                f"User {user.email} doesn't have role {role_id} "
                f"in application {app_code}"
            )
        
        session_key = f'active_role_{app_code}'
        session_data[session_key] = role_id
    
    @staticmethod
    def clear_active_role(
        app_code: str,
        session_data: Dict
    ) -> None:
        """Clear active role from session
        
        Args:
            app_code: Application code
            session_data: Session dict to update
        """
        session_key = f'active_role_{app_code}'
        if session_key in session_data:
            del session_data[session_key]
    
    @staticmethod
    def get_highest_role(
        user: User,
        app_code: str,
        role_hierarchy: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Get highest role user has according to hierarchy
        
        Args:
            user: User instance
            app_code: Application code
            role_hierarchy: List of role codes from highest to lowest
            
        Returns:
            Highest role dict or None
            
        Example:
            >>> hierarchy = [
            >>>     'GESTOR_PNGI',
            >>>     'COORDENADOR_PNGI',
            >>>     'OPERADOR_ACAO',
            >>>     'CONSULTOR_PNGI'
            >>> ]
            >>> highest = RoleResolver.get_highest_role(
            >>>     request.user, 'ACOES_PNGI', hierarchy
            >>> )
        """
        user_roles = RoleResolver.get_user_roles_for_app(user, app_code)
        user_role_codes = {role['code'] for role in user_roles}
        
        for role_code in role_hierarchy:
            if role_code in user_role_codes:
                # Find the matching role dict
                return next(
                    role for role in user_roles 
                    if role['code'] == role_code
                )
        
        return None