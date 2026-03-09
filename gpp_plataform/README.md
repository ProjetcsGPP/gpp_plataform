GPP Plataform - Modernizando a Gestão Pública do Espírito Santo 🚀

text

## 2. accounts/README.md

```markdown
# Accounts - Gestão de Usuários e Autenticação

Aplicação responsável pelo gerenciamento centralizado de usuários, autenticação e autorização multi-tenant da GPP Plataform.

## 📋 Visão Geral

A aplicação `accounts` fornece:

- **Modelo de Usuário Customizado**: Baseado em `AbstractBaseUser`
- **Autenticação Multi-tenant**: Usuários com acesso a múltiplas aplicações
- **Sistema de Roles**: Perfis de acesso por aplicação
- **Atributos Dinâmicos**: Configurações customizadas por usuário/aplicação

## 🏗️ Estrutura

accounts/
├── models.py # User, Aplicacao, Role, UserRole, Attribute
├── admin.py # Interface administrativa
├── managers.py # UserManager customizado
├── backends.py # Backend de autenticação customizado
└── migrations/ # Migrações do banco

text

## 📊 Modelos

### User

Modelo customizado de usuário que estende `AbstractBaseUser`.

**Campos principais**:
```python
idusuario              # PK (BigAutoField)
stremail               # Email (único, usado para login)
strnome                # Nome completo
strsenha               # Senha (hash)
idtipousuario          # Tipo de usuário (1: comum, 2: admin)
idstatususuario        # Status (1: ativo, 2: inativo, 3: bloqueado)
idclassificacaousuario # Classificação
is_active              # Usuário ativo
is_staff               # Acesso ao admin
is_superuser           # Superusuário
datacriacao            # Data de criação
data_alteracao         # Data de última alteração
last_login             # Último login
Exemplo de uso:

python
from accounts.models import User

# Criar usuário
user = User.objects.create_user(
    email='usuario@example.com',
    name='João Silva',
    password='senha_segura'
)

# Buscar usuário
user = User.objects.get(stremail='usuario@example.com')

# Autenticar
from django.contrib.auth import authenticate
user = authenticate(username='usuario@example.com', password='senha')
Aplicacao
Representa uma aplicação registrada na plataforma.

Campos:

python
idaplicacao       # PK
codigointerno     # Código único (ex: 'PORTAL', 'ACOES_PNGI')
nomeaplicacao     # Nome para exibição
baseurl           # URL base da aplicação
isshowinportal    # Se deve aparecer no portal
Aplicações cadastradas:

PORTAL - Portal GPP

CARGA_ORG_LOT - Carga Única de Organograma e Lotação

ACOES_PNGI - Gestão de Ações PNGI

Role
Perfis de acesso vinculados a aplicações.

Campos:

python
id             # PK
nomeperfil     # Nome descritivo (ex: 'Usuário do Portal')
codigoperfil   # Código único (ex: 'USER_PORTAL')
aplicacao      # FK para Aplicacao
Exemplo:

python
from accounts.models import Role, Aplicacao

app = Aplicacao.objects.get(codigointerno='PORTAL')
role = Role.objects.create(
    nomeperfil='Administrador Portal',
    codigoperfil='ADMIN_PORTAL',
    aplicacao=app
)
UserRole
Relacionamento muitos-para-muitos entre User, Role e Aplicacao.

Campos:

python
id          # PK
user        # FK para User
role        # FK para Role
aplicacao   # FK para Aplicacao
Exemplo:

python
from accounts.models import UserRole

# Atribuir role a usuário
UserRole.objects.create(
    user=user,
    role=role,
    aplicacao=app
)

# Verificar se usuário tem acesso
has_access = UserRole.objects.filter(
    user=user,
    aplicacao__codigointerno='PORTAL'
).exists()
Attribute
Atributos customizados por usuário e aplicação.

Campos:

