# Core IAM (Identity and Access Management)

## Visão Geral

Módulo centralizado de autenticação e autorização para a Plataforma GPP. Projetado como uma arquitetura orientada a serviços que pode ser eventualmente extraída como um microsserviço independente.

## Arquitetura

```
core/iam/
├── models.py              # Modelos IAM (Fase 1: importa de accounts)
├── services/             # Camada de serviços
│   ├── token_service.py           # Geração/validação JWT
│   ├── authorization_service.py   # Verificação de permissões
│   ├── role_resolver.py          # Gerenciamento de roles
│   └── permission_repository.py  # Queries com cache
├── interfaces/           # Interface pública
│   ├── decorators.py     # Decorators para views web
│   ├── permissions.py    # Classes DRF BasePermission
│   └── middleware.py     # Middleware de contexto
├── serializers.py        # Serializers DRF
└── README.md             # Este arquivo
```

### Princípios Arquiteturais

1. **Serviços Centralizados**: Toda lógica de autorização passa pelos serviços IAM
2. **Desacoplamento**: Aplicações de domínio NÃO importam modelos IAM diretamente
3. **Interface Única**: Web e API usam a mesma lógica de autorização
4. **Preparação para Microsserviço**: Estrutura pronta para extração futura

## Uso Rápido

### Em Views Web

```python
from core.iam.interfaces.decorators import require_permission, require_role

@require_permission('ACOES_PNGI', 'add_eixo')
def criar_eixo(request):
    # Apenas usuários com permissão 'add_eixo' podem acessar
    return render(request, 'eixo_form.html')

@require_role('ACOES_PNGI', 'GESTOR_PNGI', 'COORDENADOR_PNGI')
def gestao_view(request):
    # Apenas gestores e coordenadores
    return render(request, 'gestao.html')
```

### Em ViewSets DRF

```python
from rest_framework.viewsets import ModelViewSet
from core.iam.interfaces.permissions import HasAppPermission, RequireRole

# Permissões baseadas no modelo Django
class EixoViewSet(ModelViewSet):
    permission_classes = [HasAppPermission]
    app_code = 'ACOES_PNGI'
    queryset = Eixo.objects.all()
    serializer_class = EixoSerializer
    # Automaticamente verifica:
    # GET → 'view_eixo'
    # POST → 'add_eixo'
    # PUT/PATCH → 'change_eixo'
    # DELETE → 'delete_eixo'

# Permissões baseadas em roles
class ConfigViewSet(ModelViewSet):
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles = ['GESTOR_PNGI', 'COORDENADOR_PNGI']
    queryset = SituacaoAcao.objects.all()
    serializer_class = SituacaoAcaoSerializer

# Permissões diferentes para leitura e escrita
class AcaoViewSet(ModelViewSet):
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles_read = ['GESTOR_PNGI', 'COORDENADOR_PNGI', 'OPERADOR_ACAO', 'CONSULTOR_PNGI']
    required_roles_write = ['GESTOR_PNGI', 'COORDENADOR_PNGI', 'OPERADOR_ACAO']
    queryset = Acoes.objects.all()
    serializer_class = AcoesSerializer
```

### Verificando Permissões Programaticamente

```python
from core.iam.services import AuthorizationService

# Verificar permissão específica
if AuthorizationService.user_has_permission(user, 'ACOES_PNGI', 'add_eixo'):
    # Permitir ação
    eixo.save()

# Verificar role
if AuthorizationService.user_has_role(user, 'ACOES_PNGI', 'GESTOR_PNGI'):
    # Lógica específica para gestores
    pass

# Verificar qualquer uma das roles
if AuthorizationService.user_has_any_role(
    user, 'ACOES_PNGI', ['GESTOR_PNGI', 'COORDENADOR_PNGI']
):
    # Gestores OU coordenadores
    pass
```

### Gerando Tokens JWT

