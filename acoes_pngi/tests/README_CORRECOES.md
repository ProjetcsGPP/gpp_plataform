# Correções de Nomes de Campos nos Testes - Ações PNGI

## 📊 Resumo

**Total de erros encontrados**: 29 (todos relacionados a nomes de campos incorretos)

### Arquivos afetados:

1. **test_api_views_acoes.py**: 8 correções
   - Model: `AcaoDestaque`
   - Problema: Campos `strdescricaodestaque` e `ordenacao` não existem
   - Solução: Usar apenas `datdatadestaque`

2. **test_api_views_alinhamento_responsaveis.py**: 21 correções
   - **TipoAnotacaoAlinhamento** (9 erros): nome do campo incompleto
   - **AcaoAnotacaoAlinhamento** (6 erros): campo data com nome incompleto
   - **UsuarioResponsavel** (3 erros): PK incorreta
   - **RelacaoAcaoUsuarioResponsavel** (3 erros): PK incorreta

---

## 🚀 Opção 1: Aplicar Correções Automaticamente (RECOMENDADO)

### Passo 1: Executar o script

```bash
# Da raiz do projeto
python acoes_pngi/tests/aplicar_correcoes.py

# Ou do diretório tests
cd acoes_pngi/tests
python aplicar_correcoes.py
```

### Passo 2: Revisar as mudanças

```bash
git diff acoes_pngi/tests/test_api_views_acoes.py
git diff acoes_pngi/tests/test_api_views_alinhamento_responsaveis.py
```

### Passo 3: Testar

```bash
python manage.py test acoes_pngi.tests.test_api_views_acoes
python manage.py test acoes_pngi.tests.test_api_views_alinhamento_responsaveis
```

### Passo 4: Commit

```bash
git add acoes_pngi/tests/test_api_views_acoes.py
git add acoes_pngi/tests/test_api_views_alinhamento_responsaveis.py
git commit -m "fix: Corrige nomes de campos nos testes de API (29 erros)

Correções:
- AcaoDestaque: remove campos inexistentes, usa datdatadestaque
- TipoAnotacaoAlinhamento: usa nome completo do campo
- AcaoAnotacaoAlinhamento: usa datdataanotacaoalinhamento
- UsuarioResponsavel e RelacaoAcaoUsuarioResponsavel: corrige PKs

Total: 29 correções aplicadas"
```

---

## 🔧 Opção 2: Aplicar Correções Manualmente

### Arquivos de referência:

1. **CORREÇÕES_CAMPOS.md** - Documentação completa dos problemas
2. **PATCH_ACAODESTAQUE.txt** - 8 correções para test_api_views_acoes.py
3. **PATCH_ALINHAMENTO_RESPONSAVEIS.txt** - 21 correções para test_api_views_alinhamento_responsaveis.py

### Como usar os patches:

Abra os arquivos de patch e aplique cada correção manualmente, substituindo "ANTES" por "DEPOIS".

---

## 📝 Detalhes das Correções

### 1. AcaoDestaque (test_api_views_acoes.py)

**Model real**:
```python
class AcaoDestaque(models.Model):
    idacaodestaque = models.AutoField(primary_key=True)
    idacao = models.ForeignKey(Acoes, ...)
    datdatadestaque = models.DateTimeField(...)  # ✅ EXISTE
    # strdescricaodestaque - ❌ NÃO EXISTE
    # ordenacao - ❌ NÃO EXISTE
```

**Exemplo de correção**:
```python
# ANTES (❌ ERRADO)
AcaoDestaque.objects.create(
    idacao=self.acao,
    strdescricaodestaque='Destaque',
    ordenacao=1
)

# DEPOIS (✅ CORRETO)
from django.utils import timezone

AcaoDestaque.objects.create(
    idacao=self.acao,
    datdatadestaque=timezone.now()
)
```

### 2. TipoAnotacaoAlinhamento (test_api_views_alinhamento_responsaveis.py)

**Model real**:
```python
class TipoAnotacaoAlinhamento(models.Model):
    idtipoanotacaoalinhamento = models.AutoField(primary_key=True)
    strdescricaotipoanotacaoalinhamento = models.CharField(...)  # ✅ NOME COMPLETO
    # strdescricaotipoanotacao - ❌ INCOMPLETO
    # stralias - ❌ NÃO EXISTE
```

