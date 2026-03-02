"""IAM Serializers

Django REST Framework serializers for IAM entities.
"""

from rest_framework import serializers
from .models import User, Aplicacao, Role, UserRole, Attribute


class AplicacaoSerializer(serializers.ModelSerializer):
    """Serializer for Application model"""
    
    class Meta:
        model = Aplicacao
        fields = [
            'idaplicacao',
            'codigointerno',
            'nomeaplicacao',
            'base_url',
            'isshowinportal',
        ]
        read_only_fields = ['idaplicacao']


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role model"""
    
    aplicacao_code = serializers.CharField(
        source='aplicacao.codigointerno',
        read_only=True
    )
    aplicacao_name = serializers.CharField(
        source='aplicacao.nomeaplicacao',
        read_only=True
    )
    
    class Meta:
        model = Role
        fields = [
            'id',
            'nomeperfil',
            'codigoperfil',
            'aplicacao',
            'aplicacao_code',
            'aplicacao_name',
        ]
        read_only_fields = ['id']


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user information (safe for public exposure)"""
    
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'is_active',
        ]
        read_only_fields = ['id', 'email']


class UserRoleSerializer(serializers.ModelSerializer):
    """Serializer for UserRole relationship"""
    
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    role_name = serializers.CharField(source='role.nomeperfil', read_only=True)
    role_code = serializers.CharField(source='role.codigoperfil', read_only=True)
    app_code = serializers.CharField(
        source='aplicacao.codigointerno',
        read_only=True
    )
    app_name = serializers.CharField(
        source='aplicacao.nomeaplicacao',
        read_only=True
    )
    
    class Meta:
        model = UserRole
        fields = [
            'id',
            'user',
            'user_name',
            'user_email',
            'aplicacao',
            'app_code',
            'app_name',
            'role',
            'role_name',
            'role_code',
        ]
        read_only_fields = ['id']


class AttributeSerializer(serializers.ModelSerializer):
    """Serializer for ABAC attributes"""
    
    user_email = serializers.CharField(source='user.email', read_only=True)
    app_code = serializers.CharField(
        source='aplicacao.codigointerno',
        read_only=True
    )
    
    class Meta:
        model = Attribute
        fields = [
            'id',
            'user',
            'user_email',
            'aplicacao',
            'app_code',
            'key',
            'value',
        ]
        read_only_fields = ['id']


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed user information including roles and attributes"""
    
    roles = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'is_active',
            'is_staff',
            'date_joined',
            'last_login',
            'roles',
            'attributes',
        ]
        read_only_fields = ['id', 'email', 'date_joined', 'last_login']
    
    def get_roles(self, obj):
        """Get user roles grouped by application"""
        from ..services.role_resolver import RoleResolver
        return RoleResolver.get_all_user_roles(obj)
    
    def get_attributes(self, obj):
        """Get user ABAC attributes"""
        attrs = Attribute.objects.filter(user=obj).select_related('aplicacao')
        return AttributeSerializer(attrs, many=True).data


class TokenResponseSerializer(serializers.Serializer):
    """Serializer for token response"""
    
    token = serializers.CharField()
    token_type = serializers.CharField(default='Bearer')
    expires_in = serializers.IntegerField(help_text='Token lifetime in seconds')
    user = UserBasicSerializer()
    
    class Meta:
        fields = ['token', 'token_type', 'expires_in', 'user']