```python
from core.iam.services import TokenService

def login_api(request):
    user = authenticate(email=email, password=password)
    if user:
        # Gerar token para aplicação específica
        token = TokenService.generate_token(user, 'ACOES_PNGI')
        
        # Ou para todas as aplicações
        token = TokenService.generate_token(user)
        
        return Response({
            'token': token,
            'user': UserSerializer(user).data
        })
```

## Matriz de Permissões ACOES_PNGI

| Entidade/Ação | GESTOR | COORDENADOR | OPERADOR | CONSULTOR |
|-------------------|--------|-------------|----------|----------|
| **CONFIGURAÇÕES NÍVEL 1** | | | | |
| SituacaoAcao (R) | Sim | Sim | Sim | Sim |
| SituacaoAcao (W/D) | Sim | Não | Não | Não |
| TipoEntraveAlerta (R) | Sim | Sim | Sim | Sim |
| TipoEntraveAlerta (W/D) | Sim | Não | Não | Não |
| **CONFIGURAÇÕES NÍVEL 2** | | | | |
| Eixo (R) | Sim | Sim | Sim | Sim |
| Eixo (W/D) | Sim | Sim | Não | Não |
| VigenciaPNGI (R) | Sim | Sim | Sim | Sim |
| VigenciaPNGI (W/D) | Sim | Sim | Não | Não |
| **OPERAÇÕES** | | | | |
| Acoes (R) | Sim | Sim | Sim | Sim |
| Acoes (W/D) | Sim | Sim | Sim | Não |
| **GESTÃO USUÁRIOS** | | | | |
| Usuários/Roles (R) | Sim | Sim | Sim | Sim |
| Usuários/Roles (W/D) | Sim | Não | Não | Não |

**Legenda:**
- R = Read (GET, HEAD, OPTIONS)
- W = Write (POST, PUT, PATCH)
- D = Delete (DELETE)

## Migração em 4 Fases

### Fase 1: Criar core/iam (ATUAL)

**Status**: ✅ Concluído

- [x] Criar estrutura de diretórios
- [x] Implementar serviços (TokenService, AuthorizationService, etc.)
- [x] Criar interfaces (decorators, permissions)
- [x] Modelos ainda em `accounts` (importados via `core.iam.models`)

**Como testar**:
```python
# Em qualquer view ou teste
from core.iam.services import AuthorizationService

# Usar serviços mesmo com modelos em accounts
has_perm = AuthorizationService.user_has_permission(
    user, 'ACOES_PNGI', 'add_eixo'
)
```

### Fase 2: Refatorar Aplicações de Domínio

**Objetivo**: Remover imports diretos de modelos IAM

**Antes** (❌):
```python
# acoes_pngi/permissions.py
from accounts.models import UserRole, RolePermission, Aplicacao

class IsGestorPNGI(BasePermission):
    def has_permission(self, request, view):
        app = Aplicacao.objects.get(codigointerno='ACOES_PNGI')
        return UserRole.objects.filter(
            user=request.user,
            aplicacao=app,
            role__codigoperfil='GESTOR_PNGI'
        ).exists()
```

**Depois** (✅):
```python
# acoes_pngi/permissions.py
from core.iam.interfaces.permissions import RequireRole

class IsGestorPNGI(RequireRole):
    # Ou simplesmente use RequireRole diretamente no ViewSet:
    # permission_classes = [RequireRole]
    # required_roles = ['GESTOR_PNGI']
    pass
```

**Checklist por aplicação**:
- [ ] `acoes_pngi/permissions.py` - substituir por `core.iam.interfaces.permissions`
- [ ] `acoes_pngi/views/` - usar decorators de `core.iam.interfaces.decorators`
- [ ] `acoes_pngi/decorators.py` - remover se redundante
- [ ] `carga_org_lot/` - mesmas substituições

### Fase 3: Mover Modelos para core/iam

**Objetivo**: Migrar modelos de `accounts` para `core.iam`

