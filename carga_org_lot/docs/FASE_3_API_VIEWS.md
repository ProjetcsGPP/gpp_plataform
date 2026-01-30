# Fase 3: API Views (DRF) - Completa ✅

## Visão Geral

Implementação completa de endpoints REST para a aplicação Carga Org/Lot usando Django REST Framework, seguindo o padrão estabelecido em `acoes_pngi`.

## Arquitetura

### Estrutura de Arquivos

```
carga_org_lot/
├── utils/
│   ├── __init__.py
│   └── permissions.py          # Helpers de permissões com cache
├── permissions.py              # Classes de permissão DRF
├── views/
│   ├── __init__.py             # Centraliza imports
│   ├── api_views.py            # API Views unificadas (NOVO)
│   ├── web_views/              # Views Django tradicionais
│   └── api_views/              # (deprecated - substituído por api_views.py)
└── docs/
    └── FASE_3_API_VIEWS.md     # Esta documentação
```

---

## 1. Sistema de Permissões

### 1.1 Helper Functions (`utils/permissions.py`)

Funções auxiliares com cache automático (15 minutos) para otimização de performance:

#### `get_user_app_permissions(user, app_code='CARGA_ORG_LOT')`

Retorna conjunto de permissões do usuário para a aplicação.

```python
# Exemplo de uso
perms = get_user_app_permissions(request.user)
if 'add_tblpatriarca' in perms:
    # Usuário pode criar patriarcas
```

**Características:**
- ✅ Cache automático de 15 minutos
- ✅ Suporte a superusuários
- ✅ Retorna `set` de codenames
- ✅ Logging detalhado

#### `get_model_permissions(user, model_name, app_code='CARGA_ORG_LOT')`

Retorna permissões do usuário para um modelo específico.

```python
# Exemplo de uso
perms = get_model_permissions(request.user, 'tblpatriarca')
print(perms)
# {'can_add': True, 'can_change': True, 'can_delete': False, 'can_view': True}
```

#### `has_permission(user, permission_codename, app_code='CARGA_ORG_LOT')`

Verifica se usuário tem uma permissão específica.

```python
if has_permission(request.user, 'add_tblpatriarca'):
    # Permitir criação
```

#### `require_api_permission(permission_codename)`

Decorator para endpoints que requerem permissão específica.

```python
@action(detail=False, methods=['post'])
@require_api_permission('add_tblpatriarca')
def criar_patriarca(self, request):
    # Lógica aqui
```

#### Outras Funções

- `clear_user_permissions_cache(user, app_code)` - Limpa cache de permissões
- `get_user_role(user, app_code)` - Retorna role do usuário
- `is_gestor(user, app_code)` - Verifica se é gestor
- `is_coordenador_or_above(user, app_code)` - Coordenador ou gestor
- `is_analista_or_above(user, app_code)` - Analista ou superior

---

### 1.2 Classes de Permissão DRF (`permissions.py`)

#### `HasCargaOrgLotPermission`

Classe principal que verifica automaticamente Django permissions baseada na action do ViewSet.

**Mapeamento automático:**
- `list`, `retrieve` → `view_<model>`
- `create` → `add_<model>`
- `update`, `partial_update` → `change_<model>`
- `destroy` → `delete_<model>`
- Actions customizadas → `view_<model>` (padrão)

```python
class PatriarcaViewSet(viewsets.ModelViewSet):
    queryset = TblPatriarca.objects.all()
    serializer_class = TblPatriarcaSerializer
    permission_classes = [HasCargaOrgLotPermission]  # ← Permissões automáticas
```

#### `IsCoordenadorOrAbove`

Permite acesso apenas para Coordenadores e Gestores.

```python
@action(detail=True, methods=['post'], permission_classes=[IsCoordenadorOrAbove])
def ativar_organograma(self, request, pk=None):
    # Apenas coordenadores e gestores
```

#### `IsGestor`

Permite acesso apenas para Gestores.

```python
@action(detail=True, methods=['delete'], permission_classes=[IsGestor])
def delete_all_data(self, request, pk=None):
    # Apenas gestores
```

#### `ReadOnly`

Permite apenas operações de leitura (GET, HEAD, OPTIONS).

---

## 2. Endpoints da API

### Base URL

```
/api/v1/carga_org_lot/
```

### 2.1 Permissões do Usuário

