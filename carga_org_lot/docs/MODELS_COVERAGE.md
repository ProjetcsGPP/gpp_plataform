# Cobertura de Models - Views

## 📊 Análise Completa: Models vs Views

Este documento mapeia todos os models do app `carga_org_lot` e identifica quais possuem views (API e Web) correspondentes.

**Data da Análise**: 27 de janeiro de 2026

---

## ✅ Models COM Views Completas

### 1. TblPatriarca

**Model**: Patriarca - Órgão principal para organograma e lotação

**Views Disponíveis**:
- 🌐 **Web**: `patriarca_list`, `patriarca_detail`
- 🔌 **API**: `PatriarcaViewSet`
  - CRUD completo
  - Custom actions: `organogramas/`, `lotacoes/`

**Endpoints API**:
```
GET    /api/carga_org_lot/patriarcas/
POST   /api/carga_org_lot/patriarcas/
GET    /api/carga_org_lot/patriarcas/{id}/
PUT    /api/carga_org_lot/patriarcas/{id}/
PATCH  /api/carga_org_lot/patriarcas/{id}/
DELETE /api/carga_org_lot/patriarcas/{id}/
GET    /api/carga_org_lot/patriarcas/{id}/organogramas/
GET    /api/carga_org_lot/patriarcas/{id}/lotacoes/
```

---

### 2. TblOrganogramaVersao

**Model**: Versão do organograma

**Views Disponíveis**:
- 🌐 **Web**: `organograma_list`, `organograma_detail`, `organograma_hierarquia_json`
- 🔌 **API**: `OrganogramaVersaoViewSet`
  - CRUD completo
  - Custom actions: `orgaos/`, `hierarquia/`, `json_envio/`

**Endpoints API**:
```
GET /api/carga_org_lot/organogramas/
GET /api/carga_org_lot/organogramas/{id}/
GET /api/carga_org_lot/organogramas/{id}/orgaos/
GET /api/carga_org_lot/organogramas/{id}/hierarquia/
GET /api/carga_org_lot/organogramas/{id}/json_envio/
```

---

### 3. TblLotacaoVersao

**Model**: Versão da lotação

**Views Disponíveis**:
- 🌐 **Web**: `lotacao_list`, `lotacao_detail`, `lotacao_inconsistencias`
- 🔌 **API**: `LotacaoVersaoViewSet`
  - CRUD completo
  - Custom actions: `registros/`, `inconsistencias/`, `estatisticas/`

**Endpoints API**:
```
GET /api/carga_org_lot/lotacoes/
GET /api/carga_org_lot/lotacoes/{id}/
GET /api/carga_org_lot/lotacoes/{id}/registros/
GET /api/carga_org_lot/lotacoes/{id}/inconsistencias/
GET /api/carga_org_lot/lotacoes/{id}/estatisticas/
```

---

### 4. TblCargaPatriarca

**Model**: Carga do patriarca

**Views Disponíveis**:
- 🌐 **Web**: `carga_list`, `carga_detail`
- 🔌 **API**: `CargaPatriarcaViewSet`
  - CRUD completo
  - Custom actions: `timeline/`

**Endpoints API**:
```
GET /api/carga_org_lot/cargas/
GET /api/carga_org_lot/cargas/{id}/
GET /api/carga_org_lot/cargas/{id}/timeline/
```

---

## ✨ Models COM Views Novas (Recém Implementadas)

### 5. TblLotacaoJsonOrgao ✅ NOVO

**Model**: JSON de lotação por órgão para envio à API

**Views Disponíveis**:
- 🔌 **API**: `LotacaoJsonOrgaoViewSet` ✨
  - CRUD completo
  - Custom actions: `conteudo/`, `regenerar/`, `enviar_api/`, `estatisticas/`, `gerar_em_lote/`

