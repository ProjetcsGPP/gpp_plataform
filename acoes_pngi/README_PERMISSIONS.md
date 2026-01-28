# Sistema de Permissões - Ações PNGI

## 📑 Visão Geral

O Ações PNGI utiliza um sistema completo de **Role-Based Access Control (RBAC)** integrado com o sistema nativo de permissões do Django.

### Arquitetura

```
User (accounts.User)
  │
  ├── UserRole (liga User → Aplicação + Role)
  │     │
  │     └── Role (ex: GESTOR_PNGI)
  │           │
  │           └── RolePermission (liga Role → Permission)
  │                 │
  │                 └── Permission (Django nativa: add_eixo, change_eixo, etc)
  │
  └── Métodos customizados:
        ├── get_app_permissions(app_code)
        └── has_app_perm(app_code, perm_code)
```

---

## 🎯 Roles Disponíveis

| Role | Código | Permissões | Descrição |
|------|--------|-------------|-------------|
| **Gestor PNGI** | `GESTOR_PNGI` | add, change, delete, view (todos os modelos) | Acesso total ao sistema |
| **Coordenador PNGI** | `COORDENADOR_PNGI` | add, change, view (sem delete) | Gerencia configurações, mas não deleta |
| **Operador de Ação** | `OPERADOR_ACAO` | view (apenas leitura de config) | Futuro: gerencia ações específicas |
| **Consultor PNGI** | `CONSULTOR_PNGI` | view (apenas leitura) | Acesso read-only ao sistema |

### Permissões por Modelo

#### Eixo
- `add_eixo` - Criar eixos
- `change_eixo` - Editar eixos
- `delete_eixo` - Deletar eixos
- `view_eixo` - Visualizar eixos

#### SituacaoAcao
- `add_situacaoacao`
- `change_situacaoacao`
- `delete_situacaoacao`
- `view_situacaoacao`

#### VigenciaPNGI
- `add_vigenciapngi`
- `change_vigenciapngi`
- `delete_vigenciapngi`
- `view_vigenciapngi`

---

## 🛠️ Setup Inicial

### 1. Criar Roles e Permissões

```bash
python manage.py setup_acoes_roles
```

Este comando:
- Cria 4 roles (GESTOR_PNGI, COORDENADOR_PNGI, OPERADOR_ACAO, CONSULTOR_PNGI)
- Associa permissões Django nativas a cada role
- É idemponente (pode ser executado múltiplas vezes)

### 2. Atribuir Role a um Usuário

```python
from accounts.models import User, UserRole, Role, Aplicacao

# Buscar usuário, role e aplicação
user = User.objects.get(stremail='usuario@exemplo.com')
role = Role.objects.get(strcodigorole='GESTOR_PNGI')
app = Aplicacao.objects.get(codigointerno='ACOES_PNGI')

# Criar UserRole
UserRole.objects.create(
    user=user,
    role=role,
    aplicacao=app
)
```

---

## 💻 Uso no Código

### Views Django (Templates)

#### Decorators

```python
from django.contrib.auth.decorators import login_required
from acoes_pngi.views.web_views import require_acoes_access, require_acoes_permission

# Verificar apenas acesso à aplicação
@login_required
@require_acoes_access
def dashboard(request):
    return render(request, 'dashboard.html')

# Verificar permissão específica
@login_required
@require_acoes_access
@require_acoes_permission('add_eixo')
def criar_eixo(request):
    # Apenas usuários com permissão add_eixo podem acessar
    return render(request, 'eixos/form.html')
```

#### Métodos do User

```python
# Verificar permissão específica
if request.user.has_app_perm('ACOES_PNGI', 'add_eixo'):
    # Usuário pode criar eixos
    pass

# Obter todas as permissões do usuário
permissions = request.user.get_app_permissions('ACOES_PNGI')
# Retorna: ['add_eixo', 'change_eixo', 'delete_eixo', ...]
```

### Templates Django

O context processor `acoes_permissions` disponibiliza variáveis em todos os templates:

```html
<!-- Verificar acesso geral -->
{% if has_acoes_access %}
    <p>Bem-vindo ao Ações PNGI</p>
    <p>Sua role: {{ acoes_role_display }}</p>
{% endif %}

<!-- Verificar permissões específicas -->
{% if can_add_eixo %}
    <a href="{% url 'acoes_pngi_web:eixo_create' %}" class="btn btn-primary">
        Novo Eixo
    </a>
{% endif %}

{% if can_change_eixo %}
    <a href="{% url 'acoes_pngi_web:eixo_update' eixo.pk %}" class="btn btn-warning">
        Editar
    </a>
{% endif %}

{% if can_delete_eixo %}
    <a href="{% url 'acoes_pngi_web:eixo_delete' eixo.pk %}" class="btn btn-danger">
        Deletar
    </a>
{% endif %}

<!-- Grupos de permissões -->
{% if can_manage_config %}
    <div class="admin-panel">
        <!-- Painél de configuração -->
    </div>
{% endif %}
```

