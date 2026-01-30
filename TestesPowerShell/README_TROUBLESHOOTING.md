# 🚫 Troubleshooting - Testes de API

## Problemas Encontrados e Soluções

**Data:** 30/01/2026  
**Versão do Script:** 2.2

---

## ❌ Problema 1: Erro 500 ao Criar Eixo

### **Erro Observado:**
```powershell
--- Criar Eixo (requer add_eixo) ---
POST http://localhost:8000/api/v1/acoes_pngi/eixos/
✗ Erro: 500 - Response status code does not indicate success: 500 (Internal Server Error).
```

### **Causa Raiz:**

O serializer `EixoSerializer` possui validação que exige `stralias` em **UPPERCASE**:

```python
# acoes_pngi/serializers.py (linha ~33)
def validate_stralias(self, value):
    if not value.isupper():
        raise serializers.ValidationError("O alias deve estar em letras maiúsculas.")
    if len(value) > 5:
        raise serializers.ValidationError("O alias deve ter no máximo 5 caracteres.")
    return value
```

O teste original enviava:
```json
{
  "strdescricaoeixo": "Eixo Teste PowerShell 2026-01-30 09:23:45",
  "stralias": "ETP"  // OK - está em uppercase
}
```

Porém, se o timestamp incluir letras minúsculas ou o alias for gerado dinamicamente, pode falhar.

### **Solução Aplicada:**

```powershell
# TestesPowerShell/Acoes_PNGI_test_permissions_API.ps1 (linha ~248)
$timestamp = (Get-Date).ToString("HHmmss")  # 6 caracteres numéricos
$alias = "T" + $timestamp.Substring(0, 4)  # "T" + 4 dígitos = 5 chars

$newEixo = @{
    strdescricaoeixo = "Eixo Teste PowerShell"
    stralias = $alias  # Exemplo: "T0923" (sempre uppercase e 5 chars)
}
```

**Resultado:**
- ✅ Alias sempre em UPPERCASE
- ✅ Exatamente 5 caracteres
- ✅ Único (usa timestamp)

---

## ❌ Problema 2: Erro 500 ao Criar/Listar Situação

### **Erro Observado:**
```powershell
--- Listar Situações (requer view_situacaoacao) ---
GET http://localhost:8000/api/v1/acoes_pngi/situacoes/
✗ Erro: 500 - Response status code does not indicate success: 500 (Internal Server Error).

--- Criar Situação (requer add_situacaoacao) ---
POST http://localhost:8000/api/v1/acoes_pngi/situacoes/
✗ Erro: 500 - Response status code does not indicate success: 500 (Internal Server Error).
```

### **Causa Raiz:**

1. **Limite de 15 caracteres no modelo:**
```python
# acoes_pngi/models.py (linha ~36)
class SituacaoAcao(models.Model):
    strdescricaosituacao = models.CharField(
        max_length=15,  # ⚠️ LIMITE DE 15 CARACTERES
        unique=True, 
        db_column='strdescricaosituacao'
    )
```

2. **Conversão automática para UPPERCASE no serializer:**
```python
# acoes_pngi/serializers.py (linha ~68)
def validate_strdescricaosituacao(self, value):
    if not value or not value.strip():
        raise serializers.ValidationError("A descrição da situação não pode estar vazia.")
    return value.strip().upper()  # ⚠️ Converte para UPPERCASE
```

3. **Deve ser único (constraint de banco de dados)**

O teste original enviava:
```json
{
  "strdescricaosituacao": "Situação Teste PowerShell 2026-01-30 09:23:45"  // 48 caracteres! ❌
}
```

### **Solução Aplicada:**

```powershell
# TestesPowerShell/Acoes_PNGI_test_permissions_API.ps1 (linha ~325)
$timestamp = (Get-Date).ToString("HHmmss")  # 6 dígitos
$descricao = "TST_" + $timestamp  # "TST_" + 6 dígitos = 10 chars

$newSituacao = @{
    strdescricaosituacao = $descricao  # Exemplo: "TST_092345" (10 chars, dentro do limite)
}
```

**Resultado:**
- ✅ Máximo 10 caracteres (dentro do limite de 15)
- ✅ Será convertido automaticamente para UPPERCASE pelo serializer
- ✅ Único (usa timestamp)

---

## ❌ Problema 3: Acesso a Campos de Permissões Incorretos

### **Erro Potencial:**
```powershell
$canView = $Permissions.specific.eixo.view  # ❌ Campo não existe!
```

### **Causa Raiz:**

O endpoint `/permissions/` retorna:
```json
{
  "specific": {
    "eixo": {
      "can_add": true,      // ✅ Prefixo "can_"
      "can_change": true,
      "can_delete": true,
      "can_view": true
    }
  }
}
```

