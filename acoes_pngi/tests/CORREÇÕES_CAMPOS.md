# Correções de Nomes de Campos nos Testes

## Resumo

**Total de erros**: 26 (todos relacionados a nomes de campos incorretos)

## 1. AcaoDestaque (test_api_views_acoes.py)

**Problema**: Criando modelo com campos que não existem

**Model real**:
```python
class AcaoDestaque(models.Model):
    idacaodestaque = models.AutoField(primary_key=True)
    idacao = models.ForeignKey(Acoes, ...)
    datdatadestaque = models.DateTimeField(...)
```

**Campos que NÃO EXISTEM**:
- `strdescricaodestaque` ❌
- `ordenacao` ❌

**Linha 695 - ERRADO**:
```python
self.destaque = AcaoDestaque.objects.create(
    idacao=self.acao,
    strdescricaodestaque='Destaque Importante',  # ❌ NÃO EXISTE
    ordenacao=1  # ❌ NÃO EXISTE
)
```

**CORRETO**:
```python
from django.utils import timezone

self.destaque = AcaoDestaque.objects.create(
    idacao=self.acao,
    datdatadestaque=timezone.now()
)
```

**Impacto**: 9 testes falhando

---

## 2. TipoAnotacaoAlinhamento (test_api_views_alinhamento_responsaveis.py)

**Problema**: Nome do campo incompleto e campo alias inexistente

**Model real**:
```python
class TipoAnotacaoAlinhamento(models.Model):
    idtipoanotacaoalinhamento = models.AutoField(primary_key=True)
    strdescricaotipoanotacaoalinhamento = models.CharField(...)  # ← NOME COMPLETO
```

**Campos que NÃO EXISTEM**:
- `strdescricaotipoanotacao` ❌ (incompleto - falta "alinhamento" no final)
- `stralias` ❌

**Linhas 135 e 330 - ERRADO**:
```python
self.tipo_anotacao = TipoAnotacaoAlinhamento.objects.create(
    strdescricaotipoanotacao='Reunião',  # ❌ NOME ERRADO
    stralias='REUN'  # ❌ NÃO EXISTE
)
```

**CORRETO**:
```python
self.tipo_anotacao = TipoAnotacaoAlinhamento.objects.create(
    strdescricaotipoanotacaoalinhamento='Reunião de Alinhamento'
)
```

**Também corrigir**:
- Linha ~172: `'strdescricaotipoanotacao'` → `'strdescricaotipoanotacaoalinhamento'`
- Linha ~233: `ordering=strdescricaotipoanotacao` → `ordering=strdescricaotipoanotacaoalinhamento`
- Todos os `data = {}` que usam esses campos

**Impacto**: 14 testes falhando

---

## 3. UsuarioResponsavel - Primary Key (test_api_views_alinhamento_responsaveis.py)

**Problema**: PK incorreta sendo usada

**Model real**:
```python
class UsuarioResponsavel(models.Model):
    idusuario = models.OneToOneField(  # ← Esta É a PK
        settings.AUTH_USER_MODEL,
        primary_key=True,  # ← PK
        ...
    )
    strtelefone = models.CharField(...)
    strorgao = models.CharField(...)
```

**Campo que NÃO EXISTE**:
- `idusuarioresponsavel` ❌

**Linhas com erro**:
- Linha ~555: `self.responsavel.idusuarioresponsavel`
- Linha ~576: `resp_temp.idusuarioresponsavel`
- Linha ~595: `self.responsavel.idusuarioresponsavel`
- Linha ~731: `novo_resp.idusuarioresponsavel`
- Linha ~771: `self.responsavel.idusuarioresponsavel`

**CORRETO**:
```python
# Para acessar o ID (valor da PK):
self.responsavel.idusuario_id

# Ou para acessar o objeto User:
self.responsavel.idusuario
```

**Impacto**: 3 testes falhando

---

## 4. AcaoAnotacaoAlinhamento - Data (test_api_views_alinhamento_responsaveis.py)

**Problema**: Nome do campo data incompleto

**Model real**:
```python
class AcaoAnotacaoAlinhamento(models.Model):
    ...
    datdataanotacaoalinhamento = models.DateTimeField(...)  # ← NOME COMPLETO COM "DAT" NO INÍCIO
    ...
```

**Campo ERRADO**:
- `dtanotacaoalinhamento` ❌

**CORRETO**:
- `datdataanotacaoalinhamento` ✅

**Linhas a corrigir** (~350-400):
```python
# ERRADO:
data = {
    'dtanotacaoalinhamento': datetime.now().isoformat(),
}

# CORRETO:
data = {
    'datdataanotacaoalinhamento': datetime.now().isoformat(),
}
```

---

## 5. RelacaoAcaoUsuarioResponsavel - Primary Key

**Problema**: Nome da PK incorreto

**Model real**:
```python
class RelacaoAcaoUsuarioResponsavel(models.Model):
    idacaousuarioresponsavel = models.BigAutoField(  # ← PK CORRETA
        primary_key=True,
        ...
    )
```

**Campo ERRADO**:
- `idrelacaoacaousuarioresponsavel` ❌

**CORRETO**:
- `idacaousuarioresponsavel` ✅

**Linha 740 - ERRADO**:
```python
self.relacao.idrelacaoacaousuarioresponsavel
```

**CORRETO**:
```python
self.relacao.idacaousuarioresponsavel
```

---

## Resumo das Correções

| Arquivo | Model | Campo Errado | Campo Correto | Qtd Erros |
|---------|-------|--------------|---------------|----------|
| test_api_views_acoes.py | AcaoDestaque | `strdescricaodestaque` | - (remover) | 9 |
| test_api_views_acoes.py | AcaoDestaque | `ordenacao` | - (remover) | 9 |
| test_api_views_acoes.py | AcaoDestaque | - | `datdatadestaque` (adicionar) | 9 |
| test_api_views_alinhamento_responsaveis.py | TipoAnotacaoAlinhamento | `strdescricaotipoanotacao` | `strdescricaotipoanotacaoalinhamento` | 14 |
| test_api_views_alinhamento_responsaveis.py | TipoAnotacaoAlinhamento | `stralias` | - (remover) | 14 |
| test_api_views_alinhamento_responsaveis.py | UsuarioResponsavel | `idusuarioresponsavel` | `idusuario_id` | 3 |
| test_api_views_alinhamento_responsaveis.py | AcaoAnotacaoAlinhamento | `dtanotacaoalinhamento` | `datdataanotacaoalinhamento` | - |
| test_api_views_alinhamento_responsaveis.py | RelacaoAcaoUsuarioResponsavel | `idrelacaoacaousuarioresponsavel` | `idacaousuarioresponsavel` | 1 |

**Total**: 26 erros relacionados a nomes de campos

## Próximos Passos

1. ✅ Corrigir `test_api_views_acoes.py` - linha 695 e todas as referências
2. ✅ Corrigir `test_api_views_alinhamento_responsaveis.py` - todas as ocorrências
3. ✅ Executar testes novamente
4. ✅ Verificar se os 26 erros foram resolvidos