#### `GET /api/v1/carga_org_lot/permissions/`

Retorna permissões do usuário logado para consumo no Next.js.

**Resposta:**

```json
{
  "user_id": 1,
  "email": "user@example.com",
  "name": "Nome do Usuário",
  "role": "GESTOR_CARGA",
  "permissions": [
    "add_tblpatriarca",
    "change_tblpatriarca",
    "view_tblpatriarca",
    "..."
  ],
  "is_superuser": false,
  "groups": {
    "can_manage_patriarcas": true,
    "can_upload": true,
    "can_process": true,
    "can_send_api": false,
    "can_delete": true
  },
  "specific": {
    "patriarca": {
      "can_add": true,
      "can_change": true,
      "can_delete": true,
      "can_view": true
    },
    "organograma": { "..." },
    "lotacao": { "..." }
  }
}
```

---

### 2.2 Gerenciamento de Usuários

#### `UserManagementViewSet`

**Endpoints:**

- `GET /users/{email}/` - Busca usuário por email
- `POST /users/sync_user/` - Sincroniza usuário do portal
- `GET /users/list_users/` - Lista usuários da aplicação

---

### 2.3 Tabelas Auxiliares (Somente Leitura)

#### `StatusProgressoViewSet`
- `GET /status_progresso/` - Lista status de progresso
- `GET /status_progresso/{id}/` - Detalhe de status

#### `StatusCargaViewSet`
- `GET /status_carga/` - Lista status de carga
- `GET /status_carga/{id}/` - Detalhe de status

#### `TipoCargaViewSet`
- `GET /tipos_carga/` - Lista tipos de carga
- `GET /tipos_carga/{id}/` - Detalhe de tipo

#### `StatusTokenEnvioCargaViewSet`
- `GET /status_token/` - Lista status de token
- `GET /status_token/{id}/` - Detalhe de status

---

### 2.4 Patriarcas

#### `PatriarcaViewSet`

**Endpoints CRUD:**

- `GET /patriarcas/` - Lista patriarcas
- `POST /patriarcas/` - Cria patriarca
- `GET /patriarcas/{id}/` - Detalhe de patriarca
- `PUT /patriarcas/{id}/` - Atualiza patriarca (completo)
- `PATCH /patriarcas/{id}/` - Atualiza patriarca (parcial)
- `DELETE /patriarcas/{id}/` - Deleta patriarca

**Actions Customizadas:**

- `GET /patriarcas/list_light/` - Listagem otimizada (ID, sigla, nome)
- `GET /patriarcas/{id}/organogramas/` - Organogramas do patriarca
- `GET /patriarcas/{id}/lotacoes/` - Lotações do patriarca
- `GET /patriarcas/{id}/estatisticas/` - Estatísticas do patriarca

**Query Params:**
- `sigla` - Filtro por sigla (parcial)
- `status` - Filtro por ID de status

**Serializers:**
- List: `TblPatriarcaLightSerializer` (otimizado)
- Outros: `TblPatriarcaSerializer` (completo)

---

### 2.5 Organogramas

#### `OrganogramaVersaoViewSet`

**Endpoints CRUD:**

- `GET /organogramas/` - Lista versões de organograma
- `POST /organogramas/` - Cria versão
- `GET /organogramas/{id}/` - Detalhe de versão
- `PUT /organogramas/{id}/` - Atualiza versão
- `PATCH /organogramas/{id}/` - Atualiza parcial
- `DELETE /organogramas/{id}/` - Deleta versão

**Actions Customizadas:**

- `POST /organogramas/{id}/ativar/` - Ativa organograma (apenas Coordenador+)
- `GET /organogramas/{id}/orgaos/` - Lista órgãos (flat)
- `GET /organogramas/{id}/hierarquia/` - Estrutura hierárquica (árvore)
- `GET /organogramas/{id}/json_envio/` - JSON formatado para envio

**Query Params:**
- `patriarca` - Filtro por ID de patriarca
- `ativos` - `true` para apenas ativos
- `status` - Filtro por status de processamento

**Serializers:**
- List: `TblOrganogramaVersaoLightSerializer`
- Outros: `TblOrganogramaVersaoSerializer`

**Exemplo de Resposta - Hierarquia:**

