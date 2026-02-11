# Guia de Execução de Testes - Ações PNGI

## 📊 Visão Geral

Este guia documenta como executar e debugar os **~500 testes automatizados** implementados para o módulo Ações PNGI.

### Estrutura de Testes

```
acoes_pngi/tests/
├── __init__.py
├── test_permissions.py                         (~100 testes - FASE 3)
├── test_api_views.py                           (~100 testes - FASE 1.1)
├── test_api_views_acoes.py                     (~120 testes - FASE 1.2)
├── test_api_views_alinhamento_responsaveis.py  (~100 testes - FASE 1.3)
├── test_views.py                                (~80 testes - FASE 2)
├── run_tests.py                                 (script auxiliar)
└── README_TESTES.md                             (este arquivo)
```

---

## ⚡ Como Executar os Testes

### Opção 1: Todos os Testes de Uma Vez

```bash
# Executar TODOS os testes do módulo
python manage.py test acoes_pngi.tests

# Com mais verbosidade (recomendado)
python manage.py test acoes_pngi.tests -v 2

# Com warnings ativados
python -Wa manage.py test acoes_pngi.tests
```

### Opção 2: Por Fase (Recomendado para Debug)

```bash
# FASE 3: Testes de Permissions (~100 testes)
python manage.py test acoes_pngi.tests.test_permissions -v 2

# FASE 1.1: API - Eixo, Situação, Vigência (~100 testes)
python manage.py test acoes_pngi.tests.test_api_views -v 2

# FASE 1.2: API - Ações, Prazos, Destaques (~120 testes)
python manage.py test acoes_pngi.tests.test_api_views_acoes -v 2

# FASE 1.3: API - Alinhamento e Responsáveis (~100 testes)
python manage.py test acoes_pngi.tests.test_api_views_alinhamento_responsaveis -v 2

# FASE 2: Testes Web (~80 testes)
python manage.py test acoes_pngi.tests.test_views -v 2
```

### Opção 3: Teste Específico (Para Debug Focado)

```bash
# Uma classe específica
python manage.py test acoes_pngi.tests.test_permissions.IsCoordernadorOrGestorPNGITests -v 2

# Um método específico
python manage.py test acoes_pngi.tests.test_permissions.IsCoordernadorOrGestorPNGITests.test_coordenador_can_create -v 2
```

### Opção 4: Usando o Script Auxiliar

```bash
# Todos os testes (organizado)
python acoes_pngi/tests/run_tests.py all

# Apenas permissions
python acoes_pngi/tests/run_tests.py permissions

# Apenas API
python acoes_pngi/tests/run_tests.py api

# Apenas Web
python acoes_pngi/tests/run_tests.py web
```

---

## ⚠️ Erros Comuns e Soluções

### 1. **ImportError: No module named 'acoes_pngi.permissions'**

**Causa:** O arquivo `permissions.py` ainda não existe no módulo.

**Solução:**
```bash
# Criar o arquivo permissions.py com as classes necessárias
touch acoes_pngi/permissions.py
```

**Conteúdo mínimo necessário em `acoes_pngi/permissions.py`:**
```python
from rest_framework import permissions

class IsCoordernadorOrGestorPNGI(permissions.BasePermission):
    """Permissão para COORDENADOR e GESTOR (configurações)"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Verificar se o usuário tem role COORDENADOR ou GESTOR
        from accounts.models import UserRole
        roles = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).values_list('role__codigoperfil', flat=True)
        
        return 'COORDENADOR_PNGI' in roles or 'GESTOR_PNGI' in roles


class IsCoordernadorGestorOrOperadorPNGI(permissions.BasePermission):
    """Permissão para COORDENADOR, GESTOR e OPERADOR (operações)"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        from accounts.models import UserRole
        roles = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).values_list('role__codigoperfil', flat=True)
        
        return any(r in roles for r in [
            'COORDENADOR_PNGI',
            'GESTOR_PNGI',
            'OPERADOR_ACAO'
        ])


class IsAnyPNGIRole(permissions.BasePermission):
    """Qualquer role PNGI tem acesso"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        from accounts.models import UserRole
        return UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).exists()
```

### 2. **Database Errors: "no such table" ou "relation does not exist"**

**Causa:** Banco de dados de teste não foi criado corretamente.

**Solução:**
```bash
# Garantir que as migrações estão aplicadas
python manage.py migrate
python manage.py migrate --database=gpp_plataform_db

# Executar testes criando novo banco
python manage.py test acoes_pngi.tests --keepdb=False
```

### 3. **"databases" attribute: {'default', 'gpp_plataform_db'}**

**Causa:** Testes precisam acessar múltiplos bancos.

**Solução:** Já implementado nos testes com:
```python
class BaseAPITestCase(TestCase):
    databases = {'default', 'gpp_plataform_db'}
```

### 4. **ImportError em models**

**Causa:** Algum model não foi importado corretamente.

**Solução:**
```bash
# Verificar se todos os models existem
python manage.py shell
>>> from acoes_pngi.models import Eixo, SituacaoAcao, VigenciaPNGI, Acoes
>>> # Se houver erro, o model não existe ou tem erro de sintaxe
```

