# Sistema Automatizado de Permissões - Ações PNGI

## 🎯 Objetivo

Este sistema elimina o **hardcoding de permissões** nas views e templates, automatizando completamente o controle de acesso baseado nas tabelas `accounts_rolepermission` e `auth_permission`.

## ✨ Benefícios

- ✅ **Zero Hardcoding**: Permissões vem automaticamente do banco de dados
- ✅ **Automático**: Novas permissões adicionadas ao BD ficam disponíveis imediatamente
- ✅ **DRY**: Código reutilizável em toda a aplicação
- ✅ **Performance**: Sistema de cache para otimizar consultas
- ✅ **Segurança**: Validação centralizada e consistente

---

## 📚 Componentes

### 1. Context Processor (`context_processors.py`)

Disponibiliza automaticamente todas as permissões do usuário em TODOS os templates.

**Variáveis disponíveis:**

```python
# Flags de acesso
has_acoes_access        # Bool: Tem acesso ao Ações PNGI?
acoes_role              # String: Código do role (ex: 'ADMIN_PNGI')
acoes_role_display      # String: Nome amigável do role

# Permissões individuais (uma para cada permissão no BD)
can_add_eixo           # Bool: Pode adicionar eixo?
can_change_eixo        # Bool: Pode editar eixo?
can_delete_eixo        # Bool: Pode deletar eixo?
can_view_eixo          # Bool: Pode visualizar eixo?

can_add_situacaoacao   # Bool: Pode adicionar situação?
can_change_situacaoacao
can_delete_situacaoacao
can_view_situacaoacao

# ... e assim por diante para TODOS os modelos

# Permissões agregadas por modelo
can_manage_eixo        # Bool: Pode add OU change eixo?
can_full_eixo          # Bool: Tem todas as 4 permissões de eixo?
can_edit_eixo          # Bool: Alias para can_change_eixo

# Grupos de permissões
can_manage_config      # Bool: Pode gerenciar configurações?
can_delete_any         # Bool: Pode deletar algo?
```

### 2. Template Tags (`templatetags/acoes_permissions.py`)

Tags customizadas para verificações mais complexas.

**Tags disponíveis:**

#### `{% has_perm %}`
Verifica permissão específica:
```django
{% load acoes_permissions %}

{% has_perm 'add_eixo' as can_add %}
{% if can_add %}
    <button>Criar Eixo</button>
{% endif %}
```

#### `{% can_manage %}`
Verifica se pode gerenciar (add OU change):
```django
{% can_manage 'eixo' as can_manage_eixo %}
{% if can_manage_eixo %}
    <a href="...">Gerenciar Eixos</a>
{% endif %}
```

#### `{% has_any_perm %}`
Verifica se tem QUALQUER uma das permissões:
```django
{% has_any_perm 'add_eixo' 'change_eixo' 'delete_eixo' as has_eixo_perm %}
{% if has_eixo_perm %}
    <div>Você pode gerenciar eixos</div>
{% endif %}
```

#### `{% has_all_perms %}`
Verifica se tem TODAS as permissões:
```django
{% has_all_perms 'add_eixo' 'change_eixo' 'view_eixo' as is_admin %}
{% if is_admin %}
    <div>Administrador de Eixos</div>
{% endif %}
```

#### `{% get_user_role %}`
Obtém o role do usuário:
```django
{% get_user_role as user_role %}
<p>Seu perfil: {{ user_role.nomeperfil }}</p>
```

#### `|has_model_perm` (Filter)
Verificação inline:
```django
{% if user|has_model_perm:'add_eixo' %}
    <button>Adicionar</button>
{% endif %}
```

#### `{% permission_badge %}`
Renderiza badge visual de permissão:
```django
{% permission_badge 'add_eixo' 'Criar Eixo' %}
```

### 3. Utilitários (`utils/permissions.py`)

Funções auxiliares para views e lógica Python.

#### Decorators para Views

##### `@require_app_permission`
Requer permissão específica:
```python
from acoes_pngi.utils.permissions import require_app_permission

@require_app_permission('add_eixo')
def create_eixo(request):
    # Só executa se usuário tem permissão add_eixo
    ...
```

##### `@require_any_permission`
Requer QUALQUER uma das permissões:
```python
from acoes_pngi.utils.permissions import require_any_permission

@require_any_permission('add_eixo', 'change_eixo', 'delete_eixo')
def manage_eixo(request):
    # Só executa se tiver pelo menos uma permissão
    ...
```

##### `@require_all_permissions`
Requer TODAS as permissões:
```python
from acoes_pngi.utils.permissions import require_all_permissions

@require_all_permissions('view_eixo', 'change_eixo')
def edit_eixo(request, pk):
    # Só executa se tiver ambas as permissões
    ...
```

