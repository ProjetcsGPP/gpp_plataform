# Guia de Migração IAM - Passo a Passo

## Índice

1. [Visão Geral](#visão-geral)
2. [Fase 1: Setup Inicial](#fase-1-setup-inicial)
3. [Fase 2: Refatorar acoes_pngi](#fase-2-refatorar-acoes_pngi)
4. [Fase 3: Mover Modelos](#fase-3-mover-modelos)
5. [Fase 4: Microsserviço](#fase-4-microsserviço)
6. [Checklist de Validação](#checklist-de-validação)

## Visão Geral

Este guia detalha o processo de migração do sistema de autorização atual (acoplado) para a nova arquitetura IAM (desacoplada e orient ada a serviços).

**Duração estimada**: 4-6 semanas
**Risco**: Médio (alterações não quebram funcionalidades existentes)

## Fase 1: Setup Inicial

**Duração**: 1 dia
**Status**: ✅ Concluído

### 1.1. Adicionar ao INSTALLED_APPS

```python
# gpp_plataform/settings/base.py

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'corsheaders',
    
    # GPP apps
    'core.iam',  # <- ADICIONAR AQUI
    'accounts',
    'acoes_pngi',
    'carga_org_lot',
    'portal',
]
```

### 1.2. Configurar Cache (se ainda não configurado)

```python
# settings/base.py

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'gpp_iam',
        'TIMEOUT': 300,  # 5 minutos
    }
}

# Ou usar memória local para desenvolvimento
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'iam-cache',
    }
}
```

### 1.3. Configurar JWT

```python
# settings/base.py

# JWT Configuration
JWT_EXPIRATION_HOURS = 24  # Token expira em 24 horas
```

### 1.4. Testar Import

```bash
python manage.py shell
```

```python
>>> from core.iam.services import AuthorizationService
>>> from core.iam.interfaces.decorators import require_permission
>>> print("IAM module loaded successfully!")
```

## Fase 2: Refatorar acoes_pngi

**Duração**: 2-3 semanas
**Objetivo**: Substituir lógica de autorização por serviços IAM

### 2.1. Refatorar Permissions DRF

#### Antes (acoes_pngi/permissions.py)

```python
class IsGestorPNGI(BasePermission):
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method in self.SAFE_METHODS:
            try:
                app_acoes = Aplicacao.objects.filter(codigointerno='ACOES_PNGI').first()
                if not app_acoes:
                    return False
                
                has_any_role = UserRole.objects.filter(
                    user=request.user,
                    aplicacao=app_acoes
                ).exists()
                
                return has_any_role
            except Exception:
                return False
        
        # CREATE/UPDATE/DELETE: apenas GESTOR
        try:
            app_acoes = Aplicacao.objects.filter(codigointerno='ACOES_PNGI').first()
            if not app_acoes:
                return False
            
            allowed_roles = UserRole.objects.filter(
                user=request.user,
                aplicacao=app_acoes,
                role__codigoperfil='GESTOR_PNGI'
            ).exists()
            
            return allowed_roles
        except Exception:
            return False
```

#### Depois (acoes_pngi/permissions.py)

```python
from core.iam.interfaces.permissions import RequireRole

class IsGestorPNGI(RequireRole):
    """GESTOR pode escrever, todos podem ler"""
    app_code = 'ACOES_PNGI'
    required_roles_read = ['GESTOR_PNGI', 'COORDENADOR_PNGI', 'OPERADOR_ACAO', 'CONSULTOR_PNGI']
    required_roles_write = ['GESTOR_PNGI']
    
    def has_permission(self, request, view):
        # Inject app_code and required_roles into view
        view.app_code = self.app_code
        if request.method in self.SAFE_METHODS:
            view.required_roles = self.required_roles_read
        else:
            view.required_roles = self.required_roles_write
        return super().has_permission(request, view)

# Ou use diretamente RequireRole no ViewSet sem criar subclass
```

### 2.2. Atualizar ViewSets

#### Antes

```python
# acoes_pngi/views/api_views.py
from ..permissions import IsGestorPNGI, IsCoordernadorOrGestorPNGI

class SituacaoAcaoViewSet(ModelViewSet):
    permission_classes = [IsGestorPNGI]
    queryset = SituacaoAcao.objects.all()
    serializer_class = SituacaoAcaoSerializer

class EixoViewSet(ModelViewSet):
    permission_classes = [IsCoordernadorOrGestorPNGI]
    queryset = Eixo.objects.all()
    serializer_class = EixoSerializer
```

#### Depois

```python
# acoes_pngi/views/api_views.py
from core.iam.interfaces.permissions import RequireRole

class SituacaoAcaoViewSet(ModelViewSet):
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles_read = ['GESTOR_PNGI', 'COORDENADOR_PNGI', 'OPERADOR_ACAO', 'CONSULTOR_PNGI']
    required_roles_write = ['GESTOR_PNGI']  # Apenas gestor pode modificar
    queryset = SituacaoAcao.objects.all()
    serializer_class = SituacaoAcaoSerializer

class EixoViewSet(ModelViewSet):
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles_read = ['GESTOR_PNGI', 'COORDENADOR_PNGI', 'OPERADOR_ACAO', 'CONSULTOR_PNGI']
    required_roles_write = ['GESTOR_PNGI', 'COORDENADOR_PNGI']  # Gestor OU Coordenador
    queryset = Eixo.objects.all()
    serializer_class = EixoSerializer
```

### 2.3. Refatorar Web Views

#### Antes

```python
# acoes_pngi/views/web_views.py
from ..decorators import has_permission

@has_permission('add_eixo')
def create_eixo(request):
    if request.method == 'POST':
        form = EixoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('acoes:eixo_list')
    else:
        form = EixoForm()
    return render(request, 'eixo_form.html', {'form': form})
```

#### Depois

```python
# acoes_pngi/views/web_views.py
from core.iam.interfaces.decorators import require_permission

@require_permission('ACOES_PNGI', 'add_eixo')
def create_eixo(request):
    if request.method == 'POST':
        form = EixoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Eixo criado com sucesso!')
            return redirect('acoes:eixo_list')
    else:
        form = EixoForm()
    return render(request, 'eixo_form.html', {'form': form})
```

### 2.4. Remover Arquivos Redundantes

```bash
# Após verificar que tudo funciona

# Backup primeiro
cp acoes_pngi/decorators.py acoes_pngi/decorators.py.backup
cp acoes_pngi/permissions.py acoes_pngi/permissions.py.backup

# Se toda lógica foi migrada, deletar
rm acoes_pngi/decorators.py  # Se não tiver lógica customizada

# permissions.py pode manter apenas classes customizadas se houver
```

### 2.5. Testes de Regressão

```bash
# Executar todos os testes
python manage.py test acoes_pngi

# Testes específicos de permissões
python manage.py test acoes_pngi.tests.test_permissions
```

#### Criar Novos Testes

```python
# acoes_pngi/tests/test_iam_integration.py
from django.test import TestCase
from core.iam.services import AuthorizationService
from core.iam.models import User, UserRole, Aplicacao, Role

class AcoesPNGIIAMIntegrationTest(TestCase):
    """Testa integração com IAM services"""
    
    def setUp(self):
        # Setup app, roles e usuários
        self.app = Aplicacao.objects.get(codigointerno='ACOES_PNGI')
        self.gestor_role = Role.objects.get(
            aplicacao=self.app,
            codigoperfil='GESTOR_PNGI'
        )
        self.consultor_role = Role.objects.get(
            aplicacao=self.app,
            codigoperfil='CONSULTOR_PNGI'
        )
        
        self.gestor = User.objects.create_user(
            email='gestor@test.com',
            password='test123',
            name='Gestor Teste'
        )
        UserRole.objects.create(
            user=self.gestor,
            aplicacao=self.app,
            role=self.gestor_role
        )
        
        self.consultor = User.objects.create_user(
            email='consultor@test.com',
            password='test123',
            name='Consultor Teste'
        )
        UserRole.objects.create(
            user=self.consultor,
            aplicacao=self.app,
            role=self.consultor_role
        )
    
    def test_gestor_has_write_permissions(self):
        """Gestor deve ter permissões de escrita"""
        self.assertTrue(
            AuthorizationService.user_has_permission(
                self.gestor, 'ACOES_PNGI', 'add_eixo'
            )
        )
        self.assertTrue(
            AuthorizationService.user_has_permission(
                self.gestor, 'ACOES_PNGI', 'change_eixo'
            )
        )
    
    def test_consultor_has_only_read_permissions(self):
        """Consultor deve ter apenas leitura"""
        self.assertTrue(
            AuthorizationService.user_has_permission(
                self.consultor, 'ACOES_PNGI', 'view_eixo'
            )
        )
        self.assertFalse(
            AuthorizationService.user_has_permission(
                self.consultor, 'ACOES_PNGI', 'add_eixo'
            )
        )
```

### 2.6. Checklist de Substituição

- [ ] Substituir todas as ocorrências de `from accounts.models import UserRole`
- [ ] Substituir `UserRole.objects.filter(...)` por `AuthorizationService.user_has_role(...)`
- [ ] Substituir decorators customizados por `@require_permission` / `@require_role`
- [ ] Substituir classes `BasePermission` customizadas por `RequireRole` / `HasAppPermission`
- [ ] Remover imports de `RolePermission`, `Aplicacao` das views/permissions
- [ ] Atualizar testes para usar serviços IAM
- [ ] Executar suite completa de testes
- [ ] Testar manualmente todos os flows de autorização

## Fase 3: Mover Modelos

**Duração**: 1 semana
**Objetivo**: Migrar modelos de `accounts` para `core.iam`

### 3.1. Backup do Banco de Dados

```bash
pg_dump -h localhost -U postgres gpp_plataform > backup_antes_migracao.sql
```

### 3.2. Mover Código dos Modelos

```python
# core/iam/models.py
# Copiar TODOS os modelos de accounts/models.py

from django.db import models
from django.contrib.auth.models import BaseUserManager, Permission
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class Aplicacao(models.Model):
    # ... código existente ...
    class Meta:
        db_table = 'tblaplicacao'  # MANTÉM o mesmo nome
        managed = True

class User(AbstractBaseUser, PermissionsMixin):
    # ... código existente ...
    class Meta:
        db_table = 'tblusuario'  # MANTÉM o mesmo nome
        managed = True

# ... demais modelos ...
```

### 3.3. Atualizar Settings

```python
# settings/base.py

# Antes
AUTH_USER_MODEL = 'accounts.User'

# Depois
AUTH_USER_MODEL = 'iam.User'

INSTALLED_APPS = [
    ...,
    'core.iam',
    # 'accounts',  # Comentar ou remover
    'acoes_pngi',
    'carga_org_lot',
]
```

### 3.4. Criar Migrações

```bash
# Criar migração vazia para core.iam
python manage.py makemigrations core.iam --empty --name migrate_from_accounts
```

Editar a migração:

```python
# core/iam/migrations/0001_migrate_from_accounts.py
from django.db import migrations

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    
    operations = [
        # Apenas registra que os modelos existem
        # NÃO cria tabelas (já existem)
        migrations.RunSQL(
            sql="SELECT 1;",  # No-op
            reverse_sql="SELECT 1;"
        )
    ]
```

### 3.5. Executar Migrações

```bash
# Aplicar migração do core.iam
python manage.py migrate core.iam

# Marcar accounts como migrado (fake)
python manage.py migrate accounts --fake-zero
```

### 3.6. Atualizar Imports em Todo o Projeto

```bash
# Buscar todos os imports antigos
grep -r "from accounts.models import" .

# Substituir por
from core.iam.models import User, Role, UserRole, ...
```

### 3.7. Testar Migração

```python
python manage.py shell
```

```python
>>> from core.iam.models import User
>>> User.objects.count()
# Deve retornar contagem correta

>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> print(User._meta.app_label)  # Deve ser 'iam'
```

### 3.8. Remover App accounts

```bash
# Após confirmar que tudo funciona
mv accounts accounts.deprecated
```

## Fase 4: Microsserviço

**Duração**: 2-3 semanas
**Objetivo**: Preparar IAM para extração

### 4.1. Criar APIs REST Públicas

```python
# core/iam/views/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..services import TokenService, AuthorizationService
from ..serializers import TokenResponseSerializer

class TokenObtainAPIView(APIView):
    """POST /api/iam/token/"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        app_code = request.data.get('app_code')
        
        from django.contrib.auth import authenticate
        user = authenticate(email=email, password=password)
        
        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=401
            )
        
        token = TokenService.generate_token(user, app_code)
        
        return Response({
            'token': token,
            'token_type': 'Bearer',
            'expires_in': 86400,  # 24 hours
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name
            }
        })

class PermissionCheckAPIView(APIView):
    """POST /api/iam/check-permission/"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        app_code = request.data.get('app_code')
        permission = request.data.get('permission')
        
        allowed = AuthorizationService.user_has_permission(
            request.user, app_code, permission
        )
        
        return Response({'allowed': allowed})
```

### 4.2. Adicionar URLs

```python
# core/iam/urls.py
from django.urls import path
from .views.api_views import TokenObtainAPIView, PermissionCheckAPIView

app_name = 'iam'

urlpatterns = [
    path('api/token/', TokenObtainAPIView.as_view(), name='token_obtain'),
    path('api/check-permission/', PermissionCheckAPIView.as_view(), name='check_permission'),
]
```

### 4.3. Documentar API (OpenAPI)

```python
# core/iam/schema.py
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'email': {'type': 'string'},
                'password': {'type': 'string'},
                'app_code': {'type': 'string', 'nullable': True}
            },
            'required': ['email', 'password']
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'token': {'type': 'string'},
                'token_type': {'type': 'string'},
                'expires_in': {'type': 'integer'},
                'user': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'email': {'type': 'string'},
                        'name': {'type': 'string'}
                    }
                }
            }
        },
        401: {'description': 'Invalid credentials'}
    },
    examples=[
        OpenApiExample(
            'Login Example',
            value={
                'email': 'user@example.com',
                'password': 'secure_password',
                'app_code': 'ACOES_PNGI'
            }
        )
    ]
)
class TokenObtainAPIView(APIView):
    ...
```

## Checklist de Validação

### Fase 1
- [ ] `core.iam` adicionado ao `INSTALLED_APPS`
- [ ] Cache configurado
- [ ] JWT configurado
- [ ] Imports de serviços funcionando

### Fase 2
- [ ] Todas as permissions DRF migradas
- [ ] Todos os decorators web migrados
- [ ] Testes de regressão passando
- [ ] Testes de integração criados
- [ ] Arquivos redundantes removidos

### Fase 3
- [ ] Backup do banco realizado
- [ ] Modelos movidos para `core.iam`
- [ ] `AUTH_USER_MODEL` atualizado
- [ ] Migrações executadas
- [ ] Todos os imports atualizados
- [ ] `accounts` app removido
- [ ] Testes passando

### Fase 4
- [ ] APIs REST implementadas
- [ ] Documentação OpenAPI gerada
- [ ] Testes de API criados
- [ ] Monitoring implementado
- [ ] SLA documentado

## Rollback Plan

Caso algo dê errado:

### Rollback Fase 2
```bash
# Restaurar arquivos de backup
cp acoes_pngi/permissions.py.backup acoes_pngi/permissions.py
cp acoes_pngi/decorators.py.backup acoes_pngi/decorators.py

# Reverter commits
git revert HEAD~N
```

### Rollback Fase 3
```bash
# Restaurar banco
psql -U postgres gpp_plataform < backup_antes_migracao.sql

# Reverter settings
# AUTH_USER_MODEL = 'accounts.User'

# Reverter INSTALLED_APPS
# 'accounts',
# # 'core.iam',
```

## Suporte

Para dúvidas ou problemas:
1. Consultar este guia
2. Verificar README.md do core.iam
3. Consultar troubleshooting no README
4. Abrir issue no repositório
