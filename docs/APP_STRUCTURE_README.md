# 📚 Sistema de Documentação de Estrutura de Apps

## Objetivo

Este sistema gera documentação automática da estrutura interna do projeto Django, evitando conflitos de nomes e mantendo um mapa atualizado de todas as aplicações.

## Como Usar

### Opção 1: Comando Django Management (Recomendado)

Use o comando Django incorporado:

```bash
# Gerar em ambos os formatos (markdown + json)
python manage.py generate_structure_docs

# Especificar formato
python manage.py generate_structure_docs --format markdown
python manage.py generate_structure_docs --format json
python manage.py generate_structure_docs --format both

# Especificar diretório de saída
python manage.py generate_structure_docs --output docs/app_structure

# Modo verbose
python manage.py generate_structure_docs --verbose
```

**Saída Padrão:** `docs/app_structure/`

### Opção 2: Script Standalone (Sem Django)

Use o script Python direto:

```bash
# Gerar documentação
python docs/generate_structure.py

# Com opções
python docs/generate_structure.py --format markdown --output docs/app_structure
```

## Arquivos Gerados

### STRUCTURE.md

Documentação em Markdown legível com:
- 📋 Índice de todas as aplicações
- 📦 Estrutura de diretórios
- 📊 Modelos (Models)
- 👁️ Visões (Views)
- 🔄 ViewSets
- 📝 Serializers
- 🌐 URLs e rotas
- 📝 Formulários
- ⚙️ Admin
- 🔌 Signals

### structure.json

Documentação estruturada em JSON com:
- Timestamp de geração
- Todas as informações em formato estruturado
- Pronto para ferramentas de análise

## Estrutura de Dados Capturada

### Para cada Aplicação:

```json
{
  "name": "accounts",
  "path": "/path/to/accounts",
  "files": {
    "models.py": true,
    "views.py": true,
    "urls.py": true,
    "serializers.py": true
  },
  "models": [
    {
      "name": "User",
      "line": 15,
      "methods": ["save", "get_full_name"]
    }
  ],
  "views": [
    {
      "name": "login_view",
      "type": "function",
      "line": 42
    },
    {
      "name": "ProfileView",
      "type": "class",
      "line": 50,
      "methods": ["get", "post"]
    }
  ],
  "viewsets": [
    {
      "name": "UserViewSet",
      "line": 65,
      "methods": ["list", "create", "retrieve", "update"]
    }
  ],
  "serializers": [
    {
      "name": "UserSerializer",
      "line": 80,
      "methods": ["validate", "create"]
    }
  ],
  "urls": [
    "auth/login/",
    "auth/logout/",
    "profile/"
  ],
  "forms": [...],
  "admin": [...],
  "signals": [...]
}
```

## Quando Gerar Documentação

### Automático (Sugerido)

Adicione um **Git Hook** para gerar automaticamente:

```bash
# .git/hooks/post-commit
#!/bin/bash
echo "🔄 Atualizando documentação de estrutura..."
python manage.py generate_structure_docs --format both > /dev/null 2>&1
echo "✅ Documentação atualizada!"
```

### Manual

**Gerar quando:**
- Criar uma nova aplicação
- Adicionar/remover models
- Refatorar views
- Alterar estrutura de URLs
- Antes de fazer mudanças importantes

```bash
# Gerar antes de cada alteração
python manage.py generate_structure_docs
git add docs/app_structure/
git commit -m "docs: Atualizar documentacao de estrutura"
```

## Consultando a Documentação

### Para Verificar Nomes Existentes:

1. **Abra `docs/app_structure/STRUCTURE.md`**
2. Procure pela aplicação desejada (Ctrl+F)
3. Verifique:
   - ✅ Models existentes
   - ✅ Views/ViewSets disponíveis
   - ✅ URLs já criadas
   - ✅ Serializers

### Exemplo de Uso:

