"""
Serializers genéricos compartilhados entre aplicações.
"""

from .user_serializers import (
    UserSerializer,
    UserListSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    RoleSerializer,
    AttributeSerializer,
    UserRoleSerializer,
)

from .auth_serializers import (
    PortalAuthSerializer,
    PortalAuthResponseSerializer,
)

from .base_serializers import (
    BaseModelSerializer,
    TimestampedModelSerializer,
)

__all__ = [
    # User serializers
    'UserSerializer',
    'UserListSerializer',
    'UserCreateSerializer',
    'UserUpdateSerializer',
    'RoleSerializer',
    'AttributeSerializer',
    'UserRoleSerializer',
    
    # Auth serializers
    'PortalAuthSerializer',
    'PortalAuthResponseSerializer',
    
    # Base serializers
    'BaseModelSerializer',
    'TimestampedModelSerializer',
]