**Passos**:

1. **Criar migrações vazias** para preservar dados:
```bash
python manage.py makemigrations core.iam --empty
```

2. **Atualizar `settings.py`**:
```python
# Antes
AUTH_USER_MODEL = 'accounts.User'

# Depois
AUTH_USER_MODEL = 'iam.User'

INSTALLED_APPS = [
    ...,
    'core.iam',  # Adicionar
    # 'accounts',  # Deprecar
]
```

3. **Mover código dos modelos**:
- Copiar de `accounts/models.py` para `core/iam/models.py`
- Schema `public` permanece igual (sem mudança no banco)
- Apenas metadados Django são atualizados

4. **Atualizar imports**:
```python
# core/iam/models.py
# Não importa mais de accounts, define diretamente
class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'tblusuario'  # Mesmo nome de tabela
        managed = True
```

5. **Executar migrações**:
```bash
python manage.py migrate core.iam
python manage.py migrate accounts --fake-zero  # Marca como migrado
```

### Fase 4: Preparar Extração como Microsserviço

**Objetivo**: Estrutura pronta para serviço independente

**Implementar**:

1. **API REST pública do IAM**:
```python
# core/iam/views/api_views.py
class TokenObtainView(APIView):
    """Endpoint público para obter token"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        user = authenticate(...)
        token = TokenService.generate_token(user)
        return Response({'token': token})

class PermissionCheckView(APIView):
    """Endpoint para verificar permissões"""
    def post(self, request):
        has_perm = AuthorizationService.user_has_permission(
            request.user,
            request.data['app_code'],
            request.data['permission']
        )
        return Response({'allowed': has_perm})
```

2. **Documentar Contratos**:
- OpenAPI/Swagger para todas as APIs
- SLA e garantias de desempenho
- Versionamento de API

3. **Implementar API Gateway**:
- Nginx ou Kong como gateway
- Autenticação via cabeçalho `Authorization: Bearer <token>`
- Rate limiting por usuário/app

## Guia de Refatoração

### Substituindo Decorators Antigos

**Antes**:
```python
# acoes_pngi/decorators.py
from accounts.models import UserRole, RolePermission

def has_permission(permission_codename):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Lógica complexa duplicada
            role_permissions = RolePermission.objects.filter(...)
            ...
        return wrapper
    return decorator
```

**Depois**:
```python
# Use diretamente de core.iam
from core.iam.interfaces.decorators import require_permission

# Não precisa criar decorator customizado
# Use o fornecido pelo IAM
```

### Substituindo Permissions DRF Antigas

**Antes**:
```python
# acoes_pngi/permissions.py
class IsCoordernadorOrGestorPNGI(BasePermission):
    def has_permission(self, request, view):
        app_acoes = Aplicacao.objects.filter(codigointerno='ACOES_PNGI').first()
        return UserRole.objects.filter(
            user=request.user,
            aplicacao=app_acoes,
            role__codigoperfil__in=['COORDENADOR_PNGI', 'GESTOR_PNGI']
        ).exists()
```

**Depois**:
```python
# Use RequireRole do core.iam
from core.iam.interfaces.permissions import RequireRole

# No ViewSet:
class EixoViewSet(ModelViewSet):
    permission_classes = [RequireRole]
    required_roles = ['COORDENADOR_PNGI', 'GESTOR_PNGI']
```

### Matriz de Substituição

| Padrão Antigo | Substituto IAM | Exemplo |
|---------------|----------------|----------|
| `from accounts.models import UserRole` | `from core.iam.services import AuthorizationService` | `AuthorizationService.user_has_role(...)` |
| `UserRole.objects.filter(...)` | `AuthorizationService.user_has_any_role(...)` | Ver seção Uso Rápido |
| `RolePermission.objects.filter(...)` | `AuthorizationService.user_has_permission(...)` | Ver seção Uso Rápido |
| `@has_permission('add_eixo')` | `@require_permission('ACOES_PNGI', 'add_eixo')` | Ver Decorators |
| Custom `BasePermission` | `RequireRole` ou `HasAppPermission` | Ver Permissions DRF |