```json
{
  "organograma_id": 1,
  "patriarca": "SEGER",
  "hierarquia": [
    {
      "id": 1,
      "sigla": "SEGER",
      "nome": "Secretaria de Estado de Gestão e Recursos Humanos",
      "nivel": 1,
      "filhos": [
        {
          "id": 2,
          "sigla": "SUBSEC",
          "nome": "Subsecretaria",
          "nivel": 2,
          "filhos": []
        }
      ]
    }
  ]
}
```

---

### 2.6 Órgãos/Unidades

#### `OrgaoUnidadeViewSet`

**Endpoints CRUD:**

- `GET /orgaos/` - Lista órgãos
- `POST /orgaos/` - Cria órgão
- `GET /orgaos/{id}/` - Detalhe de órgão
- `PUT /orgaos/{id}/` - Atualiza órgão
- `PATCH /orgaos/{id}/` - Atualiza parcial
- `DELETE /orgaos/{id}/` - Deleta órgão

**Query Params:**
- `patriarca` - Filtro por ID de patriarca
- `organograma` - Filtro por ID de organograma
- `ativos` - `true` para apenas ativos
- `raiz` - `true` para apenas órgãos raiz (sem pai)
- `q` - Busca por sigla ou nome (parcial)

**Serializers:**
- List: `TblOrgaoUnidadeLightSerializer`
- Outros: `TblOrgaoUnidadeSerializer`
- Hierarquia: `TblOrgaoUnidadeTreeSerializer`

---

### 2.7 Lotações

#### `LotacaoVersaoViewSet`

**Endpoints CRUD:**

- `GET /lotacoes/` - Lista versões de lotação
- `POST /lotacoes/` - Cria versão
- `GET /lotacoes/{id}/` - Detalhe de versão
- `PUT /lotacoes/{id}/` - Atualiza versão
- `PATCH /lotacoes/{id}/` - Atualiza parcial
- `DELETE /lotacoes/{id}/` - Deleta versão

**Actions Customizadas:**

- `POST /lotacoes/{id}/ativar/` - Ativa versão (apenas Coordenador+)
- `GET /lotacoes/{id}/registros/` - Lista registros de lotação (paginado)
- `GET /lotacoes/{id}/inconsistencias/` - Lista inconsistências
- `GET /lotacoes/{id}/estatisticas/` - Estatísticas da versão

**Query Params (principal):**
- `patriarca` - Filtro por ID de patriarca
- `ativas` - `true` para apenas ativas
- `status` - Filtro por status de processamento

**Query Params (registros):**
- `page` - Número da página (padrão: 1)
- `page_size` - Tamanho da página (padrão: 100)
- `valido` - `true` ou `false` para filtrar por validade
- `cpf` - Busca por CPF (parcial)
- `orgao` - Filtro por ID de órgão

**Serializers:**
- List: `TblLotacaoVersaoLightSerializer`
- Outros: `TblLotacaoVersaoSerializer`
- Registros: `TblLotacaoLightSerializer`

**Exemplo de Resposta - Estatísticas:**

```json
{
  "total_registros": 1500,
  "validos": 1450,
  "invalidos": 50,
  "taxa_sucesso": 96.67,
  "total_inconsistencias": 75,
  "por_orgao": [
    {
      "id_orgao_lotacao__str_sigla": "SEGER",
      "count": 500
    },
    { "..." }
  ]
}
```

---

### 2.8 Cargas

#### `CargaPatriarcaViewSet`

**Endpoints CRUD:**

- `GET /cargas/` - Lista cargas
- `POST /cargas/` - Cria carga
- `GET /cargas/{id}/` - Detalhe de carga
- `PUT /cargas/{id}/` - Atualiza carga
- `PATCH /cargas/{id}/` - Atualiza parcial
- `DELETE /cargas/{id}/` - Deleta carga

**Actions Customizadas:**

- `GET /cargas/{id}/timeline/` - Timeline de mudanças de status

**Query Params:**
- `patriarca` - Filtro por ID de patriarca
- `tipo` - Filtro por ID de tipo de carga
- `status` - Filtro por ID de status

---

### 2.9 Tokens de Envio

#### `TokenEnvioCargaViewSet`

**Endpoints CRUD:**

