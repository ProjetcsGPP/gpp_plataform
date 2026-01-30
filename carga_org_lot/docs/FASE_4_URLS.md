# Fase 4: Atualização das URLs - Completa ✅

## Visão Geral

Configuração completa das URLs da API REST, registrando todos os ViewSets e endpoints criados na Fase 3 no router DRF.

---

## Arquitetura de URLs do Projeto

### Estrutura Geral

```
gpp_plataform/
├── urls.py                      # URLs principais do projeto
└── ...

carga_org_lot/
├── urls/
│   ├── __init__.py
│   ├── api_urls.py              # ← APIs REST (Fase 4)
│   └── web_urls.py              # URLs Django tradicionais
└── ...
```

### Prefixos de URL

```
/api/v1/carga/              → APIs REST (Next.js)
/carga_org_lot/             → Views Django (templates)
```

---

## Configuração Principal

### `gpp_plataform/urls.py`

Já configurado previamente:

```python
urlpatterns = [
    # ...
    
    # APIs REST para Next.js
    path('api/v1/carga/', include('carga_org_lot.urls.api_urls')),
    
    # Views Django tradicionais
    path('carga_org_lot/', include('carga_org_lot.urls.web_urls')),
]
```

---

## API URLs (`api_urls.py`)

### Estrutura do Arquivo

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views import (
    # Funções
    user_permissions,
    dashboard_stats,
    search_orgao,
    
    # ViewSets
    UserManagementViewSet,
    PatriarcaViewSet,
    OrganogramaVersaoViewSet,
    # ...
)

app_name = 'carga_org_lot_api'

# Router DRF
router = DefaultRouter()
router.register(r'patriarcas', PatriarcaViewSet, basename='patriarcas')
# ...

