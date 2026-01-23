"""
Serializers genéricos compartilhados entre aplicações.
"""

from .user_serializers import (
    UserSerializer,
    UserListSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)

from .auth_serializers import (
    PortalAuthSerializer,
    LoginSerializer,
    PasswordChangeSerializer,
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
    
    # Auth serializers
    'PortalAuthSerializer',
    'LoginSerializer',
    'PasswordChangeSerializer',
    
    # Base serializers
    'BaseModelSerializer',
    'TimestampedModelSerializer',
]
