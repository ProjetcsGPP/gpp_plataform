"""Token Service

Centralized JWT generation and validation.
No application should generate JWT tokens directly.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from ..models import User, UserRole, Attribute


class TokenService:
    """Service for JWT token generation and validation"""
    
    @staticmethod
    def generate_token(
        user: User,
        aplicacao_code: Optional[str] = None,
        expiration_hours: Optional[int] = None
    ) -> str:
        """Generate JWT token for a user
        
        Args:
            user: User instance
            aplicacao_code: Application code (optional, includes all if None)
            expiration_hours: Token expiration time (defaults to settings)
            
        Returns:
            Signed JWT token string
            
        Example:
            >>> token = TokenService.generate_token(user, 'ACOES_PNGI')
            >>> # Use token in Authorization header
        """
        if expiration_hours is None:
            expiration_hours = getattr(settings, 'JWT_EXPIRATION_HOURS', 24)
        
        payload = {
            'user_id': user.id,
            'email': user.email,
            'name': user.name,
            'exp': datetime.utcnow() + timedelta(hours=expiration_hours),
            'iat': datetime.utcnow(),
        }
        
        # Include roles and attributes in payload
        roles_data = TokenService._get_user_roles(user, aplicacao_code)
        attrs_data = TokenService._get_user_attributes(user, aplicacao_code)
        
        payload['roles'] = roles_data
        payload['attrs'] = attrs_data
        
        if aplicacao_code:
            payload['app'] = aplicacao_code
        
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def validate_token(token: str) -> Optional[Dict[str, Any]]:
        """Validate and decode JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded payload dict or None if invalid
            
        Example:
            >>> payload = TokenService.validate_token(token)
            >>> if payload:
            >>>     user_id = payload['user_id']
        """
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def refresh_token(token: str) -> Optional[str]:
        """Refresh an existing token
        
        Args:
            token: Current JWT token
            
        Returns:
            New JWT token or None if current token is invalid
        """
        payload = TokenService.validate_token(token)
        if not payload:
            return None
        
        try:
            user = User.objects.get(id=payload['user_id'])
            app_code = payload.get('app')
            return TokenService.generate_token(user, app_code)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def _get_user_roles(
        user: User,
        aplicacao_code: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Extract user roles for token payload"""
        query = UserRole.objects.filter(user=user).select_related('role', 'aplicacao')
        
        if aplicacao_code:
            query = query.filter(aplicacao__codigointerno=aplicacao_code)
        
        return [
            {
                'application__code': ur.aplicacao.codigointerno,
                'application__name': ur.aplicacao.nomeaplicacao,
                'role__code': ur.role.codigoperfil,
                'role__name': ur.role.nomeperfil,
                'role__id': ur.role.id,
            }
            for ur in query
        ]
    
    @staticmethod
    def _get_user_attributes(
        user: User,
        aplicacao_code: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Extract user ABAC attributes for token payload"""
        query = Attribute.objects.filter(user=user).select_related('aplicacao')
        
        if aplicacao_code:
            query = query.filter(aplicacao__codigointerno=aplicacao_code)
        
        return [
            {
                'application__code': attr.aplicacao.codigointerno if attr.aplicacao else None,
                'key': attr.key,
                'value': attr.value,
            }
            for attr in query
        ]