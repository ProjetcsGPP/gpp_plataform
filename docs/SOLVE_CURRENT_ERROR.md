# 🔧 Resolver: NoReverseMatch de 'patriarca_create'

## Erro Atual

```
NoReverseMatch at /carga_org_lot/patriarcas/
Reverse for 'patriarca_create' not found. 'patriarca_create' is not a valid view function or pattern name.
```

## Causa

A URL `carga_org_lot/urls/__init__.py` está tentando usar `web_views.patriarca_create`, mas essa view:
- OU não existe no arquivo Python
- OU existe mas não está no `__all__` do `web_views/__init__.py`

## Solução em 3 Passos

### Passo 1: Gerar Documentação

```bash
python manage.py generate_docs
```

### Passo 2: Consultar a Documentação

Abra `docs/app_structure.md` e procure por:

```markdown
### 👀 Views

| Nome | Tipo | Módulo |
|------|------|--------|
```

**Procure por `patriarca_create`**

#### Opção A: `patriarca_create` ESTÁ NA LISTA

✓️ A view existe! O problema pode ser que não está exportada.

Vá para o arquivo `carga_org_lot/urls/__init__.py` e verifique se:

```python
from ..views import web_views

urlpatterns = [
    path('patriarcas/novo/', web_views.patriarca_create, name='patriarca_create'),
]
```

Se vocé vê a view na documentação, a URL deve funcionar!

#### Opção B: `patriarca_create` NÃO ESTÁ NA LISTA

❌ A view não existe! Precisa ser criada.

### Passo 3: Criar a View (se necessário)

Se `patriarca_create` não existe:

#### 3a. Criar a função

Abra `carga_org_lot/views/web_views/patriarca_views.py` e adicione:

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ...models import Patriarca
from ...forms import PatriarcaForm  # Se existir

@login_required
def patriarca_create(request):
    """Criar novo Patriarca"""
    if request.method == 'POST':
        form = PatriarcaForm(request.POST)
        if form.is_valid():
            patriarca = form.save()
            return redirect('carga_org_lot:patriarca_detail', patriarca_id=patriarca.id)
    else:
        form = PatriarcaForm()

    return render(request, 'carga_org_lot/patriarca_form.html', {'form': form})
```

#### 3b. Exportar a view

Abra `carga_org_lot/views/web_views/__init__.py` e adicione ao `__all__`:

```python
from .patriarca_views import (
    patriarca_list,
    patriarca_detail,
    patriarca_create,  # ← ADICIONE AQUI
)

__all__ = [
    'patriarca_list',
    'patriarca_detail',
    'patriarca_create',  # ← E AQUI
]
```

#### 3c. Regenerar Documentação

```bash
python manage.py generate_docs
```

Agora `patriarca_create` aparecerá em `docs/app_structure.md` !

#### 3d. Adicionar URL (se ainda não estiver)

Abra `carga_org_lot/urls/__init__.py` e verifique:

```python
from ..views import web_views

urlpatterns = [
    path('patriarcas/', web_views.patriarca_list, name='patriarca_list'),
    path('patriarcas/<int:patriarca_id>/', web_views.patriarca_detail, name='patriarca_detail'),
    path('patriarcas/novo/', web_views.patriarca_create, name='patriarca_create'),  # ← Isto
]
```

## Checklist Final

- [ ] Executei `python manage.py generate_docs`
- [ ] Consultei `docs/app_structure.md`
- [ ] Confirmei que `patriarca_create` existe (ou criei)
- [ ] Adicionei ao `__all__` do `web_views/__init__.py` (se novo)
- [ ] Regenerei os docs
- [ ] Verificar que a URL está em `carga_org_lot/urls/__init__.py`
- [ ] Testei: `python manage.py runserver`
- [ ] Acessei `http://127.0.0.1:8000/carga_org_lot/patriarcas/` (sem erro)

## Se Ainda Não Funcionar

1. **Limpe cache do Django:**
   ```bash
   python manage.py clear_cache  # Se existir
   # ou reinicie o servidor
   ```

2. **Verifique a sintaxe de `__all__`:**
   ```python
   # ✅ CORRETO
   __all__ = [
       'patriarca_create',
       'patriarca_list',
   ]

   # ❌ ERRADO
   __all__ = [
       patriarca_create,  # ← Sem aspas!
   ]
   ```

3. **Verifique import na URL:**
   ```python
   # ✅ CORRETO
   from ..views import web_views
   web_views.patriarca_create  # Usar assim

   # ❌ ERRADO
   from ..views.web_views import patriarca_create  # Depois import direto
   patriarca_create  # Causa confusão
   ```

## Resumo

```bash
# 1. Gerar docs
python manage.py generate_docs

# 2. Consultar docs/app_structure.md
# 3. Se view não existe: implementar + __all__ + regenerar
# 4. Testar servidor
python manage.py runserver
```

---

**Leia QUICK_START_DOCS.md e DOCUMENTATION_GUIDE.md para mais contexto!**