```markdown
## carga_org_lot

### 📊 Models (3)
- `Patriarca` (linha 15)
  - Métodos: save, get_full_name
- `Organograma` (linha 45)
  - Métodos: save, validate
- `Lotacao` (linha 80)
  - Métodos: save, get_inconsistencies

### 👁️ Views (5)
- `patriarca_list` (function)
- `patriarca_detail` (function)
- `PatriarcaView` (class)
  - Métodos: get, post, put, delete
- `OrganoramaListView` (class)
  - Métodos: get, post

### 🌐 URLs (12)
- patriarcas/
- patriarcas/<int:id>/
- patriarcas/<int:id>/edit/
- organogramas/
- ...
```

## Checklist Antes de Modificar

Antes de **criar uma nova view, model ou URL**:

- [ ] Rodar `python manage.py generate_structure_docs`
- [ ] Abrir `docs/app_structure/STRUCTURE.md`
- [ ] Procurar pelo nome que vou usar (Ctrl+F)
- [ ] Confirmar que **não existe** com esse nome
- [ ] Verificar padrões de nomenclatura usados
- [ ] Criador modelo, view ou URL
- [ ] Atualizar documentação novamente: `python manage.py generate_structure_docs`

## Exemplo Prático

### Cenário: Adicionar nova View em carga_org_lot

1. **Gerar documentação atual:**
   ```bash
   python manage.py generate_structure_docs
   ```

2. **Verificar o que existe:**
   - Abrir `docs/app_structure/STRUCTURE.md`
   - Buscar por `carga_org_lot`
   - Ver todas as views existentes

3. **Verificar nome único:**
   ```bash
   grep -i "meu_nome_view" docs/app_structure/STRUCTURE.md
   ```
   Se retornar vazio, está seguro usar!

4. **Criar a nova view:**
   ```python
   # carga_org_lot/views/meu_nome_view.py
   def meu_nome_view(request):
       pass
   ```

5. **Adicionar à URL:**
   ```python
   # carga_org_lot/urls/__init__.py
   path('novo-endpoint/', web_views.meu_nome_view, name='meu_nome_view'),
   ```

6. **Regenerar documentação:**
   ```bash
   python manage.py generate_structure_docs
   ```

7. **Verificar que apareceu:**
   ```bash
   grep -i "meu_nome_view" docs/app_structure/STRUCTURE.md
   # Deve retornar a linha com sua nova view
   ```

## Troubleshooting

### Comando não funciona

```bash
# Verificar se common/management/ existe
ls -la common/management/
ls -la common/management/commands/

# Se não existir, criar:
mkdir -p common/management/commands
touch common/management/__init__.py
touch common/management/commands/__init__.py
```

### Arquivo não gerado

```bash
# Verificar diretório de saída
ls -la docs/app_structure/

# Se não existir, criar manualmente
mkdir -p docs/app_structure
python manage.py generate_structure_docs
```

### Informações faltando

```bash
# Usar modo verbose para diagnosticar
python manage.py generate_structure_docs --verbose

# Isso mostrará detalhes do processo de geração
```

## Integração com Git

### Adicionar pre-commit hook

```bash
# Criar arquivo
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "Atualizando documentacao de estrutura..."
python manage.py generate_structure_docs --format both 2>/dev/null
if [ $? -eq 0 ]; then
    git add docs/app_structure/ 2>/dev/null
    echo "✅ Documentacao atualizada e staged!"
fi
EOF

# Tornar executável
chmod +x .git/hooks/pre-commit
```

## Performance

- **Primeira execução:** ~2-3 segundos
- **Execuções subsequentes:** ~1-2 segundos
- **Com --verbose:** +0.5 segundos

## Limitações

- Views em arquivos fora de `views.py` ou diretório `views/` podem não ser detectadas
- URLs dinâmicas geradas em runtime não aparecem
- Apenas código estático é analisado (sem imports dinâmicos)

## Contribuindo

Se encontrar problemas ou tiver sugestões:

1. Relatar em GitHub Issues
2. Mencionar:
   - Aplicação afetada
   - Tipo de arquivo (model, view, etc)
   - Saída esperada vs. real
   - Comando executado

---

**Última atualização:** Feb 4, 2026
**Versão:** 1.0