#### Funções Helper

##### `user_can_manage_model()`
Verifica se pode gerenciar modelo:
```python
from acoes_pngi.utils.permissions import user_can_manage_model

if user_can_manage_model(request.user, 'eixo'):
    # Usuário pode add OU change
    ...
```

##### `get_model_permissions()`
Obtém todas as permissões de um modelo:
```python
from acoes_pngi.utils.permissions import get_model_permissions

perms = get_model_permissions(request.user, 'eixo')
print(perms)
# {
#     'can_add': True,
#     'can_change': True,
#     'can_delete': False,
#     'can_view': True,
#     'can_manage': True
# }
```

##### `get_user_permissions_cached()`
Obtém permissões com cache (performance):
```python
from acoes_pngi.utils.permissions import get_user_permissions_cached

perms = get_user_permissions_cached(request.user)
# set(['add_eixo', 'change_eixo', 'view_eixo', ...])
```

##### `clear_user_permissions_cache()`
Limpa cache (usar após alterar permissões):
```python
from acoes_pngi.utils.permissions import clear_user_permissions_cache

# Após mudar role do usuário
clear_user_permissions_cache(user)
```

---

## 🚀 Exemplos de Uso

### Exemplo 1: Botão Condicional no Template

```django
{% load acoes_permissions %}

<div class="card">
    <div class="card-header">
        <h5>Eixos PNGI</h5>
        
        {# Usando context processor #}
        {% if can_add_eixo %}
            <a href="{% url 'acoes_pngi_web:eixo_create' %}" class="btn btn-primary">
                <i class="bi bi-plus"></i> Novo Eixo
            </a>
        {% endif %}
    </div>
    
    <div class="card-body">
        <table class="table">
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Descrição</th>
                    {% if can_manage_eixo %}
                        <th>Ações</th>
                    {% endif %}
                </tr>
            </thead>
            <tbody>
                {% for eixo in eixos %}
                    <tr>
                        <td>{{ eixo.nome }}</td>
                        <td>{{ eixo.descricao }}</td>
                        {% if can_manage_eixo %}
                            <td>
                                {% if can_change_eixo %}
                                    <a href="{% url 'acoes_pngi_web:eixo_update' eixo.pk %}">
                                        Editar
                                    </a>
                                {% endif %}
                                
                                {% if can_delete_eixo %}
                                    <a href="{% url 'acoes_pngi_web:eixo_delete' eixo.pk %}">
                                        Deletar
                                    </a>
                                {% endif %}
                            </td>
                        {% endif %}
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
```

### Exemplo 2: Menu de Navegação Dinâmico

```django
{% load acoes_permissions %}

<nav>
    <ul class="nav flex-column">
        {% if has_acoes_access %}
            <li class="nav-item">
                <span class="badge">{{ acoes_role_display }}</span>
            </li>
            
            {% if can_view_eixo %}
                <li class="nav-item">
                    <a href="{% url 'acoes_pngi_web:eixo_list' %}">Eixos</a>
                </li>
            {% endif %}
            
            {% if can_view_situacaoacao %}
                <li class="nav-item">
                    <a href="{% url 'acoes_pngi_web:situacao_list' %}">Situações</a>
                </li>
            {% endif %}
            
            {% if can_manage_config %}
                <li class="nav-item">
                    <a href="{% url 'acoes_pngi_web:config' %}">Configurações</a>
                </li>
            {% endif %}
        {% endif %}
    </ul>
</nav>
```

### Exemplo 3: View Protegida com Decorator

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from acoes_pngi.utils.permissions import (
    require_app_permission,
    require_any_permission,
    get_model_permissions
)
from acoes_pngi.models import Eixo
from acoes_pngi.forms import EixoForm


@require_app_permission('add_eixo')
def eixo_create(request):
    """View para criar eixo - requer permissão add_eixo."""
    if request.method == 'POST':
        form = EixoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Eixo criado com sucesso!')
            return redirect('acoes_pngi_web:eixo_list')
    else:
        form = EixoForm()
    
    return render(request, 'acoes_pngi/eixo_form.html', {'form': form})


