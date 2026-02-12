# Correções Aplicadas nos Testes

## 1. Filtro Booleano em `api_views.py`

### Problema
O filtro `isacaoprazoativo` recebia string `"true"` do query parameter, mas o campo
`BooleanField` esperava valor booleano.

### Correção
```python
# ANTES:
queryset = queryset.filter(isacaoprazoativo=self.request.query_params.get('isacaoprazoativo'))

# DEPOIS:
is_ativo = self.request.query_params.get('isacaoprazoativo')
if is_ativo is not None:
    is_ativo_bool = is_ativo.lower() in ('true', '1', 'yes')
    queryset = queryset.filter(isacaoprazoativo=is_ativo_bool)
```

### Localização
- Arquivo: `acoes_pngi/views/api_views.py`
- Linha: ~496 (classe `AcaoPrazoViewSet`)

---

## 2. Datetimes Naive nos Testes

### Problema
Os testes usavam `datetime.now()` e `datetime(...)` sem timezone, mas Django está com `USE_TZ=True`.

### Correções Aplicadas

#### A. datetime.now()
```python
# ANTES:
from datetime import datetime
datdataanotacaoalinhamento=datetime.now()

# DEPOIS:
from django.utils import timezone
datdataanotacaoalinhamento=timezone.now()
```

#### B. Datetimes estáticos
```python
# ANTES:
datetime(2026, 2, 15, 10, 0, 0)

# DEPOIS:
from django.utils import timezone
timezone.make_aware(datetime(2026, 2, 15, 10, 0, 0))
```

### Arquivos Corrigidos
- Todos os arquivos `test_*.py` em `acoes_pngi/tests/`

---

## Como Executar

```bash
# 1. Executar o script de correções
python acoes_pngi/tests/corrigir_erros_testes.py

# 2. Verificar as mudanças
git diff acoes_pngi/

# 3. Rodar os testes
python manage.py test acoes_pngi.tests

# 4. Commit
git add acoes_pngi/
git commit -m "fix: Corrige filtro booleano e datetimes naive nos testes"
```

---

## Estatísticas

- **Filtros booleanos corrigidos**: 1
- **datetime.now() corrigidos**: Varia por arquivo
- **Datetimes estáticos corrigidos**: Varia por arquivo
- **Imports timezone adicionados**: Automático

---

## Próximos Passos (se ainda houver erros)

1. **Endpoints 404**: Verificar roteamento das URLs
2. **Permissões**: Revisar sistema RBAC/ABAC
3. **Bad Request 400**: Validar serializers
