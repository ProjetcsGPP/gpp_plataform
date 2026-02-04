# ⚡ Checklist Rápido - Antes de Modificar

## Como Usar Este Arquivo

**Toda vez que você vai criar uma nova view, model ou URL:**

1. Rodar comando para gerar documentação
2. Abrir este arquivo para saber o que procurar
3. Procurar no `STRUCTURE.md`
4. Confirmar que o nome não existe

---

## Passo a Passo Rápido

### 1. Gerar/Atualizar Documentação

```bash
# OPÇÃO A: Usar comando Django (melhor)
python manage.py generate_structure_docs

# OPÇÃO B: Script standalone
python docs/generate_structure.py
```

### 2. Consultar Estrutura

```bash
# Abrir no editor
code docs/app_structure/STRUCTURE.md

# Ou verificar via terminal
grep -i "seu_nome_aqui" docs/app_structure/STRUCTURE.md
```

### 3. Verificar Por App

#### 🌟 **carga_org_lot** - Cargas de Organorama e Lotação

**Procure por estes arquivos:**
- `models/` ou `models.py` → Modelos existentes
- `views/` → Views e lógica
- `urls/` → Rotas disponíveis
- `serializers.py` → Serializers de API

**Models que existem:**
```bash
grep "^- .*" docs/app_structure/STRUCTURE.md | grep -A50 "carga_org_lot"
```

**Views que existem:**
```bash
grep -A100 "### .*Views" docs/app_structure/STRUCTURE.md | grep "carga_org_lot" -A20
```

#### 👤 **accounts** - Autenticação e Usuários

**Modelos: User, Role, Permission**
**Views: login, logout, profile**
**Não adicionar modelos com esses nomes**

#### 🌉 **acoes_pngi** - Ações PNGI

**Verifier antes de:**
- Criar novo modelo de ação
- Adicionar nova view de relatório
- Criar nova rota de integração

#### 📄 **portal** - Portal Principal

**Modelos base: Project, Tenant, Config**
**Não usar nomes similares em outras apps**

#### 🗒️ **common** - Utilitários Comuns

**Modelos: Config, Log, AuditTrail**
**Views: dashboard, statistics**

#### 💫 **auth_service** - Serviço de Autenticação

**Views: authenticate, token, refresh**
**Serializers: AuthSerializer, TokenSerializer**

---

## Checklist Por Tipo

### 📊 Adicionando um Novo Model

- [ ] Abrir `docs/app_structure/STRUCTURE.md`
- [ ] Procurar (Ctrl+F) por "Models" da sua app
- [ ] Verificar que o nome não existe
- [ ] Procurar no código: `grep -r "class MeuModel" .`
- [ ] Se vazio, seguro criar!
- [ ] Criar o model
- [ ] Rodar: `python manage.py generate_structure_docs`
- [ ] Verificar que apareceu na documentação

### 👁️ Adicionando uma Nova View

- [ ] Abrir `docs/app_structure/STRUCTURE.md`
- [ ] Procurar (Ctrl+F) por "Views" da sua app
- [ ] Verificar que o nome não existe
- [ ] Procurar no código: `grep -r "def minha_view" .`
- [ ] Se vazio, seguro criar!
- [ ] Criar a view
- [ ] Rodar: `python manage.py generate_structure_docs`
- [ ] Verificar que apareceu

### 🌐 Adicionando uma Nova URL

- [ ] Abrir `docs/app_structure/STRUCTURE.md`
- [ ] Procurar (Ctrl+F) por "URLs" da sua app
- [ ] Verificar que a rota não existe
- [ ] Procurar no código: `grep -r "minha-rota" .`
- [ ] Se vazio, seguro criar!
- [ ] Adicionar a rota em `urls.py`
- [ ] Rodar: `python manage.py generate_structure_docs`
- [ ] Verificar que apareceu

### 📝 Adicionando um Novo Serializer

- [ ] Abrir `docs/app_structure/STRUCTURE.md`
- [ ] Procurar (Ctrl+F) por "Serializers" da sua app
- [ ] Verificar que não existe
- [ ] Criar o serializer
- [ ] Rotar: `python manage.py generate_structure_docs`
- [ ] Verificar que apareceu

---

## Comandos Ãteis

### Buscar Por Nome
```bash
# Verificar se nome já existe em todo projeto
grep -r "meu_nome" . --include="*.py"

# Verificar na documentação
grep "meu_nome" docs/app_structure/STRUCTURE.md
```

### Buscar Por Padrão

```bash
# Encontrar todos os models que herdam de Model
grep -r "class.*Model" . --include="models.py"

# Encontrar todas as views
grep -r "^def.*view" . --include="views.py"

# Encontrar todas as URLs
grep -r "path(" . --include="urls.py"
```

### Atualizar Documentação

```bash
# Gerar em ambos os formatos
python manage.py generate_structure_docs

# Apenas JSON (rápido)
python manage.py generate_structure_docs --format json

# Apenas Markdown (legvel)
python manage.py generate_structure_docs --format markdown
```

---

## Erros Comuns

### Erro: "View não encontrada"

**Causa:** URL referencia view que não existe  
**Solução:**
1. Abrir `docs/app_structure/STRUCTURE.md`
2. Verificar nome da view na app
3. Conferir if o nome está correto em `urls.py`
4. Verificar se foi exportada em `views/__init__.py`

### Erro: "Reverse for 'nome' not found"

**Causa:** URL com esse name não existe  
**Solução:**
1. Procurar no `STRUCTURE.md` pela URL
2. Se não existe, criar
3. Se existe, verificar o `name=` do path
4. Atualizar template com nome correto

### Erro: "Model does not exist"

**Causa:** Model referenciado não foi definido  
**Solução:**
1. Procurar no `STRUCTURE.md` → Models
2. Se não existe, criar
3. Se existe, verificar se foi exportado
4. Rodar migrations: `python manage.py migrate`

---

## Integrando com Pre-Commit

**Fazer gerar automaticamente antes de cada commit:**

```bash
# Criar hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "🔄 Gerando documentação de estrutura..."
python manage.py generate_structure_docs --format both 2>/dev/null
if [ -f docs/app_structure/STRUCTURE.md ]; then
    git add docs/app_structure/ 2>/dev/null
    echo "✅ Documentação atualizada!"
fi
EOF

# Tornar executável
chmod +x .git/hooks/pre-commit
```

Agora toda vez que você fizer commit, a documentação é atualizada automaticamente! 🌟

---

## Referência Rápida

| Aplicação | Purpose | Modelos | Views |
|---|---|---|---|
| `accounts` | Usuários & Auth | User, Role, Perm | login, profile |
| `acoes_pngi` | Ações PNGI | Acao, Relatorio | acoes_list, detail |
| `carga_org_lot` | Carga de Org | Patriarca, Organo | patriarca_list |
| `portal` | Portal Principal | Project, Tenant | dashboard |
| `common` | Utilitários | Config, Log | stats, config |
| `auth_service` | Autenticação | Token, Session | auth, refresh |
| `db_service` | Banco de Dados | - | - |

---

**📈 Sempre consulte `docs/app_structure/STRUCTURE.md` antes de modificar!**
