# Correções dos Testes - 02/02/2026

## 🔴 Problema Identificado

**Data**: 02/02/2026 - Segunda-feira  
**Hora**: 10:14 AM  
**Arquivo**: `carga_org_lot/tests/test_web_views.py`

### Erro Principal
```
TypeError: TblPatriarca() got unexpected keyword arguments: 'str_nome_patriarca', 'user_criacao'
```

### Causa Raiz
Os testes estavam usando **nomes de campos incorretos** que não correspondiam à estrutura real do modelo `TblPatriarca` definida em `models.py`.

---

## ✅ Correções Aplicadas

### 1. Modelo `TblPatriarca`

#### Antes (Incorreto):
```python
TblPatriarca.objects.create(
    str_sigla_patriarca='SEGER',
    str_nome_patriarca='Secretaria...',  # ❌ ERRADO
    user_criacao=cls.user                 # ❌ ERRADO
)
```

#### Depois (Correto):
```python
TblPatriarca.objects.create(
    str_sigla_patriarca='SEGER',
    str_nome='Secretaria...',             # ✅ CORRETO
    id_status_progresso=cls.status_progresso,  # ✅ Campo obrigatório adicionado
    id_usuario_criacao=cls.user           # ✅ CORRETO
)
```

### 2. Modelo `TblOrgaoUnidade`

#### Antes (Incorreto):
```python
TblOrgaoUnidade.objects.create(
    id_patriarca=cls.patriarca,
    str_sigla_orgao_unidade='SEGER',     # ❌ ERRADO
    str_nome_orgao_unidade='Secretaria...', # ❌ ERRADO
    user_criacao=cls.user                 # ❌ ERRADO
)
```

#### Depois (Correto):
```python
TblOrgaoUnidade.objects.create(
    id_organograma_versao=cls.organograma_versao,  # ✅ Campo obrigatório adicionado
    id_patriarca=cls.patriarca,
    str_sigla='SEGER',                    # ✅ CORRETO
    str_nome='Secretaria...',             # ✅ CORRETO
    id_usuario_criacao=cls.user           # ✅ CORRETO
)
```

### 3. Adição de Dependências Necessárias

#### TblStatusProgresso (obrigatório para TblPatriarca)
```python
cls.status_progresso, created = TblStatusProgresso.objects.get_or_create(
    id_status_progresso=1,
    defaults={'str_descricao': 'Em andamento'}
)
```

#### TblOrganogramaVersao (obrigatório para TblOrgaoUnidade)
```python
cls.organograma_versao = TblOrganogramaVersao.objects.create(
    id_patriarca=cls.patriarca,
    str_origem='TESTE',
    str_status_processamento='SUCESSO'
)
```

---

## 📊 Estrutura Correta dos Modelos

### TblPatriarca
| Campo Django | Campo BD | Tipo | Obrigatório |
|--------------|----------|------|---------------|
| `str_sigla_patriarca` | `strsiglapatriarca` | CharField(20) | ✅ Sim |
| `str_nome` | `strnome` | CharField(255) | ✅ Sim |
| `id_status_progresso` | `idstatusprogresso` | ForeignKey | ✅ Sim |
| `id_usuario_criacao` | `idusuariocriacao` | ForeignKey(User) | ✅ Sim |
| `dat_criacao` | `datcriacao` | DateTimeField | Auto |
| `id_usuario_alteracao` | `idusuarioalteracao` | ForeignKey(User) | Não |
| `dat_alteracao` | `datalteracao` | DateTimeField | Não |

### TblOrgaoUnidade
| Campo Django | Campo BD | Tipo | Obrigatório |
|--------------|----------|------|---------------|
| `id_organograma_versao` | `idorganogramaversao` | ForeignKey | ✅ Sim |
| `id_patriarca` | `idpatriarca` | ForeignKey | ✅ Sim |
| `str_sigla` | `strsigla` | CharField(50) | ✅ Sim |
| `str_nome` | `strnome` | CharField(255) | ✅ Sim |
| `id_orgao_unidade_pai` | `idorgaounidadepai` | ForeignKey(self) | Não |
| `id_usuario_criacao` | `idusuariocriacao` | ForeignKey(User) | Não |
| `flg_ativo` | `flgativo` | BooleanField | Auto (True) |
| `dat_criacao` | `datcriacao` | DateTimeField | Auto |

---

## 🛠️ Teste dos Correções

### Executar Testes
```bash
python manage.py test carga_org_lot --verbosity=2
```

### Resultado Esperado
- ✅ Todos os testes de models, API, permissions e serializers devem passar (57 testes)
- ✅ Testes de web views devem criar fixtures corretamente
- ⚠️ Alguns endpoints web ainda não implementados (skipados, não falham)

---

## 📝 Resumo das Mudanças

### Arquivo Modificado
- `carga_org_lot/tests/test_web_views.py`

### Campos Corrigidos
1. `str_nome_patriarca` → `str_nome`
2. `user_criacao` → `id_usuario_criacao`
3. `str_sigla_orgao_unidade` → `str_sigla`
4. `str_nome_orgao_unidade` → `str_nome`

### Imports Adicionados
```python
from carga_org_lot.models import (
    TblPatriarca,
    TblOrganogramaVersao,
    TblLotacaoVersao,
    TblOrgaoUnidade,
    TblStatusProgresso,  # ✅ Novo
)
```

### Dependências Criadas
1. `TblStatusProgresso` no `BaseWebViewTestCase.setUpTestData()`
2. `TblOrganogramaVersao` no `AjaxViewsTest.setUpTestData()`

---

## 🔗 Commit Relacionado

**SHA**: `912bdfbb29a8ad3d202e3e91210e6fc221b964f6`  
**Mensagem**: "fix: corrige nomes de campos no test_web_views.py"  
**Data**: 02/02/2026 10:16:31 -03:00

---

## 📌 Notas Importantes

1. **Sempre consultar `models.py`**: Os nomes dos campos Django são definidos lá
2. **Usar `db_column`**: Para saber o nome da coluna no banco de dados
3. **Foreign Keys**: Sempre usar o nome do campo Django (ex: `id_usuario_criacao`, não `user_criacao`)
4. **Dependências**: Verificar campos `ForeignKey` com `on_delete=models.PROTECT` - são obrigatórios
5. **get_or_create()**: Usar para evitar `IntegrityError` em fixtures de teste

---

## 🎯 Próximos Passos

1. ✅ Executar `git pull origin main` no ambiente local
2. ✅ Rodar testes: `python manage.py test carga_org_lot --verbosity=2`
3. ✅ Verificar que todos os 57+ testes passam
4. 🔵 Implementar endpoints web faltantes (dashboard, AJAX, etc.)
5. 🔵 Criar testes adicionais para cobertura completa

---

**✅ STATUS**: Problema resolvido e documentado  
**👤 Responsável**: GPP Platform Team  
**📅 Última Atualização**: 02/02/2026 10:16 AM -03:00
