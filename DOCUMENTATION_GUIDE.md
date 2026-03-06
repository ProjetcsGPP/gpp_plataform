# 📋 Guia de Documentação da Estrutura do GPP Platform

## O Problema

Antes de fazer modificações, você precisava:
1. Procurar em vários arquivos para entender a estrutura
2. Lembrar de nões que existem ou não
3. Criar `urls.py` com referências a views inexistentes
4. Gerar erros como: `AttributeError: module 'carga_org_lot.views.web_views' has no attribute 'organograma_upload'`

## A Solução

Um sistema automático de documentação que gera:
- **app_structure.json**: Estrutura completa em JSON (para ferramentas/scripts)
- **app_structure.md**: Documentação legível em Markdown

## Como Usar

### 1. Gerar a Documentação

```bash
python manage.py generate_docs
```

Isso cria/atualiza dois arquivos em `docs/`:
- `docs/app_structure.json`
- `docs/app_structure.md`

### 2. Consultar Antes de Modificar

Antes de criar uma URL ou referenciar uma view:

1. Abra `docs/app_structure.md`
2. Procure pela app em questão (ex: `carga_org_lot`)
3. Veja a seção **Views** para confirmar que a view existe

**Exemplo:** Procurando por `patriarca_create`:

```markdown
### 👀 Views

| Nome | Tipo | Módulo |
|------|------|--------|
| `patriarca_list` | function | web_views |
| `patriarca_detail` | function | web_views |
```

❌ Se `patriarca_create` não está lá, precisa ser criada primeiro!

### 3. Adicionar uma Nova View

Quando criar uma nova view:

1. Implemente a função no arquivo correto (ex: `carga_org_lot/views/web_views/patriarca_views.py`)
2. Adicione ao `__all__` do `__init__.py`:

```python
# carga_org_lot/views/web_views/__init__.py
__all__ = [
    # ... views existentes
    'patriarca_create',  # ← Adicione aqui
]
```

3. Regenere a documentação:

```bash
python manage.py generate_docs
```

4. Agora `patriarca_create` aparecerá em `docs/app_structure.md`

### 4. Adicionar URL com Segurança

Agora que você sabe que a view existe:

```python
# carga_org_lot/urls/__init__.py
from ..views import web_views

urlpatterns = [
    # Consultei docs/app_structure.md e confirmei que patriarca_create existe
    path('patriarcas/novo/', web_views.patriarca_create, name='patriarca_create'),
]
```

## Estrutura da Documentação

Cada app é documentada com:

### 📁 Estrutura de Arquivos
```
views/
  ├─ web_views/
  ├─ api_views/
  ├─ __init__.py
models.py
urls.py
admin.py
```

### 🗂️ Models
Todos os models com seus fields:
```
#### `Patriarca`
**Fields:** `id, nome, sigla, descricao, ativo, criado_em`
```

### 👀 Views
Todas as views disponíveis:
```
| `patriarca_list` | function | web_views |
| `patriarca_detail` | function | web_views |
```

### 🔗 URLs
Padrões e namespaces:
```
**Namespace:** `carga_org_lot`
**Padrões:**
- `patriarcas/` → `patriarca_list`
- `patriarcas/<id>/` → `patriarca_detail`
```

### 👨‍💼 Admin Registrado
Models no Django Admin:
```
- `Patriarca` (PatriarcaAdmin)
```

## Workflow Recomendado

1. **No início do sprint/task:**
   ```bash
   python manage.py generate_docs
   ```

2. **Antes de modificar URLs ou templates:**
   - Abra `docs/app_structure.md`
   - Procure pelas views/models que precisa
   - Copie o nome exato

3. **Ao criar novas views:**
   - Implemente a função
   - Adicione ao `__all__`
   - Execute `python manage.py generate_docs`
   - Agora está disponível para usar

4. **No final da task:**
   - Regenere a documentação
   - Commit os arquivos `docs/app_structure.*`

## Formato JSON

O `app_structure.json` pode ser usado por scripts/ferramentas:

```json
{
  "carga_org_lot": {
    "models": {
      "Patriarca": {
        "fields": ["id", "nome", "descricao"]
      }
    },
    "views": {
      "patriarca_list": {
        "type": "function",
        "module": "web_views"
      }
    },
    "urls": {
      "namespace": "carga_org_lot",
      "patterns": [
        {
          "pattern": "patriarcas/",
          "name": "patriarca_list"
        }
      ]
    }
  }
}
```

## Comandos Üteis

```bash
# Gerar ambos JSON e Markdown (padrão)
python manage.py generate_docs

# Apenas JSON
python manage.py generate_docs --format json

# Apenas Markdown
python manage.py generate_docs --format markdown

# Em pasta customizada
python manage.py generate_docs --output minha_pasta/
```

## Integração com Git

**Recomendado:** Commitar os arquivos de documentação

```bash
git add docs/app_structure.*
sgit commit -m "docs: Atualizar estrutura de apps"
```

Isso garante que toda a equipe tenha a mesma visão da estrutura.

## Troubleshooting

### Erro: "No module named 'management'"

Certifique-se de que `common/management/commands/__init__.py` existe:

```bash
touch common/management/__init__.py
touch common/management/commands/__init__.py
```

### Documentação vazia

1. Regenere:
   ```bash
   python manage.py generate_docs
   ```

2. Verifique se as apps tãm `__all__` definido em `views/__init__.py`

3. Verifique se os models herdam de `django.db.models.Model`

## Perguntas Frequentes

**P: Com que frequência devo regenerar?**
R: Sempre que adicionar/remover views ou models, regenere antes de commitar.

**P: E se esquecer de atualizar a documentação?**
R: É um risco! Use o arquivo como referência antes de qualquer modificação.

**P: Posso editar o Markdown manualmente?**
R: Não recomendado - será sobrescrito na próxima geração. Use o JSON para referências de código.

**P: Como saber se uma view está disponibilizada?**
R: Procure em `docs/app_structure.md` na seção Views. Se não estiver lá, não existe ou não está em `__all__`.