urlpatterns = [
    # Endpoints de função
    path('permissions/', user_permissions, name='user-permissions'),
    path('dashboard/', dashboard_stats, name='dashboard-stats'),
    path('search/orgao/', search_orgao, name='search-orgao'),
    
    # ViewSets (router)
    path('', include(router.urls)),
]
```

---

## ViewSets Registrados

### 1. Gerenciamento de Usuários

```python
router.register(r'users', UserManagementViewSet, basename='users')
```

**Rotas geradas:**
- `GET /api/v1/carga/users/`
- `GET /api/v1/carga/users/{email}/`
- `POST /api/v1/carga/users/sync_user/`
- `GET /api/v1/carga/users/list_users/`

---

### 2. Patriarcas

```python
router.register(r'patriarcas', PatriarcaViewSet, basename='patriarcas')
```

**Rotas CRUD:**
- `GET /api/v1/carga/patriarcas/` - list
- `POST /api/v1/carga/patriarcas/` - create
- `GET /api/v1/carga/patriarcas/{id}/` - retrieve
- `PUT /api/v1/carga/patriarcas/{id}/` - update
- `PATCH /api/v1/carga/patriarcas/{id}/` - partial_update
- `DELETE /api/v1/carga/patriarcas/{id}/` - destroy

**Actions customizadas:**
- `GET /api/v1/carga/patriarcas/list_light/`
- `GET /api/v1/carga/patriarcas/{id}/organogramas/`
- `GET /api/v1/carga/patriarcas/{id}/lotacoes/`
- `GET /api/v1/carga/patriarcas/{id}/estatisticas/`

---

### 3. Organogramas

```python
router.register(r'organogramas', OrganogramaVersaoViewSet, basename='organogramas')
```

**Rotas CRUD:**
- `GET /api/v1/carga/organogramas/`
- `POST /api/v1/carga/organogramas/`
- `GET /api/v1/carga/organogramas/{id}/`
- `PUT /api/v1/carga/organogramas/{id}/`
- `PATCH /api/v1/carga/organogramas/{id}/`
- `DELETE /api/v1/carga/organogramas/{id}/`

**Actions customizadas:**
- `POST /api/v1/carga/organogramas/{id}/ativar/`
- `GET /api/v1/carga/organogramas/{id}/orgaos/`
- `GET /api/v1/carga/organogramas/{id}/hierarquia/`
- `GET /api/v1/carga/organogramas/{id}/json_envio/`

---

### 4. Órgãos/Unidades

```python
router.register(r'orgaos', OrgaoUnidadeViewSet, basename='orgaos')
```

**Rotas CRUD:**
- `GET /api/v1/carga/orgaos/`
- `POST /api/v1/carga/orgaos/`
- `GET /api/v1/carga/orgaos/{id}/`
- `PUT /api/v1/carga/orgaos/{id}/`
- `PATCH /api/v1/carga/orgaos/{id}/`
- `DELETE /api/v1/carga/orgaos/{id}/`

---

### 5. Lotações

```python
router.register(r'lotacoes', LotacaoVersaoViewSet, basename='lotacoes')
```

**Rotas CRUD:**
- `GET /api/v1/carga/lotacoes/`
- `POST /api/v1/carga/lotacoes/`
- `GET /api/v1/carga/lotacoes/{id}/`
- `PUT /api/v1/carga/lotacoes/{id}/`
- `PATCH /api/v1/carga/lotacoes/{id}/`
- `DELETE /api/v1/carga/lotacoes/{id}/`

**Actions customizadas:**
- `POST /api/v1/carga/lotacoes/{id}/ativar/`
- `GET /api/v1/carga/lotacoes/{id}/registros/`
- `GET /api/v1/carga/lotacoes/{id}/inconsistencias/`
- `GET /api/v1/carga/lotacoes/{id}/estatisticas/`

---

### 6. Cargas

```python
router.register(r'cargas', CargaPatriarcaViewSet, basename='cargas')
```

**Rotas CRUD:**
- `GET /api/v1/carga/cargas/`
- `POST /api/v1/carga/cargas/`
- `GET /api/v1/carga/cargas/{id}/`
- `PUT /api/v1/carga/cargas/{id}/`
- `PATCH /api/v1/carga/cargas/{id}/`
- `DELETE /api/v1/carga/cargas/{id}/`

**Actions customizadas:**
- `GET /api/v1/carga/cargas/{id}/timeline/`

---

### 7. Tokens de Envio

```python
router.register(r'tokens', TokenEnvioCargaViewSet, basename='tokens')
```

**Rotas CRUD:**
- `GET /api/v1/carga/tokens/`
- `POST /api/v1/carga/tokens/`
- `GET /api/v1/carga/tokens/{id}/`
- `PUT /api/v1/carga/tokens/{id}/`
- `PATCH /api/v1/carga/tokens/{id}/`
- `DELETE /api/v1/carga/tokens/{id}/`

---

### 8. Tabelas Auxiliares (Read-Only)

#### Status de Progresso
```python
router.register(r'status-progresso', StatusProgressoViewSet, basename='status-progresso')
```

- `GET /api/v1/carga/status-progresso/`
- `GET /api/v1/carga/status-progresso/{id}/`

#### Status de Carga
```python
router.register(r'status-carga', StatusCargaViewSet, basename='status-carga')
```

- `GET /api/v1/carga/status-carga/`
- `GET /api/v1/carga/status-carga/{id}/`

#### Tipos de Carga
```python
router.register(r'tipos-carga', TipoCargaViewSet, basename='tipos-carga')
```

- `GET /api/v1/carga/tipos-carga/`
- `GET /api/v1/carga/tipos-carga/{id}/`

#### Status de Token
```python
router.register(r'status-token', StatusTokenEnvioCargaViewSet, basename='status-token')
```

- `GET /api/v1/carga/status-token/`
- `GET /api/v1/carga/status-token/{id}/`

---

## Endpoints de Função

### 1. Permissões do Usuário

```python
path('permissions/', user_permissions, name='user-permissions')
```

**URL:** `GET /api/v1/carga/permissions/`

**Resposta:** Permissões do usuário logado para consumo no Next.js.

---

### 2. Dashboard

```python
path('dashboard/', dashboard_stats, name='dashboard-stats')
```

**URL:** `GET /api/v1/carga/dashboard/`

**Query Params:**
- `patriarca={id}` - Filtro opcional por patriarca

**Resposta:** Estatísticas gerais do sistema.

---

### 3. Busca Rápida

```python
path('search/orgao/', search_orgao, name='search-orgao')
```

**URL:** `GET /api/v1/carga/search/orgao/`

**Query Params:**
- `q={termo}` - Termo de busca (mínimo 2 caracteres)
- `patriarca_id={id}` - Filtro opcional por patriarca

**Resposta:** Lista de órgãos que correspondem à busca (autocomplete).

---

## Namespacing

### App Name

```python
app_name = 'carga_org_lot_api'
```

Permite referências nomeadas nas URLs:

```python
# No código Python
from django.urls import reverse

