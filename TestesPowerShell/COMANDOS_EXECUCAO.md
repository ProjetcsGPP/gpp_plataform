# 🚀 Comandos de Execução dos Testes

## ⚡ Copie e Cole os Comandos Abaixo

### 1️⃣ Teste Apenas Ações PNGI

```powershell
# Teste completo da app Ações PNGI (web views + API + context)
.\TestesPowerShell\Test-AcoesPNGI-Complete.ps1
```

**Tempo de execução:** ~30-45 segundos

**O que testa:**
- ✅ Testes unitários Django (context_processors)
- ✅ Views web (4 páginas)
- ✅ API REST endpoints (4 endpoints)
- ✅ Context API para Next.js (4 endpoints)

**Resultado esperado:**
```
✓ Testes unitários executados com sucesso!
✓ Views Web: 4/4 passou
✓ API REST: 4/4 passou
✓ Contexto API: 4/4 passou
🎉 TODOS OS TESTES PASSARAM!
```

---

### 2️⃣ Teste Todas as Aplicações

```powershell
# Teste completo de TODAS as apps (carga_org_lot + acoes_pngi)
.\TestesPowerShell\Test-AllApps-Complete.ps1
```

**Tempo de execução:** ~1-2 minutos

**O que testa:**
- ✅ Ações PNGI (views web, API, context)
- ✅ Carga e Organização de Lotes (views web, API, context)
- ✅ Testes unitários de ambas as apps

**Resultado esperado:**
```
📋 APP: Ações PNGI (acoes_pngi)
✓ Unit Tests: PASSOU
✓ Web Views:  4/4 passou
✓ API REST:   4/4 passou

📋 APP: Carga e Organização de Lotes (carga_org_lot)
✓ Unit Tests: PASSOU
✓ Web Views:  3/3 passou
✓ API REST:   3/3 passou

🎉 TODOS OS TESTES PASSARAM!
```

---

### 3️⃣ Teste Vigências PNGI (Sem Autenticação)

```powershell
# Testa vigências sem criar/ativar (apenas GET)
.\TestesPowerShell\Test-Vigencia-Complete.ps1
```

**Tempo de execução:** ~10-15 segundos

**O que testa:**
- ✅ Listar vigências (GET /vigencias/)
- ✅ Buscar vigência ativa (GET /vigencias/vigencia_ativa/)
- ⚠️ Cria/ativa de vigência (requer token)

**Resultado esperado:**
```
1. LISTANDO VIGÊNCIAS
✓ Status: 200
  Total de vigências encontradas: 3

2. BUSCANDO VIGÊNCIA ATIVA (ATUAL)
✓ Vigência ativa encontrada (Status: 200)
  ID: 3
  Descrição: Vigência 2026
  Ativa: True

✓ Vigência está corretamente marcada como ativa
```

---

### 4️⃣ Teste Vigências PNGI (Com Autenticação)

```powershell
# Testa vigências com criação/ativação (requer JWT token)
.\TestesPowerShell\Test-Vigencia-Complete.ps1 -Token "seu_jwt_token_aqui"
```

**Tempo de execução:** ~15-30 segundos

**O que testa (EXTRA):**
- ✅ Criar vigência de teste
- ✅ Ativar vigência
- ✅ Validar que vigência ativa retorna dados

**Como obter o token:**

```powershell
# Opção 1: Via Python Django Shell
python manage.py shell
```

```python
from rest_framework.authtoken.models import Token
from accounts.models import User

user = User.objects.get(email='seu_email@example.com')
token, created = Token.objects.get_or_create(user=user)
print(f"Token: {token.key}")
# Copie o token e use no comando acima
```

```powershell
# Depois use:
.\TestesPowerShell\Test-Vigencia-Complete.ps1 -Token "token_copiado_acima"
```

---

## 🔄 Pipeline Completo Recomendado

