# Checklist de Limpeza - Branch refactor/iam-service-architecture

> **Issue relacionada:** [#10](https://github.com/ProjetcsGPP/gpp_plataform/issues/10)  
> **Data:** 25/02/2026

## 🚨 Passo 1: Executar Script de Limpeza

```powershell
# Execute na raiz do projeto
.\cleanup-branch.ps1
```

O script irá:
- ❌ Remover todos os arquivos `fix_*.py` (18 arquivos)
- ❌ Remover arquivos de log e diagnóstico (5 arquivos)
- ❌ Remover arquivos temporários (6 arquivos)
- ✅ Validar existência de todos os `__init__.py`

---

## 📝 Passo 2: Revisar e Atualizar __init__.py

### Accounts App

#### `accounts/__init__.py`
```python
# Exportar configuração da app
default_app_config = 'accounts.apps.AccountsConfig'
```

#### `accounts/services/__init__.py`
```python
# Exportar serviços principais
from .user_service import UserService
from .auth_service import AuthService

__all__ = ['UserService', 'AuthService']
```

#### `accounts/views/__init__.py`
```python
# Exportar views principais
from .api_views import *
from .web_views import *
```

#### `accounts/urls/__init__.py`
```python
# Pode permanecer vazio se não houver exports necessários
```

#### `accounts/templatetags/__init__.py`
```python
# Pode permanecer vazio - templatetags são carregadas automaticamente
```

#### `accounts/tests/__init__.py`
```python
# Pode permanecer vazio
```

---

### Core App

#### `core/__init__.py`
```python
# Exportar módulos principais do core
from .iam import AuthorizationService

__all__ = ['AuthorizationService']
```

#### `core/iam/__init__.py`
```python
# Exportar AuthorizationService Central
from .authorization_service import AuthorizationService
from .permissions import Permission, Role
from .decorators import require_permission, require_role

__all__ = [
    'AuthorizationService',
    'Permission',
    'Role',
    'require_permission',
    'require_role',
]
```

---

### Acoes_PNGI App

#### `acoes_pngi/__init__.py`
```python
# Exportar configuração da app
default_app_config = 'acoes_pngi.apps.AcoesPngiConfig'
```

#### `acoes_pngi/services/__init__.py`
```python
# Exportar serviços principais
from .acao_service import AcaoService
from .processo_service import ProcessoService

__all__ = ['AcaoService', 'ProcessoService']
```

#### `acoes_pngi/views/__init__.py`
```python
# Exportar views principais
from .api_views import *
from .web_views import *
```

#### `acoes_pngi/utils/__init__.py`
```python
# Exportar utilitários
from .validators import *
from .helpers import *
```

#### `acoes_pngi/urls/__init__.py`
```python
# Pode permanecer vazio
```

#### `acoes_pngi/templatetags/__init__.py`
```python
# Pode permanecer vazio
```

#### `acoes_pngi/tests/__init__.py`
```python
# Pode permanecer vazio
```

---

## 📚 Passo 3: Atualizar Documentação

### README.md (Root)

**Seções para atualizar:**

1. **Arquitetura do Projeto**
   - [ ] Adicionar diagrama/descrição do AuthorizationService Central
   - [ ] Explicar como as apps integram com o IAM
   - [ ] Documentar fluxo de autorização

2. **Setup e Instalação**
   - [ ] Atualizar requirements se necessário
   - [ ] Adicionar configurações de permissões
   - [ ] Documentar variáveis de ambiente relacionadas a IAM

3. **Uso do Sistema de Permissões**
   - [ ] Exemplos de uso do AuthorizationService
   - [ ] Como definir permissões customizadas
   - [ ] Como usar decorators de autorização

---

### accounts/README.md

**Tópicos principais:**

1. **Integração com AuthorizationService**
   ```python
   from core.iam import AuthorizationService
   
   # Exemplo de uso
   auth_service = AuthorizationService()
   if auth_service.has_permission(user, 'accounts.view_user'):
       # Lógica aqui
   ```

2. **Sistema de Permissões**
   - [ ] Listar permissões disponíveis na app
   - [ ] Explicar hierarquia de roles
   - [ ] Documentar middleware de autenticação

3. **API Endpoints**
   - [ ] Atualizar documentação de endpoints
   - [ ] Adicionar informações sobre permissões necessárias

---

### acoes_pngi/README.md

**Tópicos principais:**

1. **Uso do AuthorizationService**
   ```python
   from core.iam import require_permission
   
   @require_permission('acoes_pngi.add_acao')
   def create_acao(request):
       # Lógica aqui
   ```

2. **Permissões Específicas**
   - [ ] Listar permissões da app
   - [ ] Explicar lógica de permissões por processo
   - [ ] Documentar permissões hierárquicas (unidade, órgão, etc.)

3. **Fluxos de Autorização**
   - [ ] Fluxo de criação de ações
   - [ ] Fluxo de aprovação
   - [ ] Fluxo de visualização/edição

---

### DOCUMENTATION_GUIDE.md

**Seções para adicionar/atualizar:**

1. **Padrões de Autorização**
   - [ ] Como usar o AuthorizationService
   - [ ] Quando usar decorators vs. checks manuais
   - [ ] Boas práticas de segurança

2. **Estrutura de Permissões**
   - [ ] Naming convention: `app.action_model`
   - [ ] Hierarquia de roles
   - [ ] Permissões customizadas

3. **Testes de Autorização**
   - [ ] Como testar permissões
   - [ ] Fixtures para testes
   - [ ] Exemplos de testes

---

### QUICK_START_DOCS.md

**Adições necessárias:**

1. **Setup de Permissões**
   ```bash
   # Criar superusuario
   python manage.py createsuperuser
   
   # Carregar permissões padrão
   python manage.py loaddata permissions
   ```

2. **Primeiro Uso**
   - [ ] Como atribuir permissões a usuários
   - [ ] Como criar roles customizadas
   - [ ] Como testar autorização

---

## ✅ Passo 4: Validação Final

### 4.1 Executar Testes

```bash
# Testes completos
pytest

# Testes específicos de autorização
pytest core/iam/tests/
pytest accounts/tests/ -k "permission"
pytest acoes_pngi/tests/ -k "permission"
```

### 4.2 Verificar Imports

```bash
# Verificar se todos os imports estão funcionando
python manage.py check

# Testar imports de cada app
python -c "from core.iam import AuthorizationService; print('OK')"
python -c "from accounts.services import UserService; print('OK')"
python -c "from acoes_pngi.services import AcaoService; print('OK')"
```

### 4.3 Lint e Type Checking

```bash
# Pylance/Pyright
pyright .

# Flake8 (se configurado)
flake8 accounts/ core/ acoes_pngi/
```

---

## 🚀 Passo 5: Commit e Push

```bash
# Verificar status
git status

# Revisar mudanças
git diff

# Adicionar arquivos
git add -A

# Commit
git commit -m "feat: Limpeza e organização da branch refactor/iam-service-architecture

- Remove arquivos obsoletos de correção (fix_*.py)
- Remove arquivos de log e diagnóstico
- Remove arquivos temporários
- Atualiza e valida __init__.py de todas as apps
- Atualiza documentação focando no AuthorizationService Central

Closes #10"

# Push
git push origin refactor/iam-service-architecture
```

---

## 📊 Resumo de Arquivos

### Arquivos Removidos (Total: ~29)
- Scripts de correção: 18 arquivos
- Logs e diagnósticos: 5 arquivos
- Temporários: 6 arquivos

### Arquivos Validados
- `__init__.py`: 15 arquivos

### Arquivos Atualizados
- `README.md` (root)
- `accounts/README.md`
- `acoes_pngi/README.md`
- `DOCUMENTATION_GUIDE.md`
- `QUICK_START_DOCS.md`

---

## ❓ Troubleshooting

### Erro: "Module not found"
- Verifique se o `__init__.py` existe no diretório
- Verifique se os imports estão corretos
- Execute `python manage.py check`

### Erro: "Permission denied" ao remover arquivos
- Execute o PowerShell como Administrador
- Verifique se os arquivos não estão abertos em outro programa

### Testes falhando após limpeza
- Verifique se algum teste dependia de arquivos removidos
- Atualize fixtures se necessário
- Revise imports nos arquivos de teste

---

**Última atualização:** 25/02/2026  
**Autor:** GPP Team
