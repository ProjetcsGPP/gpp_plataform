"""
Serializers para autenticação e integração com portal.
"""

from rest_framework import serializers
from .user_serializers import UserSerializer


class PortalAuthSerializer(serializers.Serializer):
    """
    Serializer para request de autenticação via portal.
    """
    token = serializers.CharField(required=True)


class PortalAuthResponseSerializer(serializers.Serializer):
    """
    Serializer para resposta de autenticação via portal.
    """
    user = UserSerializer(read_only=True)
    local_token = serializers.CharField(read_only=True)
    app_code = serializers.CharField(read_only=True)
