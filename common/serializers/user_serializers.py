"""
Serializers de usuário genéricos para reutilização entre aplicações.
Usa request.app_context do middleware para detecção automática da aplicação.
"""

from rest_framework import serializers
from accounts.models import User, UserRole, Attribute, Role, Aplicacao
from typing import Optional


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer completo de usuário com roles e atributos.
    
    Usa request.app_context (do AppContextMiddleware) para filtrar
    roles e atributos automaticamente pela aplicação atual.
    
    Context esperado:
        - request: HttpRequest com app_context (adicionado pelo middleware)
        - app_code: str (opcional, fallback se middleware não disponível)
    
    Exemplo:
        serializer = UserSerializer(user, context={'request': request})
        # Retorna roles e atributos da aplicação atual
    """
    
    roles = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    email = serializers.CharField(source='email', read_only=True)
    name = serializers.CharField(source='nome', read_only=True)
    user_type = serializers.IntegerField(source='idtipousuario', read_only=True)
    status = serializers.IntegerField(source='idstatususuario', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 
                    'name', 
                    'email', 
                    'user_type',      # já adicionado
                    'status',         # ADICIONAR ESTE
                    'is_active', 
                    'is_staff', 
                    'is_superuser', 
                    'last_login', 
                    'date_joined', 
                    'idstatususuario', 
                    'idtipousuario', 
                    'idclassificacaousuario',
                    'roles',           # ADICIONAR
                    'attributes',      # ADICIONAR
                    ]
        read_only_fields = ['id', 'last_login', 'date_joined']
    
    def get_roles(self, obj: User) -> list:
        """
        Retorna roles do usuário para a aplicação do contexto.
        
        Prioridade:
        1. request.app_context['code'] (do middleware)
        2. context['app_code'] (fallback manual)
        3. [] (se nenhum disponível)
        """
        app_code = self._get_app_code()
        
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
    
    def get_attributes(self, obj: User) -> dict:
        """
        Retorna atributos customizados do usuário para a aplicação do contexto.
        
        Retorna dict: {'key': 'value', ...}
        """
        app_code = self._get_app_code()
        
        if not app_code:
            return {}
        
        attrs = Attribute.objects.filter(
            user=obj,
            aplicacao__codigointerno=app_code
        ).values_list('key', 'value')
        
        return dict(attrs)
    
    def _get_app_code(self) -> Optional[str]:
        """
        Obtém código da aplicação do contexto.
        
        Prioridade:
        1. request.app_context['code'] (middleware)
        2. context['app_code'] (manual)
        """
        request = self.context.get('request')
        
        # Prioridade 1: middleware
        if request and hasattr(request, 'app_context'):
            return request.app_context.get('code')
        
        # Prioridade 2: context manual (fallback)
        return self.context.get('app_code')


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer otimizado para listagem de usuários (sem roles/atributos).
    
    Use para listagens onde não precisa de roles/atributos para
    melhor performance.
    """
    
    email = serializers.CharField(source='email', read_only=True)
    name = serializers.CharField(source='nome', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'idusuario',
            'email',
            'name',
            'is_active',
            'last_login',
        ]
        read_only_fields = fields


class UserCreateSerializer(serializers.Serializer):
    """
    Serializer para criação/sincronização de usuários via portal.
    
    Cria ou atualiza usuário com roles e atributos para a aplicação
    do contexto (detectada automaticamente pelo middleware).
    
    Context esperado:
        - request: HttpRequest com app_context
        - app_code: str (fallback manual)
    
    Exemplo:
        serializer = UserCreateSerializer(
            data={
                'email': 'novo@example.com',
                'name': 'Novo Usuário',
                'roles': ['GESTOR_PNGI'],
                'attributes': {'can_upload': 'true'}
            },
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = serializer.save()
            created = serializer.validated_data['_created']
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
    password = serializers.CharField(
        required=False,
        write_only=True,
        allow_blank=True
    )
    
    def validate_email(self, value):
        """Normaliza email para lowercase"""
        return value.lower().strip()
    
    def save(self):
        """
        Cria ou atualiza usuário com roles e atributos.
        
        Usa common.services.portal_auth.PortalAuthService
        """
        from common.services.portal_auth import get_portal_auth_service
        
        # Obtém app_code do contexto
        app_code = self._get_app_code()
        
        if not app_code:
            raise serializers.ValidationError(
                "Aplicação não identificada. Configure app_code no context ou use AppContextMiddleware."
            )
        
        # Usa serviço de autenticação
        portal_service = get_portal_auth_service(app_code)
        
        user, created, app = portal_service.sync_user(
            email=self.validated_data['email'],
            name=self.validated_data['name'],
            roles_data=self.validated_data.get('roles', []),
            attributes_data=self.validated_data.get('attributes', {})
        )
        
        # Se senha foi fornecida, atualiza
        password = self.validated_data.get('password')
        if password:
            user.set_password(password)
            user.save()
        
        # Adiciona flag ao validated_data
        self.validated_data['_created'] = created
        self.validated_data['_user'] = user
        self.validated_data['_app'] = app
        
        return user
    
    def _get_app_code(self) -> Optional[str]:
        """Obtém código da aplicação (mesmo método do UserSerializer)"""
        request = self.context.get('request')
        
        if request and hasattr(request, 'app_context'):
            return request.app_context.get('code')
        
        return self.context.get('app_code')


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização parcial de usuários.
    
    Permite atualizar:
    - name (strnome)
    - is_active
    - user_type (idtipousuario)
    - status (idstatususuario)
    """
    
    name = serializers.CharField(source='nome', required=False)
    user_type = serializers.IntegerField(source='idtipousuario', required=False)
    status = serializers.IntegerField(source='idstatususuario', required=False)
    
    class Meta:
        model = User
        fields = ['name', 'is_active', 'user_type', 'status']
    
    def validate_user_type(self, value):
        """Valida tipo de usuário"""
        if value not in [1, 2]:  # 1: comum, 2: admin
            raise serializers.ValidationError("Tipo de usuário inválido")
        return value
    
    def validate_status(self, value):
        """Valida status do usuário"""
        if value not in [1, 2, 3]:  # 1: ativo, 2: inativo, 3: bloqueado
            raise serializers.ValidationError("Status inválido")
        return value

class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer para Role (perfil de acesso).
    """
    from accounts.models import Role
    
    class Meta:
        model = Role
        fields = [
            'id',
            'nomeperfil',
            'codigoperfil',
            'aplicacao',
        ]
        read_only_fields = ['id']


class AttributeSerializer(serializers.ModelSerializer):
    """
    Serializer para Attribute (atributos customizados).
    """
    from accounts.models import Attribute
    
    class Meta:
        model = Attribute
        fields = [
            'id',
            'user',
            'aplicacao',
            'key',
            'value',
        ]
        read_only_fields = ['id']


class UserRoleSerializer(serializers.ModelSerializer):
    """
    Serializer para UserRole (relação usuário-perfil-aplicação).
    """
    from accounts.models import UserRole
    
    role = RoleSerializer(read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    app_code = serializers.CharField(source='aplicacao.codigointerno', read_only=True)
    
    class Meta:
        model = UserRole
        fields = [
            'id',
            'user',
            'user_email',
            'role',
            'aplicacao',
            'app_code',
        ]
        read_only_fields = ['id']