url = reverse('carga_org_lot_api:patriarcas-list')
# Retorna: '/api/v1/carga/patriarcas/'

url = reverse('carga_org_lot_api:user-permissions')
# Retorna: '/api/v1/carga/permissions/'
```

### Basenames dos ViewSets

O DRF gera automaticamente nomes de URL baseados no `basename`:

| ViewSet | Basename | Action | Nome da URL |
|---------|----------|--------|-------------|
| PatriarcaViewSet | `patriarcas` | list | `patriarcas-list` |
| PatriarcaViewSet | `patriarcas` | retrieve | `patriarcas-detail` |
| PatriarcaViewSet | `patriarcas` | organogramas | `patriarcas-organogramas` |
| OrganogramaVersaoViewSet | `organogramas` | list | `organogramas-list` |
| OrganogramaVersaoViewSet | `organogramas` | ativar | `organogramas-ativar` |

---

## Query Parameters Comuns

### Filtros

- `patriarca={id}` - Filtra por patriarca (disponível em quase todos os endpoints)
- `ativos=true` - Apenas registros ativos
- `status={id}` - Por status
- `tipo={id}` - Por tipo (cargas)
- `q={termo}` - Busca textual

### Paginação

- `page={n}` - Número da página (padrão: 1)
- `page_size={n}` - Tamanho da página (padrão: 10-100, configurado no settings)

### Ordenação

- `ordering={field}` - Ordena por campo (ex: `-dat_processamento` para decrescente)

**Exemplo:**
```
GET /api/v1/carga/organogramas/?patriarca=1&ativos=true&ordering=-dat_processamento&page=1&page_size=20
```

---

## Autenticação

### Token Authentication

**Header:**
```
Authorization: Token {seu_token}
```

**Exemplo:**
```bash
curl -X GET "http://localhost:8000/api/v1/carga/patriarcas/" \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### Session Authentication

Também suportada para navegadores (cookies de sessão).

---

## Permissões

### Verificação Automática

Todos os ViewSets usam `HasCargaOrgLotPermission`:

- **list/retrieve** → requer `view_<model>`
- **create** → requer `add_<model>`
- **update/partial_update** → requer `change_<model>`
- **destroy** → requer `delete_<model>`

### Operações Sensíveis

Algumas actions requerem permissões elevadas:

- **Ativar organograma/lotação** → `IsCoordenadorOrAbove`
- **Operações críticas** → `IsGestor`

---

## Testes

### Verificar URLs Registradas

```bash
python manage.py show_urls | grep carga
```

**Ou via DRF:**
```bash
curl http://localhost:8000/api/v1/carga/
```

Retorna lista de endpoints disponíveis.

### Teste Manual Completo

Ver arquivo: [`TESTE_ENDPOINTS.md`](./TESTE_ENDPOINTS.md)

---

## Documentação Automática

### Django REST Framework Browsable API

Acesse qualquer endpoint no navegador:

```
http://localhost:8000/api/v1/carga/patriarcas/
```

A interface interativa do DRF permite:
- Visualizar estrutura de dados
- Testar endpoints diretamente
- Ver filtros disponíveis
- Fazer requisições POST/PUT/DELETE

### Swagger/OpenAPI (Opcional)

Se configurado no projeto:

```
http://localhost:8000/api/docs/
http://localhost:8000/api/schema/
```

---

## Migração de URLs Antigas

### URLs Antigas (Fase 1)

Se existiam URLs antigas, foram mantidas para compatibilidade:

```python
# Antigo (pode remover se não usado)
path('patriarca/', PatriarcaViewSet.as_view({'get': 'list'})),
```