**Exemplo de correção**:
```python
# ANTES (❌ ERRADO)
TipoAnotacaoAlinhamento.objects.create(
    strdescricaotipoanotacao='Reunião',
    stralias='REUN'
)

# DEPOIS (✅ CORRETO)
TipoAnotacaoAlinhamento.objects.create(
    strdescricaotipoanotacaoalinhamento='Reunião de Alinhamento'
)
```

### 3. AcaoAnotacaoAlinhamento (test_api_views_alinhamento_responsaveis.py)

**Model real**:
```python
class AcaoAnotacaoAlinhamento(models.Model):
    ...
    datdataanotacaoalinhamento = models.DateTimeField(...)  # ✅ NOME COMPLETO
    # dtanotacaoalinhamento - ❌ INCOMPLETO
```

**Exemplo de correção**:
```python
# ANTES (❌ ERRADO)
data = {
    'dtanotacaoalinhamento': datetime.now().isoformat()
}

# DEPOIS (✅ CORRETO)
data = {
    'datdataanotacaoalinhamento': datetime.now().isoformat()
}
```

### 4. UsuarioResponsavel (test_api_views_alinhamento_responsaveis.py)

**Model real**:
```python
class UsuarioResponsavel(models.Model):
    idusuario = models.OneToOneField(  # ✅ Esta É a PK
        settings.AUTH_USER_MODEL,
        primary_key=True,
        ...
    )
    # idusuarioresponsavel - ❌ NÃO EXISTE
```

**Exemplo de correção**:
```python
# ANTES (❌ ERRADO)
f'/api/.../usuarios-responsaveis/{self.responsavel.idusuarioresponsavel}/'

# DEPOIS (✅ CORRETO)
f'/api/.../usuarios-responsaveis/{self.responsavel.pk}/'
```

### 5. RelacaoAcaoUsuarioResponsavel (test_api_views_alinhamento_responsaveis.py)

**Model real**:
```python
class RelacaoAcaoUsuarioResponsavel(models.Model):
    idacaousuarioresponsavel = models.BigAutoField(primary_key=True)  # ✅
    # idrelacaoacaousuarioresponsavel - ❌ NOME ERRADO
```

**Exemplo de correção**:
```python
# ANTES (❌ ERRADO)
self.relacao.idrelacaoacaousuarioresponsavel

# DEPOIS (✅ CORRETO)
self.relacao.idacaousuarioresponsavel
```

---

## ✅ Checklist de Validação

Após aplicar as correções:

- [ ] Script executado sem erros
- [ ] `git diff` revisado
- [ ] Testes de `AcaoDestaque` passando
- [ ] Testes de `TipoAnotacaoAlinhamento` passando
- [ ] Testes de `AcaoAnotacaoAlinhamento` passando
- [ ] Testes de `UsuarioResponsavel` passando
- [ ] Testes de `RelacaoAcaoUsuarioResponsavel` passando
- [ ] Todos os 29 erros corrigidos
- [ ] Commit realizado

---

## 📄 Arquivos de Suporte

| Arquivo | Descrição |
|---------|-------------|
| `aplicar_correcoes.py` | Script automatizado para aplicar todas as correções |
| `CORREÇÕES_CAMPOS.md` | Documentação detalhada de todos os problemas encontrados |
| `PATCH_ACAODESTAQUE.txt` | Patch manual para test_api_views_acoes.py (8 correções) |
| `PATCH_ALINHAMENTO_RESPONSAVEIS.txt` | Patch manual para test_api_views_alinhamento_responsaveis.py (21 correções) |
| `README_CORRECOES.md` | Este arquivo - guia completo |

---

## 💡 Dicas

1. **Use o script automatizado**: É a forma mais rápida e segura
2. **Sempre revise com git diff**: Garante que as mudanças estão corretas
3. **Execute os testes após cada correção**: Identifica problemas rapidamente
4. **Consulte os models reais**: Em caso de dúvida, verifique `acoes_pngi/models.py`

---

## ❓ Problemas?

Se encontrar erros após aplicar as correções:

1. Verifique se todos os imports estão corretos (`from django.utils import timezone`)
2. Confirme que os nomes dos campos nos models estão corretos
3. Execute `python manage.py makemigrations --check` para verificar consistência
4. Consulte os arquivos de patch para referência

---

**Última atualização**: 12/02/2026
**Versão**: 1.0
**Status**: Pronto para uso
