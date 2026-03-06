Accounts - Base do sistema de autenticação multi-tenant da GPP Plataform

text

## 3. common/README.md

```markdown
# Common - Componentes Compartilhados

Aplicação que centraliza utilitários, serializers, serviços e componentes reutilizáveis entre todas as aplicações da GPP Plataform.

## 📋 Visão Geral

A aplicação `common` fornece:

- **Serializers Genéricos**: Classes base para serialização consistente
- **Serviços de Autenticação**: PortalAuthService para integração entre apps
- **Middlewares**: Contexto de aplicação e utilitários
- **Base Classes**: Mixins e classes abstratas reutilizáveis

## 🏗️ Estrutura

common/
├── serializers/
│ ├── init.py
│ ├── base_serializers.py # BaseModelSerializer, TimestampedModelSerializer
│ ├── user_serializers.py # Serializers de User genéricos
│ └── auth_serializers.py # Serializers de autenticação
├── services/
│ ├── init.py
│ └── portal_auth.py # PortalAuthService
├── middleware/
│ ├── init.py
│ └── app_context.py # AppContextMiddleware
├── utils/
│ └── init.py
└── README.md

text

## 🔧 Serializers

### BaseModelSerializer

Serializer base com comportamentos comuns para todos os modelos.

**Recursos**:
- Remoção automática de campos `None` (opcional)
- Validações customizáveis
- Formatação consistente

**Exemplo de uso**:
```python
from common.serializers import BaseModelSerializer

class MeuModelSerializer(BaseModelSerializer):
    class Meta:
        model = MeuModel
        fields = '__all__'
        remove_null_fields = True  # Remove campos None da resposta
TimestampedModelSerializer
Serializer para modelos com campos de timestamp (created_at, updated_at).

Recursos:

Formatação automática de datas: '%Y-%m-%d %H:%M:%S'

Campos read-only por padrão

Herda de BaseModelSerializer

Exemplo de uso:

python
from common.serializers import TimestampedModelSerializer

class EixoSerializer(TimestampedModelSerializer):
    class Meta:
        model = Eixo
        fields = [
            'ideixo',
            'strdescricaoeixo',
            'stralias',
            'created_at',    # Automaticamente formatado
            'updated_at'     # Automaticamente formatado
        ]
        read_only_fields = ['ideixo', 'created_at', 'updated_at']
UserSerializer
Serializer completo para o modelo User com roles e atributos.

Recursos:

Retorna roles do usuário para a aplicação do contexto

Retorna atributos customizados da aplicação

Filtragem automática por APP_CODE

Exemplo de uso:

python
from common.serializers import UserSerializer

# Na view
serializer = UserSerializer(
    user,
    context={
        'app_code': 'ACOES_PNGI',  # Filtra roles/atributos por app
        'request': request
    }
)

# Resposta incluirá:
# - Dados básicos do usuário
# - roles: lista de roles para ACOES_PNGI
# - attributes: dict de atributos para ACOES_PNGI
UserListSerializer
Versão otimizada para listagem de usuários (sem roles/atributos).

python
from common.serializers import UserListSerializer

users = User.objects.filter(is_active=True)
serializer = UserListSerializer(users, many=True)
UserCreateSerializer
Serializer para criação/sincronização de usuários via portal.

Exemplo de uso:

python
from common.serializers import UserCreateSerializer

serializer = UserCreateSerializer(
    data={
        'email': 'novo@example.com',
        'name': 'Novo Usuário',
        'roles': ['GESTOR_PNGI'],
        'attributes': {'can_upload': 'true'}
    },
    context={'app_code': 'ACOES_PNGI'}
)

if serializer.is_valid():
    user = serializer.save()  # Cria/atualiza usuário com roles e atributos
    created = serializer.validated_data['_created']
UserUpdateSerializer
Serializer para atualização parcial de usuários.

python
from common.serializers import UserUpdateSerializer

serializer = UserUpdateSerializer(
    user,
    data={'is_active': False},
    partial=True
)

if serializer.is_valid():
    serializer.save()
