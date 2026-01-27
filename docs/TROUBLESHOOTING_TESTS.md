# Troubleshooting - Erros de Testes

## 🚨 Problema Resolvido: ImportError em `auth_service`

### Erro Encontrado

```python
ImportError: cannot import name 'CustomTokenObtainPairView' from 'auth_service.views.api_views'
```

### Causa Raiz

**Conflito entre arquivo e diretório com mesmo nome**

A estrutura estava assim:

```
auth_service/views/
├── api_views.py          ← Arquivo com as views
├── api_views/            ← Diretório vazio (CONFLITO!)
│   └── __init__.py       ← Vazio
├── web_views.py          ← Arquivo com as views
└── web_views/            ← Diretório vazio (CONFLITO!)
    └── __init__.py       ← Vazio
```

**Como Python resolve imports:**

1. Quando você faz `from auth_service.views.api_views import ...`
2. Python **procura primeiro por diretórios** (packages)
3. Se encontra `api_views/`, carrega o `__init__.py` desse diretório
4. Como o `__init__.py` está vazio, não encontra `CustomTokenObtainPairView`
5. **Nunca chega a verificar o arquivo `api_views.py`** ❌

### Solução Aplicada

**Deletar os diretórios vazios:**

```bash
# Commits que resolveram:
# 62c91fb - Remove api_views/ directory
# d67bfcd - Remove web_views/ directory
```

**Estrutura corrigida:**

```
auth_service/views/
├── __init__.py
├── api_views.py          ← Agora importa corretamente! ✅
└── web_views.py          ← Sem conflitos! ✅
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

## 📚 Referências

- [Python Import System](https://docs.python.org/3/reference/import.html)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Python Modules](https://docs.python.org/3/tutorial/modules.html)

---

**Última Atualização**: 27 de janeiro de 2026  
**Problema Resolvido**: ✅ ImportError em auth_service  
**Commits**: [62c91fb](https://github.com/ProjetcsGPP/gpp_plataform/commit/62c91fb), [d67bfcd](https://github.com/ProjetcsGPP/gpp_plataform/commit/d67bfcd)
