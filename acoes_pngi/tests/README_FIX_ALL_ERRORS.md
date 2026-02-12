# 🔧 Fix All Test Errors - Documentação

## 👁️ Visão Geral

Script automatizado para corrigir **todos os 76 erros restantes** nos testes do módulo `acoes_pngi`.

**Status Atual dos Testes:**
```
Ran 368 tests in 13.818s
FAILED (failures=25, errors=51)
```

**Branch:** `fix/correcao-massiva-testes-pngi`

**Arquivos principais 100% OK:**
- ✅ `test_api_views_acoes.py`
- ✅ `test_api_alinhamento_views.py`
- ✅ `test_api_responsavel_views.py`

---

## 🐞 Problemas Identificados

### 1️⃣ ValidationError - datfinalvigencia (múltiplos arquivos)

**Erro:**
```python
django.core.exceptions.ValidationError: 
{'datfinalvigencia': ['This field cannot be null.']}
```

**Problema:**
Criação de `VigenciaPNGI` **sem** o campo obrigatório `datfinalvigencia`:
```python
VigenciaPNGI.objects.create(
    strdescricaovigenciapngi='PNGI 2026',
    datiniciovigencia=date(2026, 1, 1)
    # ❌ FALTA: datfinalvigencia
)
```

**Correção:**
```python
VigenciaPNGI.objects.create(
    strdescricaovigenciapngi='PNGI 2026',
    datiniciovigencia=date(2026, 1, 1),
    datfinalvigencia=date(2026, 12, 31)  # ✅ ADICIONADO
)
```

**Arquivos afetados:** TODOS os `test_*.py` que criam `VigenciaPNGI`

---

### 2️⃣ IndexError - list index out of range

**Erro:**
```python
IndexError: list index out of range
# Em testes: testorderinganotacoes, testorderingtipos, testfilterdestaquesbyacao
```

**Problema:**
Testes tentam acessar elementos de listas vazias porque **fixtures estão incompletas**:
```python
def test_ordering_anotacoes(self):
    response = self.client.get('/api/v1/anotacoes/?ordering=datcriacao')
    self.assertEqual(response.data['results'][0]['id'], 1)  # ❌ Lista vazia!
```

**Causa Raiz:**
`Acoes.objects.create()` sem relacionamentos obrigatórios `ideixo` e `idsituacaoacao`, fazendo com que queries retornem vazias.

**Correção:**
```python
def setup_test_data(self):
    # ✅ Criar Eixo e SituacaoAcao ANTES de Acoes
    self.eixo = Eixo.objects.create(
        stralias='E1',
        strdescricaoeixo='Eixo 1 - Gestão'
    )
    
    self.situacao = SituacaoAcao.objects.create(
        strdescricaosituacao='Em Andamento'
    )
    
    # ✅ Criar Acoes COM todos relacionamentos
    self.acao = Acoes.objects.create(
        strapelido='ACAO-001',
        strdescricaoacao='Teste',
        idvigenciapngi=self.vigencia,
        ideixo=self.eixo,              # ✅ ADICIONADO
        idsituacaoacao=self.situacao   # ✅ ADICIONADO
    )
```

---

### 3️⃣ AssertionError - 0 != 1 ou 0 != 2

**Erro:**
```python
AssertionError: 0 != 2
# Em testes: testfilteranotacoesbyacao, testsearchanotacoesbydescricao
```

**Problema:**
Queries retornam **0 resultados** quando deveriam retornar 1 ou 2.

**Causa:**
Mesma do IndexError - fixtures incompletas. `Acoes` criadas sem `ideixo` ou `idsituacaoacao` não aparecem em queries com filtros/joins.

**Exemplo:**
```python
def test_filter_anotacoes_by_acao(self):
    # Esperado: 2 anotações da self.acao
    response = self.client.get(f'/api/v1/anotacoes/?idacao={self.acao.idacao}')
    self.assertEqual(len(response.data['results']), 2)  # ❌ Retorna 0
```

**Correção:**
Garantir que `setup_test_data()` cria **TODAS** as dependências antes dos objetos principais.

---

### 4️⃣ AttributeError - self.eixo, self.vigencia

**Erro:**
```python
AttributeError: 'EixoAPITests' object has no attribute 'eixo'
# Em: test_api_views.py (EixoAPITests, VigenciaAPITests)
```

**Problema:**
`setup_test_data()` cria objetos mas **não os atribui a `self`**:
```python
def setup_test_data(self):
    eixo = Eixo.objects.create(...)  # ❌ Variável local
    
    # Depois, outros métodos tentam acessar:
    self.acao.ideixo = self.eixo  # ❌ AttributeError!
```

