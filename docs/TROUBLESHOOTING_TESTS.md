# Troubleshooting - Erros de Testes

## 🚨 Problema Resolvido: ImportError em Múltiplas Apps

### Erro Encontrado

```python
ImportError: cannot import name 'CustomTokenObtainPairView' from 'auth_service.views.api_views'
```

### Causa Raiz

**Conflito entre arquivo e diretório com mesmo nome em 3 aplicações**

A estrutura estava assim em **TODAS** as apps afetadas:

```
auth_service/views/
├── api_views.py          ← Arquivo com as views ✅
├── api_views/            ← Diretório vazio ❌ CONFLITO!
│   └── __init__.py       ← Vazio
├── web_views.py          ← Arquivo com as views ✅
└── web_views/            ← Diretório vazio ❌ CONFLITO!
    └── __init__.py       ← Vazio
```

**Como Python resolve imports:**

1. Quando você faz `from auth_service.views.api_views import ...`
2. Python **procura primeiro por diretórios** (packages)
3. Encontra `api_views/` e carrega o `__init__.py` desse diretório
4. Como o `__init__.py` está vazio, não encontra `CustomTokenObtainPairView`
5. **Nunca chega a verificar o arquivo `api_views.py`** ❌

---

### ✅ Solução Aplicada

**Deletados todos os diretórios vazios conflitantes em 3 apps:**

