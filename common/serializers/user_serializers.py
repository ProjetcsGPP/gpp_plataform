"""
Serializers genéricos para User e relacionados.
Usados por todas as aplicações que precisam manipular usuários.
"""

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.db import transaction

from accounts.models import User, Aplicacao, Role, UserRole, Attribute
from .base_serializers import BaseModelSerializer


class RoleSerializer(BaseModelSerializer):
    """
    Serializer para roles/perfis de usuário.
    """
    aplicacao_nome = serializers.CharField(
        source='aplicacao.nomeaplicacao',
        read_only=True
    )
    aplicacao_codigo = serializers.CharField(
        source='aplicacao.codigointerno',
        read_only=True
    )
    
    class Meta:
        model = Role
        fields = [
            'id',
            'nomeperfil',
            'codigoperfil',
            'aplicacao',
            'aplicacao_nome',
            'aplicacao_codigo'
        ]
        read_only_fields = ['id']


class AttributeSerializer(BaseModelSerializer):
    """
    Serializer para atributos customizados de usuário.
    """
    
    class Meta:
        model = Attribute
        fields = ['id', 'key', 'value', 'aplicacao', 'user']
        read_only_fields = ['id']


class UserRoleSerializer(BaseModelSerializer):
    """
    Serializer para relacionamento usuário-role.
    """
    role_details = RoleSerializer(source='role', read_only=True)
    
    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role', 'aplicacao', 'role_details']
        read_only_fields = ['id']


class UserSerializer(BaseModelSerializer):
    """
    Serializer completo para o modelo User.
    Inclui roles e atributos relacionados à aplicação do contexto.
    """
    roles = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'idusuario',
            'stremail',
            'strnome',
            'idtipousuario',
            'idstatususuario',
            'idclassificacaousuario',
            'is_active',
            'is_staff',
            'is_superuser',
            'datacriacao',
            'data_alteracao',
            'last_login',
            'date_joined',
            'roles',
            'attributes'
        ]
        read_only_fields = [
            'idusuario',
            'datacriacao',
            'data_alteracao',
            'last_login',
            'date_joined',
            'roles',
            'attributes'
        ]
    
    def get_roles(self, obj):
        """Retorna roles do usuário para a aplicação do contexto"""
        request = self.context.get('request')
        
        # ✨ Novo: pega do middleware
        if request and hasattr(request, 'app_context'):
            app_code = request.app_context['code']
        else:
            # Fallback: pega do context manual
            app_code = self.context.get('app_code')
        
        if not app_code:
            return []
        
        user_roles = UserRole.objects.filter(
            user=obj,
            aplicacao__codigointerno=app_code
        ).select_related('role')
        
        return [
            {
                'id': ur.role.id,
                'code': ur.role.codigoperfil,
                'name': ur.role.nomeperfil
            }
            for ur in user_roles
        ]
    
    def get_attributes(self, obj):
        """Retorna atributos do usuário para a aplicação do contexto"""
        from common.services.portal_auth import get_portal_auth_service
        
        app_code = self._get_app_code_from_context()
        if not app_code:
            return {}
        
        portal_service = get_portal_auth_service(app_code)
        return portal_service.get_user_attributes(obj.stremail)
    
    def _get_app_code_from_context(self):
        """Helper para obter APP_CODE do contexto"""
        # Tenta pegar do contexto explícito
        app_code = self.context.get('app_code')
        if app_code:
            return app_code
        
        # Tenta pegar do request (via middleware)
        request = self.context.get('request')
        if request and hasattr(request, 'app_code'):
            return request.app_code
        
        return None


class UserListSerializer(BaseModelSerializer):
    """
    Serializer otimizado para listagem de usuários.
    """
    
    class Meta:
        model = User
        fields = [
            'idusuario',
            'stremail',
            'strnome',
            'is_active',
            'idstatususuario',
            'datacriacao'
        ]


class UserCreateSerializer(serializers.Serializer):
    """
    Serializer para criação/sincronização de usuário via portal.
    """
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True, max_length=200)
    roles = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )
    attributes = serializers.DictField(
        child=serializers.CharField(),
        required=False,
        default=dict
    )
    
    def create(self, validated_data):
        """Cria ou atualiza usuário com roles e atributos"""
        from common.services.portal_auth import get_portal_auth_service
        
        app_code = self._get_app_code_from_context()
        if not app_code:
            raise serializers.ValidationError("APP_CODE não identificado")
        
        portal_service = get_portal_auth_service(app_code)
        
        user, created, app = portal_service.sync_user(
            email=validated_data['email'],
            name=validated_data['name'],
            roles_data=validated_data.get('roles', []),
            attributes_data=validated_data.get('attributes', {})
        )
        
        validated_data['_created'] = created
        validated_data['_app'] = app
        
        return user
    
    def _get_app_code_from_context(self):
        """Helper para obter APP_CODE do contexto"""
        app_code = self.context.get('app_code')
        if app_code:
            return app_code
        
        request = self.context.get('request')
        if request and hasattr(request, 'app_code'):
            return request.app_code
        
        return None


class UserUpdateSerializer(serializers.Serializer):
    """
    Serializer para atualização parcial de usuário.
    """
    idstatususuario = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)
    
    def update(self, instance, validated_data):
        """Atualiza apenas campos permitidos"""
        if 'idstatususuario' in validated_data:
            instance.idstatususuario = validated_data['idstatususuario']
        
        if 'is_active' in validated_data:
            instance.is_active = validated_data['is_active']
        
        instance.save()
        return instance