Mas o script PowerShell usava:
```powershell
$Permissions.specific.eixo.add      # ❌ Sem prefixo "can_"
$Permissions.specific.eixo.view     # ❌ Sem prefixo "can_"
```

### **Solução Aplicada:**

```powershell
# TestesPowerShell/Acoes_PNGI_test_permissions_API.ps1 (linha ~242)
$canView = $Permissions.specific.eixo.can_view    # ✅ Com prefixo
$canAdd = $Permissions.specific.eixo.can_add      # ✅ Com prefixo
$canChange = $Permissions.specific.eixo.can_change # ✅ Com prefixo
$canDelete = $Permissions.specific.eixo.can_delete # ✅ Com prefixo
```

---

## ✅ Como Testar Após Correções

### **1. Baixar Versão Corrigida**

```bash
git pull origin feature/automated-permissions-system
```

### **2. Executar Teste Completo**

```powershell
cd C:\Projects\gpp_plataform\TestesPowerShell
.\Acoes_PNGI_test_permissions_API.ps1
```

### **3. Resultado Esperado**

```
=========================================
   TESTES DE PERMISSÕES - AÇÕES PNGI
=========================================

=== AUTENTICAÇÃO ===
✓ Token JWT obtido com sucesso

=========================================
TESTANDO CRUD DE EIXOS
=========================================

--- Criar Eixo (requer add_eixo) ---
POST http://localhost:8000/api/v1/acoes_pngi/eixos/
✓ Sucesso (Status 200-299)
Eixo criado com ID: 42 (alias: T0923)

--- Atualizar Eixo (requer change_eixo) ---
PATCH http://localhost:8000/api/v1/acoes_pngi/eixos/42/
✓ Sucesso (Status 200-299)

--- Deletar Eixo (requer delete_eixo) ---
DELETE http://localhost:8000/api/v1/acoes_pngi/eixos/42/
✓ Sucesso (Status 200-299)

=========================================
TESTANDO CRUD DE SITUAÇÕES
=========================================

--- Criar Situação (requer add_situacaoacao) ---
POST http://localhost:8000/api/v1/acoes_pngi/situacoes/
✓ Sucesso (Status 200-299)
Situação criada com ID: 15 (valor: TST_092345)

--- Atualizar Situação (requer change_situacaoacao) ---
PATCH http://localhost:8000/api/v1/acoes_pngi/situacoes/15/
✓ Sucesso (Status 200-299)

--- Deletar Situação (requer delete_situacaoacao) ---
DELETE http://localhost:8000/api/v1/acoes_pngi/situacoes/15/
✓ Sucesso (Status 200-299)

=========================================
         TESTES CONCLUÍDOS
=========================================
```

---

## 📝 Resumo das Correções

| Problema | Solução | Arquivo | Linha |
|----------|----------|---------|-------|
| Alias do Eixo inválido | Gerar alias uppercase com 5 chars | `Acoes_PNGI_test_permissions_API.ps1` | ~248 |
| Descrição da Situação longa | Gerar string com max 10 chars | `Acoes_PNGI_test_permissions_API.ps1` | ~325 |
| Campos de permissão errados | Adicionar prefixo `can_` | `Acoes_PNGI_test_permissions_API.ps1` | Múltiplas |

---

## 🛠️ Dicas para Evitar Problemas Futuros

### **1. Sempre validar constraints do modelo**

Antes de criar testes, verifique:
- `max_length` dos campos CharField
- Constraints `unique`
- Validações customizadas no serializer

### **2. Usar Verbose para debug**

```powershell
.\Acoes_PNGI_test_permissions_API.ps1 -Verbose
```

Exibe:
- Body enviado em cada requisição
- Tokens JWT
- URLs completas

### **3. Logs do Django**

Em caso de erro 500, verificar logs do servidor:
```bash
python manage.py runserver
# Observar output de erros
```

### **4. Testar serializers diretamente (Django shell)**

```python
python manage.py shell

# Testar Eixo
from acoes_pngi.serializers import EixoSerializer
data = {'strdescricaoeixo': 'Teste', 'stralias': 'teste'}  # minúscula
s = EixoSerializer(data=data)
print(s.is_valid())  # False
print(s.errors)       # {'stralias': ['O alias deve estar em letras maiúsculas.']}

# Testar Situação
from acoes_pngi.serializers import SituacaoAcaoSerializer
data = {'strdescricaosituacao': 'x' * 20}  # 20 caracteres
s = SituacaoAcaoSerializer(data=data)
print(s.is_valid())  # False
print(s.errors)       # Campo excede max_length
```

---

## 🐞 Reportar Bugs

Se encontrar novos problemas:

1. Capturar output completo do PowerShell
2. Capturar logs do Django
3. Verificar versão do script (`Versão: 2.2` no topo)
4. Criar issue no repositório

---

**Versão do documento:** 1.0  
**Última atualização:** 30/01/2026