| App | Diretórios Removidos | Commits |
|-----|----------------------|----------|
| **auth_service** | `api_views/`, `web_views/` | [62c91fb](https://github.com/ProjetcsGPP/gpp_plataform/commit/62c91fb), [d67bfcd](https://github.com/ProjetcsGPP/gpp_plataform/commit/d67bfcd) |
| **accounts** | `api_views/`, `web_views/` | [f42535f](https://github.com/ProjetcsGPP/gpp_plataform/commit/f42535f), [fad4a8b](https://github.com/ProjetcsGPP/gpp_plataform/commit/fad4a8b) |
| **db_service** | `api_views/`, `web_views/` | [3e1192c](https://github.com/ProjetcsGPP/gpp_plataform/commit/3e1192c), [14c37dc](https://github.com/ProjetcsGPP/gpp_plataform/commit/14c37dc) |

**Total**: 6 diretórios vazios removidos ✅

---

### 📋 Resumo das Correções

```
✅ auth_service/views/
   ├── api_views.py          ← Mantido
   └── web_views.py          ← Mantido
   ❌ api_views/            ← REMOVIDO
   ❌ web_views/            ← REMOVIDO

✅ accounts/views/
   ├── api_views.py          ← Mantido
   └── web_views.py          ← Mantido
   ❌ api_views/            ← REMOVIDO
   ❌ web_views/            ← REMOVIDO

✅ db_service/views/
   └── views.py              ← Mantido
   ❌ api_views/            ← REMOVIDO
   ❌ web_views/            ← REMOVIDO
```

---

## 🛠️ Soluções Alternativas

Se você **realmente precisa** manter tanto o arquivo quanto o diretório:

### Opção 1: Exportar no `__init__.py` do diretório

```python
# auth_service/views/api_views/__init__.py
from ..api_views import (
    CustomTokenObtainPairView,
    session_login,
    session_logout,
    session_me,
    get_csrf_token
)

__all__ = [
    'CustomTokenObtainPairView',
    'session_login',
    'session_logout',
    'session_me',
    'get_csrf_token',
]
```

### Opção 2: Renomear o arquivo

```
auth_service/views/
├── api.py                ← Renomeado
└── api_views/            ← Diretório
```

E atualizar imports:

```python
# auth_service/urls/api_urls.py
from ..views.api import CustomTokenObtainPairView  # Mudou!
```

### Opção 3: Usar import absoluto

```python
# Forçar import do arquivo
import importlib.util
spec = importlib.util.spec_from_file_location(
    "api_views",
    "auth_service/views/api_views.py"
)
module = importlib.util.module_from_spec(spec)
```

⚠️ **Não recomendado** - muito verboso e confuso.

---

## 🔍 Como Diagnosticar Problemas Similares

### 1. Verificar se há conflito arquivo/diretório

```bash
# Listar arquivos e diretórios
ls -la auth_service/views/

# Verificar se existe tanto arquivo quanto diretório
ls auth_service/views/api_views*

# No Windows (PowerShell)
Get-ChildItem auth_service/views/ | Where-Object { $_.Name -like "api_views*" }
```

### 2. Testar import no Python interativo

```python
import sys
sys.path.insert(0, '.')  # Adiciona diretório atual

# Tenta importar
try:
    from auth_service.views.api_views import CustomTokenObtainPairView
    print("✅ Import OK")
    print(f"Localização: {CustomTokenObtainPairView.__module__}")
except ImportError as e:
    print(f"❌ Erro: {e}")

    # Verificar o que Python está importando
    import auth_service.views.api_views as api_views
    print(f"Arquivo: {api_views.__file__}")
    print(f"Conteúdo: {dir(api_views)}")
```

### 3. Usar `python -v` para debug de imports

```bash
python -v -c "from auth_service.views.api_views import CustomTokenObtainPairView"
```

Mostra toda a cadeia de imports e onde Python procura.

### 4. Script de Detecção Automática

```python
# detect_conflicts.py
import os
from pathlib import Path

def find_conflicts(root_dir='.'):
    """Encontra conflitos arquivo/diretório"""
    conflicts = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                base_name = filename[:-3]  # Remove .py
                if base_name in dirnames:
                    conflict_path = os.path.join(dirpath, base_name)
                    conflicts.append({
                        'file': os.path.join(dirpath, filename),
                        'dir': conflict_path
                    })

    return conflicts

if __name__ == '__main__':
    conflicts = find_conflicts()
    if conflicts:
        print(f"❌ Encontrados {len(conflicts)} conflitos:")
        for c in conflicts:
            print(f"  - {c['file']} ↔ {c['dir']}/")
    else:
        print("✅ Nenhum conflito encontrado!")
```

Uso:
```bash
python detect_conflicts.py
```

---

## ✅ Boas Práticas para Evitar o Problema

### 1. **Nunca misture arquivo e diretório com mesmo nome**

❌ **RUIM:**
```
views/
├── api_views.py
└── api_views/
```

✅ **BOM:**
```
views/
├── api.py              ← Arquivo
└── api_views/          ← Diretório
```

OU

```
views/
└── api_views/          ← Apenas diretório
    ├── __init__.py
    ├── authentication.py
    └── session.py
```

### 2. **Use convenções claras de nomenclatura**

```
views/
├── api/                ← Diretório para módulos de API
│   ├── __init__.py
│   ├── auth.py
│   └── users.py
└── web/                ← Diretório para views web
    ├── __init__.py
    ├── dashboard.py
    └── reports.py
```

### 3. **Sempre preencha `__init__.py` em packages**

Se criar um diretório como package, **sempre** exporte o que for necessário:

```python
# views/api/__init__.py
from .auth import CustomTokenObtainPairView, session_login
from .users import UserViewSet

__all__ = [
    'CustomTokenObtainPairView',
    'session_login',
    'UserViewSet',
]
```

### 4. **Use linters e pre-commit hooks**

Adicione ao `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: check-file-dir-conflicts
      name: Check for file/directory naming conflicts
      entry: python detect_conflicts.py
      language: system
      pass_filenames: false
```

---

## 📝 Outros Erros Comuns em Testes

### Erro: `Table doesn't exist`

**Causa**: Migrações não aplicadas no banco de teste.

**Solução**:
```bash
python manage.py migrate --database=gpp_plataform_db
python manage.py test carga_org_lot
```

### Erro: `Authentication credentials were not provided`

**Causa**: Testes de API sem autenticação.

**Solução**:
```python
def setUp(self):
    self.client = APIClient()
    self.user = User.objects.create_user(...)
    self.client.force_authenticate(user=self.user)  # ← Necessário!
```

### Erro: `Multiple databases`

**Causa**: App usa múltiplos bancos.

**Solução**:
```python
class MyTest(TestCase):
    databases = {'default', 'gpp_plataform_db'}  # ← Declarar!
```

---

## 📊 Estatísticas da Correção

| Métrica | Valor |
|---------|-------|
| **Apps corrigidas** | 3 |
| **Diretórios removidos** | 6 |
| **Commits de correção** | 6 |
| **Tempo de diagnóstico** | ~5 min |
| **Tempo de correção** | ~3 min |
| **Impacto** | ✅ Crítico (bloqueava testes) |

---

## 📚 Referências

- [Python Import System](https://docs.python.org/3/reference/import.html)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Python Modules](https://docs.python.org/3/tutorial/modules.html)
- [PEP 420 - Implicit Namespace Packages](https://peps.python.org/pep-0420/)

---

**Última Atualização**: 27 de janeiro de 2026
**Status**: ✅ Todos os conflitos resolvidos
**Apps Afetadas**: auth_service, accounts, db_service
**Commits**: [62c91fb](https://github.com/ProjetcsGPP/gpp_plataform/commit/62c91fb) a [14c37dc](https://github.com/ProjetcsGPP/gpp_plataform/commit/14c37dc)