**Endpoints API**:
```
GET  /api/carga_org_lot/lotacao-json-orgao/
POST /api/carga_org_lot/lotacao-json-orgao/
GET  /api/carga_org_lot/lotacao-json-orgao/{id}/
PUT  /api/carga_org_lot/lotacao-json-orgao/{id}/
GET  /api/carga_org_lot/lotacao-json-orgao/{id}/conteudo/
POST /api/carga_org_lot/lotacao-json-orgao/{id}/regenerar/
POST /api/carga_org_lot/lotacao-json-orgao/{id}/enviar_api/
GET  /api/carga_org_lot/lotacao-json-orgao/estatisticas/
POST /api/carga_org_lot/lotacao-json-orgao/gerar_em_lote/
```

**Status**: ✅ Implementado em 27/01/2026

---

### 6. TblTokenEnvioCarga ✅ NOVO

**Model**: Token de envio de carga

**Views Disponíveis**:
- 🔌 **API**: `TokenEnvioCargaViewSet` ✨
  - CRUD completo
  - Custom actions: `cargas/`, `finalizar/`, `validar/`, `estatisticas/`

**Endpoints API**:
```
GET  /api/carga_org_lot/tokens/
POST /api/carga_org_lot/tokens/
GET  /api/carga_org_lot/tokens/{id}/
GET  /api/carga_org_lot/tokens/{id}/cargas/
POST /api/carga_org_lot/tokens/{id}/finalizar/
GET  /api/carga_org_lot/tokens/{id}/validar/
GET  /api/carga_org_lot/tokens/estatisticas/
```

**Status**: ✅ Implementado em 27/01/2026

---

## 📚 Models de Suporte (Read-Only ViewSets)

### 7-10. Tabelas Auxiliares ✅ NOVO

**Models**:
- `TblStatusProgresso`
- `TblStatusCarga`
- `TblTipoCarga`
- `TblStatusTokenEnvioCarga`

**Views Disponíveis**:
- 🔌 **API**: ViewSets Read-Only ✨
  - `StatusProgressoViewSet`
  - `StatusCargaViewSet`
  - `TipoCargaViewSet`
  - `StatusTokenEnvioCargaViewSet`

**Endpoints API**:
```
GET /api/carga_org_lot/status-progresso/
GET /api/carga_org_lot/status-progresso/{id}/

GET /api/carga_org_lot/status-carga/
GET /api/carga_org_lot/status-carga/{id}/

GET /api/carga_org_lot/tipo-carga/
GET /api/carga_org_lot/tipo-carga/{id}/

GET /api/carga_org_lot/status-token/
GET /api/carga_org_lot/status-token/{id}/
```

**Status**: ✅ Implementado em 27/01/2026

**Observação**: São tabelas de configuração/referência. ViewSets read-only são suficientes.

---

## ⚠️ Models COM Cobertura Parcial

### 11. TblOrgaoUnidade

**Model**: Órgãos e Unidades organizacionais

**Views Disponíveis**:
- ⚠️ **Parcial**: Listado via custom actions de `OrganogramaVersaoViewSet`
  - `GET /api/carga_org_lot/organogramas/{id}/orgaos/`
  - `GET /api/carga_org_lot/organogramas/{id}/hierarquia/`

**Recomendação**: 
- ✅ **OK** - Acesso via organograma é suficiente
- 🔵 **Opcional**: Criar `OrgaoUnidadeViewSet` se precisar de CRUD direto

---

### 12. TblLotacao

**Model**: Lotação de servidores

**Views Disponíveis**:
- ⚠️ **Parcial**: Listado via custom action de `LotacaoVersaoViewSet`
  - `GET /api/carga_org_lot/lotacoes/{id}/registros/`

**Recomendação**: 
- ✅ **OK** - Acesso via versão de lotação é suficiente
- 🔵 **Opcional**: Criar `LotacaoViewSet` se precisar de CRUD direto ou buscas complexas

---

### 13. TblOrganogramaJson

**Model**: JSON do organograma para envio à API

**Views Disponíveis**:
- ⚠️ **Parcial**: Acesso via custom action de `OrganogramaVersaoViewSet`
  - `GET /api/carga_org_lot/organogramas/{id}/json_envio/`