**Correção:**
```python
def setup_test_data(self):
    self.eixo = Eixo.objects.create(...)  # ✅ Atribuir a self
    self.situacao = SituacaoAcao.objects.create(...)
    self.vigencia = VigenciaPNGI.objects.create(...)
```

---

## 🚀 Como Usar o Script

### Opção 1: Executar diretamente (recomendado)

```bash
# No diretório raiz do projeto
cd /caminho/para/gpp_plataform

# IMPORTANTE: Checkout da branch correta
git checkout fix/correcao-massiva-testes-pngi

# Executar script
python acoes_pngi/tests/fix_all_test_errors.py
```

### Opção 2: Executar via Django manage.py

```bash
python manage.py shell
```

```python
>>> from acoes_pngi.tests.fix_all_test_errors import main
>>> main()
```

---

## 📊 O Que o Script Faz

### Etapa 1: Adicionar datfinalvigencia
✅ Procura todos `VigenciaPNGI.objects.create(...)`  
✅ Adiciona `datfinalvigencia=date(YYYY, 12, 31)` automaticamente  
✅ Usa ano de `datiniciovigencia` como referência  
✅ Arquivos: TODOS os `test_*.py`

### Etapa 2: Corrigir AttributeErrors
✅ Encontra classes com `setup_test_data()`  
✅ Transforma `eixo = Eixo.objects.create()` em `self.eixo = ...`  
✅ Transforma `vigencia = VigenciaPNGI.objects.create()` em `self.vigencia = ...`  
✅ Transforma `situacao = SituacaoAcao.objects.create()` em `self.situacao = ...`  
✅ Arquivo: `test_api_views.py`

### Etapa 3: Garantir Fixtures Completas
✅ Procura `Acoes.objects.create()` sem `ideixo` ou `idsituacaoacao`  
✅ Adiciona FKs faltando usando `self.eixo` e `self.situacao`  
✅ Garante que `setup_test_data()` cria `Eixo` e `SituacaoAcao` **antes** de usar  
✅ Arquivos: `test_api_views.py`, `test_api_acoes_views.py`, `test_api_alinhamento_views.py`, `test_api_responsavel_views.py`

---

## 📋 Resultado Esperado

### Antes
```
Ran 368 tests in 13.818s
FAILED (failures=25, errors=51)

Problemas:
❌ ValidationError datfinalvigencia (20+ arquivos)
❌ IndexError list index out of range (15+ testes)
❌ AssertionError 0 != 1/2 (20+ testes)
❌ AttributeError self.eixo, self.vigencia (5+ testes)
```

### Depois
```
Ran 368 tests in ~14s
OK ou FAILED com MUITO menos erros

✅ ValidationError datfinalvigencia: 0
✅ AttributeError: 0
🔄 IndexError e AssertionError: Reduzidos drasticamente
```

---

## 💡 Próximos Passos Após Executar o Script

1. **Rodar testes novamente:**
   ```bash
   python manage.py test acoes_pngi.tests
   ```

2. **Analisar resultado:**
   - Se **0 errors**: 🎉 Perfeito!
   - Se ainda houver erros: Verificar logs específicos

3. **Commit das mudanças:**
   ```bash
   git add acoes_pngi/tests/test_*.py
   git commit -m "fix(tests): Corrigir 76 erros nos testes via fix_all_test_errors.py"
   git push origin fix/correcao-massiva-testes-pngi
   ```

4. **Executar novamente para validar:**
   ```bash
   python manage.py test acoes_pngi.tests --verbosity=2
   ```

---

## ⚠️ Notas Importantes

### Backup Automático
⚠️ O script **NÃO** cria backups. Faça commit antes de executar:
```bash
git add .
git commit -m "backup antes de fix_all_test_errors"
```

### Idempotência
✅ O script é **idempotente** - pode ser executado múltiplas vezes sem problemas.  
✅ Não duplica correções já aplicadas.

### Expressões Regulares
⚠️ Usa regex avançadas - pode haver casos edge não cobertos.  
👁️ Sempre revisar diff antes de commitar.

---

## 👨‍💻 Contribuindo

Se encontrar bugs ou casos não cobertos:

1. Documentar exemplo em issue
2. Adicionar caso de teste ao script
3. Submeter PR com correção

---

## 📚 Referências

- Padrão de testes: `test_api_views_acoes.py` (✅ 100% funcionando)
- Commits recentes: Ver histórico de correções anteriores
- Django Testing: https://docs.djangoproject.com/en/stable/topics/testing/

---

**Branch:** `fix/correcao-massiva-testes-pngi`  
**Última atualização:** 12/02/2026  
**Status:** ✅ Pronto para uso
