# Views - Ações PNGI

## Estrutura Modular

A estrutura de views foi padronizada seguindo o modelo de `carga_org_lot`, dividindo as views em módulos especializados para melhor organização e manutenção.

### Organização

```
views/
├── __init__.py                  # Exports de todas as views (API e Web)
├── api_views.py                # Arquivo de compatibilidade (importa de api_views/)
├── web_views.py                # Arquivo de compatibilidade (importa de web_views/)
├── README.md                   # Esta documentação
├── api_views/
│   ├── __init__.py             # Exports de API ViewSets
│   ├── auth_views.py          # Autenticação e gerenciamento de usuários
│   ├── core_views.py          # Eixo, Situação, Vigência, Tipo Entrave/Alerta
│   ├── acoes_views.py         # Ações, Prazos, Destaques
│   ├── alinhamento_views.py   # Tipo Anotação e Anotações de Alinhamento
│   └── responsavel_views.py   # Usuários Responsáveis e Relações
└── web_views/
    ├── __init__.py             # Exports de Web CBVs
    ├── core_web_views.py      # Eixo, Situação, Vigência, Tipo Entrave/Alerta
    ├── acoes_web_views.py     # Ações, Prazos, Destaques
    ├── alinhamento_web_views.py  # Tipo Anotação e Anotações de Alinhamento
    └── responsavel_web_views.py  # Usuários Responsáveis e Relações
```

## API Views (DRF ViewSets)

### auth_views.py
**Responsável por:** Autenticação e gerenciamento de usuários

- `portal_auth` - Endpoint de autenticação via token do portal
- `UserManagementViewSet` - CRUD e operações de usuários
  - `sync_user` - Sincroniza usuário com roles
  - `list_users` - Lista usuários da aplicação
  - `get_user_by_email` - Busca por email
  - `update_user_status` - Atualiza status

### core_views.py
**Responsável por:** Entidades principais/auxiliares

- `EixoViewSet` - CRUD de Eixos do PNGI
  - `list_light` - Listagem otimizada
- `SituacaoAcaoViewSet` - CRUD de Situações de Ações
- `VigenciaPNGIViewSet` - CRUD de Vigências
  - `vigencia_ativa` - Vigência atualmente ativa
  - `vigente` - Vigências vigentes no momento
  - `ativar` - Ativa uma vigência específica
- `TipoEntraveAlertaViewSet` - CRUD de Tipos de Entrave/Alerta

### acoes_views.py
**Responsável por:** Gerenciamento de ações

- `AcoesViewSet` - CRUD de Ações do PNGI
  - `prazos_ativos` - Lista prazos ativos da ação
  - `responsaveis_list` - Lista responsáveis da ação
- `AcaoPrazoViewSet` - CRUD de Prazos de Ações
  - `ativos` - Lista apenas prazos ativos
- `AcaoDestaqueViewSet` - CRUD de Destaques de Ações

### alinhamento_views.py
**Responsável por:** Anotações de alinhamento

- `TipoAnotacaoAlinhamentoViewSet` - CRUD de Tipos de Anotação
- `AcaoAnotacaoAlinhamentoViewSet` - CRUD de Anotações de Alinhamento

### responsavel_views.py
**Responsável por:** Usuários responsáveis

- `UsuarioResponsavelViewSet` - CRUD de Usuários Responsáveis
- `RelacaoAcaoUsuarioResponsavelViewSet` - CRUD de Relações Ação-Responsável

## Web Views (Django CBVs)

Cada módulo em `web_views/` contém Class-Based Views para interface web:
- ListView
- DetailView
- CreateView
- UpdateView
- DeleteView

### core_web_views.py
CBVs para: Eixo, SituacaoAcao, VigenciaPNGI, TipoEntraveAlerta

### acoes_web_views.py
CBVs para: Acoes, AcaoPrazo, AcaoDestaque

### alinhamento_web_views.py
CBVs para: TipoAnotacaoAlinhamento, AcaoAnotacaoAlinhamento

### responsavel_web_views.py
CBVs para: UsuarioResponsavel, RelacaoAcaoUsuarioResponsavel

## Como Usar

### Import Direto (Recomendado)

```python
# API Views
from acoes_pngi.views import AcoesViewSet, portal_auth

# Web Views
from acoes_pngi.views import AcoesListView, AcoesDetailView
```

### Import de Módulos Específicos

```python
# API
from acoes_pngi.views.api_views import AcoesViewSet
from acoes_pngi.views.api_views.acoes_views import AcoesViewSet

# Web
from acoes_pngi.views.web_views import AcoesListView
from acoes_pngi.views.web_views.acoes_web_views import AcoesListView
```

## Compatibilidade

Os arquivos `api_views.py` e `web_views.py` na raiz de `views/` são mantidos para compatibilidade com código antigo. Eles importam e re-exportam tudo dos módulos especializados.

## Permissões

Todas as views API utilizam `IsAuthenticated` como permissão base. Para permissões específicas por role, utilize:

```python
from acoes_pngi.permissions import (
    CanViewAcoesPngi,      # Leitura (todos os perfis)
    CanEditAcoesPngi,      # Edição (Coordenador, Gestor, Operador)
    CanManageAcoesPngi,    # Gerenciamento completo (Coordenador, Gestor)
)
```

Veja `acoes_pngi/permissions.py` para detalhes.

## Padrões

### API ViewSets
- Sempre usar `select_related` e `prefetch_related` para otimização
- Implementar filtros, busca e ordenação com `DjangoFilterBackend`
- Usar serializers diferentes para `list` e `detail` quando necessário
- Adicionar actions customizadas com `@action` decorator

### Web Views
- Todas herdam de `LoginRequiredMixin`
- Usar `messages` para feedback ao usuário
- Definir `success_url` com `reverse_lazy`
- Implementar busca no `get_queryset` quando aplicável

## Manutenção

Ao adicionar novas entidades:

1. Crie o ViewSet em `api_views/[categoria]_views.py`
2. Crie as CBVs em `web_views/[categoria]_web_views.py`
3. Adicione exports nos respectivos `__init__.py`
4. Atualize esta documentação

## Referências

- Estrutura baseada em: `carga_org_lot/views/`
- Documentação DRF: https://www.django-rest-framework.org/
- Django CBV: https://docs.djangoproject.com/en/stable/topics/class-based-views/