## Testes

### Testando Serviços

```python
# tests/test_iam_services.py
from django.test import TestCase
from core.iam.services import AuthorizationService
from core.iam.models import User, UserRole, Aplicacao, Role

class AuthorizationServiceTest(TestCase):
    def setUp(self):
        self.app = Aplicacao.objects.create(
            codigointerno='ACOES_PNGI',
            nomeaplicacao='Ações PNGI'
        )
        self.role = Role.objects.create(
            aplicacao=self.app,
            codigoperfil='GESTOR_PNGI',
            nomeperfil='Gestor'
        )
        self.user = User.objects.create_user(
            email='gestor@test.com',
            password='test123'
        )
        UserRole.objects.create(
            user=self.user,
            aplicacao=self.app,
            role=self.role
        )
    
    def test_user_has_role(self):
        has_role = AuthorizationService.user_has_role(
            self.user, 'ACOES_PNGI', 'GESTOR_PNGI'
        )
        self.assertTrue(has_role)
    
    def test_user_does_not_have_role(self):
        has_role = AuthorizationService.user_has_role(
            self.user, 'ACOES_PNGI', 'COORDENADOR_PNGI'
        )
        self.assertFalse(has_role)
```

### Testando Permissions DRF

```python
# tests/test_iam_permissions.py
from rest_framework.test import APITestCase
from rest_framework import status

class EixoPermissionTest(APITestCase):
    def setUp(self):
        # Setup users with different roles
        self.gestor = self.create_user_with_role('GESTOR_PNGI')
        self.consultor = self.create_user_with_role('CONSULTOR_PNGI')
    
    def test_gestor_can_create_eixo(self):
        self.client.force_authenticate(user=self.gestor)
        response = self.client.post('/api/eixos/', {...})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_consultor_cannot_create_eixo(self):
        self.client.force_authenticate(user=self.consultor)
        response = self.client.post('/api/eixos/', {...})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
```

## Troubleshooting

### Problema: ImportError ao importar de core.iam

**Solução**: Adicionar `core.iam` ao `INSTALLED_APPS`:
```python
# settings.py
INSTALLED_APPS = [
    ...,
    'core.iam',
]
```

### Problema: Permissões não funcionam após mudanças

**Solução**: Invalidar cache:
```python
from core.iam.services import PermissionRepository

# Invalidar cache do usuário
PermissionRepository.invalidate_user_cache(user.id, 'ACOES_PNGI')

# Ou invalidar cache de toda uma role
PermissionRepository.invalidate_role_cache(role.id)
```

### Problema: Token JWT expirado

**Solução**: Implementar refresh token:
```python
from core.iam.services import TokenService

new_token = TokenService.refresh_token(old_token)
if new_token:
    return Response({'token': new_token})
else:
    return Response({'error': 'Invalid token'}, status=401)
```

## Próximos Passos

1. [ ] Concluir Fase 2: Refatorar `acoes_pngi` para usar serviços IAM
2. [ ] Concluir Fase 2: Refatorar `carga_org_lot` para usar serviços IAM
3. [ ] Implementar testes unitários para todos os serviços
4. [ ] Implementar testes de integração para flows completos
5. [ ] Documentar APIs REST do IAM (OpenAPI/Swagger)
6. [ ] Implementar monitoring e logging estruturado
7. [ ] Iniciar Fase 3: Mover modelos para core.iam

## Referências

- Django Authentication: https://docs.djangoproject.com/en/4.2/topics/auth/
- DRF Permissions: https://www.django-rest-framework.org/api-guide/permissions/
- JWT Best Practices: https://tools.ietf.org/html/rfc8725
- Microservices Patterns: https://microservices.io/patterns/
