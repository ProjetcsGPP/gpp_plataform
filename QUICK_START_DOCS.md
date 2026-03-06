# 🚀 Quick Start - Documentação de Estrutura

## TL;DR

```bash
# 1. Gerar documentação
python manage.py generate_docs

# 2. Abrir docs/app_structure.md
# 3. Procurar pela view/model que precisa
# 4. Se não existir, implementar primeiro
# 5. Adicionar ao __all__ e regenerar
```

### Windows PowerShell

```powershell
.\generate-docs.ps1
```

## O Problema Que Resolve

**Antes:**
```
AttributeError: module 'carga_org_lot.views.web_views' has no attribute 'organograma_upload'
```

**Agora:**
1. Abra `docs/app_structure.md`
2. Procure por `organograma_upload`
3. Se não estiver lá → Não existe! Precisa criar
4. Se estiver lá → Use com segurança

## Exemplo Prático

### Quer usar `patriarca_create`?

1. **Gere docs:**
   ```bash
   python manage.py generate_docs
   ```

2. **Abra `docs/app_structure.md` e procure:**
   ```markdown
   ## carga_org_lot

   ### 👀 Views

   | Nome | Tipo | Módulo |
   |------|------|--------|
   | `patriarca_list` | function | web_views |
   | `patriarca_detail` | function | web_views |
   ```

3. **Não encontrou `patriarca_create`?**
   ```bash
   # Implemente em carga_org_lot/views/web_views/patriarca_views.py
   def patriarca_create(request):
       ...

   # Adicione ao __all__ em carga_org_lot/views/web_views/__init__.py
   __all__ = [
       'patriarca_list',
       'patriarca_detail',
       'patriarca_create',  # <-- NOVO
   ]

   # Regenere
   python manage.py generate_docs
   ```

4. **Agora use na URL:**
   ```python
   # carga_org_lot/urls/__init__.py
   path('patriarcas/novo/', web_views.patriarca_create, name='patriarca_create'),
   ```

## Estrutura do Markdown

Cada app tem:

```markdown
## carga_org_lot

### 📁 Estrutura de Arquivos
### 🗂️ Models
### 👀 Views
### 🔗 URLs
### 👨‍💼 Admin Registrado
```

Procure pela seção **Views** ou **Models** que precisa!

## Comandos Útel

```bash
# Gerar tudo (padrão)
python manage.py generate_docs

# Só Markdown
python manage.py generate_docs --format markdown

# Só JSON (para scripts)
python manage.py generate_docs --format json

# Em pasta customizada
python manage.py generate_docs --output minha_pasta/
```

## Checklist Antes de Modificar

- [ ] Execute `python manage.py generate_docs`
- [ ] Abra `docs/app_structure.md`
- [ ] Procure pelas views/models que vai usar
- [ ] Se não existem → Implemente primeiro
- [ ] Se existem → Use o nome exato do Markdown
- [ ] Se criou novas views → Regenere docs
- [ ] Commit `docs/app_structure.*` junto com o código

## Links Útely

- `DOCUMENTATION_GUIDE.md` - Guia completo
- `docs/app_structure.md` - Documentação gerada (consulte)
- `docs/app_structure.json` - Para scripts/ferramentas

## Troubleshooting Rápido

**"Command not found"**
```bash
touch common/management/__init__.py
touch common/management/commands/__init__.py
```

**Docs vazio**
- Certifique-se que as views tãm `__all__` definido
- Regenere com `python manage.py generate_docs`

**View não aparece nos docs**
- Ação: Adicione ao `__all__` do `__init__.py` da app
- Depois: Regenere os docs

---

**Leia DOCUMENTATION_GUIDE.md para mais detalhes!**
