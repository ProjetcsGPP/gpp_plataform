# Testes Completos do GPP Platform

Guia de execução de testes para web views, APIs e context processors.

## 📋 Scripts Disponíveis

### 1. **Test-AcoesPNGI-Complete.ps1**
Testa APENAS a aplicação Ações PNGI

**O que testa:**
- ✅ Testes unitários Django (context_processors)
- ✅ Views web (renderização de templates)
- ✅ Endpoints REST API
- ✅ Endpoints de contexto para Next.js

**Localização:** `TestesPowerShell/Test-AcoesPNGI-Complete.ps1`

---

### 2. **Test-AllApps-Complete.ps1**
Testa TODAS as aplicações do platform

**O que testa:**
- ✅ Testes unitários Django para cada app
- ✅ Views web de cada aplicação
- ✅ Endpoints REST API
- ✅ Endpoints de contexto para Next.js

**Aplicações testadas:**
- carga_org_lot
- acoes_pngi

**Localização:** `TestesPowerShell/Test-AllApps-Complete.ps1`

---

### 3. **Test-Vigencia-Complete.ps1**
Testa CRUD completo de Vigências PNGI

**O que testa:**
- ✅ Listar todas as vigências
- ✅ Buscar vigência ativa (retorna 404 se vazia, conforme esperado)
- ✅ Criar vigência de teste
- ✅ Ativar vigência
- ✅ Validar que vigência ativa retorna dados corretos

**Localização:** `TestesPowerShell/Test-Vigencia-Complete.ps1`

---

## 🚀 Como Executar

### Pré-requisitos

1. **PowerShell 5.0+** (Windows)
2. **Django server rodando** em `http://localhost:8000`
3. **Python virtualenv ativado** (com Django instalado)
4. **Permissão de execução** de scripts PowerShell (se necessário)

```powershell
# Permitir execução de scripts (execute uma vez)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📝 Comandos de Execução

### Opção 1: Testar Apenas Ações PNGI

```powershell
# Básico
.\TestesPowerShell\Test-AcoesPNGI-Complete.ps1

# Com verbose
.\TestesPowerShell\Test-AcoesPNGI-Complete.ps1 -Verbose

# Com URL customizada
.\TestesPowerShell\Test-AcoesPNGI-Complete.ps1 -BaseURL "http://seu-server:8000"
```

**Saída esperada:**
```
✓ Testes unitários executados com sucesso!
✓ Views Web:    4/4 passou
✓ API REST:     4/4 passou
✓ Contexto API: 4/4 passou
🎉 TODOS OS TESTES PASSARAM!
```

---

### Opção 2: Testar Todas as Aplicações

```powershell
# Teste padrão (carga_org_lot + acoes_pngi)
.\TestesPowerShell\Test-AllApps-Complete.ps1

# Com verbose
.\TestesPowerShell\Test-AllApps-Complete.ps1 -Verbose

# Apenas aplicações específicas
.\TestesPowerShell\Test-AllApps-Complete.ps1 -Apps @('acoes_pngi')

# Com URL customizada
.\TestesPowerShell\Test-AllApps-Complete.ps1 -BaseURL "http://seu-server:8000"
```

**Saída esperada:**
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
Pronto para deploy!
```

---

### Opção 3: Testar Vigências PNGI

```powershell
# Teste sem autenticação (apenas leitura)
.\TestesPowerShell\Test-Vigencia-Complete.ps1

# Teste completo (com criação/ativação de vigência)
.\TestesPowerShell\Test-Vigencia-Complete.ps1 -Token "seu_jwt_token"

# Com URL customizada
.\TestesPowerShell\Test-Vigencia-Complete.ps1 -BaseURL "http://seu-server:8000" -Token "seu_jwt_token"
```

**Saída esperada (sem token):**
```
1. LISTANDO VIGÊNCIAS
✓ Status: 200
  Total de vigências encontradas: 3
  Primeiras vigências:
    - ID: 1, Descrição: Vigência 2024, Ativa: False
    - ID: 2, Descrição: Vigência 2025, Ativa: False
    - ID: 3, Descrição: Vigência 2026, Ativa: True

2. BUSCANDO VIGÊNCIA ATIVA (ATUAL)
✓ Vigência ativa encontrada (Status: 200)
  ID: 3
  Descrição: Vigência 2026
  Ativa: True

✓ Vigência está corretamente marcada como ativa
```

---

## 🎯 O que Cada Teste Valida

### Test-AcoesPNGI-Complete.ps1

#### 1. Testes Unitários (Django)
- ✅ `context_processors.py` funciona corretamente
- ✅ Permissões são calculadas corretamente
- ✅ Contexto da app está disponível
- ✅ Informações dos modelos são retornadas

#### 2. Views Web
- ✅ GET `/acoes_pngi/` → 200 ou 403 (auth)
- ✅ GET `/acoes_pngi/eixos/` → 200 ou 403
- ✅ GET `/acoes_pngi/situacoes/` → 200 ou 403
- ✅ GET `/acoes_pngi/vigencias/` → 200 ou 403