### URLs Novas (Fase 4)

```python
# Novo (DRF Router)
router.register(r'patriarcas', PatriarcaViewSet, basename='patriarcas')
```

**Vantagens do Router:**
- Gera todas as rotas CRUD automaticamente
- Inclui actions customizadas
- Suporta viewsets nativamente
- Reduz código duplicado

---

## Melhores Práticas

### 1. Use Plural para Recursos

✅ **Correto:**
```python
router.register(r'patriarcas', PatriarcaViewSet)
```

❌ **Incorreto:**
```python
router.register(r'patriarca', PatriarcaViewSet)
```

### 2. Use Hífens para URLs Compostas

✅ **Correto:**
```python
router.register(r'status-progresso', StatusProgressoViewSet)
```

❌ **Incorreto:**
```python
router.register(r'status_progresso', StatusProgressoViewSet)
```

### 3. Basename Consistente

✅ **Correto:**
```python
router.register(r'patriarcas', PatriarcaViewSet, basename='patriarcas')
```

Permite `reverse('carga_org_lot_api:patriarcas-list')`.

### 4. Agrupe URLs Relacionadas

```python
# Bom: todos os status juntos
router.register(r'status-progresso', StatusProgressoViewSet)
router.register(r'status-carga', StatusCargaViewSet)
router.register(r'status-token', StatusTokenEnvioCargaViewSet)
```

---

## Estrutura Completa de URLs

```
/api/v1/carga/
├── permissions/                    # Função
├── dashboard/                      # Função
├── search/
│   └── orgao/                      # Função
├── users/                          # ViewSet
│   ├── sync_user/                  # Action
│   └── list_users/                 # Action
├── patriarcas/                     # ViewSet
│   ├── {id}/
│   │   ├── organogramas/           # Action
│   │   ├── lotacoes/               # Action
│   │   └── estatisticas/           # Action
│   └── list_light/                 # Action
├── organogramas/                   # ViewSet
│   └── {id}/
│       ├── ativar/                 # Action
│       ├── orgaos/                 # Action
│       ├── hierarquia/             # Action
│       └── json_envio/             # Action
├── orgaos/                         # ViewSet
├── lotacoes/                       # ViewSet
│   └── {id}/
│       ├── ativar/                 # Action
│       ├── registros/              # Action
│       ├── inconsistencias/        # Action
│       └── estatisticas/           # Action
├── cargas/                         # ViewSet
│   └── {id}/
│       └── timeline/               # Action
├── tokens/                         # ViewSet
├── status-progresso/               # ViewSet (read-only)
├── status-carga/                   # ViewSet (read-only)
├── tipos-carga/                    # ViewSet (read-only)
└── status-token/                   # ViewSet (read-only)
```

---

## Checklist de Conclusão

### Arquivos Criados/Atualizados

- ✅ `carga_org_lot/urls/__init__.py`
- ✅ `carga_org_lot/urls/api_urls.py`
- ✅ `carga_org_lot/docs/FASE_4_URLS.md`
- ✅ `carga_org_lot/docs/TESTE_ENDPOINTS.md`

### Funcionalidades Implementadas

- ✅ 11 ViewSets registrados no router
- ✅ 3 endpoints de função configurados
- ✅ Namespacing (`app_name`)
- ✅ Basenames consistentes
- ✅ Documentação inline completa
- ✅ Guia de testes criado

### Testes Recomendados

- ☐ Verificar todas as URLs com `show_urls`
- ☐ Testar CRUD de cada ViewSet
- ☐ Testar actions customizadas
- ☐ Testar filtros e paginação
- ☐ Testar permissões
- ☐ Navegar pela browsable API do DRF

---

## Próximos Passos

### Fase 5: Testes Automatizados

☐ Criar testes unitários para ViewSets
☐ Criar testes de integração de endpoints
☐ Criar testes de permissões
☐ Configurar coverage
☐ CI/CD

### Integração com Frontend

☐ Criar SDK TypeScript para Next.js
☐ Implementar hooks React
☐ Configurar cache no frontend
☐ Tratamento de erros

---

**Fase 4 Completa! ✅**

Data: 30/01/2026
Versão: 1.0
