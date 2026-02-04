# 📋 Pasta de Documentação - Estrutura do Projeto

## 📄 Arquivos Nesta Pasta

### `app_structure.json` 🔐
**Gerado automaticamente por:** `python manage.py generate_docs`

Estrutura completa em formato JSON com todos os models, views, URLs, namespaces.
- **Uso:** Scripts, ferramentas, analisadores de código
- **Atualizar:** Execute o comando generate_docs quando adicionar views/models

### `app_structure.md` 📑
**Gerado automaticamente por:** `python manage.py generate_docs`

Documentação legível em Markdown com índice e detalhes de cada app.
- **Uso:** Consultar antes de criar URLs ou referenciar views
- **Atualizar:** Execute o comando generate_docs quando adicionar views/models

### `EXAMPLE_app_structure.md` 👁
Exemplo de como o arquivo `app_structure.md` fica após ser gerado.
- Mostra a estrutura esperada
- Serve de referência visual

### `SOLVE_CURRENT_ERROR.md` 🔧
Guia passo a passo para resolver o erro atual de `patriarca_create`.
- Passos exatos
- Checklist final
- Troubleshooting

---

## 🚀 Quick Start

### 1. Gerar Documentação

```bash
python manage.py generate_docs
```

**Windows PowerShell:**
```powershell
.\generate-docs.ps1
```

### 2. Consultar Antes de Modificar

Abra `app_structure.md` e procure:
- A **app** que quer modificar (ex: `carga_org_lot`)
- A seção **Views** ou **Models**
- Confirme que o que precisa existe

### 3. Se não Existir

1. Implemente a view/model
2. Adicione ao `__all__` do `__init__.py`
3. Regenere: `python manage.py generate_docs`

---

## 📚 Guias Completos

| Arquivo | Conteúdo | Quando Ler |
|---------|----------|----------|
| [QUICK_START_DOCS.md](../QUICK_START_DOCS.md) | TL;DR e exemplo prático | Primeira vez / Precisa lembrar rápido |
| [DOCUMENTATION_GUIDE.md](../DOCUMENTATION_GUIDE.md) | Guia completo e detalhado | Precisa entender o sistema |
| [SOLVE_CURRENT_ERROR.md](./SOLVE_CURRENT_ERROR.md) | Resolver erro de patriarca_create | Tem erro NoReverseMatch agora |
| [EXAMPLE_app_structure.md](./EXAMPLE_app_structure.md) | Exemplo de output | Quer ver como fica o Markdown |

---

## 😛 Por Que Isso Existe

**Antes:**
```
AttributeError: module 'carga_org_lot.views.web_views' has no attribute 'organograma_upload'
```

**Agora:**
1. Execute `python manage.py generate_docs`
2. Abra `app_structure.md`
3. Procure por `organograma_upload`
4. Se não estiver lá → Não existe! Crie primeiro
5. Se estiver lá → Use com segurança

---

## 📌 Checklist de Uso

- [ ] Lí QUICK_START_DOCS.md (se primeira vez)
- [ ] Executei `python manage.py generate_docs`
- [ ] Consultei `app_structure.md` antes de modificar
- [ ] Confirmei que a view/model existe
- [ ] Se criei algo novo: atualizei `__all__` e regenerei docs
- [ ] Commitei `app_structure.*` junto com meu código

---

## 🛠️ Manuais de Referencia

### Ver todas as views de uma app

Abra `app_structure.md`, procure pela app (ex `carga_org_lot`), e veja a seção **Views**.

### Ver padrões de URL

Abra `app_structure.md`, procure pela app, e veja a seção **URLs**.

### Ver todos os models

Abra `app_structure.md`, procure pela app, e veja a seção **Models**.

### Ver estrutura de pastas

Abra `app_structure.md`, procure pela app, e veja a seção **Estrutura de Arquivos**.

---

## 📄 Gerar Docs

```bash
# Ambos (padrão)
python manage.py generate_docs

# Só Markdown
python manage.py generate_docs --format markdown

# Só JSON
python manage.py generate_docs --format json

# Em pasta customizada
python manage.py generate_docs --output minha_pasta/
```

---

## ❓ Dúvidas?

1. **"Como saber se uma view existe?"**
   → Consulte `app_structure.md`, procure na seção Views

2. **"Como adicionar uma nova view?"**
   → Implemente + adicione ao `__all__` + regenere docs

3. **"Preciso atualizar os docs?"**
   → Sim! Sempre que adicionar/remover views ou models

4. **"Posso editar app_structure.md manualmente?"**
   → Não recomendado - será sobrescrito na próxima geração

---

**Lê [QUICK_START_DOCS.md](../QUICK_START_DOCS.md) para começar! 🚀**
