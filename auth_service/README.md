AuthService
Serviço genérico para autenticação e sincronização de usuários entre aplicações.

Inicialização
python
from common.services.portal_auth import get_portal_auth_service

# Obtém instância do serviço para uma aplicação
portal_service = get_portal_auth_service('ACOES_PNGI')
Métodos Principais
authenticate_user(token: str)
Autentica usuário via token do portal.

python
user = portal_service.authenticate_user(jwt_token)

if user:
    # Usuário autenticado
    print(f"Bem-vindo, {user.strnome}")
else:
    # Token inválido
    print("Autenticação falhou")
sync_user(email, name, roles_data, attributes_data)
Sincroniza usuário com roles e atributos da aplicação.

python
user, created, app = portal_service.sync_user(
    email='usuario@example.com',
    name='João Silva',
    roles_data=['GESTOR_PNGI', 'USER_PORTAL'],
    attributes_data={'can_upload': 'true', 'max_file_size': '50MB'}
)

if created:
    print("Novo usuário criado")
else:
    print("Usuário atualizado")
get_user_roles(email: str)
Retorna roles do usuário para a aplicação.

python
roles = portal_service.get_user_roles('usuario@example.com')
# [{'code': 'GESTOR_PNGI', 'name': 'Gestor PNGI'}, ...]
get_user_attributes(email: str)
Retorna atributos do usuário para a aplicação.

python
attributes = portal_service.get_user_attributes('usuario@example.com')
# {'can_upload': 'true', 'max_file_size': '50MB'}
🎯 Casos de Uso
1. Criar Serializer para Novo Modelo
python
# acoes_pngi/serializers.py
from common.serializers import TimestampedModelSerializer
from .models import MinhaEntidade

class MinhaEntidadeSerializer(TimestampedModelSerializer):
    class Meta:
        model = MinhaEntidade
        fields = [
            'id',
            'nome',
            'descricao',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
2. Endpoint de Autenticação via Portal
python
# acoes_pngi/views/api_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from common.services.portal_auth import get_portal_auth_service
from common.serializers import PortalAuthSerializer, UserSerializer

@api_view(['POST'])
def portal_auth(request):
    # Valida input
    input_serializer = PortalAuthSerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)
    
    token = input_serializer.validated_data['token']
    
    # Autentica via portal
    portal_service = get_portal_auth_service('ACOES_PNGI')
    user = portal_service.authenticate_user(token)
    
    if not user:
        return Response(
            {'detail': 'Token inválido'},
            status=401
        )
    
    # Serializa usuário com contexto da aplicação
    user_serializer = UserSerializer(
        user,
        context={'app_code': 'ACOES_PNGI', 'request': request}
    )
    
    return Response({
        'user': user_serializer.data,
        'app_code': 'ACOES_PNGI'
    })
3. Sincronizar Usuário do Portal
python
from common.services.portal_auth import get_portal_auth_service

portal_service = get_portal_auth_service('CARGA_ORG_LOT')

# Dados vindos do portal
user_data = {
    'email': 'novo.gestor@example.com',
    'name': 'Novo Gestor',
    'roles': ['GESTOR_CARGA'],
    'attributes': {
        'can_upload': 'true',
        'max_patriarcas': '10'
    }
}

# Sincroniza
user, created, app = portal_service.sync_user(
    email=user_data['email'],
    name=user_data['name'],
    roles_data=user_data['roles'],
    attributes_data=user_data['attributes']
)

print(f"Usuário {'criado' if created else 'atualizado'} para {app.nomeaplicacao}")
🧩 Integração com Outras Apps
acoes_pngi
python
# acoes_pngi/serializers.py
from common.serializers import TimestampedModelSerializer, UserSerializer

# acoes_pngi/views/api_views.py
from common.services.portal_auth import get_portal_auth_service
carga_org_lot
python
# carga_org_lot/serializers.py
from common.serializers import BaseModelSerializer

# carga_org_lot/views/api_views.py
from common.serializers import UserCreateSerializer
🔄 Fluxo de Autenticação com Common
text
1. Frontend envia token JWT para /api/v1/acoes_pngi/auth/portal/
   ↓
2. View usa PortalAuthSerializer para validar input
   ↓
3. View chama portal_service.authenticate_user(token)
   ↓
4. PortalAuthService valida token com portal (ou mock em dev)
   ↓
5. Retorna User object se válido
   ↓
6. View usa UserSerializer com app_code context
   ↓
7. UserSerializer busca roles e atributos para a aplicação
   ↓
8. Resposta JSON com dados completos do usuário
📚 Dependências
A aplicação common depende de:

accounts: Para modelos User, Role, UserRole, Attribute, Aplicacao

rest_framework: Para serializers

requests: Para comunicação com portal (em produção)

🧪 Testes
bash
# Testar common
python manage.py test common

# Testar serviços
python manage.py test common.tests.test_services

# Testar serializers
python manage.py test common.tests.test_serializers
🛠️ Extensibilidade
Criar Novo Serializer Base
python
# common/serializers/base_serializers.py

class AuditableModelSerializer(TimestampedModelSerializer):
    """Serializer para modelos com auditoria"""
    
    created_by = serializers.CharField(
        source='idusuariocriacao.strnome',
        read_only=True
    )
    updated_by = serializers.CharField(
        source='idusuarioalteracao.strnome',
        read_only=True
    )
    
    class Meta:
        abstract = True
        fields = TimestampedModelSerializer.Meta.fields + [
            'created_by',
            'updated_by'
        ]
Criar Novo Serviço
python
# common/services/novo_servico.py

class NovoServico:
    """Descrição do serviço"""
    
    def __init__(self, app_code: str):
        self.app_code = app_code
    
    def metodo_util(self):
        # Lógica reutilizável
        pass

# common/services/__init__.py
from .novo_servico import NovoServico

__all__ = ['get_portal_auth_service', 'PortalAuthService', 'NovoServico']
📖 Referências
DRF Serializers

Python Type Hints