python
id          # PK
user        # FK para User
aplicacao   # FK para Aplicacao
key         # Chave do atributo (ex: 'can_upload')
value       # Valor do atributo (string)
Exemplo:

python
from accounts.models import Attribute

# Definir atributo
Attribute.objects.create(
    user=user,
    aplicacao=app,
    key='can_upload',
    value='true'
)

# Buscar atributos
attrs = Attribute.objects.filter(
    user=user,
    aplicacao__codigointerno='CARGA_ORG_LOT'
)
attributes_dict = {a.key: a.value for a in attrs}
🔐 Autenticação
Backend Customizado
A aplicação usa um backend customizado que permite login com email:

python
# accounts/backends.py
class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        # Autentica usando email ao invés de username
        ...
Configuração no settings.py
python
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'accounts.User'
🎯 Casos de Uso
1. Criar Usuário com Permissões
python
from django.db import transaction
from accounts.models import User, Aplicacao, Role, UserRole

with transaction.atomic():
    # Criar usuário
    user = User.objects.create_user(
        email='gestor@example.com',
        name='Maria Gestora',
        password='senha123'
    )

    # Buscar aplicação e role
    app = Aplicacao.objects.get(codigointerno='ACOES_PNGI')
    role = Role.objects.get(
        codigoperfil='GESTOR_PNGI',
        aplicacao=app
    )

    # Atribuir role
    UserRole.objects.create(
        user=user,
        role=role,
        aplicacao=app
    )
2. Verificar Permissões na View
python
from django.shortcuts import redirect
from django.contrib import messages
from accounts.models import UserRole

def minha_view(request):
    # Verifica se usuário tem acesso
    has_access = UserRole.objects.filter(
        user=request.user,
        aplicacao__codigointerno='ACOES_PNGI'
    ).exists()

    if not has_access:
        messages.error(request, 'Acesso negado')
        return redirect('portal:home')

    # Continua com a lógica...
3. Buscar Atributos do Usuário
python
from accounts.models import Attribute

def get_user_permissions(user, app_code):
    """Retorna atributos de permissão do usuário"""
    attrs = Attribute.objects.filter(
        user=user,
        aplicacao__codigointerno=app_code
    ).values_list('key', 'value')

    return dict(attrs)

# Uso
permissions = get_user_permissions(request.user, 'CARGA_ORG_LOT')
can_upload = permissions.get('can_upload') == 'true'
🛠️ Admin
A interface administrativa está configurada para gerenciar:

Usuários (com filtros por status, tipo, aplicações)

Aplicações

Roles

Relacionamentos UserRole

Atributos

Acesse: http://localhost:8000/admin/

📝 Migrations
Criar nova migration
bash
python manage.py makemigrations accounts
Aplicar migrations
bash
python manage.py migrate accounts
🧪 Testes
bash
# Testar aplicação accounts
python manage.py test accounts

# Testar apenas autenticação
python manage.py test accounts.tests.test_authentication
🔒 Segurança
Senhas: Hashadas com PBKDF2-SHA256

Login: Email + senha (case-insensitive no email)

Sessões: Expiração configurável

Tokens: Suporte a JWT e tokens de sessão

📚 Relacionamento com Outras Apps
text
accounts
  ├── Usado por: portal (autenticação)
  ├── Usado por: acoes_pngi (verificação de permissões)
  ├── Usado por: carga_org_lot (verificação de permissões)
  └── Usa: common (serializers genéricos)
🔄 Fluxo de Autenticação Multi-tenant
text
1. Usuário faz login no Portal
   ↓
2. Sistema valida credenciais (User)
   ↓
3. Portal lista aplicações disponíveis
   ↓
4. Usuário clica em uma aplicação
   ↓
5. Sistema verifica UserRole para aquela aplicação
   ↓
6. Se autorizado, redireciona para a aplicação
   ↓
7. Aplicação verifica novamente as permissões
   ↓
8. Carrega atributos específicos (Attribute)
📖 Referências
Django Custom User Model

Django Authentication Backends
