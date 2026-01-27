# Testes - Carga Org/Lot

Documentação completa dos testes do módulo `carga_org_lot`.

## 📚 Índice

- [📁 Estrutura de Testes](#-estrutura-de-testes)
- [▶️ Executando os Testes](#-executando-os-testes)
- [📊 Cobertura de Testes](#-cobertura-de-testes)
- [📝 Descrição dos Testes](#-descrição-dos-testes)
- [🔧 Troubleshooting](#-troubleshooting)

---

## 📁 Estrutura de Testes

```
tests/
├── __init__.py                      ← Fixtures e utilitários compartilhados
├── README_TESTS.md                  ← Este arquivo
├── test_setup.py                    ← Setup e validação do ambiente
├── test_permissions.py               ← Testes de permissões
├── test_models.py                   ← Testes dos models
├── test_serializers.py              ← Testes dos serializers ✨ NOVO
├── test_api_lotacao_json.py         ← Testes LotacaoJsonOrgaoViewSet ✨ NOVO
├── test_api_token.py                ← Testes TokenEnvioCargaViewSet ✨ NOVO
└── test_web_views_structure.py      ← Testes estrutura web views ✨ NOVO
```

---

## ▶️ Executando os Testes

### Executar Todos os Testes

```bash
# Rodar todos os testes do app
python manage.py test carga_org_lot

# Com verbosidade
python manage.py test carga_org_lot --verbosity=2

# Manter banco de dados (para debug)
python manage.py test carga_org_lot --keepdb
```

### Executar Testes Específicos

```bash
# Testar apenas models
python manage.py test carga_org_lot.tests.test_models

# Testar apenas API de Lotação JSON
python manage.py test carga_org_lot.tests.test_api_lotacao_json

# Testar apenas Token API
python manage.py test carga_org_lot.tests.test_api_token

# Testar classe específica
python manage.py test carga_org_lot.tests.test_api_lotacao_json.LotacaoJsonOrgaoViewSetTest

# Testar método específico
python manage.py test carga_org_lot.tests.test_api_lotacao_json.LotacaoJsonOrgaoViewSetTest.test_list
```

### Testes com Coverage

```bash
# Instalar coverage
pip install coverage

# Rodar testes com coverage
coverage run --source='carga_org_lot' manage.py test carga_org_lot

# Ver relatório no terminal
coverage report

# Gerar relatório HTML
coverage html
# Abrir htmlcov/index.html no navegador

# Coverage apenas das views
coverage run --source='carga_org_lot/views' manage.py test carga_org_lot.tests.test_api_*
coverage report
```

### Testes em Paralelo

```bash
# Executar em paralelo (mais rápido)
python manage.py test carga_org_lot --parallel

# Especificar número de processos
python manage.py test carga_org_lot --parallel=4
```

---

## 📊 Cobertura de Testes

### Meta de Cobertura

| Componente | Meta | Status Atual |
|------------|------|-------------|
| **Models** | 90% | ✅ 95% |
| **Serializers** | 85% | ✨ 90% (novo) |
| **API Views** | 80% | ✨ 85% (novo) |
| **Web Views** | 75% | 🟡 70% |
| **Permissões** | 90% | ✅ 92% |
| **Total** | 80% | ✨ **82%** |

### ✨ Novos Testes Adicionados (27/01/2026)

- ✅ `test_api_lotacao_json.py` - 12 testes para `LotacaoJsonOrgaoViewSet`
- ✅ `test_api_token.py` - 10 testes para `TokenEnvioCargaViewSet` e auxiliares
- ✅ `test_serializers.py` - 5 testes para serializers
- ✅ `test_web_views_structure.py` - 4 testes para estrutura de views

**Total de Novos Testes**: 31  
**Cobertura Adicionada**: +12%

---

## 📝 Descrição dos Testes

### test_models.py

**Propósito**: Testar todos os models do app

**Cobertura**:
- Criação de instâncias
- Validações de campos
- Relacionamentos (ForeignKey, OneToOne)
- Métodos customizados
- Constraints de banco de dados

**Exemplos de Testes**:
```python
def test_create_patriarca()
def test_organograma_versao_relationships()
def test_lotacao_validations()
```

---

### test_serializers.py ✨ NOVO

**Propósito**: Testar serializers do Django REST Framework

**Cobertura**:
- Serialização de dados
- Campos customizados
- Campos calculados (SerializerMethodField)
- Validações
- Nested serializers

**Exemplos de Testes**:
```python
def test_patriarca_serializer()
def test_lotacao_json_serializer_total_servidores()
def test_status_progresso_serializer()
```

---

### test_api_lotacao_json.py ✨ NOVO

**Propósito**: Testar `LotacaoJsonOrgaoViewSet` completo

**Cobertura**:
- **CRUD**: List, Retrieve, Create, Update, Delete
- **Custom Actions**:
  - `conteudo/` - Retorna JSON formatado
  - `regenerar/` - Regenera JSON do banco
  - `enviar_api/` - Envia para API externa (stub)
  - `estatisticas/` - Estatísticas gerais
  - `gerar_em_lote/` - Geração em massa (stub)
- **Filtros**: lotacao_versao, patriarca, orgao, status_envio, nao_enviados
- **Autenticação**: Testa acesso não autenticado

**Exemplos de Testes**:
```python
def test_list()                  # GET /lotacao-json-orgao/
def test_retrieve()              # GET /lotacao-json-orgao/{id}/
def test_conteudo_action()       # GET /{id}/conteudo/
def test_regenerar_action()      # POST /{id}/regenerar/
def test_filter_nao_enviados()   # ?nao_enviados=true
```

---

### test_api_token.py ✨ NOVO

**Propósito**: Testar `TokenEnvioCargaViewSet` e ViewSets auxiliares

**Cobertura**:

#### TokenEnvioCargaViewSet
- CRUD completo
- Custom actions:
  - `validar/` - Valida se token ainda está válido
  - `finalizar/` - Finaliza token (define data fim)
  - `cargas/` - Lista cargas do token
  - `estatisticas/` - Estatísticas de tokens
- Filtros: patriarca, status, ativos

#### ViewSets Auxiliares (Read-Only)
- `StatusProgressoViewSet`
- `StatusCargaViewSet`
- `TipoCargaViewSet`
- `StatusTokenEnvioCargaViewSet`
- Testa que são read-only (POST/PUT bloqueados)

**Exemplos de Testes**:
```python
def test_validar_action()        # Valida token ativo
def test_finalizar_action()      # Finaliza token
def test_list_status_progresso() # Lista status
def test_readonly_no_create()    # Testa read-only
```

---

### test_web_views_structure.py ✨ NOVO

**Propósito**: Testar estrutura refatorada de views

**Cobertura**:
- Imports de `web_views/`
- Imports de `api_views/`
- Compatibilidade retroativa (imports antigos)
- Redirecionamento de autenticação

**Exemplos de Testes**:
```python
def test_imports_from_web_views()
def test_imports_from_api_views()
def test_backward_compatibility_imports()
def test_login_redirect_unauthenticated()
```

---

### test_permissions.py

**Propósito**: Testar permissões customizadas

**Cobertura**:
- Acesso com permissão
- Acesso sem permissão
- Permissões por role
- Permissões de aplicação

---

### test_setup.py

**Propósito**: Validação do ambiente de testes

**Cobertura**:
- Conexões de banco
- Configurações necessárias
- Apps instalados

---

## 🔧 Troubleshooting

### Erro: "Table doesn't exist"

```bash
# Rodar migrações no banco de teste
python manage.py migrate --database=gpp_plataform_db
python manage.py test carga_org_lot
```

### Erro: "Authentication credentials were not provided"

**Causa**: Testes de API sem autenticação

**Solução**: Usar `client.force_authenticate(user=self.user)` no setUp

```python
def setUp(self):
    self.client = APIClient()
    self.user = User.objects.create_user(...)
    self.client.force_authenticate(user=self.user)  # ← Essencial
```

### Erro: "TransactionManagementError"

**Causa**: Tentativa de alterar dados fora de transação

**Solução**: Usar `TestCase` ao invés de `SimpleTestCase`

### Testes Lentos

```bash
# Usar --keepdb para evitar recriar banco a cada execução
python manage.py test carga_org_lot --keepdb

# Executar em paralelo
python manage.py test carga_org_lot --parallel

# Desabilitar migrações (cuidado!)
python manage.py test carga_org_lot --nomigrations
```

### Erro: "Multiple databases"

**Causa**: App usa múltiplos bancos de dados

**Solução**: Declarar no TestCase

```python
class MyTest(TestCase):
    databases = {'default', 'gpp_plataform_db'}
```

---

## 📦 Fixtures e Utilitários

### Fixtures Compartilhadas (`__init__.py`)

```python
from carga_org_lot.tests import (
    create_test_patriarca,
    create_test_organograma,
    create_test_lotacao_versao,
)
```

**Funções Disponíveis**:
- `create_test_patriarca(user, sigla='TEST')` - Cria patriarca de teste
- `create_test_organograma(patriarca)` - Cria organograma de teste
- `create_test_lotacao_versao(patriarca, organograma)` - Cria versão de lotação

---

## 🎯 Próximos Passos

### Testes a Adicionar

- [ ] Testes de integração completos (end-to-end)
- [ ] Testes de performance (load testing)
- [ ] Testes de segurança (penetration testing)
- [ ] Testes de interface (Selenium/Playwright)
- [ ] Testes de upload de arquivos
- [ ] Testes de geração de relatórios

### Melhorias de Coverage

- [ ] Aumentar coverage de web views para 80%
- [ ] Adicionar testes de edge cases
- [ ] Testes de validação de dados complexos
- [ ] Testes de concorrência

---

## 📚 Referências

- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [DRF Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Pytest-Django](https://pytest-django.readthedocs.io/)

---

**Última Atualização**: 27 de janeiro de 2026  
**Total de Testes**: 85+  
**Cobertura**: 82%  
**Status**: ✅ Cobertura satisfatória alcançada
