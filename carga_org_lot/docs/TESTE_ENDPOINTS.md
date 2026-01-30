# Guia de Testes dos Endpoints - Carga Org/Lot

## Pré-requisitos

### 1. Servidor Rodando

```bash
python manage.py runserver
```

### 2. Obter Token de Autenticação

**Opção 1: Via Django Admin**
1. Acesse `http://localhost:8000/admin/`
2. Login com superusuário
3. Vá em "Auth Token" > "Tokens"
4. Copie o token do seu usuário

**Opção 2: Via Python Shell**
```python
python manage.py shell

from rest_framework.authtoken.models import Token
from accounts.models import User

user = User.objects.get(email='seu_email@example.com')
token, created = Token.objects.get_or_create(user=user)
print(f"Token: {token.key}")
```

### 3. Configurar Variável de Ambiente

```bash
# Bash/Linux/Mac
export TOKEN="seu_token_aqui"

# Windows CMD
set TOKEN=seu_token_aqui

# Windows PowerShell
$env:TOKEN="seu_token_aqui"
```

---

## Testes dos Endpoints

### 1. Permissões do Usuário

```bash
# Buscar permissões
curl -X GET "http://localhost:8000/api/v1/carga/permissions/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

**Resultado esperado:**
- Status: 200 OK
- JSON com: user_id, email, role, permissions[], groups{}, specific{}

---

### 2. Dashboard

```bash
# Estatísticas gerais
curl -X GET "http://localhost:8000/api/v1/carga/dashboard/" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# Estatísticas de um patriarca específico
curl -X GET "http://localhost:8000/api/v1/carga/dashboard/?patriarca=1" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

**Resultado esperado:**
- Status: 200 OK
- JSON com: patriarcas{}, organogramas{}, lotacoes{}, cargas{}

---

### 3. Patriarcas

#### 3.1 Listar Patriarcas

```bash
# Listar todos
curl -X GET "http://localhost:8000/api/v1/carga/patriarcas/" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# Listar com filtro por sigla
curl -X GET "http://localhost:8000/api/v1/carga/patriarcas/?sigla=SEGER" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# Listagem otimizada (light)
curl -X GET "http://localhost:8000/api/v1/carga/patriarcas/list_light/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 3.2 Criar Patriarca

```bash
curl -X POST "http://localhost:8000/api/v1/carga/patriarcas/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "str_sigla_patriarca": "TESTE",
    "str_nome": "Patriarca de Teste",
    "id_status_progresso": 1
  }' \
  | jq .
```

#### 3.3 Buscar Patriarca

```bash
# Substituir {id} pelo ID retornado na criação
curl -X GET "http://localhost:8000/api/v1/carga/patriarcas/{id}/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 3.4 Atualizar Patriarca

```bash
# Atualização parcial (PATCH)
curl -X PATCH "http://localhost:8000/api/v1/carga/patriarcas/{id}/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "str_nome": "Patriarca de Teste Atualizado"
  }' \
  | jq .
```

#### 3.5 Organogramas do Patriarca

```bash
curl -X GET "http://localhost:8000/api/v1/carga/patriarcas/{id}/organogramas/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 3.6 Lotações do Patriarca

```bash
curl -X GET "http://localhost:8000/api/v1/carga/patriarcas/{id}/lotacoes/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 3.7 Estatísticas do Patriarca

```bash
curl -X GET "http://localhost:8000/api/v1/carga/patriarcas/{id}/estatisticas/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 3.8 Deletar Patriarca

```bash
curl -X DELETE "http://localhost:8000/api/v1/carga/patriarcas/{id}/" \
  -H "Authorization: Token $TOKEN"
```

**Resultado esperado:** Status 204 No Content

---

### 4. Organogramas

#### 4.1 Listar Organogramas

```bash
# Todos
curl -X GET "http://localhost:8000/api/v1/carga/organogramas/" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# De um patriarca específico
curl -X GET "http://localhost:8000/api/v1/carga/organogramas/?patriarca=1" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# Apenas ativos
curl -X GET "http://localhost:8000/api/v1/carga/organogramas/?patriarca=1&ativos=true" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 4.2 Detalhe de Organograma

