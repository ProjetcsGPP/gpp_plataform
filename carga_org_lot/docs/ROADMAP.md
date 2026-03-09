# 🗺️ ROADMAP - Conversão Google App Script → Django/Python

## 🎯 Objetivo

Converter o sistema **Carga Única de Organograma e Lotação** de Google App Script para uma aplicação Django moderna, mantendo todas as funcionalidades e melhorando a arquitetura.

---

## 📊 PROGRESSO GERAL

```
████████████████████████████░░░░░░░░░░░░ 70%
```

| Fase | Status | Completo |
|------|--------|----------|
| **1. Modelos e DB** | ✅ Concluído | 100% |
| **2. Serializers** | ✅ Concluído | 100% |
| **3. API Views** | ✅ Concluído | 100% |
| **4. URLs** | ✅ Concluído | 100% |
| **5. Templates Base** | ✅ Concluído | 100% |
| **6. Web Views** | 🟡 Em Progresso | 70% |
| **7. Processamento** | ⚠️ Pendente | 30% |
| **8. Integração API** | ⚠️ Pendente | 20% |
| **9. Testes** | ❌ Não Iniciado | 0% |

---

## 📝 MAPA DE CONVERSÃO: Google App Script → Django

### 📦 **ARQUIVOS GAS ORIGINAIS**

Arquivos encontrados em `carga_org_lot/docs/CargaUnica_GAS/`:

| Arquivo GAS | Função | Equivalente Django | Status |
|-------------|---------|-------------------|--------|
| **login.html** | Tela de login | `auth_views.py` + `login.html` | ✅ |
| **principal.html** | Dashboard com menu | `base.html` + `dashboard.html` | ✅ |
| **patriarcas.html** | Lista de patriarcas | `patriarca_list.html` + `patriarca_views.py` | ✅ |
| **organograma.html** | Upload organograma | `organograma_upload.html` + `organograma_views.py` | ✅ |
| **organograma_edicao.html** | Editar org visual | `organograma_edit.html` (ReactFlow) | 🟡 |
| **lotacao.html** | Upload lotação | `lotacao_upload.html` + `lotacao_views.py` | ✅ |
| **enviarParaAPI.html** | Envio para API | `carga_enviar.html` + `carga_views.py` | ✅ |
| **validarEnvioParaAPI.html** | Status de envio | `carga_status.html` + `carga_views.py` | ✅ |
| **Código.GS** | Lógica backend | Múltiplas views Python | 🟡 |

---

## 1️⃣ **FASE 1: MODELOS E BANCO DE DADOS** ✅

### ✅ **Completo**

- [x] Modelo `Patriarca` (tabela `patriarca`)
- [x] Modelo `StatusProgresso` (tabela `statusprogresso`)
- [x] Modelo `OrganogramaVersao` (tabela `organogramaversao`)
- [x] Modelo `OrgaoUnidade` (tabela `orgaounidade`)
- [x] Modelo `LotacaoVersao` (tabela `lotacaoversao`)
- [x] Modelo `Lotacao` (tabela `lotacao`)
- [x] Modelo `InconsistenciaLotacao` (tabela `inconsistencialotacao`)
- [x] Modelo `OrganogramaJSON` (tabela `organogramajson`)
- [x] Modelo `StatusTokenEnvioCarga` (tabela `statustokenenviocarga`)
- [x] Modelo `TipoCarga` (tabela `tipocarga`)
- [x] Modelo `StatusCarga` (tabela `statuscarga`)
- [x] Modelo `CargaPatriarca` (tabela `cargapatriarca`)
- [x] DB Router para schema `cargaorglot`
- [x] Migrations criadas e aplicadas

**Arquivos:**
- `models.py` (24KB)
- `db_router.py`

---

## 2️⃣ **FASE 2: SERIALIZERS** ✅

### ✅ **Completo**

- [x] `PatriarcaSerializer`
- [x] `OrganogramaVersaoSerializer`
- [x] `OrgaoUnidadeSerializer`
- [x] `OrgaoUnidadeHierarquiaSerializer` (nested)
- [x] `LotacaoVersaoSerializer`
- [x] `LotacaoSerializer`
- [x] `InconsistenciaLotacaoSerializer`
- [x] `OrganogramaJSONSerializer`
- [x] `CargaPatriarcaSerializer`
- [x] `CargaPatriarcaDetalhadoSerializer`

