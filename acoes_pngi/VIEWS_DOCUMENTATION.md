# Documentação das Views - Ações PNGI

Esta documentação descreve todas as views criadas para o módulo **Ações PNGI**, incluindo views de API (REST) e views Web.

## 📦 Estrutura Criada

```
acoes_pngi/
├── serializers.py          # Serializers completos para todas as tabelas
├── views/
│   ├── __init__.py          # Exportação de todas as views
│   ├── api_views.py         # ViewSets da API REST
│   └── web_views.py         # Class-Based Views para interface web
└── urls/
    ├── api_urls.py          # Rotas da API
    └── web_urls.py          # Rotas da interface web
```

---

## 📡 API Views (REST)

Todas as API Views seguem o padrão **ViewSet** do Django REST Framework com:
- Operações CRUD completas
- Filtros, busca e ordenação
- Serializers otimizados para listagem e detalhamento
- Autenticação obrigatória

### Endpoints Disponíveis

#### 1. **Eixos** (`/api/v1/acoes_pngi/eixos/`)
- `GET` - Lista todos os eixos
- `POST` - Cria novo eixo
- `GET /{id}/` - Detalhe de um eixo
- `PUT/PATCH /{id}/` - Atualiza eixo
- `DELETE /{id}/` - Remove eixo
- `GET /list_light/` - Listagem otimizada

**Filtros**: `stralias`  
**Busca**: `strdescricaoeixo`, `stralias`  
**Ordenação**: `stralias`, `strdescricaoeixo`, `created_at`

#### 2. **Situações de Ação** (`/api/v1/acoes_pngi/situacoes/`)
- Operações CRUD completas

**Busca**: `strdescricaosituacao`  
**Ordenação**: `strdescricaosituacao`, `created_at`

#### 3. **Vigências PNGI** (`/api/v1/acoes_pngi/vigencias/`)
- Operações CRUD completas
- `GET /vigencia_ativa/` - Retorna vigência ativa
- `GET /vigente/` - Retorna vigências vigentes no momento
- `POST /{id}/ativar/` - Ativa uma vigência específica

**Filtros**: `isvigenciaativa`  
**Busca**: `strdescricaovigenciapngi`  
**Ordenação**: `datiniciovigencia`, `datfinalvigencia`, `created_at`

#### 4. **Tipos de Entrave/Alerta** (`/api/v1/acoes_pngi/tipos-entrave-alerta/`)
- Operações CRUD completas

**Busca**: `strdescricaotipoentravealerta`  
**Ordenação**: `strdescricaotipoentravealerta`, `created_at`

#### 5. **Ações** (`/api/v1/acoes_pngi/acoes/`)
- Operações CRUD completas
- `GET /{id}/prazos_ativos/` - Retorna prazos ativos da ação
- `GET /{id}/responsaveis_list/` - Retorna responsáveis da ação

**Inclui relacionamentos**: prazos, destaques, anotações de alinhamento, responsáveis

**Filtros**: `idvigenciapngi`, `idtipoentravealerta`  
**Busca**: `strapelido`, `strdescricaoacao`, `strdescricaoentrega`  
**Ordenação**: `strapelido`, `datdataentrega`, `created_at`

#### 6. **Prazos de Ação** (`/api/v1/acoes_pngi/acoes-prazo/`)
- Operações CRUD completas
- `GET /ativos/` - Retorna apenas prazos ativos

**Filtros**: `idacao`, `isacaoprazoativo`  
**Busca**: `strprazo`, `idacao__strapelido`  
**Ordenação**: `created_at`, `isacaoprazoativo`

#### 7. **Destaques de Ação** (`/api/v1/acoes_pngi/acoes-destaque/`)
- Operações CRUD completas

**Filtros**: `idacao`  
**Busca**: `idacao__strapelido`  
**Ordenação**: `datdatadestaque`, `created_at`

#### 8. **Tipos de Anotação de Alinhamento** (`/api/v1/acoes_pngi/tipos-anotacao-alinhamento/`)
- Operações CRUD completas

**Busca**: `strdescricaotipoanotacaoalinhamento`  
**Ordenação**: `strdescricaotipoanotacaoalinhamento`, `created_at`

#### 9. **Anotações de Alinhamento** (`/api/v1/acoes_pngi/acoes-anotacao-alinhamento/`)
- Operações CRUD completas

**Filtros**: `idacao`, `idtipoanotacaoalinhamento`  
**Busca**: `idacao__strapelido`, `strdescricaoanotacaoalinhamento`, `strnumeromonitoramento`  
**Ordenação**: `datdataanotacaoalinhamento`, `created_at`

#### 10. **Usuários Responsáveis** (`/api/v1/acoes_pngi/usuarios-responsaveis/`)
- Operações CRUD completas

**Filtros**: `strorgao`  
**Busca**: `idusuario__name`, `idusuario__email`, `strorgao`, `strtelefone`  
**Ordenação**: `created_at`

#### 11. **Relações Ação x Responsável** (`/api/v1/acoes_pngi/relacoes-acao-responsavel/`)
- Operações CRUD completas