```bash
curl -X GET "http://localhost:8000/api/v1/carga/organogramas/{id}/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 4.3 Órgãos do Organograma (flat)

```bash
curl -X GET "http://localhost:8000/api/v1/carga/organogramas/{id}/orgaos/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 4.4 Hierarquia do Organograma (árvore)

```bash
curl -X GET "http://localhost:8000/api/v1/carga/organogramas/{id}/hierarquia/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 4.5 JSON de Envio

```bash
curl -X GET "http://localhost:8000/api/v1/carga/organogramas/{id}/json_envio/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 4.6 Ativar Organograma (requer Coordenador+)

```bash
curl -X POST "http://localhost:8000/api/v1/carga/organogramas/{id}/ativar/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

---

### 5. Órgãos/Unidades

#### 5.1 Listar Órgãos

```bash
# Todos
curl -X GET "http://localhost:8000/api/v1/carga/orgaos/" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# De um patriarca
curl -X GET "http://localhost:8000/api/v1/carga/orgaos/?patriarca=1" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# De um organograma
curl -X GET "http://localhost:8000/api/v1/carga/orgaos/?organograma=1" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# Apenas raiz (sem pai)
curl -X GET "http://localhost:8000/api/v1/carga/orgaos/?raiz=true" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# Busca textual
curl -X GET "http://localhost:8000/api/v1/carga/orgaos/?q=SEGER" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 5.2 Busca Rápida (Autocomplete)

```bash
curl -X GET "http://localhost:8000/api/v1/carga/search/orgao/?q=SE" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# Com filtro de patriarca
curl -X GET "http://localhost:8000/api/v1/carga/search/orgao/?q=SE&patriarca_id=1" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

---

### 6. Lotações

#### 6.1 Listar Lotações

```bash
# Todas
curl -X GET "http://localhost:8000/api/v1/carga/lotacoes/" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# De um patriarca
curl -X GET "http://localhost:8000/api/v1/carga/lotacoes/?patriarca=1" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# Apenas ativas
curl -X GET "http://localhost:8000/api/v1/carga/lotacoes/?ativas=true" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 6.2 Registros de Lotação (paginado)

```bash
# Página 1, 100 registros
curl -X GET "http://localhost:8000/api/v1/carga/lotacoes/{id}/registros/" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# Página 2, 50 registros
curl -X GET "http://localhost:8000/api/v1/carga/lotacoes/{id}/registros/?page=2&page_size=50" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# Apenas válidos
curl -X GET "http://localhost:8000/api/v1/carga/lotacoes/{id}/registros/?valido=true" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# Busca por CPF
curl -X GET "http://localhost:8000/api/v1/carga/lotacoes/{id}/registros/?cpf=123" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 6.3 Inconsistências

```bash
curl -X GET "http://localhost:8000/api/v1/carga/lotacoes/{id}/inconsistencias/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 6.4 Estatísticas da Lotação

```bash
curl -X GET "http://localhost:8000/api/v1/carga/lotacoes/{id}/estatisticas/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 6.5 Ativar Lotação (requer Coordenador+)

```bash
curl -X POST "http://localhost:8000/api/v1/carga/lotacoes/{id}/ativar/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

---

### 7. Cargas

#### 7.1 Listar Cargas

```bash
# Todas
curl -X GET "http://localhost:8000/api/v1/carga/cargas/" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# De um patriarca
curl -X GET "http://localhost:8000/api/v1/carga/cargas/?patriarca=1" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# Por tipo
curl -X GET "http://localhost:8000/api/v1/carga/cargas/?tipo=1" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# Por status
curl -X GET "http://localhost:8000/api/v1/carga/cargas/?status=1" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### 7.2 Timeline da Carga

```bash
curl -X GET "http://localhost:8000/api/v1/carga/cargas/{id}/timeline/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

---

### 8. Tokens de Envio