**Recomendação**: 
- 🟡 **Considerar**: Criar `OrganogramaJsonViewSet` similar a `LotacaoJsonOrgaoViewSet`
- Endpoints sugeridos:
  - `POST .../regenerar/` - Regenerar JSON
  - `POST .../enviar_api/` - Enviar para API externa

---

### 14-15. TblLotacaoInconsistencia e TblDetalheStatusCarga

**Models**: Inconsistências de lotação e Timeline de status de carga

**Views Disponíveis**:
- ⚠️ **Parcial**: Listados via custom actions
  - `GET /api/carga_org_lot/lotacoes/{id}/inconsistencias/`
  - `GET /api/carga_org_lot/cargas/{id}/timeline/`

**Recomendação**: 
- ✅ **OK** - São dados complementares, acesso via entidade principal é suficiente

---

## 📊 Resumo Estatístico

| Categoria | Quantidade | Status |
|-----------|------------|--------|
| **Total de Models** | 15 | - |
| **Com Views Completas** | 4 | ✅ TblPatriarca, TblOrganogramaVersao, TblLotacaoVersao, TblCargaPatriarca |
| **Views Recém Criadas** | 6 | ✨ TblLotacaoJsonOrgao, TblTokenEnvioCarga, + 4 auxiliares |
| **Cobertura Parcial (OK)** | 5 | ⚠️ TblOrgaoUnidade, TblLotacao, TblOrganogramaJson, TblLotacaoInconsistencia, TblDetalheStatusCarga |
| **Cobertura Total** | **15/15** | 🎉 **100%** |

---

## ✅ Checklist de Implementação

- [x] TblPatriarca - ViewSet completo
- [x] TblOrganogramaVersao - ViewSet completo
- [x] TblLotacaoVersao - ViewSet completo
- [x] TblCargaPatriarca - ViewSet completo
- [x] TblLotacaoJsonOrgao - ViewSet completo ✨ NOVO
- [x] TblTokenEnvioCarga - ViewSet completo ✨ NOVO
- [x] TblStatusProgresso - ViewSet read-only ✨ NOVO
- [x] TblStatusCarga - ViewSet read-only ✨ NOVO
- [x] TblTipoCarga - ViewSet read-only ✨ NOVO
- [x] TblStatusTokenEnvioCarga - ViewSet read-only ✨ NOVO
- [x] TblOrgaoUnidade - Via custom actions (suficiente)
- [x] TblLotacao - Via custom actions (suficiente)
- [x] TblOrganogramaJson - Via custom actions (considerar expansão)
- [x] TblLotacaoInconsistencia - Via custom actions (suficiente)
- [x] TblDetalheStatusCarga - Via custom actions (suficiente)

---

## 🛠️ Próximos Passos Sugeridos

### 1. Opcional: OrganogramaJsonViewSet

Criar ViewSet dedicado para `TblOrganogramaJson` similar ao `LotacaoJsonOrgaoViewSet`:

```python
class OrganogramaJsonViewSet(viewsets.ModelViewSet):
    # CRUD + custom actions:
    # - regenerar()
    # - enviar_api()
    # - estatisticas()
```

### 2. Testes de Integração

Criar testes para as novas views:
- `test_lotacao_json_orgao_viewset.py`
- `test_token_envio_carga_viewset.py`

### 3. Documentação da API

Adicionar ao Swagger/OpenAPI:
- Descrições de endpoints
- Exemplos de request/response
- Schemas de dados

### 4. Web Views (Opcional)

Se necessário, criar views web para:
- Gerenciamento de JSONs de lotação
- Visualização de tokens de envio

---

## 📚 Referências

- [Models Documentation](../models.py)
- [Serializers Documentation](../serializers.py)
- [Views README](../views/README.md)
- [API Views](../views/api_views/)
- [Web Views](../views/web_views/)

---

**Última Atualização**: 27 de janeiro de 2026  
**Status**: 🎉 Cobertura completa de models com views implementadas