```powershell
# 1. Ativar virtualenv
.\venv\Scripts\Activate.ps1

# 2. Iniciar servidor Django (em outro terminal PowerShell)
# python manage.py runserver
# (execute em OUTRO terminal)

# 3. Volte ao terminal original e execute:

# Teste 1: Apenas Ações PNGI
.\TestesPowerShell\Test-AcoesPNGI-Complete.ps1

# Teste 2: Todas as aplicações
.\TestesPowerShell\Test-AllApps-Complete.ps1

# Teste 3: Vigências (sem token)
.\TestesPowerShell\Test-Vigencia-Complete.ps1

# Teste 4: Vigências (com token - opcional)
.\TestesPowerShell\Test-Vigencia-Complete.ps1 -Token "seu_token"
```

---

## 📊 Resumo de Testes

| Teste | Comando | Tempo | Cobertura |
|-------|---------|-------|----------|
| Ações PNGI | `.\Test-AcoesPNGI-Complete.ps1` | 30-45s | Web + API + Context |
| Todas as Apps | `.\Test-AllApps-Complete.ps1` | 1-2m | Múltiplas apps |
| Vigências (read) | `.\Test-Vigencia-Complete.ps1` | 10-15s | GET endpoints |
| Vigências (full) | `.\Test-Vigencia-Complete.ps1 -Token "..."` | 15-30s | CRUD completo |

---

## ✅ Checklist de Validação

Antes de fazer MERGE/DEPLOY:

```powershell
# Executar os 3 testes principais em sequência:

# 1. Teste Ações PNGI
.\TestesPowerShell\Test-AcoesPNGI-Complete.ps1
# ☐ Verificar se passou

# 2. Teste Todas as Apps
.\TestesPowerShell\Test-AllApps-Complete.ps1
# ☐ Verificar se passou

# 3. Teste Vigências
.\TestesPowerShell\Test-Vigencia-Complete.ps1
# ☐ Verificar se passou

# Se TODOS passarem:
# ✅ Pronto para merge na branch main
# ✅ Pronto para deploy em produção
```

---

## 🐛 Troubleshooting Rápido

### Erro: "Python not found"

```powershell
# Solução: Ativar virtualenv
.\venv\Scripts\Activate.ps1

# Depois tentar novamente
.\TestesPowerShell\Test-AcoesPNGI-Complete.ps1
```

### Erro: "Connection refused"

```powershell
# Solução: Iniciar Django em outro terminal
# Em OUTRO PowerShell:
python manage.py runserver

# Depois volte ao terminal original e execute os testes
```

### Erro: "Scripts disabled on this system"

```powershell
# Solução: Permitir execução de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Depois tentar novamente
.\TestesPowerShell\Test-AcoesPNGI-Complete.ps1
```

---

## 📝 Informações Adicionais

### URLs Testadas (Ações PNGI)

**Web Views:**
- GET http://localhost:8000/acoes_pngi/
- GET http://localhost:8000/acoes_pngi/eixos/
- GET http://localhost:8000/acoes_pngi/situacoes/
- GET http://localhost:8000/acoes_pngi/vigencias/

**API REST:**
- GET http://localhost:8000/api/v1/acoes_pngi/eixos/
- GET http://localhost:8000/api/v1/acoes_pngi/situacoes/
- GET http://localhost:8000/api/v1/acoes_pngi/vigencias/
- GET http://localhost:8000/api/v1/acoes_pngi/vigencias/vigencia_ativa/

**Context API (Next.js):**
- GET http://localhost:8000/api/v1/acoes_pngi/context/app/
- GET http://localhost:8000/api/v1/acoes_pngi/context/permissions/
- GET http://localhost:8000/api/v1/acoes_pngi/context/models/
- GET http://localhost:8000/api/v1/acoes_pngi/context/full/

---

## 🎯 Próximos Passos Após Testes

1. ✅ **Testes Passaram?**
   - Fazer commit dos testes em PowerShell
   - Fazer merge da branch `feat/acoes-pngi-context-processors-update` para `main`
   - Fazer deploy em staging para validação

2. ❌ **Testes Falharam?**
   - Revisar logs no arquivo de teste
   - Verificar erros específicos
   - Corrigir o código
   - Executar testes novamente

---

**Última atualização:** 2026-02-05
**Status:** ✅ Pronto para uso
