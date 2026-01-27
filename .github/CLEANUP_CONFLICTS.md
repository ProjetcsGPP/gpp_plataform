# Limpeza de Diretórios Conflitantes

## Diretórios Removidos

Os seguintes diretórios vazios foram removidos para prevenir conflitos de import:

### auth_service
- ✅ `auth_service/views/api_views/` (commit 62c91fb)
- ✅ `auth_service/views/web_views/` (commit d67bfcd)

### accounts  
- ✅ `accounts/views/api_views/` (este commit)
- ✅ `accounts/views/web_views/` (este commit)

### db_service
- ✅ `db_service/views/api_views/` (este commit)
- ✅ `db_service/views/web_views/` (este commit)

## Arquivos Mantidos

Os seguintes **arquivos** `.py` foram mantidos:

- ✅ `auth_service/views/api_views.py`
- ✅ `auth_service/views/web_views.py`
- ✅ `accounts/views/api_views.py`
- ✅ `accounts/views/web_views.py`
- ✅ `db_service/views/views.py`

## Motivo

Python prioriza diretórios (packages) sobre arquivos ao fazer imports.
Se existir tanto `api_views.py` quanto `api_views/`, o diretório
será importado primeiro, causando ImportError se o `__init__.py` estiver vazio.

## Referência

Ver: docs/TROUBLESHOOTING_TESTS.md
