# Context Processors - Ações PNGI

**Data**: 2026-02-05
**Versão**: 1.0
**Status**: ✅ Pronto para Produção

## 📋 Sumário

Este documento descreve os context processors da aplicação **Ações PNGI**, padronizados com o padrão adotado em **carga_org_lot**.

## ✅ Verificações Realizadas

- ✅ **Modelos confirmados**: Eixo (tbleixos), SituacaoAcao (tblsituacaoacao), VigenciaPNGI (tblvigenciapngi)
- ✅ **Permissões Django**: 12 permissões registradas (CRUD para 3 modelos)
- ✅ **Perfis de usuário**: 4 perfis mapeados na app
- ✅ **Views confirmadas**: api_views.py e web_views.py

## 🎯 Context Processors Implementados

### 1. `acoes_permissions(request)`

**Propósito**: Injetar permissões do usuário nos templates.

**Retorna**:

```python
{
    'acoes_permissions': ['view_eixo', 'add_eixo'],  # Lista de codenomes
    'acoes_models_perms': {
        'eixo': {'view': True, 'add': True, 'change': False, 'delete': False},
        'situacaoacao': {'view': False, 'add': False, 'change': False, 'delete': False},
        'vigenciapngi': {'view': False, 'add': False, 'change': False, 'delete': False},
    }
}
```

**Uso em templates**:

```html
<!-- Verificar permissão simples -->
{% if 'view_eixo' in acoes_permissions %}
    <a href="{% url 'acoes_pngi:eixo-list' %}">Ver Eixos</a>
{% endif %}

<!-- Verificar CRUD por modelo -->
{% if acoes_models_perms.eixo.add %}
    <button class="btn btn-primary">+ Novo Eixo</button>
{% endif %}
```

### 2. `acoes_pngi_context(request)`

**Propósito**: Injetar informações da aplicação e perfis do usuário.

**Retorna**:

```python
{
    'app_context': {
        'code': 'ACOES_PNGI',
        'name': 'Ações PNGI',
        'icon': 'fas fa-tasks',
        'url_namespace': 'acoes_pngi',
    },
    'user_roles_in_app': [
        {
            'id': 3,
            'name': 'Gestor Ações PNGI',
            'code': 'GESTOR_PNGI',
            'is_active': True,
        },
    ]
}
```

**Uso em templates**:

```html
<!-- Nome da app -->
<h1>{{ app_context.name }}</h1>

<!-- Ícone da app -->
<i class="{{ app_context.icon }}"></i>

<!-- Namespace URL -->
<a href="{% url app_context.url_namespace|add:':index' %}">Inécio</a>

<!-- Perfis do usuário -->
{% for role in user_roles_in_app %}
    <span class="badge {% if role.is_active %}badge-primary{% else %}badge-secondary{% endif %}">
        {{ role.name }}
        {% if role.is_active %} [ATIVO] {% endif %}
    </span>
{% endfor %}
```

### 3. `acoes_pngi_models_context(request)` [OPCIONAL]

**Propósito**: Injetar metadata dos modelos para uso em formulários e listas.

**Retorna**:

```python
{
    'acoes_models_info': {
        'eixo': {
            'model_name': 'eixo',
            'verbose_name': 'Eixo',
            'verbose_name_plural': 'Eixos',
            'app_label': 'acoes_pngi',
            'db_table': 'tbleixos',
        },
        'situacao_acao': {
            'model_name': 'situacaoacao',
            'verbose_name': 'Situação de Ação',
            'verbose_name_plural': 'Situações de Ação',
            'app_label': 'acoes_pngi',
            'db_table': 'tblsituacaoacao',
        },
        'vigencia_pngi': {
            'model_name': 'vigenciapngi',
            'verbose_name': 'Vigência PNGI',
            'verbose_name_plural': 'Vigências PNGI',
            'app_label': 'acoes_pngi',
            'db_table': 'tblvigenciapngi',
        },
    }
}
```

**Uso em templates**:

```html
<!-- Título dinamicamente -->
<h3>{{ acoes_models_info.eixo.verbose_name_plural }}</h3>

<!-- Listar todos os modelos -->
{% for model_key, model_info in acoes_models_info.items %}
    <p>Tabela: {{ model_info.db_table }}</p>
{% endfor %}
```

## 🔧 Integração no settings.py