**Arquivo:**
- `serializers.py` (17.6KB)

---

## 3️⃣ **FASE 3: API VIEWS (REST)** ✅

### ✅ **Completo**

- [x] `PatriarcaViewSet` - CRUD completo de patriarcas
- [x] `OrganogramaVersaoViewSet` - CRUD de versões
- [x] `OrgaoUnidadeViewSet` - CRUD de unidades
- [x] `LotacaoVersaoViewSet` - CRUD de versões de lotação
- [x] `LotacaoViewSet` - CRUD de registros de lotação
- [x] `OrganogramaJSONViewSet` - CRUD de JSONs
- [x] `CargaPatriarcaViewSet` - CRUD de cargas
- [x] Endpoints de dashboard e estatísticas
- [x] Endpoints de busca/filtros
- [x] Permissões configuradas

**Arquivo:**
- `views/api_views.py` (35.8KB)

---

## 4️⃣ **FASE 4: URLS** ✅

### ✅ **Completo**

- [x] `urls.py` principal (redirecionamentos)
- [x] `urls/api_urls.py` (rotas REST)
- [x] `urls/web_urls.py` (rotas web)
- [x] Integração com `gpp_plataform/urls.py`

**Arquivos:**
- `urls.py` (3.7KB)
- `urls/api_urls.py`
- `urls/web_urls.py`

---

## 5️⃣ **FASE 5: TEMPLATES BASE E ESTRUTURA** ✅

### ✅ **Completo**

#### **Arquitetura de Herança**

```
templates/base.html (GLOBAL)
  ↓ herda
carga_org_lot/templates/carga_org_lot/base.html (MENU LATERAL)
  ↓ herda
Páginas específicas (dashboard, patriarca, etc.)
```

#### **Templates Criados**

- [x] `templates/base.html` - Base global do projeto (header, footer, Bootstrap)
- [x] `carga_org_lot/templates/carga_org_lot/base.html` - Base da app + menu lateral
- [x] `login.html` - Tela de login
- [x] `dashboard.html` - Dashboard principal
- [x] `patriarca_list.html` - Lista de patriarcas
- [x] `patriarca_form.html` - Formulário de patriarca
- [x] `organograma_upload.html` - Upload de organograma
- [x] `organograma_edit.html` - Edição visual (ReactFlow)
- [x] `lotacao_upload.html` - Upload de lotação
- [x] `carga_enviar.html` - Envio de carga
- [x] `carga_status.html` - Status de cargas

#### **CSS Customizado**

- [x] `static/carga_org_lot/css/menu.css` - Estilos do menu lateral e componentes

**Status:**
- ✅ Estrutura de templates completa
- ✅ Menu lateral responsivo
- ✅ CSS customizado com cores da aplicação
- ✅ Herança correta (base global → base app → páginas)

---

## 6️⃣ **FASE 6: WEB VIEWS (DJANGO)** 🟡 70%

### ✅ **Já Implementado**

- [x] `auth_views.py` - Login, logout, decoradores (4.2KB)
- [x] `dashboard_views.py` - Dashboard básico (1.8KB)
- [x] `patriarca_views.py` - CRUD de patriarcas (9.4KB)
- [x] `organograma_views.py` - Views de organograma (3.7KB)
- [x] `lotacao_views.py` - Views de lotação (4KB)
- [x] `carga_views.py` - Views de carga (2.6KB)
- [x] `upload_views.py` - Upload genérico (1.5KB)
- [x] `ajax_views.py` - Endpoints AJAX (1.2KB)

### ⚠️ **Pendente - A Implementar**

#### **6.1. Dashboard Completo**
- [ ] Estatísticas em tempo real
- [ ] Gráficos de progresso
- [ ] Últimas atividades
- [ ] Alertas e notificações

#### **6.2. Patriarcas**
- [ ] Formulário de criação/edição completo
- [ ] Validação de sigla única
- [ ] Deleção com confirmação
- [ ] Histórico de alterações