### 5. **URL Reversal Errors em test_views.py**

**Causa:** URLs ainda não foram criadas.

**Solução temporária:** Os testes web já estão preparados com `try/except` para não quebrar se as URLs não existirem ainda.

### 6. **Conflitos de fixtures ou dados**

**Causa:** Dados criados em um teste interferem em outro.

**Solução:**
```python
# Usar TransactionTestCase se necessário
from django.test import TransactionTestCase

class MyTest(TransactionTestCase):
    databases = {'default', 'gpp_plataform_db'}
```

---

## 🔍 Troubleshooting Passo a Passo

### Passo 1: Verificar Pré-requisitos

```bash
# 1. Confirmar que o Django está instalado
python -c "import django; print(django.get_version())"

# 2. Confirmar DRF instalado
python -c "import rest_framework; print('OK')"

# 3. Verificar estrutura do app
ls -la acoes_pngi/
ls -la acoes_pngi/tests/

# 4. Verificar se __init__.py existe
ls acoes_pngi/tests/__init__.py
```

### Passo 2: Testar Imports

```bash
python manage.py shell

# No shell:
>>> from acoes_pngi.tests import test_permissions
>>> from acoes_pngi.tests import test_api_views
>>> from acoes_pngi import permissions
>>> from acoes_pngi import models
>>> # Se algum falhar, há erro de import
```

### Passo 3: Executar Teste Mais Simples Primeiro

```bash
# Começar com teste de permissions (sem dependência de views)
python manage.py test acoes_pngi.tests.test_permissions.IsAnyPNGIRoleTests -v 2
```

### Passo 4: Analisar Erros Específicos

```bash
# Executar com --debug-mode para mais detalhes
python manage.py test acoes_pngi.tests.test_permissions --debug-mode -v 2

# Ou com traceback completo
python -Wa manage.py test acoes_pngi.tests.test_permissions -v 2 2>&1 | tee test_output.txt
```

---

## 📝 Checklist de Arquivos Necessários

Antes de executar os testes, confirme que existem:

- [ ] `acoes_pngi/models.py` - Com todos os 11 models
- [ ] `acoes_pngi/permissions.py` - Com as 3 classes de permissão
- [ ] `acoes_pngi/serializers.py` - Com serializers para os models
- [ ] `acoes_pngi/views.py` ou `acoes_pngi/api_views.py` - Com os ViewSets
- [ ] `acoes_pngi/urls.py` - Com rotas da API
- [ ] `accounts/models.py` - Com User, Aplicacao, Role, UserRole
- [ ] Migrações aplicadas em ambos os bancos

---

## 📊 Cobertura de Testes

### Por Model (11 models):

| # | Model | Testes API | Testes Web | Permission |
|---|-------|------------|------------|------------|
| 1 | Eixo | ✓ | ✓ | ✓ |
| 2 | SituacaoAcao | ✓ | - | ✓ |
| 3 | VigenciaPNGI | ✓ | ✓ | ✓ |
| 4 | TipoEntraveAlerta | ✓ | - | ✓ |
| 5 | Acoes | ✓ | ✓ | ✓ |
| 6 | AcaoPrazo | ✓ | - | ✓ |
| 7 | AcaoDestaque | ✓ | - | ✓ |
| 8 | TipoAnotacaoAlinhamento | ✓ | - | ✓ |
| 9 | AcaoAnotacaoAlinhamento | ✓ | - | ✓ |
| 10 | UsuarioResponsavel | ✓ | - | ✓ |
| 11 | RelacaoAcaoUsuarioResponsavel | ✓ | - | ✓ |

### Por Role (4 roles):

- ✓ COORDENADOR_PNGI: Acesso total
- ✓ GESTOR_PNGI: Acesso total
- ✓ OPERADOR_ACAO: Bloqueado em configurações
- ✓ CONSULTOR_PNGI: Apenas leitura

### Por Action:

- ✓ LIST (GET)
- ✓ RETRIEVE (GET)
- ✓ CREATE (POST)
- ✓ UPDATE (PUT/PATCH)
- ✓ DELETE (DELETE)
- ✓ Custom Actions (ativar, list_light, ativos, etc.)

---

## 🚀 Próximos Passos Após Executar Testes

1. **Analisar output dos testes**
   - Contar quantos passaram vs falharam
   - Identificar padrões de erro

2. **Corrigir erros por categoria**
   - Erros de import primeiro
   - Depois erros de banco de dados
   - Por último, erros de lógica

3. **Executar novamente após correções**
   ```bash
   python manage.py test acoes_pngi.tests.test_permissions -v 2
   ```

4. **Verificar cobertura**
   ```bash
   coverage run --source='acoes_pngi' manage.py test acoes_pngi.tests
   coverage report
   coverage html
   ```

---

## 📞 Suporte

Se encontrar erros não documentados aqui:

1. Copie o traceback completo
2. Identifique qual arquivo de teste está falhando
3. Verifique se o arquivo correspondente (permissions.py, views.py, etc.) existe
4. Consulte este README para erros conhecidos

---

**Última atualização:** 11/02/2026  
**Total de testes:** ~500  
**Status:** Pronto para execução e ajustes