#### 3. API REST
- ✅ GET `/api/v1/acoes_pngi/eixos/` → 200
- ✅ GET `/api/v1/acoes_pngi/situacoes/` → 200
- ✅ GET `/api/v1/acoes_pngi/vigencias/` → 200
- ✅ GET `/api/v1/acoes_pngi/vigencias/vigencia_ativa/` → 200 ou 404

#### 4. Context API (para Next.js)
- ✅ GET `/api/v1/acoes_pngi/context/app/` → retorna código, nome, icon
- ✅ GET `/api/v1/acoes_pngi/context/permissions/` → retorna permissões do usuário
- ✅ GET `/api/v1/acoes_pngi/context/models/` → retorna metadata dos modelos
- ✅ GET `/api/v1/acoes_pngi/context/full/` → retorna tudo integrado

---

## 🔍 Interpretando Resultados

### Status Codes Esperados

| Status | Significado | Reação |
|--------|-------------|--------|
| **200** | OK - Requisição bem-sucedida | ✅ Teste passa |
| **201** | Created - Recurso criado | ✅ Teste passa |
| **301/302** | Redirect (auth) | ✅ Teste passa (esperado sem auth) |
| **403** | Forbidden - Sem permissão | ✅ Teste passa (esperado sem auth) |
| **401** | Unauthorized - Não autenticado | ✅ Teste passa (esperado sem token) |
| **404** | Not Found | ⚠️ Depende do contexto (veja abaixo) |
| **500** | Server Error | ❌ Teste falha |

### Casos Especiais

#### 1. Vigência Ativa Retornando 404

**Esperado:** ✅ Correto

Quando nenhuma vigência está ativa no banco de dados:
```
GET /api/v1/acoes_pngi/vigencias/vigencia_ativa/
→ 404 Not Found (com mensagem "Nenhuma vigência ativa encontrada")
```

**Solução:** Crie e ative uma vigência usando o test script com token

#### 2. Endpoints Retornando 403 Sem Autenticação

**Esperado:** ✅ Correto (segurança)

Se não tiver JWT token:
```
GET /api/v1/acoes_pngi/eixos/
→ 403 Forbidden
```

**Solução:** Obtenha um token JWT e execute:
```powershell
.\Test-AcoesPNGI-Complete.ps1 -Token "seu_jwt_token"
```

---

## 🐛 Troubleshooting

### Erro: "Python not found"

```powershell
# Ativar virtualenv antes de executar
.\venv\Scripts\Activate.ps1

# Depois executar o teste
.\TestesPowerShell\Test-AcoesPNGI-Complete.ps1
```

### Erro: "Connection refused" ou "Server not running"

```powershell
# Iniciar Django em outro terminal PowerShell
python manage.py runserver

# Depois executar os testes
.\TestesPowerShell\Test-AcoesPNGI-Complete.ps1
```

### Erro: "Scripts disabled on this system"

```powershell
# Permitir execução de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ou executar com Unblock-File
Unblock-File -Path ".\TestesPowerShell\Test-AcoesPNGI-Complete.ps1"
```

---

## 📊 Pipeline de Testes Recomendado

**Ordem sugerida de execução:**

```powershell
# 1. Teste individual da app mais recente
.\TestesPowerShell\Test-AcoesPNGI-Complete.ps1

# 2. Teste completo de todas as apps
.\TestesPowerShell\Test-AllApps-Complete.ps1

# 3. Teste específico de vigências (com dados)
.\TestesPowerShell\Test-Vigencia-Complete.ps1 -Token "seu_jwt_token"
```

---

## 🔐 Obtendo Token JWT para Testes

### Via Endpoint de Autenticação

```powershell
$loginData = @{
    "email" = "seu_email@example.com"
    "password" = "sua_senha"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login/" `
    -Method POST `
    -Body $loginData `
    -Headers @{'Content-Type' = 'application/json'}

$token = $response.token
Write-Host "Token: $token"

# Depois usar no teste
.\TestesPowerShell\Test-AcoesPNGI-Complete.ps1 -Token $token
```

### Via Django Shell

```powershell
python manage.py shell
```

```python
from rest_framework.authtoken.models import Token
from accounts.models import User

user = User.objects.get(email='seu_email@example.com')
token, created = Token.objects.get_or_create(user=user)
print(f"Token: {token.key}")
```

---

## ✅ Checklist de Validação

Antes de fazer merge/deploy:

- [ ] Testes unitários Django passam
- [ ] Views web acessíveis (200 ou 403 esperado)
- [ ] Endpoints API retornam dados corretos
- [ ] Context API endpoints funcionam
- [ ] Vigências podem ser listadas
- [ ] Vigência ativa pode ser buscada (retorna dados quando existir)
- [ ] Sem erros 500 ou exceptions
- [ ] Logs do Django não mostram warnings graves

---

## 📞 Referências

- [Documentação Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [PowerShell Invoke-RestMethod](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod)

---

**Última atualização:** 2026-02-05
**Status:** ✅ Pronto para uso