**Filtros**: `idacao`, `idusuarioresponsavel`  
**Busca**: `idacao__strapelido`, `idusuarioresponsavel__idusuario__name`  
**Ordenação**: `created_at`

---

## 🌐 Web Views (Interface HTML)

Todas as Web Views seguem o padrão **Class-Based Views** do Django com:
- Herança de `LoginRequiredMixin` (autenticação obrigatória)
- Mensagens de feedback para o usuário
- Paginação (20 itens por página)
- Busca integrada (quando aplicável)
- Otimização de queries com `select_related` e `prefetch_related`

### Rotas Web Disponíveis

Cada entidade possui 5 rotas:

1. **Lista** - `/entidade/`
2. **Detalhe** - `/entidade/{id}/`
3. **Criar** - `/entidade/novo/`
4. **Editar** - `/entidade/{id}/editar/`
5. **Excluir** - `/entidade/{id}/excluir/`

### Entidades com Views Web

1. **Eixos** - `/eixos/`
2. **Situações de Ação** - `/situacoes-acao/`
3. **Vigências PNGI** - `/vigencias-pngi/`
4. **Tipos de Entrave/Alerta** - `/tipos-entrave-alerta/`
5. **Ações** - `/acoes/`
6. **Prazos de Ação** - `/acoes-prazo/`
7. **Destaques de Ação** - `/acoes-destaque/`
8. **Tipos de Anotação de Alinhamento** - `/tipos-anotacao-alinhamento/`
9. **Anotações de Alinhamento** - `/acoes-anotacao-alinhamento/`
10. **Usuários Responsáveis** - `/usuarios-responsaveis/`
11. **Relações Ação x Responsável** - `/relacoes-acao-responsavel/`

---

## 📝 Serializers

Todos os serializers incluem:
- **Validações customizadas**
- **Campos read-only** (IDs, timestamps)
- **Campos calculados** (quando aplicável)
- **Related fields** para exibição de relacionamentos
- **Serializers otimizados** para listagem

### Serializers Principais

1. `EixoSerializer` / `EixoListSerializer`
2. `SituacaoAcaoSerializer`
3. `VigenciaPNGISerializer` / `VigenciaPNGIListSerializer`
4. `TipoEntraveAlertaSerializer`
5. `AcoesSerializer` / `AcoesListSerializer`
6. `AcaoPrazoSerializer`
7. `AcaoDestaqueSerializer`
8. `TipoAnotacaoAlinhamentoSerializer`
9. `AcaoAnotacaoAlinhamentoSerializer`
10. `UsuarioResponsavelSerializer`
11. `RelacaoAcaoUsuarioResponsavelSerializer`

---

## ⚙️ Funcionalidades Especiais

### API

#### Vigências
- **Ativação automática**: Ao ativar uma vigência, as demais são desativadas automaticamente
- **Propriedades calculadas**: `esta_vigente`, `duracao_dias`
- **Endpoints customizados**: `/vigencia_ativa/`, `/vigente/`, `/{id}/ativar/`

#### Ações
- **Serializer completo**: Inclui todos os relacionamentos (prazos, destaques, anotações, responsáveis)
- **Serializer de listagem**: Otimizado sem relacionamentos
- **Endpoints customizados**: `/{id}/prazos_ativos/`, `/{id}/responsaveis_list/`

#### Prazos de Ação
- **Validação**: Apenas um prazo ativo por ação
- **Endpoint customizado**: `/ativos/`

### Web

#### Busca
- **Eixos**: Busca por descrição e alias
- **Ações**: Busca por apelido e descrição

#### Otimização de Queries
- Uso de `select_related` para FK
- Uso de `prefetch_related` para relações ManyToMany e reverse FK

#### Mensagens de Feedback
- Mensagens de sucesso em todas as operações
- Utiliza Django Messages Framework

---

## 📚 Templates Necessários

Para as views web funcionarem, é necessário criar os seguintes templates:

```
acoes_pngi/templates/acoes_pngi/
├── eixo/
│   ├── list.html
│   ├── detail.html
│   ├── form.html
│   └── confirm_delete.html
├── situacaoacao/
├── vigenciapngi/
├── tipoentravealerta/
├── acoes/
├── acaoprazo/
├── acaodestaque/
├── tipoanotacaoalinhamento/
├── acaoanotacaoalinhamento/
├── usuarioresponsavel/
└── relacaoacaousuarioresponsavel/
```

---

## ✅ Próximos Passos

1. **Criar templates HTML** para as views web
2. **Adicionar testes unitários** para views e serializers
3. **Configurar permissões** mais granulares (além de `IsAuthenticated`)
4. **Adicionar filtros avançados** nas views de listagem
5. **Implementar exportação** de dados (CSV, Excel, PDF)
6. **Criar dashboard** com estatísticas das ações

---

## 📌 Observações Importantes

- Todas as views de API requerem autenticação (`IsAuthenticated`)
- Todas as views web requerem login (`LoginRequiredMixin`)
- Serializers incluem validações de negócio dos models
- URLs seguem padrões RESTful e Django convencionais
- Código documentado com docstrings em português

---

**Data de criação**: 09/02/2026  
**Branch**: `feature/acoes-pngi-new-tables`