@require_any_permission('change_eixo', 'view_eixo')
def eixo_detail(request, pk):
    """View para ver/editar eixo - requer view OU change."""
    eixo = get_object_or_404(Eixo, pk=pk)
    
    # Verificar se pode editar
    perms = get_model_permissions(request.user, 'eixo')
    
    if request.method == 'POST' and perms['can_change']:
        form = EixoForm(request.POST, instance=eixo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Eixo atualizado!')
            return redirect('acoes_pngi_web:eixo_list')
    else:
        form = EixoForm(instance=eixo) if perms['can_change'] else None
    
    return render(request, 'acoes_pngi/eixo_detail.html', {
        'eixo': eixo,
        'form': form,
        'permissions': perms
    })
```

### Exemplo 4: Template com Template Tags

```django
{% load acoes_permissions %}

{# Verificar múltiplas permissões #}
{% has_any_perm 'add_eixo' 'change_eixo' 'delete_eixo' as can_admin_eixo %}

{% if can_admin_eixo %}
    <div class="alert alert-info">
        <h4>Painel de Administração</h4>
        
        {# Exibir badges de permissão #}
        {% permission_badge 'add_eixo' 'Criar' %}
        {% permission_badge 'change_eixo' 'Editar' %}
        {% permission_badge 'delete_eixo' 'Deletar' %}
        {% permission_badge 'view_eixo' 'Visualizar' %}
    </div>
{% endif %}

{# Obter e exibir role #}
{% get_user_role as role %}
{% if role %}
    <p class="text-muted">
        Você está logado como: <strong>{{ role.nomeperfil }}</strong>
    </p>
{% endif %}
```

---

## ⚙️ Configuração

O sistema já está configurado em `settings.py`:

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

---

## 🧪 Testes

Executar testes:

```bash
python manage.py test acoes_pngi.tests.test_permissions
```

Os testes cobrem:
- Context processor com diferentes roles
- Template tags
- Funções helper
- Sistema de cache
- Decorators de views

---

## 🔄 Migração de Código Antigo

### Antes (Hardcoded):
```python
# View antiga
def eixo_list(request):
    if request.user.email != 'admin@example.com':
        return HttpResponseForbidden()
    ...
```

```django
{# Template antigo #}
{% if user.email == 'admin@example.com' %}
    <button>Criar</button>
{% endif %}
```

### Depois (Automatizado):
```python
# View nova
@require_app_permission('view_eixo')
def eixo_list(request):
    ...
```

```django
{# Template novo #}
{% if can_add_eixo %}
    <button>Criar</button>
{% endif %}
```

---

## 📝 Checklist de Implementação

- [x] Context processor implementado
- [x] Template tags criadas
- [x] Utilitários e decorators
- [x] Sistema de cache
- [x] Testes unitários
- [x] Documentação completa
- [ ] Aplicar em todas as views do `acoes_pngi`
- [ ] Atualizar todos os templates
- [ ] Replicar para `carga_org_lot`

---

## 🔐 Segurança

### Boas Práticas

1. **Sempre proteger views**: Use decorators em TODAS as views sensíveis
2. **Validar no backend**: Nunca confie apenas em controles de UI
3. **Limpar cache**: Após alterar permissões, limpe o cache
4. **Testar permissões**: Escreva testes para cada role

### Exemplo de View Segura

```python
@require_app_permission('delete_eixo')
def eixo_delete(request, pk):
    """Delete protegido por decorator + validação dupla."""
    # Validação adicional (defesa em profundidade)
    if not request.user.has_app_perm('ACOES_PNGI', 'delete_eixo'):
        raise PermissionDenied
    
    eixo = get_object_or_404(Eixo, pk=pk)
    
    if request.method == 'POST':
        eixo.delete()
        messages.success(request, 'Eixo deletado!')
        return redirect('acoes_pngi_web:eixo_list')
    
    return render(request, 'acoes_pngi/eixo_confirm_delete.html', {
        'eixo': eixo
    })
```

---

## 🎓 Próximos Passos

1. **Aplicar em `acoes_pngi`**: Atualizar todas as views e templates existentes
2. **Criar padrão**: Documentar padrão de uso para novos desenvolvedores
3. **Replicar para `carga_org_lot`**: Adaptar o sistema para o app maior
4. **Monitoramento**: Adicionar logging de acessos negados
5. **Audit log**: Registrar alterações de permissões

---

## ❓ FAQ

**P: Como adicionar uma nova permissão?**  
R: Basta adicionar no banco de dados via Django Admin ou migração. O sistema detecta automaticamente.

**P: O cache pode causar problemas?**  
R: O cache é de apenas 15 minutos e pode ser limpo manualmente com `clear_user_permissions_cache()`.

**P: Como testar permissões?**  
R: Use `python manage.py test acoes_pngi.tests.test_permissions` ou crie testes específicos.

**P: Posso usar em APIs REST?**  
R: Sim! Use os decorators nas views de API ou crie permission classes baseadas nos helpers.

---

## 📞 Suporte

Para dúvidas ou problemas, consulte:
- Este README
- Código fonte comentado
- Testes unitários (exemplos de uso)
- `acoes_pngi/README_PERMISSIONS.md` (documentação original)
