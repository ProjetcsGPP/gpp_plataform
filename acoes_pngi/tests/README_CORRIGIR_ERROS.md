# 🛠️ Correção de Erros nos Testes

Script automatizado para corrigir os principais erros encontrados nos testes do `acoes_pngi`.

---

## 📋 Problemas Corrigidos

### 1. ❌ Filtro Booleano Inválido

**Erro Original:**
```python
django.core.exceptions.ValidationError: ['"true" value must be either True or False.']
```

**Localização:** `acoes_pngi/views/api_views.py` (linha ~496)

**Problema:**
O método `query_params.get()` retorna **string** (`"true"`), mas o campo `BooleanField` espera **booleano** (`True`).

**Código Original:**
```python
queryset = queryset.filter(isacaoprazoativo=self.request.query_params.get('isacaoprazoativo'))
```

**Correção Aplicada:**
```python
# Converte string para booleano
is_ativo = self.request.query_params.get('isacaoprazoativo')
if is_ativo is not None:
    is_ativo_bool = is_ativo.lower() in ('true', '1', 'yes')
    queryset = queryset.filter(isacaoprazoativo=is_ativo_bool)
```

---

### 2. ⏰ Datetimes Naive (sem timezone)

**Aviso Original:**
```python
RuntimeWarning: DateTimeField received a naive datetime while time zone support is active.
```

**Arquivos Afetados:**
- `test_api_views_alinhamento_responsaveis.py`
- `test_api_views_acoes.py`

**Problema:**
Os testes criam datetimes sem timezone (naive), mas o Django está configurado com `USE_TZ=True`.

**Código Original:**
```python
from datetime import datetime

datdataanotacaoalinhamento=datetime(2026, 2, 15, 10, 0, 0)
```

**Correção Aplicada:**
```python
from datetime import datetime
from django.utils import timezone

datdataanotacaoalinhamento=timezone.make_aware(datetime(2026, 2, 15, 10, 0, 0))
```

---

## 🚀 Como Usar o Script

### Passo 1: Executar o Script

```bash
python acoes_pngi/tests/corrigir_erros_testes.py
```

**Saída Esperada:**
```
============================================================
🔧 SCRIPT DE CORREÇÃO DE ERROS NOS TESTES
============================================================

1️⃣  Corrigindo filtro booleano em api_views.py...
✅ Corrigido filtro booleano em: acoes_pngi/views/api_views.py

2️⃣  Corrigindo datetimes naive em test_api_views_alinhamento_responsaveis.py...
✅ Corrigidos 20 datetimes naive em: acoes_pngi/tests/test_api_views_alinhamento_responsaveis.py

3️⃣  Corrigindo datetimes naive em test_api_views_acoes.py...
✅ Corrigidos 5 datetimes naive em: acoes_pngi/tests/test_api_views_acoes.py

4️⃣  Criando documentação...
✅ Documentação criada em: acoes_pngi/tests/CORRECOES_APLICADAS.md

============================================================
📊 RESUMO DAS CORREÇÕES
============================================================
✅ Filtro booleano
✅ Datetimes alinhamento
✅ Datetimes acoes

Total: 3/3 correções aplicadas com sucesso

🎉 Todas as correções foram aplicadas!
```

---

### Passo 2: Revisar as Mudanças

```bash
git diff acoes_pngi/
```

Verifique se as correções foram aplicadas corretamente.

---

### Passo 3: Executar os Testes

```bash
python manage.py test acoes_pngi.tests
```

**Resultado Esperado:**
- ✅ Redução significativa de erros
- ✅ Sem erros de `ValidationError` para booleanos
- ✅ Sem warnings de `naive datetime`

---

### Passo 4: Commit das Correções

```bash
git add acoes_pngi/
git commit -m "fix: Corrige filtro booleano e datetimes naive nos testes"
```

---

## 📊 Estatísticas

| Tipo de Correção | Quantidade | Impacto |
|------------------|------------|----------|
| Filtro booleano | 1 | 🔴 Crítico |
| Datetimes naive | ~25+ | 🟡 Moderado |
| Arquivos modificados | 3 | - |

