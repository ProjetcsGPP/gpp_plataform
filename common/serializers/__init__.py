"""
Serializers genéricos compartilhados entre aplicações.
"""

from .auth_serializers import (
    LoginSerializer,
    PasswordChangeSerializer,
    PortalAuthSerializer,
)
from .base_serializers import BaseModelSerializer, TimestampedModelSerializer
from .user_serializers import (
    UserCreateSerializer,
    UserListSerializer,
    UserSerializer,
    UserUpdateSerializer,
)

__all__ = [
    # User serializers
    "UserSerializer",
    "UserListSerializer",
    "UserCreateSerializer",
    "UserUpdateSerializer",
    # Auth serializers
    "PortalAuthSerializer",
    "LoginSerializer",
    "PasswordChangeSerializer",
    # Base serializers
    "BaseModelSerializer",
    "TimestampedModelSerializer",
]
