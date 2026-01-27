# Views - Carga Org/Lot

Estrutura organizada de views para o módulo Carga Org/Lot, separando responsabilidades entre views web (Django templates) e API REST.

## 📚 Índice

- [🏛️ Estrutura](#-estrutura)
- [🌐 Web Views](#-web-views-django-templates)
- [🔌 API Views](#-api-views-rest-framework)
- [📦 Imports e Compatibilidade](#-imports-e-compatibilidade)
- [📝 Exemplos de Uso](#-exemplos-de-uso)

---

## 🏛️ Estrutura

```
views/
├── __init__.py                    ← Centraliza todos os imports
├── README.md                      ← Este arquivo
├── web_views/                     ← Views Django (páginas HTML)
│   ├── __init__.py
│   ├── auth_views.py              ← Login, logout, decoradores
│   ├── dashboard_views.py         ← Dashboard principal
│   ├── patriarca_views.py         ← CRUD Patriarcas
│   ├── organograma_views.py       ← CRUD Organogramas
│   ├── lotacao_views.py           ← CRUD Lotações
│   ├── carga_views.py             ← CRUD Cargas
│   ├── upload_views.py            ← Upload de arquivos
│   └── ajax_views.py              ← Endpoints AJAX
│
└── api_views/                     ← Views REST API
    ├── __init__.py
    ├── dashboard_api.py           ← Stats e utilitários
    ├── patriarca_api.py           ← ViewSet Patriarca
    ├── organograma_api.py         ← ViewSet Organograma
    ├── lotacao_api.py             ← ViewSet Lotação
    └── carga_api.py               ← ViewSet Carga
```

---

## 🌐 Web Views (Django Templates)

Views tradicionais Django que renderizam templates HTML.

### 🔑 Auth Views (`auth_views.py`)

**Funções:**
- `carga_login()` - Página de login com validação de permissões
- `carga_logout()` - Logout do sistema
- `carga_org_lot_required()` - Decorador de autenticação/autorização

**URLs:**
```python
GET/POST /carga_org_lot/login/
GET      /carga_org_lot/logout/
```

### 📊 Dashboard Views (`dashboard_views.py`)

**Funções:**
- `carga_dashboard()` - Dashboard principal com estatísticas

**URLs:**
```python
GET /carga_org_lot/
```

### 🏛️ Patriarca Views (`patriarca_views.py`)

**Funções:**
- `patriarca_list()` - Lista de patriarcas com filtros
- `patriarca_detail()` - Detalhes de um patriarca

**URLs:**
```python
GET /carga_org_lot/patriarcas/
GET /carga_org_lot/patriarcas/{id}/
```

### 🌳 Organograma Views (`organograma_views.py`)

**Funções:**
- `organograma_list()` - Lista de versões de organogramas
- `organograma_detail()` - Detalhes de uma versão
- `organograma_hierarquia_json()` - Hierarquia em formato JSON

**URLs:**
```python
GET /carga_org_lot/organogramas/
GET /carga_org_lot/organogramas/{id}/
GET /carga_org_lot/organogramas/{id}/hierarquia/json/
```

### 💼 Lotação Views (`lotacao_views.py`)

**Funções:**
- `lotacao_list()` - Lista de versões de lotação
- `lotacao_detail()` - Detalhes de uma versão
- `lotacao_inconsistencias()` - Lista de inconsistências

**URLs:**
```python
GET /carga_org_lot/lotacoes/
GET /carga_org_lot/lotacoes/{id}/
GET /carga_org_lot/lotacoes/{id}/inconsistencias/
```

### 📦 Carga Views (`carga_views.py`)

**Funções:**
- `carga_list()` - Lista de cargas
- `carga_detail()` - Detalhes de uma carga com timeline

**URLs:**
```python
GET /carga_org_lot/cargas/
GET /carga_org_lot/cargas/{id}/
```

### 📄 Upload Views (`upload_views.py`)

**Funções:**
- `upload_page()` - Página de upload
- `upload_organograma_handler()` - Processa upload de organograma
- `upload_lotacao_handler()` - Processa upload de lotação

**URLs:**
```python
GET  /carga_org_lot/upload/
POST /carga_org_lot/upload/organograma/
POST /carga_org_lot/upload/lotacao/
```

### ⚡ AJAX Views (`ajax_views.py`)

**Funções:**
- `search_orgao_ajax()` - Busca de órgãos (autocomplete)

**URLs:**
```python
GET /carga_org_lot/ajax/search/orgao/
```

---

## 🔌 API Views (REST Framework)

ViewSets e endpoints RESTful usando Django REST Framework.

### 📊 Dashboard API (`dashboard_api.py`)

**Endpoints:**
- `dashboard_stats()` - Estatísticas gerais do sistema
- `search_orgao()` - Busca de órgãos
- `upload_organograma()` - Upload de arquivo (API)
- `upload_lotacao()` - Upload de arquivo (API)

**URLs:**
```python
GET  /api/carga_org_lot/dashboard/
GET  /api/carga_org_lot/search/orgao/
POST /api/carga_org_lot/upload/organograma/
POST /api/carga_org_lot/upload/lotacao/
```

### 🏛️ Patriarca API (`patriarca_api.py`)

**ViewSet:** `PatriarcaViewSet`

**Endpoints padrão:**
```python
GET    /api/carga_org_lot/patriarcas/           # List
POST   /api/carga_org_lot/patriarcas/           # Create
GET    /api/carga_org_lot/patriarcas/{id}/      # Retrieve
PUT    /api/carga_org_lot/patriarcas/{id}/      # Update
PATCH  /api/carga_org_lot/patriarcas/{id}/      # Partial Update
DELETE /api/carga_org_lot/patriarcas/{id}/      # Destroy
```

**Custom actions:**
```python
GET /api/carga_org_lot/patriarcas/{id}/organogramas/  # Organogramas do patriarca
GET /api/carga_org_lot/patriarcas/{id}/lotacoes/      # Lotações do patriarca
```

### 🌳 Organograma API (`organograma_api.py`)

**ViewSet:** `OrganogramaVersaoViewSet`

**Custom actions:**
```python
GET /api/carga_org_lot/organogramas/{id}/orgaos/       # Lista de órgãos
GET /api/carga_org_lot/organogramas/{id}/hierarquia/   # Hierarquia em árvore
GET /api/carga_org_lot/organogramas/{id}/json_envio/   # JSON para API externa
```

### 💼 Lotação API (`lotacao_api.py`)

**ViewSet:** `LotacaoVersaoViewSet`

**Custom actions:**
```python
GET /api/carga_org_lot/lotacoes/{id}/registros/        # Registros de lotação
GET /api/carga_org_lot/lotacoes/{id}/inconsistencias/  # Inconsistências
GET /api/carga_org_lot/lotacoes/{id}/estatisticas/     # Estatísticas
```

### 📦 Carga API (`carga_api.py`)

**ViewSet:** `CargaPatriarcaViewSet`

**Custom actions:**
```python
GET /api/carga_org_lot/cargas/{id}/timeline/  # Timeline de status
```

---

## 📦 Imports e Compatibilidade

### Compatibilidade Retroativa

O arquivo `__init__.py` centraliza todos os imports, garantindo que código existente continue funcionando:

```python
# Antes da refatoração (ainda funciona)
from carga_org_lot.views import carga_login, PatriarcaViewSet

# Depois da refatoração (recomendado)
from carga_org_lot.views.web_views import carga_login
from carga_org_lot.views.api_views import PatriarcaViewSet
```

### Import Direto dos Submódulos

```python
# Web Views
from carga_org_lot.views.web_views.auth_views import carga_login
from carga_org_lot.views.web_views.dashboard_views import carga_dashboard

# API Views
from carga_org_lot.views.api_views.patriarca_api import PatriarcaViewSet
from carga_org_lot.views.api_views.dashboard_api import dashboard_stats
```

---

## 📝 Exemplos de Uso

### URLs Configuration

**Web URLs (`urls/web_urls.py`):**
```python
from django.urls import path
from ..views.web_views import (
    carga_login,
    carga_dashboard,
    patriarca_list,
    patriarca_detail,
)

urlpatterns = [
    path('login/', carga_login, name='login'),
    path('', carga_dashboard, name='dashboard'),
    path('patriarcas/', patriarca_list, name='patriarca_list'),
    path('patriarcas/<int:patriarca_id>/', patriarca_detail, name='patriarca_detail'),
]
```

**API URLs (`urls/api_urls.py`):**
```python
from rest_framework.routers import DefaultRouter
from ..views.api_views import (
    PatriarcaViewSet,
    OrganogramaVersaoViewSet,
    LotacaoVersaoViewSet,
    CargaPatriarcaViewSet,
)

router = DefaultRouter()
router.register(r'patriarcas', PatriarcaViewSet, basename='patriarca')
router.register(r'organogramas', OrganogramaVersaoViewSet, basename='organograma')
router.register(r'lotacoes', LotacaoVersaoViewSet, basename='lotacao')
router.register(r'cargas', CargaPatriarcaViewSet, basename='carga')

urlpatterns = router.urls
```

### Usando o Decorador de Autenticação

```python
from carga_org_lot.views.web_views.auth_views import carga_org_lot_required

@carga_org_lot_required
def minha_view_protegida(request):
    # Apenas usuários autenticados e com permissão CARGA_ORG_LOT
    return render(request, 'template.html')
```

---

## ✅ Benefícios da Nova Estrutura

1. **Separação de Responsabilidades**: Web views e API views em subpastas distintas
2. **Módulos Menores**: Cada arquivo focado em uma entidade/funcionalidade
3. **Navegação Facilitada**: Fácil localizar código por contexto
4. **Manutenibilidade**: Mudanças isoladas em arquivos específicos
5. **Escalabilidade**: Estrutura preparada para crescimento
6. **Compatibilidade**: Código existente continua funcionando

---

## 📚 Referências

- [Django Views](https://docs.djangoproject.com/en/stable/topics/http/views/)
- [Django REST Framework ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)
- [Django URL Dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/)
