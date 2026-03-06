from .models import User  # Importar o modelo de usuário personalizado
from .services.authorization_service import (
    AuthorizationService,
    get_authorization_service,
)
from .services.permission_repository import Permission, Role
from .services.role_resolver import require_permission, require_role
from .services.token_service import TokenService, get_token_service

__all__ = [
    "AuthorizationService",
    "Permission",
    "Role",
    "require_permission",
    "require_role",
    "User",
    "TokenService",
    "get_token_service",
    "get_authorization_service",
]