#### **6.3. Organograma - Upload e Processamento**
- [ ] Upload de arquivo Word/Excel/Google Drive
- [ ] Parser de documentos estruturados
- [ ] Validação de hierarquia
- [ ] Preview antes de salvar
- [ ] Log de processamento

#### **6.4. Organograma - Edição Visual**
- [ ] Integração completa com ReactFlow
- [ ] Arrastar e soltar nós
- [ ] Adicionar/remover unidades
- [ ] Editar propriedades inline
- [ ] Atalhos de teclado
- [ ] Exportar para JSON/imagem

#### **6.5. Lotação - Upload e Processamento**
- [ ] Upload de planilha Excel multi-abas
- [ ] Parser de planilhas
- [ ] Validação de CPF/matrícula
- [ ] Validação de consistência com organograma
- [ ] Relatório de inconsistências
- [ ] Correção manual de erros

#### **6.6. Envio para API Externa**
- [ ] Seleção de patriarcas para envio
- [ ] Pré-validação antes do envio
- [ ] Envio assíncrono (Celery)
- [ ] Barra de progresso
- [ ] Retry automático em caso de erro

#### **6.7. Status e Monitoramento**
- [ ] Timeline de eventos
- [ ] Logs detalhados
- [ ] Filtros avançados
- [ ] Exportação de relatórios
- [ ] Notificações por email

---

## 7️⃣ **FASE 7: PROCESSAMENTO E LÓGICA DE NEGÓCIO** ⚠️ 30%

### ✅ **Já Implementado**

- [x] Estrutura de utils
- [x] Forms básicos (7.7KB)

### ⚠️ **Pendente - Converter de Google App Script**

#### **7.1. Processamento de Organograma**
- [ ] `processar_documento_organograma()` - Lê Word/Excel/Google Docs
- [ ] `extrair_hierarquia()` - Extrai estrutura hierárquica
- [ ] `validar_estrutura_organograma()` - Valida integridade
- [ ] `construir_arvore_hierarquica()` - Constrói árvore
- [ ] `calcular_numeros_hierarquicos()` - Gera numeração (1.1, 1.2, etc.)
- [ ] `salvar_versao_organograma()` - Persiste no BD

**Referência GAS:**
```javascript
// Em Código.GS
function processarOrganograma(fileId) {
  var doc = DocumentApp.openById(fileId);
  var body = doc.getBody();
  // ...
}
```

#### **7.2. Processamento de Lotação**
- [ ] `processar_planilha_lotacao()` - Lê Excel/Google Sheets
- [ ] `extrair_dados_lotacao()` - Extrai registros de cada aba
- [ ] `validar_cpf()` - Valida formato de CPF
- [ ] `validar_matricula()` - Valida matrícula
- [ ] `vincular_lotacao_organograma()` - Vincula servidor à unidade
- [ ] `detectar_inconsistencias()` - Identifica erros
- [ ] `salvar_versao_lotacao()` - Persiste no BD

**Referência GAS:**
```javascript
// Em Código.GS
function processarLotacao(sheetId) {
  var ss = SpreadsheetApp.openById(sheetId);
  var sheets = ss.getSheets();
  // ...
}
```

#### **7.3. Geração de JSON para API**
- [ ] `gerar_json_organograma()` - Formata organograma para API externa
- [ ] `gerar_json_lotacao()` - Formata lotação para API externa
- [ ] `validar_json_schema()` - Valida contra schema da API
- [ ] `comprimir_json()` - Otimiza tamanho

**Referência GAS:**
```javascript
// Em Código.GS
function gerarJSONOrganograma(idPatriarca) {
  var json = {
    orgaos: [],
    unidades: []
  };
  // ...
  return JSON.stringify(json);
}
```

#### **7.4. Utilities**
- [ ] `validar_sigla_unica()` - Garante sigla única
- [ ] `normalizar_nome()` - Remove acentos, capitaliza
- [ ] `gerar_uuid_externo()` - Gera identificadores
- [ ] `log_atividade()` - Registra ações do usuário

---

## 8️⃣ **FASE 8: INTEGRAÇÃO COM API EXTERNA** ⚠️ 20%