```bash
# Listar todos
curl -X GET "http://localhost:8000/api/v1/carga/tokens/" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# Apenas ativos
curl -X GET "http://localhost:8000/api/v1/carga/tokens/?ativos=true" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# De um patriarca
curl -X GET "http://localhost:8000/api/v1/carga/tokens/?patriarca=1" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

---

### 9. Tabelas Auxiliares

#### Status de Progresso
```bash
curl -X GET "http://localhost:8000/api/v1/carga/status-progresso/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### Status de Carga
```bash
curl -X GET "http://localhost:8000/api/v1/carga/status-carga/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### Tipos de Carga
```bash
curl -X GET "http://localhost:8000/api/v1/carga/tipos-carga/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### Status de Token
```bash
curl -X GET "http://localhost:8000/api/v1/carga/status-token/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

---

### 10. Gerenciamento de Usuários

#### Listar Usuários da Aplicação
```bash
curl -X GET "http://localhost:8000/api/v1/carga/users/list_users/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### Buscar Usuário por Email
```bash
curl -X GET "http://localhost:8000/api/v1/carga/users/user@example.com/" \
  -H "Authorization: Token $TOKEN" \
  | jq .
```

#### Sincronizar Usuário do Portal
```bash
curl -X POST "http://localhost:8000/api/v1/carga/users/sync_user/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "Nome do Usuário",
    "roles": ["GESTOR_CARGA"],
    "attributes": {"can_upload": "true"}
  }' \
  | jq .
```

---

## Testes de Permissões

### Caso 1: Usuário sem Permissão

1. Criar usuário sem role em CARGA_ORG_LOT
2. Tentar acessar qualquer endpoint
3. **Esperado:** 403 Forbidden

```bash
curl -X GET "http://localhost:8000/api/v1/carga/patriarcas/" \
  -H "Authorization: Token $TOKEN_SEM_PERMISSAO"
```

### Caso 2: Usuário com Permissão View Apenas

1. Criar usuário com apenas `view_tblpatriarca`
2. Testar GET (deve funcionar)
3. Testar POST (deve falhar)

```bash
# Deve funcionar
curl -X GET "http://localhost:8000/api/v1/carga/patriarcas/" \
  -H "Authorization: Token $TOKEN_VIEW_ONLY"

# Deve falhar (403)
curl -X POST "http://localhost:8000/api/v1/carga/patriarcas/" \
  -H "Authorization: Token $TOKEN_VIEW_ONLY" \
  -H "Content-Type: application/json" \
  -d '{"str_sigla_patriarca": "TESTE"}'
```

### Caso 3: Operações Sensíveis (Coordenador+)

1. Usuário comum tenta ativar organograma
2. **Esperado:** 403 Forbidden

```bash
curl -X POST "http://localhost:8000/api/v1/carga/organogramas/1/ativar/" \
  -H "Authorization: Token $TOKEN_USUARIO_COMUM"
```

3. Coordenador tenta ativar
4. **Esperado:** 200 OK

```bash
curl -X POST "http://localhost:8000/api/v1/carga/organogramas/1/ativar/" \
  -H "Authorization: Token $TOKEN_COORDENADOR"
```

---

## Testes de Filtros

### Filtro por Patriarca

```bash
# Criar 2 patriarcas
PATRIARCA_1=$(curl -X POST "http://localhost:8000/api/v1/carga/patriarcas/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"str_sigla_patriarca": "P1", "str_nome": "Patriarca 1", "id_status_progresso": 1}' \
  | jq -r '.id_patriarca')

PATRIARCA_2=$(curl -X POST "http://localhost:8000/api/v1/carga/patriarcas/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"str_sigla_patriarca": "P2", "str_nome": "Patriarca 2", "id_status_progresso": 1}' \
  | jq -r '.id_patriarca')

# Criar organogramas para cada um
# (comandos de criação aqui)

# Filtrar organogramas do P1
curl -X GET "http://localhost:8000/api/v1/carga/organogramas/?patriarca=$PATRIARCA_1" \
  -H "Authorization: Token $TOKEN" \
  | jq .

# Verificar que retorna apenas do P1
```

---

## Testes de Paginação

