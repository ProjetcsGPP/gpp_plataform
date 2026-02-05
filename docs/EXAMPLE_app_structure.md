# 📋 Documentação da Estrutura do GPP Platform

*Exemplo de como o arquivo fica após executar `python manage.py generate_docs`*

## 📑 Índice

- [Common](#common)
- [Accounts](#accounts)
- [Auth Service](#auth_service)
- [Portal](#portal)
- [Carga Org Lot](#carga_org_lot)
- [Ações PNGI](#acoes_pngi)

---

## Common

**Path:** `C:\Projects\gpp_plataform\common`

### 📁 Estrutura de Arquivos

```
.
  ├─ __init__.py
  ├─ admin.py
  ├─ apps.py
  ├─ models.py
  ├─ views.py
  ├─ tests.py
  ├─ management/
  ├─ templates/
  ├─ middleware/
  ├─ services/
migrations/
  ├─ __init__.py
  ├─ 0001_initial.py
```

### 🗂️ Models

#### `AppConfig`

**Fields:** `id, name, description, url, icon, order, created_at, updated_at`

#### `AuditLog`

**Fields:** `id, user, action, model, object_id, timestamp, details`

### 👀 Views

| Nome | Tipo | Módulo |
|------|------|--------|
| `error_404` | function | views |
| `error_500` | function | views |

### 👨‍💼 Admin Registrado

- `AppConfig` (AppConfigAdmin)
- `AuditLog` (AuditLogAdmin)

---

## Accounts

**Path:** `C:\Projects\gpp_plataform\accounts`

### 📁 Estrutura de Arquivos

```
.
  ├─ __init__.py
  ├─ models.py
  ├─ views.py
  ├─ admin.py
  ├─ backends.py
  ├─ serializers.py
middleware/
  ├─ active_role.py
views/
  ├─ __init__.py
  ├─ auth_views.py
templates/
  ├─ login.html
```

### 🗂️ Models

#### `User`

**Fields:** `id, email, username, first_name, last_name, is_staff, is_active, is_superuser, date_joined, last_login`

#### `Role`

**Fields:** `id, name, description, permissions`

#### `UserRole`

**Fields:** `id, user, role, assigned_at`

### 👀 Views

| Nome | Tipo | Módulo |
|------|------|--------|
| `login` | function | auth_views |
| `logout` | function | auth_views |
| `register` | function | auth_views |
| `profile` | function | auth_views |
| `change_password` | function | auth_views |

### 🔗 URLs

**Namespace:** `accounts`

**Padrões:**
- `login/` → `login`
- `logout/` → `logout`
- `register/` → `register`
- `profile/` → `profile`
- `password/` → `change_password`

### 👨‍💼 Admin Registrado

- `User` (UserAdmin)
- `Role` (RoleAdmin)

---

## Carga Org Lot

**Path:** `C:\Projects\gpp_plataform\carga_org_lot`

### 📁 Estrutura de Arquivos

```
.
  ├─ __init__.py
  ├─ models.py
  ├─ admin.py
views/
  ├─ __init__.py
  ├─ web_views/
  ├─    ├─ __init__.py
  ├─    ├─ auth_views.py
  ├─    ├─ patriarca_views.py
  ├─    ├─ organograma_views.py
  ├─    ├─ lotacao_views.py
  ├─    ├─ carga_views.py
  ├─    ├─ dashboard_views.py
  ├─    ├─ upload_views.py
  ├─ api_views/
  ├─    ├─ __init__.py
  ├─    ├─ serializers.py
urls/
  ├─ __init__.py
  ├─ api_urls.py
```

### 🗂️ Models

#### `Patriarca`

**Fields:** `id, nome, sigla, descricao, ativo, criado_em, atualizado_em`

#### `Organograma`

**Fields:** `id, patriarca, nome, versao, data_vigencia, ativo, criado_em`

#### `Lotacao`

**Fields:** `id, organograma, codigo, nome, nivel, ativo, criado_em`

#### `Carga`

**Fields:** `id, patriarca, data_envio, status, processado_em`

### 👀 Views

| Nome | Tipo | Módulo |
|------|------|--------|
| `carga_dashboard` | function | web_views |
| `patriarca_list` | function | web_views |
| `patriarca_detail` | function | web_views |
| `organograma_list` | function | web_views |
| `organograma_detail` | function | web_views |
| `organograma_hierarquia_json` | function | web_views |
| `lotacao_list` | function | web_views |
| `lotacao_detail` | function | web_views |
| `lotacao_inconsistencias` | function | web_views |
| `carga_list` | function | web_views |
| `carga_detail` | function | web_views |
| `upload_page` | function | web_views |
| `upload_organograma_handler` | function | web_views |
| `upload_lotacao_handler` | function | web_views |
| `search_orgao_ajax` | function | web_views |

### 🔗 URLs

**Namespace:** `carga_org_lot`

**Padrões:**
- `` → `dashboard`
- `patriarcas/` → `patriarca_list`
- `patriarcas/<id>/` → `patriarca_detail`
- `organogramas/` → `organograma_list`
- `organogramas/<id>/` → `organograma_detail`
- `organogramas/<id>/hierarquia/json/` → `organograma_hierarquia_json`
- `lotacoes/` → `lotacao_list`
- `lotacoes/<id>/` → `lotacao_detail`
- `lotacoes/<id>/inconsistencias/` → `lotacao_inconsistencias`
- `cargas/` → `carga_list`
- `cargas/<id>/` → `carga_detail`
- `upload/` → `upload_page`
- `upload/organograma/` → `upload_organograma_handler`
- `upload/lotacao/` → `upload_lotacao_handler`
- `ajax/search-orgao/` → `search_orgao_ajax`

### 👨‍💼 Admin Registrado

- `Patriarca` (PatriarcaAdmin)
- `Organograma` (OrganoramaAdmin)
- `Lotacao` (LotacaoAdmin)
- `Carga` (CargaAdmin)

---

## Ações PNGI

**Path:** `C:\Projects\gpp_plataform\acoes_pngi`

### 📁 Estrutura de Arquivos

```
.
  ├─ __init__.py
  ├─ models.py
  ├─ admin.py
views/
  ├─ __init__.py
  ├─ web_views/
  ├─    ├─ __init__.py
  ├─    ├─ acao_views.py
  ├─    ├─ dashboard_views.py
  ├─ api_views/
  ├─    ├─ __init__.py
  ├─    ├─ acao_api.py
urls/
  ├─ __init__.py
  ├─ api_urls.py
```

### 🗂️ Models

#### `Acao`

**Fields:** `id, titulo, descricao, status, patriarca, responsavel, data_inicio, data_fim`

#### `AcaoMeta`

**Fields:** `id, acao, meta, valor_alvo, valor_atingido, data_atualizacao`

### 👀 Views

| Nome | Tipo | Módulo |
|------|------|--------|
| `acoes_dashboard` | function | web_views |
| `acao_list` | function | web_views |
| `acao_detail` | function | web_views |
| `acao_create` | function | web_views |
| `acao_edit` | function | web_views |

### 🔗 URLs

**Namespace:** `acoes_pngi`

**Padrões:**
- `` → `dashboard`
- `acoes/` → `acao_list`
- `acoes/<id>/` → `acao_detail`
- `acoes/novo/` → `acao_create`
- `acoes/<id>/editar/` → `acao_edit`

---

## Como Usar Esta Documentação

1. **Procure pela app que precisa** (ex: `carga_org_lot`)
2. **Veja a seção 👀 Views** para confirmar que a view existe
3. **Copie o nome exato** da documentação
4. **Use com confiança** sabendo que a view existe

Exemplo:
```python
# ✅ Seguro - view existe
path('patriarcas/', web_views.patriarca_list, name='patriarca_list'),

# ❌ Erro - view não existe (não está na documentação)
path('patriarcas/novo/', web_views.patriarca_create, name='patriarca_create'),
```

---

**Gere esta documentação com:** `python manage.py generate_docs`