---

## 🔍 Detalhes Técnicos

### Script: `corrigir_erros_testes.py`

O script executa 4 operações:

1. **`corrigir_filtro_booleano()`**
   - Localiza e corrige o filtro em `api_views.py`
   - Usa regex para encontrar o padrão exato
   - Adiciona conversão string → booleano

2. **`corrigir_datetimes_naive()`**
   - Adiciona `from django.utils import timezone`
   - Envolve todos os `datetime(...)` com `timezone.make_aware(...)`
   - Evita duplicações de `make_aware`

3. **`corrigir_datetimes_em_test_acoes()`**
   - Similar ao anterior, mas para `test_api_views_acoes.py`
   - Foca em `datdataentrega` e campos similares

4. **`criar_documentacao()`**
   - Gera `CORRECOES_APLICADAS.md` com detalhes

---

## ⚠️ Problemas Conhecidos (Não Corrigidos por Este Script)

### Endpoints 404

Vários endpoints retornam **404 Not Found** em vez de **200 OK**:
- `/api/v1/acoes_pngi/anotacoes-alinhamento/`
- `/api/v1/acoes_pngi/destaques/`
- `/api/v1/acoes_pngi/prazos/`

**Causa Provável:** ViewSets não registrados no router ou URLs incorretas.

**Solução:** Verificar `urls.py` e `router.register()` em `acoes_pngi/urls.py`.

---

### Permissões Incorretas

Alguns testes esperam **403 Forbidden** mas recebem **201 Created** ou **204 No Content**.

**Exemplo:**
```python
AssertionError: 201 != 403  # Esperava bloqueio, mas criou recurso
```

**Causa Provável:** Sistema de permissões RBAC/ABAC não está funcionando corretamente.

**Solução:** Revisar `permissions.py` e decorators de permissão.

---

## 📚 Documentação Adicional

- [CORRECOES_APLICADAS.md](./CORRECOES_APLICADAS.md) - Detalhes das correções
- [README_CORRECOES.md](./README_CORRECOES.md) - Primeira correção de nomes de campos
- [CORREÇÕES_CAMPOS.md](./CORREÇÕES_CAMPOS.md) - Mapeamento de campos corrigidos

---

## 🆘 Troubleshooting

### "Padrão não encontrado em api_views.py"

**Causa:** O código já foi modificado manualmente ou o padrão mudou.

**Solução:** Edite `api_views.py` manualmente:
```python
# Procure por:
queryset.filter(isacaoprazoativo=self.request.query_params.get('isacaoprazoativo'))

# Substitua por:
is_ativo = self.request.query_params.get('isacaoprazoativo')
if is_ativo is not None:
    is_ativo_bool = is_ativo.lower() in ('true', '1', 'yes')
    queryset = queryset.filter(isacaoprazoativo=is_ativo_bool)
```

### "Nenhum datetime naive encontrado"

**Causa:** Os datetimes já foram corrigidos ou estão em formato diferente.

**Solução:** Verifique manualmente se há warnings de timezone ao rodar os testes.

---

## ✅ Checklist de Validação

Após executar o script, verifique:

- [ ] Script executou sem erros
- [ ] `git diff` mostra as correções esperadas
- [ ] `python manage.py test acoes_pngi.tests` executa sem erros críticos
- [ ] Sem `ValidationError` para filtros booleanos
- [ ] Sem `RuntimeWarning` sobre naive datetimes
- [ ] Testes passam ou mostram apenas erros de endpoints/permissões (não corrigidos por este script)

---

## 🎯 Próximos Passos

Se ainda houver falhas após executar este script:

1. **Investigar endpoints 404**
   ```bash
   # Verificar rotas registradas
   python manage.py show_urls | grep acoes_pngi
   ```

2. **Revisar permissões**
   - Verificar `acoes_pngi/permissions.py`
   - Conferir decorators em ViewSets

3. **Validar serializers**
   - Verificar campos obrigatórios
   - Conferir validações customizadas

---

**Criado em:** 12/02/2026  
**Última atualização:** 12/02/2026  
**Versão:** 1.0