- `GET /tokens/` - Lista tokens
- `POST /tokens/` - Cria token
- `GET /tokens/{id}/` - Detalhe de token
- `PUT /tokens/{id}/` - Atualiza token
- `PATCH /tokens/{id}/` - Atualiza parcial
- `DELETE /tokens/{id}/` - Deleta token

**Query Params:**
- `patriarca` - Filtro por ID de patriarca
- `ativos` - `true` para apenas tokens ativos (sem data fim)

---

### 2.10 Dashboard

#### `GET /api/v1/carga_org_lot/dashboard/`

Retorna estatísticas gerais do sistema.

**Query Params:**
- `patriarca` - Filtro opcional por ID de patriarca

**Resposta:**

```json
{
  "patriarcas": {
    "total": 5,
    "por_status": [
      {
        "id_status_progresso__str_descricao": "Ativo",
        "count": 3
      }
    ]
  },
  "organogramas": {
    "total": 15,
    "ativos": 5,
    "por_status": []
  },
  "lotacoes": {
    "total_versoes": 20,
    "versoes_ativas": 5,
    "total_registros": 5000,
    "validos": 4800,
    "invalidos": 200
  },
  "cargas": {
    "total": 50,
    "por_status": [],
    "por_tipo": []
  }
}
```

---

### 2.11 Busca Rápida

#### `GET /api/v1/carga_org_lot/search/orgao/`

Busca órgãos por sigla ou nome (autocomplete).

**Query Params:**
- `q` - Termo de busca (mínimo 2 caracteres)
- `patriarca_id` - Filtro opcional por patriarca

**Resposta:**

```json
{
  "results": [
    {
      "id": 1,
      "sigla": "SEGER",
      "nome": "Secretaria de Estado de Gestão e RH",
      "patriarca": "SEGER",
      "nivel": 1
    }
  ]
}
```

---

## 3. Padrões e Convenções

### 3.1 Permissões

✅ **Verificação Automática**
- Usa `HasCargaOrgLotPermission` em todos os ViewSets
- Mapeia actions automaticamente para permissões Django
- Logs detalhados de acessos negados

✅ **Operações Sensíveis**
- Usa `IsCoordenadorOrAbove` para ativações
- Usa `IsGestor` para deleções em massa

✅ **Cache de Performance**
- Permissões cacheadas por 15 minutos
- Reduz consultas ao banco de dados
- Cache limpo automaticamente ao alterar roles

---

### 3.2 Serializers

✅ **Serializers Light**
- Usado em `list` actions para performance
- Retorna apenas campos essenciais
- Reduz payload da resposta

✅ **Serializers Completos**
- Usado em `retrieve`, `create`, `update`
- Inclui todos os campos e relacionamentos
- Permite edição completa

---

### 3.3 Filtros

✅ **Filtro por Patriarca**
- Disponível em todos os ViewSets principais
- Query param: `patriarca={id}`
- Essencial para isolamento de dados

✅ **Filtros Comuns**
- `ativos=true` - Apenas registros ativos
- `status={id}` - Por status
- `q={termo}` - Busca textual

---

### 3.4 Paginação

✅ **DRF Default Pagination**
- Configurado globalmente no `settings.py`
- Query params padrão: `page`, `page_size`

✅ **Paginação Manual**
- Usado em `/lotacoes/{id}/registros/`
- Maior controle para grandes datasets

---

### 3.5 Logging

✅ **Eventos Importantes**
- Ativações de organogramas/lotações
- Acessos negados por permissão
- Erros de sincronização de usuários

```python
logger.info(f"Organograma {id} ativado por {user.email}")
logger.warning(f"Usuário {user.email} sem permissão '{perm}'")
logger.error(f"Erro ao ativar lotação: {str(e)}")
```

---

### 3.6 Tratamento de Erros

✅ **Respostas Consistentes**

```json
// Erro 404
{
  "detail": "JSON de envio não encontrado para este organograma"
}

// Erro 403
{
  "detail": "Você não tem permissão para esta operação",
  "required_permission": "add_tblpatriarca"
}

// Erro 500
{
  "detail": "Erro ao ativar organograma: {mensagem}"
}
```

---

## 4. Integração com Next.js

### 4.1 Endpoint de Permissões

Use `/api/v1/carga_org_lot/permissions/` no frontend para:

✅ **Controle de UI**
```typescript
// Exemplo Next.js
const { data: perms } = await fetch('/api/v1/carga_org_lot/permissions/');

if (perms.groups.can_upload) {
  // Mostrar botão de upload
}

if (perms.specific.patriarca.can_add) {
  // Mostrar formulário de criação
}
```

✅ **Navegação Condicional**
```typescript
const routes = [
  { path: '/patriarcas', visible: perms.specific.patriarca.can_view },
  { path: '/cargas', visible: perms.groups.can_upload },
];
```

---

### 4.2 Listagens Otimizadas

Use endpoints `list_light` para dropdowns e autocompletes:

```typescript
// Autocomplete de patriarcas
const patriarcas = await fetch('/api/v1/carga_org_lot/patriarcas/list_light/');

// Retorna apenas: { id, str_sigla_patriarca, str_nome }
```

---

### 4.3 Filtros Combinados

```typescript
// Listar organogramas ativos de um patriarca
const url = '/api/v1/carga_org_lot/organogramas/' +
  '?patriarca=1' +
  '&ativos=true' +
  '&ordering=-dat_processamento';
```

---

## 5. Exemplos de Uso

### 5.1 Criar Patriarca

```bash
curl -X POST http://localhost:8000/api/v1/carga_org_lot/patriarcas/ \
  -H "Authorization: Token {seu_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "str_sigla_patriarca": "SEGER",
    "str_nome": "Secretaria de Estado de Gestão e RH",
    "id_status_progresso": 1
  }'
```

---

### 5.2 Listar Organogramas de um Patriarca

```bash
curl -X GET "http://localhost:8000/api/v1/carga_org_lot/patriarcas/1/organogramas/" \
  -H "Authorization: Token {seu_token}"
```

---

### 5.3 Ativar Organograma

```bash
curl -X POST "http://localhost:8000/api/v1/carga_org_lot/organogramas/5/ativar/" \
  -H "Authorization: Token {seu_token}"
```

---

### 5.4 Buscar Inconsistências de uma Lotação

```bash
curl -X GET "http://localhost:8000/api/v1/carga_org_lot/lotacoes/3/inconsistencias/" \
  -H "Authorization: Token {seu_token}"
```

---

### 5.5 Dashboard com Filtro

```bash
curl -X GET "http://localhost:8000/api/v1/carga_org_lot/dashboard/?patriarca=1" \
  -H "Authorization: Token {seu_token}"
```

---

## 6. Próximos Passos

### Fase 4: Atualização das URLs

☐ Registrar todos os ViewSets no router DRF
☐ Configurar URLs para endpoints de função (@api_view)
☐ Testar todas as rotas
☐ Documentar URLs finais

### Fase 5: Testes Automatizados

☐ Testes de permissões
☐ Testes de ViewSets
☐ Testes de filtros
☐ Testes de integração

---

## 7. Checklist de Conclusão

### Arquivos Criados/Atualizados

- ✅ `carga_org_lot/utils/__init__.py`
- ✅ `carga_org_lot/utils/permissions.py`
- ✅ `carga_org_lot/permissions.py`
- ✅ `carga_org_lot/views/api_views.py`
- ✅ `carga_org_lot/views/__init__.py`
- ✅ `carga_org_lot/docs/FASE_3_API_VIEWS.md`

### Funcionalidades Implementadas

- ✅ Sistema de permissões com cache
- ✅ Classes de permissão DRF
- ✅ Endpoint de permissões para Next.js
- ✅ ViewSets completos com CRUD
- ✅ Actions customizadas
- ✅ Filtros por patriarca
- ✅ Serializers Light/Completos
- ✅ Dashboard de estatísticas
- ✅ Busca rápida
- ✅ Logging detalhado
- ✅ Tratamento de erros
- ✅ Documentação completa

---

## 8. Manutenção

### Adicionar Novo Modelão no Sistema

1. Criar serializers (Light + Completo)
2. Criar ViewSet com `HasCargaOrgLotPermission`
3. Adicionar filtro por patriarca (se aplicável)
4. Registrar no router (URLs)
5. Adicionar em `/permissions/` endpoint
6. Atualizar documentação

### Limpar Cache de Permissões

```python
from carga_org_lot.utils.permissions import clear_user_permissions_cache

# Ao alterar roles do usuário
clear_user_permissions_cache(user)
```

---

**Fase 3 Completa! ✅**

Data: 30/01/2026
Versão: 1.0