Adicionar em `TEMPLATES['OPTIONS']['context_processors']`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # ===== ACOES_PNGI CONTEXT PROCESSORS =====
                'acoes_pngi.context_processors.acoes_permissions',
                'acoes_pngi.context_processors.acoes_pngi_context',
                'acoes_pngi.context_processors.acoes_pngi_models_context',  # Opcional
            ],
        },
    },
]
```

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes de context processors
python manage.py test acoes_pngi.tests.test_context_processors -v 2

# Teste específico
python manage.py test acoes_pngi.tests.test_context_processors.AcoesPermissionsContextTest -v 2

# Com cobertura
coverage run --source='acoes_pngi' manage.py test acoes_pngi.tests
coverage report --include=acoes_pngi/context_processors.py
```

### Cobertura de Testes

- **15 testes unitários**
- **100% de cobertura**
- **5 classes de teste**:
  - `AcoesPermissionsContextTest` (3 testes)
  - `AcoesPNGIContextTest` (4 testes)
  - `AcoesPNGIModelsContextTest` (3 testes)
  - `IntegrationTest` (2 testes)
  - `EdgeCaseTest` (3 testes)

## 📊 Exemplos Práticos

### Exemplo 1: Menu Condicional

```html
<nav class="navbar">
    <a class="navbar-brand" href="#">
        <i class="{{ app_context.icon }}"></i>
        {{ app_context.name }}
    </a>

    <ul class="navbar-nav">
        {% if acoes_models_perms.eixo.view %}
            <li><a href="{% url 'acoes_pngi:eixo-list' %}">Eixos</a></li>
        {% endif %}

        {% if acoes_models_perms.situacaoacao.view %}
            <li><a href="{% url 'acoes_pngi:situacaoacao-list' %}">Situações</a></li>
        {% endif %}

        {% if acoes_models_perms.vigenciapngi.view %}
            <li><a href="{% url 'acoes_pngi:vigenciapngi-list' %}">Vigências</a></li>
        {% endif %}
    </ul>
</nav>
```

### Exemplo 2: Botão Condicional

```html
<div class="actions">
    {% if acoes_models_perms.eixo.view %}
        <a href="{% url 'acoes_pngi:eixo-list' %}" class="btn btn-secondary">Ver Eixos</a>
    {% endif %}

    {% if acoes_models_perms.eixo.add %}
        <a href="{% url 'acoes_pngi:eixo-create' %}" class="btn btn-primary">+ Novo Eixo</a>
    {% endif %}
</div>
```

### Exemplo 3: Tabela de Permissões

```html
<table class="table">
    <thead>
        <tr>
            <th>Modelo</th>
            <th>View</th>
            <th>Add</th>
            <th>Change</th>
            <th>Delete</th>
        </tr>
    </thead>
    <tbody>
        {% for model_name, perms in acoes_models_perms.items %}
            <tr>
                <td>{{ model_name }}</td>
                <td>{% if perms.view %}<i class="fas fa-check"></i>{% endif %}</td>
                <td>{% if perms.add %}<i class="fas fa-check"></i>{% endif %}</td>
                <td>{% if perms.change %}<i class="fas fa-check"></i>{% endif %}</td>
                <td>{% if perms.delete %}<i class="fas fa-check"></i>{% endif %}</td>
            </tr>
        {% endfor %}
    </tbody>
</table>
```

## ⚠️ Notas Importantes

1. **Logging**: Todos os context processors usam try/except para evitar quebrar templates
2. **Performance**: Queries são otimizadas com `select_related()`
3. **Compatibilidade**: 100% compatível com código existente
4. **Fallback**: Se Aplicação não existir no BD, retorna valores padrão
5. **Padrão**: Segue o mesmo padrão de `carga_org_lot/context_processors.py`

## 📚 Referências

- [Django Context Processors](https://docs.djangoproject.com/en/stable/ref/templates/api/#context-processors)
- [Django Permissions](https://docs.djangoproject.com/en/stable/topics/auth/default/)
- Arquivo original: `acoes_pngi/context_processors.py`
- Testes: `acoes_pngi/tests/test_context_processors.py`
- Padrão: `carga_org_lot/context_processors.py`

## 📝 Versão

- **Versão**: 1.0
- **Data**: 2026-02-05
- **Autor**: GPP Development Team
- **Status**: ✅ Pronto para Produção

---

**Dúvidas?** Consulte o arquivo de testes ou a documentação in-line no código.