```bash
# Criar 150 registros de teste (script)
# ...

# Página 1
curl -X GET "http://localhost:8000/api/v1/carga/patriarcas/?page=1&page_size=50" \
  -H "Authorization: Token $TOKEN" \
  | jq '.count, .results | length'

# Página 2
curl -X GET "http://localhost:8000/api/v1/carga/patriarcas/?page=2&page_size=50" \
  -H "Authorization: Token $TOKEN" \
  | jq '.results | length'
```

---

## Testes de Erros

### 404 Not Found

```bash
curl -X GET "http://localhost:8000/api/v1/carga/patriarcas/99999/" \
  -H "Authorization: Token $TOKEN"
```

**Esperado:**
```json
{
  "detail": "Not found."
}
```

### 400 Bad Request

```bash
curl -X POST "http://localhost:8000/api/v1/carga/patriarcas/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Esperado:**
```json
{
  "str_sigla_patriarca": ["This field is required."],
  "str_nome": ["This field is required."]
}
```

### 401 Unauthorized

```bash
curl -X GET "http://localhost:8000/api/v1/carga/patriarcas/"
```

**Esperado:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## Checklist de Validação

### Endpoints Básicos
- ☐ `/permissions/` retorna permissões corretamente
- ☐ `/dashboard/` retorna estatísticas
- ☐ `/search/orgao/` retorna resultados de busca

### CRUD de Patriarcas
- ☐ GET lista patriarcas
- ☐ POST cria patriarca
- ☐ GET {id} retorna detalhe
- ☐ PATCH atualiza parcialmente
- ☐ DELETE remove patriarca
- ☐ Actions customizadas funcionam

### CRUD de Organogramas
- ☐ Todas operações CRUD
- ☐ Ativar organograma (requer Coordenador+)
- ☐ Hierarquia retorna árvore
- ☐ Actions funcionam

### CRUD de Lotações
- ☐ Todas operações CRUD
- ☐ Registros paginados
- ☐ Inconsistências listadas
- ☐ Estatísticas corretas
- ☐ Ativar lotação (requer Coordenador+)

### Filtros
- ☐ Filtro por patriarca funciona
- ☐ Filtros de status funcionam
- ☐ Busca textual funciona
- ☐ Filtros combinados funcionam

### Permissões
- ☐ Usuário sem permissão é bloqueado (403)
- ☐ View-only permite GET mas bloqueia POST/PUT/DELETE
- ☐ Operações sensíveis requerem Coordenador+
- ☐ Superusuário tem acesso total

### Paginação
- ☐ Paginação funciona corretamente
- ☐ page_size é respeitado
- ☐ Metadados de paginação corretos

### Erros
- ☐ 404 para recursos inexistentes
- ☐ 400 para dados inválidos
- ☐ 401 sem autenticação
- ☐ 403 sem permissão
- ☐ Mensagens de erro claras

---

## Scripts de Teste Automatizado

### Script Bash Completo

```bash
#!/bin/bash
# teste_endpoints.sh

BASE_URL="http://localhost:8000/api/v1/carga"
TOKEN="seu_token_aqui"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    echo -n "Testando $method $endpoint... "
    
    if [ -z "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X $method "$BASE_URL$endpoint" \
            -H "Authorization: Token $TOKEN")
    else
        response=$(curl -s -w "\n%{http_code}" -X $method "$BASE_URL$endpoint" \
            -H "Authorization: Token $TOKEN" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}OK ($http_code)${NC}"
        return 0
    else
        echo -e "${RED}FAIL ($http_code)${NC}"
        return 1
    fi
}

echo "=== Testando Endpoints ==="
echo ""

test_endpoint "GET" "/permissions/"
test_endpoint "GET" "/dashboard/"
test_endpoint "GET" "/patriarcas/"
test_endpoint "GET" "/organogramas/"
test_endpoint "GET" "/lotacoes/"
test_endpoint "GET" "/cargas/"
test_endpoint "GET" "/tokens/"
test_endpoint "GET" "/status-progresso/"

echo ""
echo "=== Testes Concluídos ==="
```

Executar:
```bash
chmod +x teste_endpoints.sh
./teste_endpoints.sh
```

---

**Data:** 30/01/2026  
**Versão:** 1.0