### ⚠️ **Pendente - Implementar**

#### **8.1. Autenticação OAuth2**
- [ ] `obter_token_acesso()` - Solicita token da API externa
- [ ] `renovar_token()` - Renova token expirado
- [ ] `armazenar_token()` - Salva em `StatusTokenEnvioCarga`

**Referência GAS:**
```javascript
// Em Código.GS
function obterToken() {
  var response = UrlFetchApp.fetch(TOKEN_URL, {
    method: 'post',
    payload: {
      grant_type: 'client_credentials',
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET
    }
  });
  // ...
}
```

**Django:**
```python
import requests
from django.conf import settings

def obter_token_acesso():
    response = requests.post(
        settings.API_EXTERNA_TOKEN_URL,
        data={
            'grant_type': 'client_credentials',
            'client_id': settings.API_EXTERNA_CLIENT_ID,
            'client_secret': settings.API_EXTERNA_CLIENT_SECRET,
        }
    )
    return response.json()['access_token']
```

#### **8.2. Envio de Organograma**
- [ ] `enviar_organograma_api()` - POST para endpoint da API
- [ ] `verificar_status_envio()` - Consulta status via token
- [ ] `processar_retorno_api()` - Trata resposta
- [ ] `atualizar_status_carga()` - Atualiza BD

**Endpoints API Externa:**
```
POST https://api.externa.gov.br/v1/organogramas
GET  https://api.externa.gov.br/v1/status/{token}
```

#### **8.3. Envio de Lotação**
- [ ] `enviar_lotacao_api()` - POST para endpoint da API
- [ ] `verificar_status_lotacao()` - Consulta status
- [ ] `processar_retorno_lotacao()` - Trata resposta

#### **8.4. Tratamento de Erros**
- [ ] Retry automático (3 tentativas)
- [ ] Exponential backoff
- [ ] Logging detalhado
- [ ] Alertas para administradores

#### **8.5. Tarefas Assíncronas (Celery)**
- [ ] Configurar Celery
- [ ] Task `processar_organograma.delay()`
- [ ] Task `processar_lotacao.delay()`
- [ ] Task `enviar_para_api.delay()`
- [ ] Monitoramento de tasks

---

## 9️⃣ **FASE 9: TESTES** ❌ 0%

### ⚠️ **Pendente - Criar**

#### **9.1. Testes Unitários**
- [ ] Tests de models
- [ ] Tests de serializers
- [ ] Tests de utils
- [ ] Tests de forms

#### **9.2. Testes de Integração**
- [ ] Tests de API views
- [ ] Tests de web views
- [ ] Tests de processamento
- [ ] Tests de envio API

#### **9.3. Testes de Interface**
- [ ] Selenium para fluxos críticos
- [ ] Upload de arquivos
- [ ] Navegação do menu
- [ ] Formulários

#### **9.4. Carga de Dados de Teste**
- [ ] Fixtures com dados realistas
- [ ] Scripts de população do banco
- [ ] Arquivos de exemplo

---

## 🔟 **PRÓXIMOS PASSOS IMEDIATOS**

### 🎯 **Sprint Atual: Interface Web Completa**

1. **Dashboard com Estatísticas** (2-3 dias)
   - Cards de estatísticas
   - Gráficos Chart.js
   - Últimas atividades

2. **Formulário de Patriarca Completo** (1 dia)
   - Validações frontend
   - Mensagens de erro amigáveis
   - Confirmação de deleção

3. **Upload e Processamento de Organograma** (5-7 dias)
   - Parser de Word (python-docx)
   - Parser de Excel (openpyxl)
   - Lógica de extração de hierarquia
   - Testes com arquivo real

4. **Editor Visual ReactFlow** (5-7 dias)
   - Setup do ReactFlow
   - Renderização da árvore
   - Edição de nós
   - Persistência de mudanças

5. **Upload e Processamento de Lotação** (3-5 dias)
   - Parser de Excel multi-abas
   - Validação de CPF
   - Vinculação com organograma
   - Relatório de erros

### 🎯 **Sprint Seguinte: Integração API**

6. **Cliente API Externa** (3-5 dias)
   - Autenticação OAuth2
   - Envio de organograma
   - Envio de lotação
   - Verificação de status