### APIs REST (DRF)

#### Permission Classes

```python
from rest_framework import viewsets
from acoes_pngi.permissions import HasAcoesPermission, IsGestorPNGI

class EixoViewSet(viewsets.ModelViewSet):
    queryset = Eixo.objects.all()
    serializer_class = EixoSerializer
    
    # Verifica automaticamente por HTTP method
    # GET = view_eixo, POST = add_eixo, etc
    permission_classes = [HasAcoesPermission]
    
    # Ou restringir apenas para gestores
    # permission_classes = [IsGestorPNGI]
```

#### Endpoint de Permissões

```bash
# Obter permissões do usuário autenticado
GET /api/v1/acoes_pngi/permissions/
Authorization: Bearer <token>
```

**Resposta:**
```json
{
  "email": "usuario@exemplo.com",
  "name": "Nome do Usuário",
  "role": "GESTOR_PNGI",
  "is_superuser": false,
  "permissions": [
    "add_eixo",
    "change_eixo",
    "delete_eixo",
    "view_eixo",
    "add_situacaoacao",
    "change_situacaoacao",
    "delete_situacaoacao",
    "view_situacaoacao",
    "add_vigenciapngi",
    "change_vigenciapngi",
    "delete_vigenciapngi",
    "view_vigenciapngi"
  ],
  "groups": {
    "can_manage_config": true,
    "can_manage_acoes": false,
    "can_delete": true
  },
  "specific": {
    "eixo": {
      "add": true,
      "change": true,
      "delete": true,
      "view": true
    },
    "situacaoacao": {
      "add": true,
      "change": true,
      "delete": true,
      "view": true
    },
    "vigenciapngi": {
      "add": true,
      "change": true,
      "delete": true,
      "view": true
    }
  }
}
```

---

## 🧪 Testes

### Testes PowerShell

```powershell
# Teste completo de permissões e CRUD
.\TestesPowerShell\Acoes_PNGI_test_permissions_API.ps1

# Debug manual
.\TestesPowerShell\Debug-AcoesAPI.ps1 -Token "<seu_token>"
```

### Testes Python (TODO)

```bash
python manage.py test acoes_pngi.tests.test_permissions
```

---

## 📝 Context Processor

O `acoes_permissions` já está configurado em `settings.py`:

```python
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            # ...
            'acoes_pngi.context_processors.acoes_permissions',
        ],
    },
}]
```

### Variáveis Disponíveis

```python
# Acesso geral
has_acoes_access: bool
acoes_role: str  # Código da role (ex: 'GESTOR_PNGI')
acoes_role_display: str  # Nome da role (ex: 'Gestor PNGI')

# Permissões de Eixos
can_add_eixo: bool
can_change_eixo: bool
can_delete_eixo: bool
can_view_eixo: bool

# Permissões de Situações
can_add_situacao: bool
can_change_situacao: bool
can_delete_situacao: bool
can_view_situacao: bool

# Permissões de Vigências
can_add_vigencia: bool
can_change_vigencia: bool
can_delete_vigencia: bool
can_view_vigencia: bool

# Grupos de permissões
can_manage_config: bool  # Pode gerenciar configurações
can_manage_acoes: bool   # Pode gerenciar ações (futuro)
can_delete_any: bool     # Tem alguma permissão de delete
```

---

## 🔐 Segurança

### Boas Práticas

1. **Sempre use decorators em views**
   ```python
   @login_required
   @require_acoes_access
   @require_acoes_permission('add_eixo')
   def criar_eixo(request):
       ...
   ```

2. **Verifique permissões nos templates**
   ```html
   {% if can_delete_eixo %}
       <!-- Botão de deletar -->
   {% endif %}
   ```

3. **Use permission_classes em ViewSets**
   ```python
   class EixoViewSet(viewsets.ModelViewSet):
       permission_classes = [HasAcoesPermission]
   ```

4. **Não confie apenas no frontend**
   - Backend SEMPRE valida permissões
   - Frontend usa permissões apenas para UX (esconder botões)

---

## 🚀 Próximos Passos

- [ ] Implementar views web para Situações
- [ ] Implementar views web para Vigências
- [ ] Criar testes automatizados Python
- [ ] Adicionar permissões para modelo de Ações (quando criado)
- [ ] Integrar com Next.js (hook `useAcoesPermissions`)
- [ ] Admin Django customizado com permissões

---

## 📚 Referências

- [Documentação Django Permissions](https://docs.djangoproject.com/en/6.0/topics/auth/default/#permissions-and-authorization)
- [DRF Permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [RBAC Best Practices](https://en.wikipedia.org/wiki/Role-based_access_control)