7. **Tarefas Assíncronas** (2-3 dias)
   - Setup Celery + Redis
   - Tasks de processamento
   - Tasks de envio
   - Monitoramento

8. **Testes Automatizados** (3-5 dias)
   - Cobertura mínima de 70%
   - Testes críticos
   - CI/CD básico

---

## 📋 **CHECKLIST DE TESTES MANUAIS**

Antes de fazer pull request para main:

### ✅ **Interface**
- [ ] Login funciona
- [ ] Logout funciona
- [ ] Menu lateral aparece
- [ ] Menu é responsivo (mobile)
- [ ] Todas as páginas carregam sem erro 500
- [ ] Navegação entre páginas funciona
- [ ] Mensagens de sucesso/erro aparecem

### ✅ **Patriarcas**
- [ ] Listar patriarcas
- [ ] Criar novo patriarca
- [ ] Editar patriarca existente
- [ ] Deletar patriarca
- [ ] Seleção de patriarca ativo

### ✅ **Organograma**
- [ ] Página de upload carrega
- [ ] Upload de arquivo (mesmo sem processar)
- [ ] Visualização de versões
- [ ] Editor visual (mesmo que placeholder)

### ✅ **Lotação**
- [ ] Página de upload carrega
- [ ] Upload de planilha
- [ ] Listagem de versões

### ✅ **Carga**
- [ ] Página de envio carrega
- [ ] Lista patriarcas disponíveis
- [ ] Página de status carrega
- [ ] Histórico de cargas (mesmo vazio)

### ✅ **API REST**
- [ ] `/api/carga_org_lot/` responde
- [ ] `/api/carga_org_lot/patriarcas/` lista
- [ ] Autenticação funciona
- [ ] Permissões aplicadas

---

## 📚 **REFERÊNCIAS**

### **Documentos do Projeto**
- [README.md](../README.md) - Visão geral da aplicação
- [MODELS_COVERAGE.md](./MODELS_COVERAGE.md) - Cobertura de modelos
- [FASE_3_API_VIEWS.md](./FASE_3_API_VIEWS.md) - Documentação das APIs
- [FASE_4_URLS.md](./FASE_4_URLS.md) - Mapeamento de URLs
- [views/README.md](../views/README.md) - Estrutura de views

### **Código Original (Google App Script)**
- `docs/CargaUnica_GAS/Código.GS` - Lógica principal
- `docs/CargaUnica_GAS/principal.html` - Interface principal
- `docs/CargaUnica_GAS/*.html` - Demais telas

### **Bibliotecas Python Necessárias**
```txt
django>=4.2
djangorestframework>=3.14
python-docx>=0.8  # Parser de Word
openpyxl>=3.1     # Parser de Excel
celery>=5.3       # Tarefas assíncronas
redis>=4.6        # Message broker
requests>=2.31    # Cliente HTTP
validate-docbr    # Validação de CPF/CNPJ
```

---

## ✅ **CRITÉRIOS DE ACEITAÇÃO FINAL**

Para considerar a conversão **100% completa**:

1. **Funcionalidades**
   - [ ] Todas as funcionalidades do GAS original estão implementadas
   - [ ] Upload e processamento de organograma funciona
   - [ ] Upload e processamento de lotação funciona
   - [ ] Envio para API externa funciona
   - [ ] Editor visual de organograma funciona

2. **Qualidade**
   - [ ] Cobertura de testes ≥ 70%
   - [ ] Zero erros 500 em produção
   - [ ] Performance aceitável (< 3s por requisição)
   - [ ] Responsivo (funciona em mobile)

3. **Documentação**
   - [ ] README atualizado
   - [ ] Comentários em código complexo
   - [ ] Documentação da API (Swagger/OpenAPI)
   - [ ] Manual de usuário

4. **Deploy**
   - [ ] Ambiente de homologação funcional
   - [ ] CI/CD configurado
   - [ ] Monitoramento ativo
   - [ ] Backup automático do banco

---

**Última Atualização:** 03/02/2026 - 15:15 BRT
**Responsável:** Equipe GPP
**Versão:** 1.0
