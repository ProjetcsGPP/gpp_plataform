const CONFIG = {

  LOGIN_PAGE: 'login',
  PRINCIPAL_PAGE: 'principal',

  SPREADSHEET_PARAM: 'CargaInicial - Organograma e Lotacao',

  SHEET_LISTAS: 'Listas',
  SHEET_LOG: 'Log',
  SHEET_STATUS_ENVIO: 'Status_Envio',

  TAB_USUARIOS: 'A1:E100',
  TAB_PATRIARCA: 'G1:N90',
  TAB_TOKEN: 'A2:E1000',
  TAB_ORGANOGRAMA: 'A1:E1000',
  TAB_STATUS_CARGA: 'A1:M1000',

  COL_NOME_PATRIARCA: 'G',
  COL_PASSWD: 'K',
  IDX_COL_PASSWD: '11',

  SMTP_SERVER: 'seger.correio.es.gov.br',
  SMTP_PORT: '443',
  SMTP_SERVER_COMP: '/service/soap',
  EMAIL_SENDER: 'acoesgpp@seger.es.gov.br',
  EMAIL_SENDER_DISPLAY: 'Ações GPP',
  PASSWD_EMAIL_SENDER: 'GPP@acoes2025',

  URL_GET_TOKEN: 'https://acessocidadao.es.gov.br/is/connect/token',

  AUTORIZATION_BEARER_HML: '',
  URL_CARGA_HML: 'https://api.cargarh.hom.es.gov.br/',

  AUTORIZATION_BEARER_PRD: '',
  URL_CARGA_PRD: 'https://api.cargarh.es.gov.br/',

  CARGA_V3: 'v3/',

  RESPONSE_CODE_SUCCESS_GENERIC: 200,
  RESPONSE_CODE_SUCCESS_CARGA: 201,
  RESPONSE_CODE_SUCCESS_MSG: 'A solicitação para a chamada do método da API foi executada com sucesso!',
  
  RESPONSE_CODE_BAD_REQUEST: 400,
  RESPONSE_CODE_BAD_REQUEST_MSG: 'A sintaxe da solicitação para a chamada do método da API está inválida ou malformada.',
  
  RESPONSE_CODE_UNAUTHORIZED: 401,
  RESPONSE_CODE_UNAUTHORIZED_MSG: 'A solicitação para a chamada do método da API não está autorizada; são necessárias credenciais válidas.',
  
  RESPONSE_CODE_FORBIDDEN: 403,
  RESPONSE_CODE_FORBIDDEN_MSG: 'O servidor recebeu a solicitação, mas foi negada!',
  
  RESPONSE_CODE_NOT_FOUND: 404,
  RESPONSE_CODE_NOT_FOUND_MSG: 'A solicitação para a chamada do método da API não existe no servidor.',
  
  RESPONSE_CODE_METHOD_NOT_ALLOWED: 405,
  RESPONSE_CODE_METHOD_NOT_ALLOWED_MSG: 'O método HTTP utilizado (GET, POST, etc.) não é permitido para a chamada do método da API.',
  
  RESPONSE_CODE_NOT_ACCEPTABLE: 406,
  RESPONSE_CODE_NOT_ACCEPTABLE_MSG: 'O servidor não pode gerar uma resposta no formato solicitado (Accept header).',
  
  RESPONSE_CODE_REQUEST_TIMEOUT: 408,
  RESPONSE_CODE_REQUEST_TIMEOUT_MSG: 'O tempo de resposta da solicitação para a chamada ao método da API expirou!',
  
  RESPONSE_CODE_CONFLICT: 409,
  RESPONSE_CODE_CONFLICT_MSG: 'A solicitação para a chamada ao método da API conflita com o estado atual do recurso no servidor.',
  
  RESPONSE_CODE_UNPROCESSABLE_ENTITY: 422,
  RESPONSE_CODE_UNPROCESSABLE_ENTITY_MSG: 'A solicitação para a chamada ao método da API estava bem formada, mas contém erros semânticos (falha na validação de regra).',
  
  RESPONSE_CODE_TOO_MANY_REQUESTS: 429, // Nova constante
  RESPONSE_CODE_TOO_MANY_REQUESTS_MSG: 'Foram executadas muitas requisições à API! O limite foi excedido!', // 'Muitas solicitações (Erro 429). O limite de taxa foi excedido.',
  
  RESPONSE_CODE_INTERNAL_SERVER_ERROR: 500,
  RESPONSE_CODE_INTERNAL_SERVER_ERROR_MSG: 'Ocorreu um erro genérico na solicitação para a chamada do método da API', //'Um erro genérico ocorreu no servidor.',

  RESPONSE_CODE_BAD_GATEWAY: 502,
  RESPONSE_CODE_BAD_GATEWAY_MSG: 'O servidor (atuando como proxy) recebeu uma resposta inválida do servidor upstream.',

  RESPONSE_CODE_SERVICE_UNAVAILABLE: 503,
  RESPONSE_CODE_SERVICE_UNAVAILABLE_MSG: 'O servidor está temporariamente indisponível.',

  RESPONSE_CODE_GATEWAY_TIMEOUT: 504,
  RESPONSE_CODE_GATEWAY_TIMEOUT_MSG: 'O servidor (atuando como proxy) não recebeu uma resposta para a solicitação da chamada ao método da API a tempo do servidor upstream.',

  // Configurações de Retry (Tentativa)
  // Número máximo de tentativas
  MAX_RETRIES: 5,
  // Tempo base de espera (1 segundo)
  INITIAL_BACKOFF_MS: 1000,

  CLIENT_ID_CARGARH: 'f1407cd0-511e-44b3-8103-e3e9887a03fd',
  CLIENT_SECRET_CARGARH: '1UT5X$NVvL8eRCre6g1TKhovcSNcfi',
  CLIENT_SCOPE_CARGARH: 'api-cargarh-base api-cargarh-inicial',
  
  // Configurações de verificação de status
  STATUS_CHECK_INTERVAL_MS: 180000, // 3 minutos em milissegundos
  STATUS_MAX_ATTEMPTS: 5, // Máximo de tentativas de verificação

  // Enums da API
  TIPO_CARGA: {
    INICIAL_ORGANOGRAMA: 3,
    INICIAL_LOTACOES: 4,
    INICIAL_LOTACOES_PACOTE: 5
  },

  TIPO_CARGA_TEXT: {
    3: 'Organograma',
    4: 'Lotações',
    5: 'Lotações Pacote'
  },

  STATUS_CARGA: {
    AGUARDANDO_ANALISE_INICIAL: 0,
    AGUARDANDO_ORGANOGRAMA: 1,
    ORGANOGRAMA_FINALIZADO: 2,
    AGUARDANDO_ACESSO_CIDADAO: 3,
    ACESSO_CIDADAO_FINALIZADO: 4,
    FINALIZADO: 5,
    ERRO: 6,
    AGUARDANDO_ACESSO_CIDADAO_LOTACAO: 7,
    AGUARDANDO_ORGANOGRAMA_CARGA_INICIAL: 8,
    AGUARDANDO_LOTACAO_CARGA_INICIAL: 9,
    AGUARDANDO_LOTACAO_CARGA_INICIAL_PACOTE: 10
  },

  STATUS_CARGA_TEXT: {
    0: 'Análise Incial',
    1: 'Aguardando Organograma',
    2: 'Organograma Finalizado',
    3: 'Aguardadno Acesso Cidadão',
    4: 'Acesso Cidadão Finalizado',
    5: 'Finalizado',
    6: 'Erro',
    7: 'Aguardando Acesso Cidadão Lotação',
    8: 'Aguardando Acesso Cidadão Organograma',
    9: 'Aguardando Carga Inicial de Lotação',
    10: 'Aguardando Carga Inicial de Lotação Pacote'
  },

  // Endpoints da API v3
  API_ENDPOINTS: {
    ORGANOGRAMA: 'CargaInicial/organograma/',
    LOTACOES: 'CargaInicial/lotacoes/',
    LOTACOES_PACOTE: 'CargaInicial/lotacoes/pacote/',
    STATUS: 'CargaInicial/{guid}/status'
  },

  // Padrões de nome de arquivos JSON
  JSON_PATTERNS: {
    ORGANOGRAMA: 'cargadeorgaos_{sigla}.json',      // Ex: cargadeorgaos_PMEXE.json
    LOTACAO: 'cargalotacao_{sigla}_{orgao}.json'   // Ex: cargalotacao_PMEXE_SMMA.json
  },
  
  // Pasta no Drive
  FOLDER_CARGA_ENVIO: 'Carga - Para Envio'  
};

const MimeType = {
  
  GOOGLE_FORMS: "application/vnd.google-apps.form",
  GOOGLE_FOLDER: "application/vnd.google-apps.folder",
  GOOGLE_FILES: "application/vnd.google-apps.file",
  GOOGLE_SITES: "application/vnd.google-apps.site",
  GOOGLE_DOCUMENT: "application/vnd.google-apps.document",
  GOOGLE_SPREADSHEET: "application/vnd.google-apps.spreadsheet",

  MICROSOFT_EXCEL: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  MICROSOFT_EXCEL_LEGACY: "application/vnd.ms-excel",
  MICROSOFT_WORD: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  MICROSOFT_WORD_LEGACY: "application/msword",
  JSON_PATTERN: "application/json",

  OPEN_DOCUMENT_TEXT: "application/vnd.oasis.opendocument.text",
  OPEN_DOCUMENT_SPREADSHEET: "application/vnd.oasis.opendocument.spreadsheet"
};

var DICIONARIO_GENERO = {
  // Administração / Gestão
  "ADMINISTRADOR": "ADMINISTRADOR(A)",
  "ANALISTA": "ANALISTA(A)",
  "ASSESSOR": "ASSESSOR(A)",
  "ASSISTENTE": "ASSISTENTE(A)",
  "AUXILIAR": "AUXILIAR(A)",
  "CHEFE": "CHEFE(A)",
  "COORDENADOR": "COORDENADOR(A)",
  "DIRETOR": "DIRETOR(A)",
  "GERENTE": "GERENTE(A)",
  "PRESIDENTE": "PRESIDENTE(A)",
  "SUPERINTENDENTE": "SUPERINTENDENTE(A)",
  "VICE-PRESIDENTE": "VICE-PRESIDENTE(A)",

  // Educação
  "PROFESSOR": "PROFESSOR(A)",
  "EDUCADOR": "EDUCADOR(A)",
  "PEDAGOGO": "PEDAGOGO(A)",
  "ORIENTADOR": "ORIENTADOR(A)",

  // Saúde
  "MÉDICO": "MÉDICO(A)",
  "ENFERMEIRO": "ENFERMEIRO(A)",
  "FISIOTERAPEUTA": "FISIOTERAPEUTA(A)",
  "FONOAUDIÓLOGO": "FONOAUDIÓLOGO(A)",
  "ODONTÓLOGO": "ODONTÓLOGO(A)",
  "PSICÓLOGO": "PSICÓLOGO(A)",
  "FARMACÊUTICO": "FARMACÊUTICO(A)",
  "BIOQUÍMICO": "BIOQUÍMICO(A)",
  "NUTRICIONISTA": "NUTRICIONISTA(A)",
  "VETERINÁRIO": "VETERINÁRIO(A)",

  // Jurídico
  "ADVOGADO": "ADVOGADO(A)",
  "PROCURADOR": "PROCURADOR(A)",
  "PROMOTOR": "PROMOTOR(A)",
  "DEFENSOR": "DEFENSOR(A)",
  "JUIZ": "JUIZ(A)", // aqui talvez prefira "MAGISTRADO(A)"
  "MAGISTRADO": "MAGISTRADO(A)",
  "DELEGADO": "DELEGADO(A)",

  // Engenharia / Técnico
  "ENGENHEIRO": "ENGENHEIRO(A)",
  "ARQUITETO": "ARQUITETO(A)",
  "URBANISTA": "URBANISTA(A)",
  "GEÓLOGO": "GEÓLOGO(A)",
  "TÉCNICO": "TÉCNICO(A)",
  "DESENHISTA": "DESENHISTA(A)",
  "OPERADOR": "OPERADOR(A)",
  "PROGRAMADOR": "PROGRAMADOR(A)",

  // Finanças / Contábil
  "CONTADOR": "CONTADOR(A)",
  "TESOUREIRO": "TESOUREIRO(A)",
  "ECONOMISTA": "ECONOMISTA(A)",
  "AUDITOR": "AUDITOR(A)",
  "CONTROLADOR": "CONTROLADOR(A)",

  // Política / Administração Pública
  "PREFEITO": "PREFEITO(A)",
  "VEREADOR": "VEREADOR(A)",
  "GOVERNADOR": "GOVERNADOR(A)",
  "SECRETÁRIO": "SECRETÁRIO(A)",
  "MINISTRO": "MINISTRO(A)",
  "SENADOR": "SENADOR(A)",
  "DEPUTADO": "DEPUTADO(A)",

  // Outras profissões
  "ESTAGIÁRIO": "ESTAGIÁRIO(A)",
  "MONITOR": "MONITOR(A)",
  "PESQUISADOR": "PESQUISADOR(A)",
  "CONSULTOR": "CONSULTOR(A)",
  "ESPECIALISTA": "ESPECIALISTA(A)",
  "INSTRUTOR": "INSTRUTOR(A)",
  "ARTISTA": "ARTISTA(A)",
  "JORNALISTA": "JORNALISTA(A)",

  // Áreas diversas
  "AGENTE": "AGENTE(A)",
  "INSPETOR": "INSPETOR(A)",
  "FISCAL": "FISCAL(A)",
  "GUARDA": "GUARDA(A)",
  "POLICIAL": "POLICIAL(A)"
};

var DICIONARIO_ABREVIACOES = {
  "ASG": "AUXILIAR DE SERVIÇOS GERAIS",
  "DT": "DELEGADO TÉCNICO",
  "OCUPAÇÃO/CARGO": "CARGO",
  "(A)": "", // marcador de gênero, será tratado no dicionário de gênero
  "SECRETÁRIO(A)": "SECRETÁRIO",
  "MÉDICO(A)": "MÉDICO",
  "PROFESSOR(A)": "PROFESSOR",
  "ENFERMEIRO(A)": "ENFERMEIRO",
  "COORDENADOR(A)": "COORDENADOR",
  "PEDAGOGO(A)": "PEDAGOGO",
  "PSICÓLOGO(A)": "PSICÓLOGO",
  "TESOUREIRO(A)": "TESOUREIRO",
  "FARMACÊUTICO(A)": "FARMACÊUTICO",
  "BIOQUÍMICO(A)": "BIOQUÍMICO",
  "ESTAGIÁRIO(A)": "ESTAGIÁRIO",
  "DIRETOR(A)": "DIRETOR",
  "SUPERINTENDENTE(A)": "SUPERINTENDENTE",
  "PRESIDENTE": "PRESIDENTE",
  "VICE-PRESIDENTE": "VICE-PRESIDENTE",
  "DT": "DETENTOR DE TAREFAS",
  "CAPS": "CENTRO DE ATENÇÃO PSICOSSOCIAL",
  "NASF": "NÚCLEO DE APOIO À SAÚDE DA FAMÍLIA",
  "RH": "RECURSOS HUMANOS",
  "CRECHE": "CRECHE",
  "PRÉ-ESCOLA": "PRÉ-ESCOLA",
  "FUNDEB": "FUNDO DE MANUTENÇÃO E DESENVOLVIMENTO DA EDUCAÇÃO BÁSICA",
  "AUD": "AUDITORIA",
  "CAD": "CADASTRO",
  "ALM": "ALMOXARIFADO",
  "TEC": "TÉCNICO",
  "ADM": "ADMINISTRATIVO",
  "ADM MUNICIPAL": "ADMINISTRATIVO MUNICIPAL",
  "GESTÃO": "GESTÃO",
  "FIN": "FINANCEIRO",
  "FISC": "FISCAL",
  "TRIB": "TRIBUTÁRIO",
  "PROJ": "PROJETOS",
  "TUR": "TURISMO",
  "CONT": "CONTRATOS",
  "COMP": "COMPRAS",
  "CULT": "CULTURA",
  "ESP": "ESPORTES",
  "LAZ": "LAZER",
  "PAT": "PATRIMÔNIO",
  "OUV": "OUVIDORIA",
  "ADM ESC": "ADMINISTRATIVO ESCOLAR",
  "ADM FIN": "ADMINISTRATIVO FINANCEIRO",
  "TEC INF": "TÉCNICO DE INFORMÁTICA",
  "SUP": "SUPERINTENDÊNCIA",
  "FISC AMB": "FISCAL DE VIGILÂNCIA AMBIENTAL",
  "FISC SAN": "FISCAL DE VIGILÂNCIA SANITÁRIA",
  "ENG CIVIL": "ENGENHEIRO CIVIL",
  "EDUC FIS": "EDUCADOR FÍSICO",
  "GEST PROJ": "GESTOR DE PROJETOS",
  "MED VET": "MÉDICO VETERINÁRIO",
  "PROF(A)": "PROFESSOR(A)",    // caso específico de professores
  "PROF.EDU": "PROFESSOR(A)",  // professor de educação
  "PROF.FIS": "PROFESSOR(A)",  // professor de educação
  "PROF.MAT": "PROFESSOR(A)",  // professor de educação
  "PROF.POR": "PROFESSOR(A)",  // professor de educação
  "PROF.CIE": "PROFESSOR(A)",  // professor de educação
  "PROF.ART": "PROFESSOR(A)",  // professor de educação
  "PROF.GEO": "PROFESSOR(A)",  // professor de educação
  "PROF.HIS": "PROFESSOR(A)",  // professor de educação
  "PROF.ING": "PROFESSOR(A)",  // professor de educação
  "PROF.REL": "PROFESSOR(A)",  // professor de educação
  "PROF.QUI": "PROFESSOR(A)",  // professor de educação
  "PROF.BIO": "PROFESSOR(A)",  // professor de educação
  "PROF.ESP": "PROFESSOR(A)",  // professor de educação
  "PROF.TEC": "PROFESSOR(A)",  // professor de educação
  "PROF.SOC": "PROFESSOR(A)",  // professor de educação
  "PROF.FIL": "PROFESSOR(A)",  // professor de educação
  "PROF.LIT": "PROFESSOR(A)",  // professor de educação
  "PROF.INF": "PROFESSOR(A)",  // professor de educação
  "PROF.ENF": "PROFESSOR(A)",  // professor de educação
  "PROF.MEC": "PROFESSOR(A)",  // professor de educação
  "PROF.ADM": "PROFESSOR(A)",  // professor de educação
  "PROF.LOG": "PROFESSOR(A)",  // professor de educação
  "PROF.": "PROFISSIONAL",
  "PROF": "PROFISSIONAL"
};

/**
 * Mapeamento dos códigos de Status da API para dados de UI.
 */

const StatusCargaMap = {
  5: "Finalizado",
  6: "Erro",
  8: "Aguardando Organograma",
  9: "Aguardando Lotação",
  10: "Aguardando Pacote de Lotação"
};

const StatusCargaUIData = {
  5: { status: "Finalizado", progress: 100, badgeClass: 'success' },
  6: { status: "Erro", progress: 100, badgeClass: 'danger' },
  8: { status: "Aguardando Organograma", progress: 50, badgeClass: 'info' },
  9: { status: "Aguardando Lotação", progress: 75, badgeClass: 'info' },
  10: { status: "Aguardando Pacote de Lotação", progress: 75, badgeClass: 'info' },
  'default': { status: "Processando", progress: 25, badgeClass: 'secondary' }
};

// ====================================
// FUNÇÕES DO USUÁRIO
// ====================================

function setSiteProperty() {
  const scriptProperties = PropertiesService.getScriptProperties();
  scriptProperties.setProperty('siteURL', ScriptApp.getService().getUrl());
  return { siteURL: ScriptApp.getService().getUrl() };
}

function getSiteProperty() {
  const scriptProperties = PropertiesService.getScriptProperties();
  return { siteURL: scriptProperties.getProperty('siteURL') };
}

function setEmailProperty(email){
  const propriedades = PropertiesService.getUserProperties();
  propriedades.setProperty('email_to_passwd', email);
  return {email: email};
}

function getEmailProperty(){
  const userProperties = PropertiesService.getUserProperties();
  return { email: userProperties.getProperty('email_to_passwd') };
}

function setUserSessionIdProperties(sessionId, email, nome, tipo_usuario){
  const propriedades = PropertiesService.getUserProperties();
  if (sessionId == null || sessionId == undefined || (String(sessionId).trim() == ""))
  {
    sessionId = Utilities.getUuid();
  }
  propriedades.setProperty("sessionId", sessionId);
  propriedades.setProperty("email", email);
  propriedades.setProperty("nome", nome);
  propriedades.setProperty("url", ScriptApp.getService().getUrl());
  const now = new Date().getTime();
  propriedades.setProperty("sessionStart", String(now));
  propriedades.setProperty("tipo_usuario", tipo_usuario);
  // Limpa o patriarca selecionado ao iniciar uma nova sessão
  propriedades.deleteProperty("selectedPatriarca");
  return {sessionId: sessionId, email: email, nome: nome, url: ScriptApp.getService().getUrl(), sessionStart: now, tipo_usuario: tipo_usuario};
}

function getSelectedPatriarca() {
  const userProperties = PropertiesService.getUserProperties();
  const selectedPatriarcaJson = userProperties.getProperty("selectedPatriarca");
  if (selectedPatriarcaJson) {
    return JSON.parse(selectedPatriarcaJson);
  }
  return null;
}

function setSelectedPatriarca(patriarcaId, noValidationMode) {
  try {

    var validateStatus = true;

    if((noValidationMode === null) || (noValidationMode === undefined)){
      validateStatus = true;
    }else{
      validateStatus = !noValidationMode;
    }

    const nomeAba = CONFIG.SHEET_LISTAS;
    const tabelaPatriarca = CONFIG.TAB_PATRIARCA;

    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) {
      return { success: false, message: `Erro ao abrir a planilha: ${CONFIG.SPREADSHEET_PARAM}` };
    }

    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId);
    const sheet = spreadsheet.getSheetByName(nomeAba);
    if (!sheet) {
      return { success: false, message: `Aba '${nomeAba}' não encontrada na planilha.` };
    }

    const data = sheet.getRange(tabelaPatriarca).getValues();
    let foundPatriarca = null;
    for (let i = 1; i < data.length; i++) { // Começa de 1 para pular o cabeçalho
      const [rowNome, rowSigla, rowId, rowStatus, rowOrg_gerado, rowLot_Gerado, rowToken, rowDataSolicitacao] = data[i];
      if (rowId.toString() === patriarcaId.toString()) {
        foundPatriarca = { 
          nome: rowNome, 
          sigla: rowSigla, 
          idpatriarca: rowId, 
          status: rowStatus, 
          organogramagerado: rowOrg_gerado, 
          lotacaogerado: rowLot_Gerado, 
          token: rowToken, 
          datasolicitacao: rowDataSolicitacao
        };
        break;
      }
    }

    if (!foundPatriarca) {
      return { success: false, message: `Patriarca com ID ${patriarcaData.idpatriarca} não encontrado.` };
    }

    if (validateStatus){
      if (foundPatriarca.status.toLowerCase() !== 'em progresso' && foundPatriarca.status.toLowerCase() !== 'novo' && foundPatriarca.status.toLowerCase() !== 'Enviando carga') {
        var msg = `Patriarca '${foundPatriarca.nome}' não pode ser selecionado! Status atual: ${foundPatriarca.status}.`;
        return { success: false, message: msg };
      }  
    }

    const userProperties = PropertiesService.getUserProperties();
    userProperties.setProperty("selectedPatriarca", JSON.stringify(foundPatriarca));
    return { success: true, message: `Patriarca '${foundPatriarca.nome}' selecionado com sucesso.`, patriarca: foundPatriarca };
  } catch (e) {
    Logger.log("Erro em setSelectedPatriarca: " + e.message);
    return { success: false, message: `Erro ao selecionar patriarca: ${e.message}` };
  }
}

/**
 * Seleciona um patriarca e reinicia seu status, se necessário.
 * - Se o status for 'enviando carga' e a solicitação tiver menos de 1 hora,
 *   apenas seleciona o patriarca sem alterar seus dados.
 * - Se o prazo de 1 hora tiver expirado ou o status for 'novo'/'em progresso',
 *   reinicia o status para 'em progresso', limpa o token e atualiza a data.
 *
 * @param {string|number} patriarcaId O ID do patriarca a ser processado.
 * @returns {{success: boolean, message: string, patriarca?: object}} Um objeto indicando o sucesso ou falha da operação.
 */
function resetPatriarca(patriarcaId) {
  try {
    const nomeAba = CONFIG.SHEET_LISTAS;
    const tabelaPatriarca = CONFIG.TAB_PATRIARCA;

    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) {
      return { success: false, message: `Erro ao abrir a planilha: ${CONFIG.SPREADSHEET_PARAM}` };
    }

    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId);
    const sheet = spreadsheet.getSheetByName(nomeAba);
    if (!sheet) {
      return { success: false, message: `Aba '${nomeAba}' não encontrada na planilha.` };
    }

    const range = sheet.getRange(tabelaPatriarca);
    const data = range.getValues();
    const startRow = range.getRow();

    let patriarcaData = null;
    let rowIndexInSheet = -1;
    let shouldUpdateSheet = true; // Flag para controlar a atualização da planilha

    for (let i = 1; i < data.length; i++) {
      const [rowNome, rowSigla, rowId, rowStatus, rowOrg_gerado, rowLot_Gerado, rowToken, rowDataSolicitacao] = data[i];

      if (rowId.toString() === patriarcaId.toString()) {
        const currentStatus = rowStatus.toString().toLowerCase();
        rowIndexInSheet = startRow + i;

        // NOVO: Lógica para status 'enviando carga'
        if (currentStatus === 'enviando carga') {
          if (rowDataSolicitacao && rowDataSolicitacao instanceof Date) {
            const dataSolicitacao = new Date(rowDataSolicitacao);
            const agora = new Date();
            const diffMs = agora.getTime() - dataSolicitacao.getTime(); // Diferença em milissegundos [1][6]
            const diffHoras = diffMs / (1000 * 60 * 60); // Converte para horas

            if (diffHoras <= 1) {
              // DENTRO DO PRAZO: Mantém os dados e apenas seleciona
              patriarcaData = {
                nome: rowNome, sigla: rowSigla, idpatriarca: rowId, status: rowStatus,
                organogramagerado: rowOrg_gerado, lotacaogerado: rowLot_Gerado,
                token: rowToken, datasolicitacao: rowDataSolicitacao
              };
              shouldUpdateSheet = false; // Não atualiza a planilha
              break; 
            }
          }
          // Se não houver data ou o prazo expirou, a função continuará para o reset.
        }
        
        // NOVO: Lógica para status 'carga processada'
        if (currentStatus === 'carga processada') {
          if (rowDataSolicitacao && rowDataSolicitacao instanceof Date) {
            const dataSolicitacao = new Date(rowDataSolicitacao);
            const agora = new Date();
            const diffMs = agora.getTime() - dataSolicitacao.getTime(); // Diferença em milissegundos [1][6]
            const diffHoras = diffMs / (1000 * 60 * 60); // Converte para horas

            if (diffHoras > 1) {
              // FORA DO PRAZO: 
              patriarcaData = {
                nome: rowNome, sigla: rowSigla, idpatriarca: rowId, status: 'Em progresso',
                organogramagerado: rowOrg_gerado, lotacaogerado: rowLot_Gerado,
                token: '', datasolicitacao: ''
              };
              shouldUpdateSheet = true; // atualiza a planilha
              break; 
            }
          }
          // Se não houver data ou o prazo expirou, a função continuará para o reset.
        } else {
          // Lógica de reset (original, com ajustes)
          const validStatusForReset = ['novo', 'em progresso', 'enviando carga'];
          if (!validStatusForReset.includes(currentStatus)) {
            return { success: false, message: `Patriarca '${rowNome}' não pode ser reiniciado! Status atual: ${rowStatus}.` };
          }

          patriarcaData = {
            nome: rowNome, sigla: rowSigla, idpatriarca: rowId, status: 'Em progresso',
            organogramagerado: rowOrg_gerado, lotacaogerado: rowLot_Gerado, token: '',
            datasolicitacao: null
          };
          break;
        }
      }
    }

    if (!patriarcaData) {
      return { success: false, message: `Patriarca com ID ${patriarcaId} não encontrado.` };
    }

    // Só atualiza a planilha se a flag for verdadeira
    if (shouldUpdateSheet) {
      const valuesToSet = [[
        patriarcaData.nome, patriarcaData.sigla, patriarcaData.idpatriarca, 'Em progresso',
        patriarcaData.organogramagerado, patriarcaData.lotacaogerado,
        '', ''
      ]];
      const startCol = convertLetterToColumn(CONFIG.COL_NOME_PATRIARCA);
      sheet.getRange(rowIndexInSheet, startCol, 1, valuesToSet[0].length).setValues(valuesToSet);
    }

    //const userProperties = PropertiesService.getUserProperties();
    //userProperties.setProperty("selectedPatriarca", JSON.stringify(patriarcaData));
    setSelectedPatriarca(patriarcaData.idpatriarca, false);

    const message = shouldUpdateSheet
      ? `Patriarca '${patriarcaData.nome}' foi reiniciado e selecionado com sucesso.`
      : `Patriarca '${patriarcaData.nome}' já estava em envio e foi selecionado (dentro do prazo de 1h).`;

    return { success: true, message: message, patriarca: patriarcaData };

  } catch (e) {
    Logger.log(`Erro em resetPatriarca: ${e.message} Stack: ${e.stack}`);
    return { success: false, message: `Erro ao processar patriarca: ${e.message}` };
  }
}

function clearSelectedPatriarca() {
  const userProperties = PropertiesService.getUserProperties();
  userProperties.deleteProperty("selectedPatriarca");
  return { success: true, message: "Patriarca selecionado limpo." };
}

function getUserProperties() {
  const userProperties = PropertiesService.getUserProperties();
  var tipo_usuario = userProperties.getProperty('tipo_usuario');
  return {
    sessionId: userProperties.getProperty('sessionId'),
    email: userProperties.getProperty('email'),
    nome: userProperties.getProperty('nome'),
    url: userProperties.getProperty('url'),
    sessionStart: userProperties.getProperty('sessionStart'),
    tipo_usuario: userProperties.getProperty('tipo_usuario')
  };
}

function removeAllSiteProperties(){  
  const scriptProperties = PropertiesService.getScriptProperties();
  scriptProperties.deleteAllProperties();

  return { success: true };
}

function removeAllUserProperties(){
  PropertiesService.getUserProperties().deleteAllProperties();
  return { success: true };
}

// ===== Controle de timeout do site =======

const SESSION_TIMEOUT = 60 * 60 * 1000; // 60 minutos

function validateTimeOutUserSession(){
  try {
    const user = getUserProperties();    
    const now = new Date().getTime();
    const elapsed = now - parseInt(user.sessionStart, 10);

    Logger.log("now: " + now);
    Logger.log("user.sessionStart: " + user.sessionStart);
    Logger.log("elapsed: " + elapsed.toString());
    Logger.log("SESSION_TIMEOUT: " + SESSION_TIMEOUT.toString());

    if (elapsed > SESSION_TIMEOUT) {
      return { sessionExpired: true };
    }
    return { sessionExpired: false };
  }
  catch(error){    
    return { sessionExpired: false };
  }
}

function doGet(e) {
  setSiteProperty();

  var page = e.parameter.page || CONFIG.LOGIN_PAGE;
  Logger.log("doGet(e) - page: " + page );

  const valid_pages = ['login', 'principal', 'patriarcas'];
  var htmlFile = valid_pages.includes(page) ? page : CONFIG.LOGIN_PAGE;
  Logger.log("doGet(e) - htmlFile: " + htmlFile);

  var retUserProps = getUserProperties();

  Logger.log("doGet(e) - retUserProps: " + JSON.stringify(retUserProps));


  if ((retUserProps.sessionId !== null) && (retUserProps.sessionStart !== null)){
    var retValidTimeOut = validateTimeOutUserSession();
    
    Logger.log("doGet(e) - retValidTimeOut: " + JSON.stringify(retValidTimeOut));
  
    if (retValidTimeOut.sessionExpired === true || retUserProps.sessionId.trim() === '') {
      page = 'login';
      htmlFile = 'login';
    }
    if (retValidTimeOut.sessionExpired === false && retUserProps.sessionId.trim() !== '') {
      page = 'principal';
      htmlFile = 'principal';
    }
  }else{
    page = 'login';
    htmlFile = 'login';
  }
  
  Logger.log("doGet(e) - page: " + page + ", htmlFile: " + htmlFile + ", getUrl(): " + ScriptApp.getService().getUrl());

  switch (page) {
    case 'login':
      return HtmlService.createHtmlOutputFromFile('login')
        .setTitle("Login");
        //.setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);

    case 'principal':
      return HtmlService.createHtmlOutputFromFile('principal')
        .setTitle("Painel");
        //.setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);

    default:
      return HtmlService.createHtmlOutputFromFile('login')
        .setTitle("Login");
        //.setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
  }
}

function verificarEAbrirPlanilha(nomeArquivo) {
  // Nome do arquivo da planilha que você deseja abrir
  //var nomeArquivo = "MinhaPlanilha";

  // Pesquisa no Google Drive por arquivos com o nome especificado e tipo de Google Sheets
  var arquivos = DriveApp.getFilesByName(nomeArquivo);

  // Verifica se encontrou pelo menos um arquivo
  if (arquivos.hasNext()) {
    var arquivo = arquivos.next(); // Pega o primeiro arquivo encontrado

    // Obtém o ID do arquivo
    var fileId = arquivo.getId();

    return { success: true, fileId: fileId };
    // Abre a planilha pelo ID
    //var planilha = SpreadsheetApp.openById(fileId);

    // Exibe o nome da planilha no Log
    //Logger.log("Planilha aberta: " + planilha.getName());

  } else {
    Logger.log("Nenhum arquivo encontrado com o nome: " + nomeArquivo);
    return { success: false, fileId: null };
  }
}

function authenticateUser(email, password) {
  try {    
    var retorno = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);

    if(retorno.success){
      const spreadsheet = SpreadsheetApp.openById(retorno.fileId); 
      const sheet = spreadsheet.getSheetByName(CONFIG.SHEET_LISTAS); 
      if (!sheet) throw new Error("Aba 'Listas' não encontrada.");
      Logger.log(sheet.getName());

      const data = sheet.getRange(CONFIG.TAB_USUARIOS).getValues();
      for (let i = 1; i < data.length; i++) {
        const [rowEmail, rowNome, rowSenha, rowStatus, tipo_usuario] = data[i];
        if (rowEmail && rowEmail.toLowerCase() === email.toLowerCase() && rowSenha.toString() === password) {
          if (rowStatus && rowStatus.toLowerCase() === 'ativo'){
            let retorno = setUserSessionIdProperties("", rowEmail, rowNome, tipo_usuario);
            return { success: true, sessionId: retorno.sessionId };
          } else {
            return { success: false, message: 'O usuário (' + rowNome + ') está inativo.\nSolicite a ativação para poder continuar!' };
          }
        }
      }
    }
    else{
      return { success: false, message: 'não foi possível encontrar o arquivo ' + nomeSheetLogin };
    }

    return { success: false, message: 'Email ou senha inválidos.' };
  } catch (error) {
    throw new Error("Erro ao autenticar: " + error.message);
  }
}

/**
 * Retorna um fragmento HTML para ser injetado na #content do principal.html
 * - nome deve ser 'patriarcas', 'organograma', 'lotacao'
 */
function getHtmlPage(nome) {
  Logger.log('getHtmlPage: ' + nome);
  var fileName = '';
  switch (nome) {
    case 'patriarcas':
      fileName = 'patriarcas';
      break;
    case 'organograma':
      fileName = 'organograma';
      break;
    case 'organogramaEdicao':
      fileName = 'organograma_edicao'; // NOVA TELA
      break;
    case 'lotacao':
      fileName = 'lotacao';
      break;
    case 'enviarParaAPI':
      fileName = 'enviarParaAPI';
      break;
    case 'validarEnvioParaAPI':
      fileName = 'validarEnvioParaAPI';
    case 'selecionarOrgaosLotacao':
      fileName = 'selecionarOrgaosLotacao';
      break;
    case 'login':
      fileName = 'login';
      break;
    default:
      fileName = 'patriarcas';
  }
  return HtmlService.createTemplateFromFile(fileName).evaluate().getContent();
}

function findSpreadsheetData(nomePlanilha, nomeAba, nomeTabela, valorProcurado){

  var retLerArq = verificarEAbrirPlanilha(nomePlanilha);
  
  var success = false;
  var msg = '';
  var data = [];
  var dados = {};

  if (retLerArq.success){
    
    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId); 
    const sheet = spreadsheet.getSheetByName(nomeAba); 
    if (!sheet){
      msg = 'A aba ' + nomeAba + ' não foi encontrada!';
    }
    if (nomeTabela.trim() !== ''){
      data = sheet.getRange(nomeTabela).getValues();
    }else{
      
      data = sheet.getDataRange().getValues();
    }

    const rowIndex = data.findIndex(row => 
                                      row.some(cell => 
                                          String(cell).trim().toUpperCase().includes(String(valorProcurado).trim().toUpperCase())
                                      )
                                    );

    if (rowIndex !== -1) {
      //Logger.log(`findSpreadsheetData - Encontrado na linha ${rowIndex + 1}`);
      //Logger.log(`findSpreadsheetData - Dados:`, data[rowIndex]);

      const linha = data[rowIndex];

      // Cria objeto dinâmico
      for (let c = 0; c < linha.length; c++) {
        if (linha[c] !== "" && linha[c] !== null) {  
          dados["coluna" + (c + 1)] = linha[c]; // chave = "coluna1", "coluna2"...
        }
      }

      // Adiciona número real da linha na planilha
      dados.numeroLinha = rowIndex + 1;
      //Logger.log(dados);
      success = true;

    } else {
      msg = 'O valor: ' + valorProcurado + ' não foi encontrado!';
      Logger.log(msg);
    }
  }
  else{
    msg = 'Erro ao abrir o arquivo ' + nomePlanilha;
  }

  var retorno = {success: success, message: msg, dados: dados };

  return retorno;
}


/**
 * Lista todos os patriarcas, verifica se possuem
 * histórico de envio e valida a expiração do token para os que estão prontos
 * para o envio de lotações.
 *
 * @returns {{success: boolean, message: string, dados: Array<object>}}
 */
function listarPatriarcas() {
  try {
    
    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);

    if (!retLerArq.success) throw new Error(`Erro ao abrir o arquivo: ${CONFIG.SPREADSHEET_PARAM}.`);

    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId);

    const sheetListas = spreadsheet.getSheetByName(CONFIG.SHEET_LISTAS);
    const sheetStatus = spreadsheet.getSheetByName(CONFIG.SHEET_STATUS_ENVIO);

    if (!sheetListas || !sheetStatus) {
      throw new Error("Abas 'Listas' ou 'Status_Envio' não encontradas.");
    }

    // Otimização: Lê todos os IDs da aba de status uma única vez
    const statusValues = sheetStatus.getRange("A2:A" + sheetStatus.getLastRow()).getValues();
    const idsComHistorico = new Set(statusValues.flat().filter(id => id));

    const rangePatriarcas = sheetListas.getRange(CONFIG.TAB_PATRIARCA);
    const valuesPatriarcas = rangePatriarcas.offset(1, 0, rangePatriarcas.getNumRows() - 1).getValues();

    const dados = valuesPatriarcas.map(row => {
      const [nome, sigla, id, status, orgGerado, lotGerado, token, dataSolicitacao] = row;
      
      let tokenValido = false; // Valor padrão
      
      // >>> VALIDAÇÃO DE TOKEN REINTEGRADA <<<
      // Se o patriarca está pronto para o próximo passo (enviar lotações), valida o token.
      if (status && status.trim() === 'Carga processada') {
       
        const patriarcaParaValidar = {
          nome: nome,
          sigla: sigla,
          idpatriarca: id, 
          status: status,
          organogramaGerado: orgGerado,
          lotacaoGerado: lotGerado,
          token: token,
          dataSolicitacao: dataSolicitacao
        };
        const validacao = validarTokenParaEnvio(patriarcaParaValidar);
        tokenValido = validacao.tokenValido;
      }

      return {
        nome: nome,
        sigla: sigla,
        idPatriarca: id,
        status: status,
        organogramaGerado: orgGerado,
        lotacaoGerado: lotGerado,
        token: token,
        dataSolicitacao: dataSolicitacao instanceof Date ? dataSolicitacao.toISOString() : dataSolicitacao,
        temHistoricoDeEnvio: idsComHistorico.has(id), // << NOVA FLAG: Verificação de histórico
        tokenValido: tokenValido // << NOVA FLAG: Verificação de token
      };
    }).filter(p => p.nome || p.sigla);

    return { success: true, message: 'Patriarcas carregados com sucesso.', dados: dados };

  } catch (error) {
    Logger.log(`ERRO CRÍTICO em listarPatriarcas: ${error.message}`);
    return { success: false, message: error.message, dados: [] };
  }
}

function getPatriarca(idPatriarca) {
  try {
    if (!idPatriarca) {
      throw new Error("ID do Patriarca não foi fornecido para a busca.");
    }

    const sheet = SpreadsheetApp.openById(verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM).fileId).getSheetByName(CONFIG.SHEET_LISTAS);
    const range = sheet.getRange(CONFIG.TAB_PATRIARCA); // Ex: 'G1:N90'
    const values = range.getValues();

    // Mapeamento fixo de índices baseado no intervalo G:N
    const COLS = {
      NOME: 0, SIGLA: 1, ID_PATRIARCA: 2, STATUS: 3,
      ORGANOGRAMA_GERADO: 4, LOTACAO_GERADO: 5, TOKEN: 6, DATA_SOLICITACAO: 7
    };

    for (let i = 1; i < values.length; i++) {
      const row = values[i];
      if (row[COLS.ID_PATRIARCA] && row[COLS.ID_PATRIARCA].toString() === idPatriarca.toString()) {
        
        // Monta o objeto com a propriedade 'idpatriarca' em minúsculo
        const patriarcaData = {
          nome: row[COLS.NOME],
          sigla: row[COLS.SIGLA],
          idpatriarca: row[COLS.ID_PATRIARCA], // <<< CORREÇÃO APLICADA AQUI
          status: row[COLS.STATUS],
          organogramaGerado: row[COLS.ORGANOGRAMA_GERADO],
          lotacaoGerado: row[COLS.LOTACAO_GERADO],
          token: row[COLS.TOKEN],
          dataSolicitacao: row[COLS.DATA_SOLICITACAO]
        };

        return { success: true, message: 'Patriarca encontrado.', dados: patriarcaData };
      }
    }
    
    throw new Error(`Patriarca com ID ${idPatriarca} não encontrado.`);

  } catch (e) {
    Logger.log(`Erro em getPatriarca: ${e.message}`);
    return { success: false, message: e.message, dados: null };
  }
}

/**
 * Login já existente – apenas garante que retorna o principal renderizado
 */
function loginAndRenderPrincipal(email, password) {
  var auth = authenticateUser(email, password); // mantém sua função existente
  if (!auth.success) return { success: false, message: auth.message };

  var template = HtmlService.createTemplateFromFile("principal");
  template.initialPage = 'patriarcas'; // define página inicial
  template.webAppUrl = ScriptApp.getService().getUrl();
  
  return {
    success: true,
    html: template.evaluate().getContent()
  };
}

function logout() {
  var retSite = removeAllSiteProperties();
  var retUser = removeAllUserProperties();

  if (retSite.success && retUser.success) {
    var template = HtmlService.createTemplateFromFile("login");
    template.webAppUrl = ScriptApp.getService().getUrl();
    return template.evaluate().getContent();
  }
}

function testeIncluirNovoPatriarca(){

  const sigla = 'PMBGD';
  const nome = 'PREFEITURA MUNICIPAL DE BAIXO GUANDU';
  const id = '0bcb8c7d-56cf-438b-8242-d79f61ecbaaa';
  const estado = 'Novo';

  const patriarcaData = {
    sigla: sigla,
    nome: nome,
    idPatriarca: id,
    status: estado
  };

  varRetIncluir = incluirNovoPatriarca(patriarcaData);

  Logger.log('Retorno da inclusão: ' + JSON.stringify(varRetIncluir));

}

/**
 * Inclui um novo patriarca na planilha de forma segura.
 * Esta versão foi corrigida para lidar com inconsistências de nome de propriedade
 * e utiliza appendRow para garantir a inserção dos dados.
 *
 * @param {object} patriarcaData Objeto contendo dados do patriarca.
 * @return {object} Objeto com status de sucesso e mensagem.
 */
function incluirNovoPatriarca(patriarcaData) {
  try {
    const nomeAba = CONFIG.SHEET_LISTAS;
    const tabelaPatriarca = CONFIG.TAB_PATRIARCA;

    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) {
      return { success: false, message: `Erro ao abrir a planilha: ${CONFIG.SPREADSHEET_PARAM}` };
    }

    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId);
    const sheet = spreadsheet.getSheetByName(nomeAba);
    if (!sheet) {
      return { success: false, message: `Aba '${nomeAba}' não encontrada na planilha.` };
    }

    // --- CORREÇÃO 1: Normaliza o ID para evitar erros de case-sensitive ---
    const idPatriarcaNormalizado = patriarcaData.idPatriarca || patriarcaData.idpatriarca;
    if (!idPatriarcaNormalizado) {
        return { success: false, message: 'O ID do Patriarca (idPatriarca) não foi fornecido.' };
    }

    // --- CORREÇÃO 2: Aprimora a validação de duplicidade ---
    const data = sheet.getRange(tabelaPatriarca).getValues();
    const siglaParaVerificar = patriarcaData.sigla.toLowerCase();

    for (let i = 1; i < data.length; i++) { // Começa de 1 para pular o cabeçalho
      const rowSigla = data[i][1]; // Coluna H: Sigla
      const rowId = data[i][2];    // Coluna I: ID do Patriarca

      if (rowSigla && rowSigla.toLowerCase() === siglaParaVerificar) {
        return { success: false, message: `A sigla '${patriarcaData.sigla}' já existe.` };
      }
      if (rowId && rowId.toString() === idPatriarcaNormalizado.toString()) {
        return { success: false, message: `O Id do Patriarca '${idPatriarcaNormalizado}' já existe.` };
      }
    }

    // --- CORREÇÃO 3: Usa appendRow para adicionar dados de forma segura ---
    const novaLinha = [
      patriarcaData.nome,           // Coluna G
      patriarcaData.sigla,          // Coluna H
      idPatriarcaNormalizado,       // Coluna I (Usa o ID normalizado)
      patriarcaData.status,         // Coluna J
      '',                           // Coluna K (Org_gerado)
      '',                           // Coluna L (Lot_Gerado)
      '',                           // Coluna M (Token)
      ''                            // Coluna N (DataSolicitacao)
    ];

    // Logging para depuração: mostra exatamente o que será gravado.
    Logger.log(`Incluindo novo patriarca: ${JSON.stringify(novaLinha)}`);
    
    // O appendRow adiciona os dados na primeira linha vazia da planilha.
    // Para garantir que os dados sejam inseridos na tabela correta,
    // é preciso criar um array com o número certo de colunas vazias no início.
    const colGIndex = 7; // 'G' é a 7ª coluna
    const linhaParaPlanilha = new Array(colGIndex - 1).fill('').concat(novaLinha);
    
    sheet.appendRow(linhaParaPlanilha);

    return { success: true, message: 'Patriarca incluído com sucesso!' };

  } catch (error) {
    Logger.log(`Erro em incluirNovoPatriarca: ${error.message} Stack: ${error.stack}`);
    return { success: false, message: `Erro ao incluir patriarca: ${error.message}` };
  }
}

function testeAtualizarPatriarca(){
    atualizarPatriarca('24663877-6b59-4ae4-8dcf-f0b4d9abebcc', {
      token: 'adsfasdfasdfasdfasdftoken',
      datasolicitacao: new Date(),
      status: 'Enviando Carga'
    });

}

/**
 * Atualiza campos específicos de um patriarca.
 * É compatível com chamadas antigas e novas, e remove tags [translate].
 *
 * @param {string} idPatriarca - O ID para localizar a linha.
 * @param {object|string} dadosParaAtualizar - Objeto com campos ou uma string para o status.
 * @returns {object} Resultado da operação.
 */
function atualizarPatriarca(idPatriarca, dadosParaAtualizar) {
  try {
    if (!idPatriarca) throw new Error("ID do Patriarca é nulo ou indefinido.");

    if (typeof dadosParaAtualizar === 'string') {
      dadosParaAtualizar = { status: dadosParaAtualizar };
    } else if (typeof dadosParaAtualizar !== 'object' || dadosParaAtualizar === null) {
      throw new Error("Dados para atualização são inválidos.");
    }

    const sheet = SpreadsheetApp.openById(verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM).fileId).getSheetByName(CONFIG.SHEET_LISTAS);
    const range = sheet.getRange(CONFIG.TAB_PATRIARCA);
    const values = range.getValues();
    const header = values[0];
    const startRow = range.getRow();

    const colMap = {};
    header.forEach((colName, index) => { if (colName) colMap[colName.toLowerCase()] = index; });
    const idColIndex = colMap['Código'.toLowerCase()];

    for (let i = 1; i < values.length; i++) {
      if (values[i][idColIndex] && values[i][idColIndex].toString() === idPatriarca.toString()) {
        const linhaParaAtualizar = startRow + i;
        
        for (const key in dadosParaAtualizar) {
          const lowerKey = key.toLowerCase();
          if (colMap.hasOwnProperty(lowerKey)) {
            const colIndex = colMap[lowerKey];
            let valor = dadosParaAtualizar[key];
            
            if (typeof valor === 'string') {
              valor = valor.replace(/\[translate:|\]/g, '').trim();
            }
            sheet.getRange(linhaParaAtualizar, range.getColumn() + colIndex).setValue(valor);
          }
        }
        
        Logger.log(`Patriarca ID ${idPatriarca} atualizado na linha ${linhaParaAtualizar}.`);
        return { success: true, message: 'Patriarca atualizado com sucesso.' };
      }
    }
    
    throw new Error(`Patriarca com ID ${idPatriarca} não encontrado.`);
  } catch (error) {
    Logger.log(`ERRO CRÍTICO em atualizarPatriarca: ${error.message}`);
    return { success: false, message: error.message };
  }
}

/**
 * Procura um arquivo JSON pelo nome em uma pasta específica do Google Drive.
 * @param {string} folderName O nome da pasta onde procurar.
 * @param {string} fileName O nome do arquivo a ser encontrado.
 * @returns {object|null} O conteúdo do arquivo JSON parseado ou null se não for encontrado.
 */
function findJsonFileContentByName(folderName, fileName) {
  try {
    const folders = DriveApp.getFoldersByName(folderName);
    if (!folders.hasNext()) {
      Logger.log(`Pasta "${folderName}" não encontrada.`);
      return null;
    }
    const folder = folders.next();
    const files = folder.getFilesByName(fileName);
    if (files.hasNext()) {
      const file = files.next();
      const content = file.getBlob().getDataAsString();
      Logger.log(`Arquivo JSON "${fileName}" encontrado e lido com sucesso.`);
      return JSON.parse(content);
    }
    Logger.log(`Arquivo "${fileName}" não encontrado na pasta "${folderName}".`);
    return null;
  } catch (e) {
    Logger.log(`Erro em findJsonFileContentByName: ${e.message}`);
    return null;
  }
}

function getOrganogramaJsonParaEdicao(userChoice = null) {
  try {
    const patriarca = getSelectedPatriarca();
    if (!patriarca) throw new Error("Nenhum Patriarca selecionado para edição.");

    // 1. SEMPRE comparar dados do arquivo com planilha
    const reactFlowFileName = `cargadeorgaos_${patriarca.sigla}_reactflow.json`;
    const reactFlowContent = findJsonFileContentByName("Carga - Para Envio", reactFlowFileName);
    
    // 2. Obter dados da planilha
    const nomeAba = patriarca.sigla + '_O';
    const spreadsheet = SpreadsheetApp.openById(verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM).fileId);
    const sheet = spreadsheet.getSheetByName(nomeAba);
    
    let planilhaData = [];
    if (sheet && sheet.getLastRow() > 1) {
      const data = sheet.getDataRange().getValues();
      planilhaData = data.slice(1).map(([nome, sigla, paiSigla, numero]) => ({
        nome, sigla, paiSigla, numero: numero || ''
      }));
    }

    // 3. Se há arquivo JSON, comparar com planilha
    if (reactFlowContent && userChoice === null) {
      const diferencas = compararDadosJsonPlanilha(reactFlowContent, planilhaData);
      
      if (diferencas.length > 0) {
        return {
          success: false,
          requiresUserChoice: true,
          message: "Detectadas diferenças entre arquivo JSON e planilha",
          data: {
            diferencas: diferencas,
            jsonData: reactFlowContent,
            planilhaData: planilhaData
          }
        };
      }
    }

    // 4. Processar escolha do usuário
    if (userChoice === 'json' && reactFlowContent) {
      Logger.log(`Usuário escolheu manter dados do JSON para '${patriarca.sigla}'.`);
      return { 
        success: true, 
        data: adicionarNumerosPlanilhaAoJson(reactFlowContent, planilhaData)
      };
    }
    
    if (userChoice === 'planilha' || !reactFlowContent) {
      Logger.log(`Construindo layout da planilha para '${patriarca.sigla}'.`);
      return construirLayoutDaPlanilha(patriarca, planilhaData);
    }

    // 5. Se não há diferenças, continuar normalmente
    if (reactFlowContent) {
      return { 
        success: true, 
        data: adicionarNumerosPlanilhaAoJson(reactFlowContent, planilhaData)
      };
    }

    // 6. Construir novo layout se não há arquivo
    return construirLayoutDaPlanilha(patriarca, planilhaData);

  } catch (e) {
    Logger.log(`Erro em getOrganogramaJsonParaEdicao: ${e.message} ${e.stack}`);
    return { success: false, message: `Erro ao buscar organograma para edição: ${e.message}` };
  }
}

/**
 * Compara os dados de um arquivo JSON do ReactFlow com os dados de uma planilha.
 * A comparação é feita por sigla, nome e número.
 * @param {object} jsonData - O conteúdo do arquivo JSON (com {nodes, edges}).
 * @param {Array<object>} planilhaData - Um array de objetos da planilha, cada um com {sigla, nome, numero}.
 * @returns {Array<object>} Um array de objetos, onde cada objeto descreve uma diferença encontrada.
 */
function compararDadosJsonPlanilha(jsonData, planilhaData) {
  const diferencas = [];

  // 1. Converte os dados para mapas para uma busca mais eficiente, usando a sigla como chave.
  const jsonMap = new Map();
  if (jsonData && jsonData.nodes) {
    jsonData.nodes.forEach(node => {
      jsonMap.set(node.data.sigla, {
        nome: node.data.nome || '',
        numero: node.data.numero || ''
      });
    });
  }

  const planilhaMap = new Map();
  if (planilhaData) {
    planilhaData.forEach(item => {
      planilhaMap.set(item.sigla, {
        nome: item.nome || '',
        numero: item.numero || ''
      });
    });
  }

  // 2. Compara a quantidade total de itens
  if (jsonMap.size !== planilhaMap.size) {
    diferencas.push({
      tipo: 'Quantidade',
      detalhe: `O arquivo salvo contém ${jsonMap.size} itens, enquanto a planilha contém ${planilhaMap.size} itens.`
    });
  }

  // 3. Verifica cada item da planilha contra os itens do arquivo JSON
  for (const [sigla, planilhaItem] of planilhaMap.entries()) {
    const jsonItem = jsonMap.get(sigla);

    if (!jsonItem) {
      diferencas.push({
        tipo: 'Item Ausente no Arquivo Salvo',
        detalhe: `A sigla '${sigla}' (Nome: ${planilhaItem.nome}) existe na planilha, mas não foi encontrada no arquivo salvo.`
      });
    } else {
      // Compara o campo 'nome'
      if (jsonItem.nome.trim() !== planilhaItem.nome.trim()) {
        diferencas.push({
          tipo: 'Nome Divergente',
          detalhe: `Para a sigla '${sigla}', o nome no arquivo é "${jsonItem.nome}" e na planilha é "${planilhaItem.nome}".`
        });
      }
      // Compara o campo 'numero'
      if (String(jsonItem.numero).trim() !== String(planilhaItem.numero).trim()) {
         diferencas.push({
          tipo: 'Número Divergente',
          detalhe: `Para a sigla '${sigla}', o número no arquivo é "${jsonItem.numero}" e na planilha é "${planilhaItem.numero}".`
        });
      }
    }
  }

  // 4. Verifica se há itens no arquivo JSON que não existem mais na planilha
  for (const [sigla, jsonItem] of jsonMap.entries()) {
    if (!planilhaMap.has(sigla)) {
      diferencas.push({
        tipo: 'Item Ausente na Planilha',
        detalhe: `A sigla '${sigla}' (Nome: ${jsonItem.nome}) existe no arquivo salvo, mas não foi encontrada na planilha.`
      });
    }
  }

  return diferencas;
}


// Função auxiliar para adicionar números da planilha ao JSON
function adicionarNumerosPlanilhaAoJson(jsonData, planilhaData) {
  const numeroMap = new Map();
  planilhaData.forEach(item => {
    numeroMap.set(item.sigla, item.numero);
  });
  
  const nodesComNumero = jsonData.nodes.map(node => ({
    ...node,
    data: {
      ...node.data,
      numero: numeroMap.get(node.data.sigla) || ''
    }
  }));
  
  return {
    ...jsonData,
    nodes: nodesComNumero
  };
}

// Função auxiliar para construir layout da planilha (mantém código existente)
function construirLayoutDaPlanilha(patriarca, planilhaData) {
  // Se não há dados da planilha, retorna layout com apenas o patriarca
  if (planilhaData.length === 0) {
    
    Logger.log(`planilhaData.length == 0 para '${patriarca.sigla}'. Retornando estrutura para criar novo Organograma!`);
    return {
      success: true,
      data: {
        nodes: [{
          id: "root",
          type: "input",
          data: { 
            label: `${patriarca.sigla} - ${patriarca.nome}`,
            nome: patriarca.nome,
            sigla: patriarca.sigla,
            numero: ''
          },
          position: { x: 400, y: 50 },
          className: 'xy-theme__node'
        }],
        edges: []
      }
    };
  }

  // *** TODO O CÓDIGO EXISTENTE DA FUNÇÃO ORIGINAL AQUI ***
  // Com a modificação importante de incluir o campo numero em todos os nós criados
  
  // Exemplo de como modificar a criação dos nós:
  const nodes = [];
  const edges = [];
  
  // Criar mapa dos dados
  const treeMap = new Map();
  const rootNodes = [];
  
  // Primeira passada: criar nós
  planilhaData.forEach(item => {
    const { nome, sigla, paiSigla, numero } = item;
    treeMap.set(sigla, {
      nome,
      sigla,
      paiSigla,
      numero: numero || '',
      children: [],
      x: 0,
      y: 0,
      width: 0
    });
  });
  
  // Segunda passada: estabelecer hierarquia
  planilhaData.forEach(item => {
    const { sigla, paiSigla } = item;
    const node = treeMap.get(sigla);
    if (paiSigla && treeMap.has(paiSigla)) {
      treeMap.get(paiSigla).children.push(node);
    } else {
      rootNodes.push(node);
    }
  });

  // Na conversão final para ReactFlow, sempre incluir o numero:
  function convertTreeToReactFlow(treeNode, isRoot = false) {
    const node = {
      id: isRoot ? "root" : treeNode.sigla,
      type: isRoot ? "input" : "default",
      data: {
        label: `${treeNode.sigla} - ${treeNode.nome}`,
        nome: treeNode.nome,
        sigla: treeNode.sigla,
        numero: treeNode.numero || '' // *** CAMPO NUMERO ADICIONADO ***
      },
      position: { x: treeNode.x, y: treeNode.y },
      className: 'xy-theme__node'
    };
    
    nodes.push(node);
    
    treeNode.children.forEach(child => {
      edges.push({
        id: `e-${node.id}-${child.sigla}`,
        source: node.id,
        target: child.sigla,
        type: 'smoothstep'
      });
      convertTreeToReactFlow(child);
    });
  }

  // Localizar patriarca e processar
  const patriarcaNode = rootNodes.find(node => node.sigla === patriarca.sigla);
  if (!patriarcaNode) {
    throw new Error("Patriarca não encontrado como nó raiz na planilha.");
  }

  // Definir os espaçamentos corretos (da sua versão antiga)
  const x_spacing = 300;
  const y_spacing = 180;
  
  // 1ª Passada (Bottom-up): Calcula a largura de cada sub-árvore
  function calculateWidth(node) {
    if (node.children.length === 0) {
      node.width = x_spacing; // Nós folha têm largura padrão
      return;
    }
    let totalWidth = 0;
    node.children.forEach(child => {
      calculateWidth(child);
      totalWidth += child.width;
    });
    node.width = totalWidth;
  }

  // 2ª Passada (Top-down): Atribui as posições X e Y
  function assignPositions(node, level, startX) {
    // Posição do nó atual é centralizada em relação à largura de sua sub-árvore
    node.x = startX + (node.width / 2) - (x_spacing / 2);
    node.y = level * y_spacing;

    let currentX = startX;
    node.children.forEach(child => {
      assignPositions(child, level + 1, currentX);
      currentX += child.width;
    });
  }

  // *** EXECUTAR TODO O ALGORITMO DE LAYOUT EXISTENTE ***
  calculateWidth(patriarcaNode);
  assignPositions(patriarcaNode, 0, 0);
  convertTreeToReactFlow(patriarcaNode, true);

  return { success: true, data: { nodes, edges } };
}

// ====================================
// FUNÇÕES MISCELANIA
// ====================================

function convertColumnToLetter(column) {
  let letter = '';
  while (column > 0) {
    let temp = (column - 1) % 26;
    letter = String.fromCharCode(temp + 65) + letter;
    column = (column - temp - 1) / 26;
  }
  return letter;
}

function convertLetterToColumn(columnLetter) {
  let columnNumber = 0;
  // Convert the input to uppercase to handle both "a" and "A"
  columnLetter = columnLetter.toUpperCase(); 

  for (let i = 0; i < columnLetter.length; i++) {
    const char = columnLetter[i];
    // Get the character code and adjust for 'A' (A=1, B=2, etc.)
    const charValue = char.charCodeAt(0) - 'A'.charCodeAt(0) + 1; 
    
    // Multiply by 26 for each position to the left (like base-26)
    columnNumber = columnNumber * 26 + charValue; 
  }
  return columnNumber;
}

function getConfigValue(variavel){

  if (CONFIG.hasOwnProperty(variavel)) {
    return { success: true, configKey: variavel, value: CONFIG[variavel] };
  }
  else {
    console.warn(`Chave "${variavel}" não encontrada em CONFIG.`);
    return { success: false, configKey: variavel, value: null };
  }
}

function getConfigValueByKey(variableName, key) {
  if (CONFIG.hasOwnProperty(variableName)) {
    var obj = CONFIG[variableName];
    if (obj.hasOwnProperty(key)) {
      return { success: true, variable: variableName, key: key, value: obj[key] };
    } else {
      console.warn(`Chave "${key}" não encontrada em ${variableName}.`);
      return { success: false, variable: variableName, key: key, value: null };
    }
  } else {
    console.warn(`Variável "${variableName}" não encontrada em CONFIG.`);
    return { success: false, variable: variableName, key: key, value: null };
  }
}


function getMimeTypeValue(variavel){

  if (MimeType.hasOwnProperty(variavel)) {
    return { success: true, mimeTypeKey: variavel, value: MimeType[variavel] };
  }
  else {
    console.warn(`Chave "${variavel}" não encontrada em MimeType.`);
    return { success: false, mimeTypeKey: variavel, value: null };
  }
}


/**
 * Lê as abas de uma planilha e retorna os nomes das abas
 * @param {string} base64Content O conteúdo do arquivo em base64.
 * @param {string} fileName O nome do arquivo.
 * @param {string} fileMimeType O tipo MIME do arquivo.
 * @return {object} Um objeto com status de sucesso, mensagem e os nomes das abas.
 */
function readSpreadsheetTabs(base64Content, fileName, fileMimeType) {
  let fileId = null;
  
  try {
    const selectedPatriarca = getSelectedPatriarca();
    if (!selectedPatriarca) {
      return { success: false, message: 'Nenhum Patriarca selecionado. Por favor, selecione um Patriarca antes de processar o arquivo.', data: null };
    }

    const decodedBlob = Utilities.newBlob(
      Utilities.base64Decode(base64Content), 
      fileMimeType, 
      fileName
    );
    
    let tabNames = [];
    
    // Verificar se é um arquivo Excel ou ODS
    if (fileMimeType === MimeType.MICROSOFT_EXCEL || 
        fileMimeType === MimeType.MICROSOFT_EXCEL_LEGACY || 
        fileMimeType === MimeType.OPEN_DOCUMENT_SPREADSHEET) {
      
      // Converter para Google Sheets temporariamente para ler as abas
      const tempFile = DriveApp.createFile(decodedBlob);
      fileId = tempFile.getId();
      
      const convertedFile = Drive.Files.copy(
        { parents: [{ id: DriveApp.getRootFolder().getId() }] },
        fileId,
        { convert: true }
      );
      
      const spreadsheet = SpreadsheetApp.openById(convertedFile.id);
      const sheets = spreadsheet.getSheets();
      
      tabNames = sheets.map(sheet => sheet.getName());
      
      // Limpar arquivos temporários
      DriveApp.getFileById(fileId).setTrashed(true);
      DriveApp.getFileById(convertedFile.id).setTrashed(true);
      
    } else {
      return { success: false, message: 'Tipo de arquivo não suportado para leitura de abas. Use arquivos Excel (.xlsx, .xls) ou OpenDocument (.ods).', data: null };
    }
    
    return { success: true, message: `${tabNames.length} aba(s) encontrada(s) no arquivo.`, data: tabNames };

  } catch (error) {
    if (fileId) {
      DriveApp.getFileById(fileId).setTrashed(true);
    }
    Logger.log('Erro ao ler abas do arquivo: ' + error.message);
    return { success: false, message: 'Erro no servidor: ' + error.message, data: null };
  }
}

// Substitua a sua função checkDuplicateAcronyms por esta:
function checkDuplicateAcronyms(itemsArray) {
  const acronymsMap = new Map();
  const errors = [];

  // Mapeia os itens pela sigla
  itemsArray.forEach(item => {
    if (item.acronym && item.acronym.trim() !== '') {
      const lowerAcronym = item.acronym.toLowerCase();
      if (!acronymsMap.has(lowerAcronym)) {
        acronymsMap.set(lowerAcronym, []);
      }
      acronymsMap.get(lowerAcronym).push(item.text); // Armazena o nome do órgão para o relatório
    }
  });

  // Encontra siglas com mais de uma ocorrência
  acronymsMap.forEach((items, acronym) => {
    if (items.length > 1) {
      errors.push({
        value: acronym.toUpperCase(),
        type: 'acronym',
        message: `Sigla '${acronym.toUpperCase()}' duplicada nos órgãos: ${items.join(', ')}`
      });
    }
  });

  return errors; // Retorna diretamente o array de erros
}

// Substitua a sua função checkDuplicateTexts por esta:
function checkDuplicateTexts(itemsArray) {
  const textsMap = new Map();
  const errors = [];

  // Mapeia os itens pelo nome
  itemsArray.forEach(item => {
    if (item.text && item.text.trim() !== '') {
      const lowerText = item.text.toLowerCase();
      if (!textsMap.has(lowerText)) {
        textsMap.set(lowerText, []);
      }
      textsMap.get(lowerText).push(item.acronym); // Armazena a sigla para o relatório
    }
  });

  // Encontra nomes com mais de uma ocorrência
  textsMap.forEach((items, text) => {
    if (items.length > 1) {
      errors.push({
        value: text,
        type: 'text',
        message: `Nome '${text}' duplicado com as siglas: ${items.join(', ')}`
      });
    }
  });

  return errors; // Retorna diretamente o array de erros
}

/**
 * FUNÇÃO DE VALIDAÇÃO UNIFICADA E ROBUSTA
 * Valida a estrutura completa de um organograma, combinando todas as críticas das versões anteriores.
 * A função espera dados no formato de array 2D: [Nome, Sigla, Pai_Sigla, ...].
 *
 * @param {Array<Array<string>>} dados - Array 2D representando as linhas do organograma.
 * @returns {{success: boolean, errors: Array<string>}} Objeto com o resultado da validação e uma lista detalhada de erros.
 */
function validarEstruturaOrganograma(dados) {
  const erros = [];
  const mapaNomes = new Map();
  const mapaSiglas = new Map();
  const todasSiglas = new Set();

  // 1ª Passagem: Mapear todas as siglas existentes e validar a formatação inicial.
  dados.forEach((linha, index) => {
    const sigla = linha[1] ? String(linha[1]).trim() : '';
    if (sigla) {
      todasSiglas.add(sigla.toLowerCase());
    }
  });

  // 2ª Passagem: Realizar todas as validações linha a linha.
  dados.forEach((linha, index) => {
    const linhaNum = index + 2; // Assume que os dados começam na linha 2 da planilha.
    const nome = linha[0] ? String(linha[0]).trim() : '';
    const sigla = linha[1] ? String(linha[1]).trim() : '';
    const paiSigla = linha[2] ? String(linha[2]).trim() : '';

    // Validação 1: Campos essenciais em branco.
    if (!nome) {
      erros.push(`Linha ${linhaNum}: O campo 'Nome' está em branco.`);
    }
    if (!sigla) {
      erros.push(`Linha ${linhaNum}: O campo 'Sigla' está em branco.`);
    }

    // Validação 2: Sigla não pode conter espaços (crítica da função antiga).
    if (sigla && sigla.includes(' ')) {
      erros.push(`Linha ${linhaNum}: A sigla '${sigla}' não pode conter espaços. Utilize ponto, traço ou underline para unir os termos.`);
    }

    // Validação 3: Hierarquia circular (item não pode ser pai de si mesmo).
    if (sigla && paiSigla && sigla.toLowerCase() === paiSigla.toLowerCase()) {
      erros.push(`Linha ${linhaNum}: Hierarquia circular detectada. A unidade '${nome}' (${sigla}) não pode ser pai de si mesma.`);
    }

    // Validação 4: A 'Pai_Sigla', se preenchida, deve existir na lista de siglas.
    if (paiSigla && !todasSiglas.has(paiSigla.toLowerCase())) {
      erros.push(`Linha ${linhaNum}: A unidade '${nome}' (${sigla}) aponta para uma 'Pai_Sigla' ('${paiSigla}') que não existe no organograma.`);
    }

    // Coleta de dados para checagem de duplicidade.
    if (nome) {
      const nomeLower = nome.toLowerCase();
      if (!mapaNomes.has(nomeLower)) mapaNomes.set(nomeLower, []);
      mapaNomes.get(nomeLower).push(linhaNum);
    }
    if (sigla) {
      const siglaLower = sigla.toLowerCase();
      if (!mapaSiglas.has(siglaLower)) mapaSiglas.set(siglaLower, []);
      mapaSiglas.get(siglaLower).push(linhaNum);
    }
  });

  // Validação 5: Nomes duplicados.
  mapaNomes.forEach((ocorrencias, nome) => {
    if (ocorrencias.length > 1) {
      erros.push(`O nome '${nome.toUpperCase()}' está duplicado e aparece nas linhas: ${ocorrencias.join(', ')}.`);
    }
  });

  // Validação 6: Siglas duplicadas.
  mapaSiglas.forEach((ocorrencias, sigla) => {
    if (ocorrencias.length > 1) {
      erros.push(`A sigla '${sigla.toUpperCase()}' está duplicada e aparece nas linhas: ${ocorrencias.join(', ')}.`);
    }
  });

  // Retorno final. Remove erros duplicados antes de retornar.
  const uniqueErrors = [...new Set(erros)];
  if (uniqueErrors.length > 0) {
    return { success: false, errors: uniqueErrors };
  }

  return { success: true, errors: [] };
}

//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

function _testeProcessUploadedFileOrganograma(){

  var patriarcaData = {
    nome: 'PREFEITURA BAIXO GANDU',
    sigla: 'PMBG',
    idpatriarca: 'd8474987-c9e5-4f66-bfd9-6d04600c3abf',
    status: 'Em progresso',
    org_gerado: 'X',
    lot_gerado: 'X',
    token: '',
    datasolicitacao: ''
  };

  var retSetSelectedPatriarca = setSelectedPatriarca(patriarcaData.idpatriarca);
  
  var nomeArquivo = 'encodedBlob_' + patriarcaData.sigla + '.txt';
  
  const folders = DriveApp.getFoldersByName(CONFIG.FOLDER_CARGA_ENVIO);
  if (!folders.hasNext()) {
    return { success: false, message: `Pasta '${CONFIG.FOLDER_CARGA_ENVIO}' não encontrada` };
  }
  const folder = folders.next();
  var folderName = folder.getName();
  const files = folder.getFilesByName(nomeArquivo);
    
  if (!files.hasNext()) {
    return { success: false, message: `Arquivo '${nomeArquivo}' não encontrado` };
  } 
  
  const file = files.next();
  var fileName = file.getName();
  var fileId = file.getId();
  var fileDate = file.getLastUpdated();
  var fileURL = file.getUrl();
  const content = file.getBlob().getDataAsString();

  //var fileMimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
  //'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    // Divide o conteúdo por linha
  var linhas = content.split('\n');
  // Pega o mimetype da primeira linha
  var fileMimeType = linhas[0].trim();
  // Junta as demais linhas para formar o base64Content
  var base64Content = linhas.slice(1).join('\n').replace(/^\n/, '');

  var ret = processUploadedFileOrganograma(base64Content, nomeArquivo, fileMimeType);

  Logger.log('teste processUploadedFileOrganograma - retorno: ' + ret.success + ', codError: ' + ret.errorCode + ', Message:' + ret.message + ', data: ' + JSON.stringify(ret.data) );

}

function processUploadedFileOrganograma(base64Content, fileName, fileMimeType) {
  let convertedFile = null;

  try {
    const selectedPatriarca = getSelectedPatriarca();
    if (!selectedPatriarca) {
      return { success: false, errorCode: 100, message: 'Nenhum Patriarca selecionado.', data: null };
    }

    const decodedBlob = Utilities.newBlob(Utilities.base64Decode(base64Content), fileMimeType, fileName);

    var textFile = fileMimeType + '\n' + base64Content;
    saveTxtToFile(textFile, "Carga - Para Envio", 'encodedBlob_' + selectedPatriarca.sigla + '.txt');

    let hierarchicalData = [];
    let dados = [];
    let dadosPatriarca = { nomePatriarca: '', siglaPatriarca: '' };
    let processedData = [];
    let dadosParaValidacao = [];
    let validacao = [];
    let linhaVazia = 0;
    let tipoArquivo = '';
    let fileNameAlter = '';
    let bSemHierarquiaNoPatriarca = false;
  
    const folders = DriveApp.getFoldersByName(CONFIG.FOLDER_CARGA_ENVIO);
    if (!folders.hasNext()) {
      return { success: false, errorCode: -1010, message: `Pasta '${CONFIG.FOLDER_CARGA_ENVIO}' não encontrada`, errors: null };
    }
    const folder = folders.next();
    const folderId = folder.getId();

    if (fileMimeType === MimeType.MICROSOFT_EXCEL ||
        fileMimeType === MimeType.MICROSOFT_EXCEL_LEGACY ||
        fileMimeType === MimeType.GOOGLE_SPREADSHEET ||
        fileMimeType === MimeType.OPEN_DOCUMENT_SPREADSHEET) {

      fileNameAlter = fileName.replace(/\.\w+$/, '.gsheet');
      convertedFile = Drive.Files.insert(
        { title: fileNameAlter, 
          mimeType: MimeType.GOOGLE_SPREADSHEET,
          parents: [
            {
              id: folderId
            }
          ],
        },
        decodedBlob,
        {
          convert: true
        }
      );

      tipoArquivo = MimeType.GOOGLE_SPREADSHEET;
      const spreadsheet = SpreadsheetApp.openById(convertedFile.id);
      const sheet = spreadsheet.getSheets()[0];
      const range = sheet.getDataRange();
      processedData = range.getValues();

      // Normaliza o valor da hierarquia removendo ponto final ao final da string
      function normalizarHierarquia(hierarquia) {
        if (typeof hierarquia === 'string' && hierarquia.endsWith('.')) {
          return hierarquia.slice(0, -1);
        }
        return hierarquia;
      }

      for (let i = 0; i < processedData.length; i++) {
        // cabeçalho
        if (i == 0) continue;

        const [colItemRaw, colNomeOrgao, colSigla, colResposavel] = processedData[i];

        let colItem = normalizarHierarquia(colItemRaw);

        if ((!colItem || colItem === '') &&
            (!colNomeOrgao || colNomeOrgao === '') &&
            (!colSigla || colSigla === '')) {

          // 5 linhas vazias consecutivas
          if (linhaVazia > 5) break;
          linhaVazia += 1;
          continue;
        }

        if (selectedPatriarca.sigla === colSigla) {
          if(!colItemRaw || colItemRaw === '') {
            colItem = "0";
            bSemHierarquiaNoPatriarca = true;
          }
        } 

        dados.push({
          linhaPlanilha: i,
          hierarquiaOrgaoUnidade: colItem,
          nomeOrgaoUnidade: colNomeOrgao,
          siglaOrgaoUnidade: colSigla
        });
        
        linhaVazia = 0;
      }

      dados = organizarHierarquia(dados);

      if (bSemHierarquiaNoPatriarca){
        var retorno = reorganizarItemSemHierarquiaNoPatriarca(dados);
        if (retorno.success){
          dados = retorno.dados;
        }
        else {
          const errorMsg = 'Erro ao reorganizar a hierarquia do organograma! Verifique, altere e retorne para a leitura do organograma.';
          Logger.log(errorMsg);
          return { success: false, errorCode: -1150, message: errorMsg, errors: validacao };
        }
      }

      dados = associarSiglaPai(dados, dadosPatriarca.siglaPatriarca);

      if(dados[0].siglaOrgaoUnidade === selectedPatriarca.sigla ){
        dados[0].siglaPai = '';
      }
     
      validacao = validarTodosOsCriterios(dados);

      if (validacao.length > 0) {
        const errorMsg = 'O arquivo contém erros que impedem o processamento: ' + validacao.map(e => e.erro).join('; ');
        Logger.log(errorMsg);
        return { success: false, errorCode: 150, message: errorMsg, errors: validacao };
      }

      hierarchicalData = construirHierarchicalData(dados);

    } else if (fileMimeType === MimeType.MICROSOFT_WORD ||
               fileMimeType === MimeType.MICROSOFT_WORD_LEGACY ||
               fileMimeType === MimeType.GOOGLE_DOCUMENT ||
               fileMimeType === MimeType.OPEN_DOCUMENT_TEXT) {


      fileNameAlter = fileName.replace(/\.\w+$/, '.gdoc');
      convertedFile = Drive.Files.insert(
        { title: fileNameAlter, 
          mimeType: MimeType.GOOGLE_DOCUMENT,
          parents: [
            {
              id: folderId
            }
          ],
        },
        decodedBlob,
        {
          convert: true
        }
      );

      tipoArquivo = MimeType.GOOGLE_DOCUMENT;
      const doc = DocumentApp.openById(convertedFile.id);
      const body = doc.getBody();
      const parentStack = [];

      for (let i = 0; i < body.getNumChildren(); i++) {
        const element = body.getChild(i);
        if (element.getType() !== DocumentApp.ElementType.LIST_ITEM) continue;
        const listItem = element.asListItem();
        let text = listItem.getText().trim();
        if (!text) continue;
        let marker = null;
        const markerMatch = text.match(/^(\d+(\.\d+)*)\.?\s+/);
        if (markerMatch) {
          marker = markerMatch[1];
          text = text.substring(markerMatch[0].length).trim();
        }
        const nestingLevel = listItem.getNestingLevel();
        let cleanText = text;
        let acronym = null;
        const acronymMatch = text.match(/^(.*)\s+[-–]\s+(.*)$/);
        if (acronymMatch) {
          cleanText = acronymMatch[1].trim();
          acronym = acronymMatch[2].trim();
        }
        const item = {
          id: Utilities.getUuid(),
          text: cleanText,
          acronym: acronym,
          nestingLevel: nestingLevel,
          marker: marker,
          parentId: null,
          originalLine: text
        };
        while (parentStack.length > 0) {
          const potentialParent = parentStack[parentStack.length - 1];
          if (item.marker && potentialParent.marker) {
            if (item.marker.startsWith(potentialParent.marker + ".") &&
                item.marker.length > potentialParent.marker.length) break;
          } else if (item.nestingLevel > potentialParent.nestingLevel) {
            break;
          }
          parentStack.pop();
        }
        if (parentStack.length > 0) item.parentId = parentStack[parentStack.length - 1].id;
        parentStack.push(item);
        hierarchicalData.push(item);
      }

      dadosParaValidacao = converterHierarquiaParaFormatoPaiSigla(hierarchicalData, selectedPatriarca);

      
      const validacao = validarEstruturaOrganograma(dadosParaValidacao);
      if (!validacao.success) {
        const errorMsg = 'O arquivo contém erros que impedem o processamento: ' + validacao.errors.join('; ');
        Logger.log(errorMsg);
        // Aqui você provavelmente já tem um retorno de erro para o frontend
        return { success: false, errorCode: 120, message: errorMsg, errors: validacao.errors };
      }

    } else {
      return { success: false, errorCode: 110, message: 'Tipo de arquivo não suportado.', data: null };
    }

    const retProc = processAndSaveOrganograma(selectedPatriarca, hierarchicalData, 'processUploadedFileOrganograma', tipoArquivo);

    if (!retProc.success) {
      throw new Error(retProc.message);
    }

    const lotacaoImportada = selectedPatriarca.lot_gerado === "X";

    selectedPatriarca.status = "Em progresso";
    selectedPatriarca.org_gerado = "X";

    if (lotacaoImportada) {
      selectedPatriarca.lot_gerado = "A";
    }

    const retAtualizarPatriarca = atualizarPatriarca(selectedPatriarca.idpatriarca, selectedPatriarca);

    if (!retAtualizarPatriarca.success) {
      return { success: false, errorCode: 2000, message: retAtualizarPatriarca.message, data: null };
    }

    const dadosParaExibicao = hierarchicalData.map(item => ({
      Nome: item.text,
      Sigla: item.acronym,
      nestingLevel: item.nestingLevel
    }));

    Logger.log("Dados padronizados para exibição no frontend. Retornando sucesso.");

    return { success: true, errorCode: 0, message: 'Arquivo processado com sucesso!', data: dadosParaExibicao, atualizarLotacao: lotacaoImportada };

  } catch (error) {
    Logger.log('Erro ao processar o arquivo enviado: ' + error.message + ' ' + error.stack);
    return { success: false, errorCode: 1000, message: 'Erro ao processar o arquivo enviado: ' + error.message, data: null };
  } finally {
    if (convertedFile && convertedFile.id) {
      DriveApp.getFileById(convertedFile.id).setTrashed(true);
    }
  }
}


function organizarHierarquia(dados) {
    // Ordena pelo colItem (hierarquia)
    dados.sort((a, b) => {
        const aParts = a.hierarquiaOrgaoUnidade ? a.hierarquiaOrgaoUnidade.split('.').map(Number) : [0];
        const bParts = b.hierarquiaOrgaoUnidade ? b.hierarquiaOrgaoUnidade.split('.').map(Number) : [0];
        for (let i = 0; i < Math.max(aParts.length, bParts.length); i++) {
            const aVal = aParts[i] || 0;
            const bVal = bParts[i] || 0;
            if (aVal !== bVal) return aVal - bVal;
        }
        return 0;
    });

    // Cria um mapa de siglas por hierarquia para facilitar a busca do pai
    const mapaHierarquia = {};
    dados.forEach(item => {
        mapaHierarquia[item.hierarquiaOrgaoUnidade] = item.siglaOrgaoUnidade;
    });

    // Adiciona o atributo siglaPai a cada item
    //dados.forEach(item => {
    //    const partes = item.hierarquiaOrgaoUnidade ? item.hierarquiaOrgaoUnidade.split('.') : [];
    //    if (partes.length > 1) {
    //        const pai = partes.slice(0, -1).join('.');
    //        item.siglaPai = mapaHierarquia[pai] || '';
    //    } else {
    //        item.siglaPai = ''; // Primeiro nível não tem pai
    //    }
    //});

    return dados;
}

function reorganizarItemSemHierarquiaNoPatriarca(itens) {
  
  //{linhaPlanilha, hierarquiaOrgaoUnidade, nomeOrgaoUnidade, siglaOrgaoUnidade}
  var hierarquiaInicial = "1.";

  // Busca o item inicial linhaPlanilha===1
  var item = itens.find(dados => dados.linhaPlanilha === 1);
  
  if (!item) {
    return { success: false, message: 'Registro inicial não encontrado!', dados: [] };
  }

  if (item.hierarquiaOrgaoUnidade === "0") {
    item.hierarquiaOrgaoUnidade = "1";

    for (let i = 1; i < itens.length; i++) {
      itens[i].hierarquiaOrgaoUnidade = hierarquiaInicial + itens[i].hierarquiaOrgaoUnidade;
    }
  }

  // Retorna sucesso e os itens possivelmente modificados
  return { success: true, message: 'Reorganização concluída.', dados: itens };
}



/**
 * VERSÃO FINAL E DEFINITIVA
 * Orquestra o processamento, gravação e montagem do JSON para a API,
 * utilizando a coluna 'Numero' como fonte de verdade para a hierarquia.
 * @param {Object} patriarca O patriarca selecionado.
 * @param {Array<Object>} items Os dados brutos lidos do arquivo.
 */
function processAndSaveOrganograma(patriarca, items, origem, tipoArquivo) {
  try {
    var dadosParaPlanilha = [];

    if(origem == 'processUploadedFileOrganograma'){
      if(tipoArquivo == MimeType.GOOGLE_DOCUMENT){
        // Etapas 1, 2 e 3: Sua lógica original, que já funciona perfeitamente, é mantida.
        dadosParaPlanilha = converterHierarquiaParaFormatoPaiSigla(items, patriarca);
        dadosParaPlanilha = adicionarNumeracaoHierarquica(dadosParaPlanilha);
      }
      else {
        //dadosParaPlanilha = adicionarNumeracaoHierarquica(items);
        
        dadosParaPlanilha = items.map(item => [
              item.text,
              item.acronym,
              item.siglaPai,
              item.marker
            ]);
      }
    }
    else{
      dadosParaPlanilha = items.map(item => [
            item.text,
            item.acronym,
            item.paiSigla,
            item.numero
          ]);
    }
    const nomeAba = patriarca.sigla + '_O';
    const retGravarPlanilha = gravarOrganogramaEmPlanilha(nomeAba, dadosParaPlanilha);
    if (!retGravarPlanilha.success) {
      throw new Error(retGravarPlanilha.message);
    }

    // --- INÍCIO DA MONTAGEM DO JSON (LÓGICA CORRIGIDA COM BASE NA NUMERAÇÃO) ---

    // Passo A: Criar mapas para acesso rápido por Sigla e por Número
    const mapaPorSigla = new Map();
    const mapaPorNumero = new Map();
    dadosParaPlanilha.forEach(([nome, sigla, paiSigla, numero]) => {
      const item = { Nome: nome, Sigla: sigla, Numero: numero };
      mapaPorSigla.set(sigla, item);
      mapaPorNumero.set(numero, item);
    });

    // Passo B: Identificar os Órgãos (nível 1.x)
    const orgaos = dadosParaPlanilha
      .filter(([nome, sigla, paiSigla, numero]) => numero && numero.startsWith('1.') && numero.split('.').length === 2)
      .map(([nome, sigla, paiSigla, numero]) => mapaPorSigla.get(sigla));

    // Passo C: Para cada órgão, encontrar todas as suas unidades descendentes
    const orgaosJson = orgaos.map(orgao => {
      const unidadesDoOrgao = [];

      // Filtra todos os itens da planilha que são descendentes deste órgão
      dadosParaPlanilha.forEach(([nome, sigla, paiSigla, numero]) => {
        // Uma unidade pertence a um órgão se seu número começar com o número do órgão + "."
        if (numero && numero.startsWith(orgao.Numero + '.')) {
          
          // Lógica para encontrar a UnidadePai
          const partesNumero = numero.split('.');
          const numeroPai = partesNumero.slice(0, -1).join('.'); // Ex: de "1.1.2.a" para "1.1.2"
          
          let siglaUnidadePai = null;
          // Se o pai da unidade NÃO é o próprio órgão, encontramos a sigla do pai
          if (numeroPai !== orgao.Numero) {
            const pai = mapaPorNumero.get(numeroPai);
            if (pai) {
              siglaUnidadePai = pai.Sigla;
            }
          }
          
          // Adiciona a unidade à lista, sem campos extras
          unidadesDoOrgao.push({
            Nome: nome,
            Sigla: sigla,
            UnidadePai: siglaUnidadePai
          });
        }
      });

      return {
        Nome: orgao.Nome,
        Sigla: orgao.Sigla,
        Unidades: unidadesDoOrgao
      };
    });

    // Passo D: Montar o objeto JSON final
    const finalJson = {
      PatriarcaId: patriarca.idpatriarca,
      Orgaos: orgaosJson
    };

    // --- FIM DA MONTAGEM DO JSON ---

    // Etapa Final: Salvar o arquivo JSON para envio
    const jsonString = JSON.stringify(finalJson, null, 2);
    saveJsonToFile(jsonString, "Carga - Para Envio", `cargadeorgaos_${patriarca.sigla}.json`);

    return { success: true, message: 'Organograma processado e salvo com sucesso.' };

  } catch (error) {
    Logger.log('Erro em processAndSaveOrganograma com origem (' + origem + '): ' + error.message + ' Stack: ' + error.stack);
    return { success: false, message: 'Erro ao processar e salvar organograma: ' + error.message };
  }
}


function validarTodosOsCriterios(dados) {
  const problemas = [];
  const nomesVistos = {};
  const siglasVistas = {};

  dados.forEach((item) => {
    const linha = item.linhaPlanilha + 1;
    const nome = item.nomeOrgaoUnidade?.toString().trim();
    const sigla = item.siglaOrgaoUnidade?.toString().trim();
    const hierarquia = item.hierarquiaOrgaoUnidade?.toString().trim();

    if (!hierarquia) {
      problemas.push({ linhaPlanilha: linha, erro: 'O número relativo a hierarquia está vazio na linha: ' + linha + ' da planilha de dados.' });
    }
    if (!nome) {
      problemas.push({ linhaPlanilha: linha, erro: 'O nome do Órgão ou Unidade está vazio na linha: ' + linha + ' da planilha de dados.' });
    }
    if (!sigla) {
      problemas.push({ linhaPlanilha: linha, erro: 'A sigla está vazia na linha: ' + linha + ' da planilha de dados.' });
    } else if (/\s/.test(sigla)) {
      problemas.push({ linhaPlanilha: linha, erro: 'A sigla ' + sigla + ' contém espaços na linha: ' + linha + ' da planilha de dados.' });
    }
    if (hierarquia && !/^\d+(\.\d+)*$/.test(hierarquia)) {
      problemas.push({ linhaPlanilha: linha, erro: 'O número relativo a hierarquia ' + hierarquia + ' está mal formatada na linha: ' + linha + ' da planilha de dados.' });
    }

    if (nome) {
      if (nomesVistos[nome]) {
        problemas.push({ linhaPlanilha: linha, erro: 'Foi encontrado nome do Órgão ou Unidade duplicado: ' + nome + ' na linha: ' + linha + ' da planilha de dados.' });
      } else {
        nomesVistos[nome] = true;
      }
    }
    if (sigla) {
      if (siglasVistas[sigla]) {
        problemas.push({ linhaPlanilha: linha, erro: 'Foi encontrada sigla duplicada: ' + sigla + ' na linha: ' + linha + ' da planilha de dados.' });
      } else {
        siglasVistas[sigla] = true;
      }
    }
  });

  const problemasHierarquia = validaHierarquiaCompleta(dados);
  problemas.push(...problemasHierarquia);

  return problemas;
}

function validaHierarquiaCompleta(dados) {
  const mapa = {};
  const filhosPorPai = {};
  const problemas = [];
  const hierarquiasRegistradas = {};

  dados.forEach(item => {
    const hierarquia = item.hierarquiaOrgaoUnidade?.toString().trim();
    if (!hierarquia) return;

    if (!/^\d+(\.\d+)*$/.test(hierarquia)) {
      problemas.push({
        linhaPlanilha: item.linhaPlanilha,
        erro: `Hierarquia mal formada: ${hierarquia}`
      });
      return;
    }

    const partes = hierarquia.split('.');
    if (partes.length > 1) {
      const pai = partes.slice(0, -1).join('.');
      if (hierarquia === pai) {
        problemas.push({
          linhaPlanilha: item.linhaPlanilha,
          erro: `Item referencia a si mesmo na hierarquia: ${hierarquia}`
        });
        return;
      }
      filhosPorPai[pai] = filhosPorPai[pai] || [];
      filhosPorPai[pai].push(hierarquia);
    }

    hierarquiasRegistradas[hierarquia] = hierarquiasRegistradas[hierarquia] || [];
    hierarquiasRegistradas[hierarquia].push(item.linhaPlanilha);

    mapa[hierarquia] = item;
  });

  Object.entries(hierarquiasRegistradas).forEach(([hierarquia, linhas]) => {
    if (linhas.length > 1) {
      linhas.forEach(linha => {
        problemas.push({
          linhaPlanilha: linha + 1,
          erro: `Hierarquia duplicada: "${hierarquia}" encontrada na linha: ${linha + 1} da planilha de dados.`
        });
      });
    }
  });

  Object.keys(mapa).forEach(hierarquia => {
    const partes = hierarquia.split('.');
    if (partes.length > 1) {
      const pai = partes.slice(0, -1).join('.');
      if (!mapa[pai]) {
        problemas.push({
          linhaPlanilha: mapa[hierarquia].linhaPlanilha + 1,
          erro: `O item "${hierarquia}" está sem pai lógico (${pai}) encontrado na linha: ${mapa[hierarquia].linhaPlanilha + 1} da planilha de dados.`
        });
      }
    }
  });

  Object.entries(filhosPorPai).forEach(([pai, filhos]) => {
    const indices = filhos.map(h => {
      const segs = h.split('.');
      return parseInt(segs[segs.length - 1]);
    });

    indices.sort((a, b) => a - b);

    const verificaDuplicados = (arr) => arr.some((e, i) => arr.indexOf(e) !== i);
    if (verificaDuplicados(indices)) {
      problemas.push({
        linhaPlanilha: mapa[filhos[0]].linhaPlanilha + 1,
        erro: `Duplicidade de filhos no mesmo nível sob "${pai}" encontrado na linha: ${mapa[filhos[0]].linhaPlanilha + 1} da planilha de dados.`
      });
    }

    // quando um órgão não tem filhos.
    //for (let i = 1; i < indices.length; i++) {
    //  if (indices[i] !== indices[i-1] + 1) {
    //    problemas.push({
    //      linhaPlanilha: mapa[filhos[i]].linhaPlanilha,
    //      erro: `Lacuna na sequência de filhos em "${pai}" - esperado ${indices[i-1]+1}, encontrado ${indices[i]}`
    //    });
    //  }
    //}

  });

  Object.keys(filhosPorPai).forEach(pai => {
    filhosPorPai[pai].forEach(filho => {
      if (filho === pai) {
        problemas.push({
          linhaPlanilha: mapa[filho].linhaPlanilha + 1,
          erro: `Ciclo detectado: "${pai}" é pai de si próprio. Problema encontrado na linha: ${mapa[filho].linhaPlanilha + 1} da planilha de dados.`
        });
      }
    });
  });

  // ordenar pelo número da linha da planilha.
  problemas.sort((a, b) => {
    const linhaA = a.linhaPlanilha || 0;
    const linhaB = b.linhaPlanilha || 0;
    return linhaA - linhaB;
  });

  return problemas;
}

function associarSiglaPai(dados, siglaPatriarca) {
  const mapaSiglaPorHierarquia = new Map();

  dados.forEach(item => {
    mapaSiglaPorHierarquia.set(item.hierarquiaOrgaoUnidade, item.siglaOrgaoUnidade);
  });

  dados.forEach(item => {
    const hierarquia = item.hierarquiaOrgaoUnidade;
    if (!hierarquia || !hierarquia.includes('.')) {
      item.siglaPai = siglaPatriarca || null;
    } else {
      const hierarquiaPai = hierarquia.substring(0, hierarquia.lastIndexOf('.'));
      item.siglaPai = mapaSiglaPorHierarquia.get(hierarquiaPai) || siglaPatriarca || null;
    }
  });

  return dados;
}

function construirHierarchicalData(dados) {
  return dados.map(item => {
    const nestingLevel = (item.hierarquiaOrgaoUnidade.match(/\./g) || []).length;
    return {
      id: Utilities.getUuid(),
      text: item.nomeOrgaoUnidade,
      acronym: item.siglaOrgaoUnidade,
      nestingLevel: nestingLevel,
      marker: item.hierarquiaOrgaoUnidade,
      parentId: null,
      originalLine: item.nomeOrgaoUnidade + ' - ' + item.siglaOrgaoUnidade,
      siglaPai: item.siglaPai || null
    };
  });
}





/**
 * Converte os dados hierárquicos brutos (extraídos de um arquivo) para o formato de planilha.
 * @param {Array<Object>} items - A lista de itens hierárquicos extraída de processUploadedFileOrganograma.
 * @param {Object} patriarca - O objeto do patriarca selecionado.
 * @returns {Array<Array<string>>} Dados no formato [Nome, Sigla, Pai_Sigla].
 */
function converterHierarquiaParaFormatoPaiSigla(items, patriarca) {
  const dadosParaPlanilha = [];
  if (!items || items.length === 0) {
    Logger.log("Aviso: O array de itens para conversão está vazio. Adicionando apenas o patriarca.");
    dadosParaPlanilha.push([patriarca.nome, patriarca.sigla, '']);
    return dadosParaPlanilha;
  }
  const itemsById = new Map(items.map(item => [item.id, item]));
  items.forEach(item => {
    let paiSigla = '';
    if (item.parentId) {
      const pai = itemsById.get(item.parentId);
      if (pai) {
        paiSigla = pai.acronym;
      }
    }
    dadosParaPlanilha.push([item.text, item.acronym, paiSigla]);
  });
  const patriarcaNaLista = dadosParaPlanilha.some(row => row[1] === patriarca.sigla && row[2] === '');
  if (!patriarcaNaLista) {
    dadosParaPlanilha.unshift([patriarca.nome, patriarca.sigla, '']);
  }
  return dadosParaPlanilha;
}

/**
 * Recebe os dados do organograma e adiciona a coluna com a numeração hierárquica (WBS).
 * @param {Array<Array<string>>} dadosPlanilha - Dados no formato [Nome, Sigla, Pai_Sigla].
 * @returns {Array<Array<string>>} Dados com a nova coluna, no formato [Nome, Sigla, Pai_Sigla, Numero].
 */
function adicionarNumeracaoHierarquica(dadosPlanilha) {
  if (!dadosPlanilha || dadosPlanilha.length === 0) {
    return [];
  }

  //const camposObrigatorios = ['nome', 'sigla', 'paiSigla'];
  //function validarCamposEmTodos(arrayDeObjetos, campos) {
  //    return arrayDeObjetos.every(objeto => {
  //        // Para cada objeto, verifique se todos os campos obrigatórios existem
  //        return campos.every(campo => {
  //            return campo in objeto; // Use o operador 'in' para verificar a existência do campo
  //        });
  //    });
  //}
  //if(!validarCamposEmTodos(dadosPlanilha, camposObrigatorios)){
  //}

  // Mapeia filhos por pai para construir a árvore.
  const filhosPorPai = {};
  dadosPlanilha.forEach(([nome, sigla, paiSigla]) => {
    const pai = paiSigla || 'root';
    if (!filhosPorPai[pai]) {
      filhosPorPai[pai] = [];
    }
    filhosPorPai[pai].push(sigla);
  });

  const mapaDeNumeracao = {};

  // Função recursiva para percorrer a árvore e atribuir a numeração.
  function percorrerEAtribuir(siglaNoAtual, prefixo, caminhoAtual) {
    // Detecção de ciclo para segurança
    if (caminhoAtual.has(siglaNoAtual)) {
      Logger.log(`AVISO: Ciclo detectado na hierarquia envolvendo a sigla '${siglaNoAtual}'.`);
      mapaDeNumeracao[siglaNoAtual] = `${prefixo} [CICLO!]`;
      return;
    }

    caminhoAtual.add(siglaNoAtual);
    mapaDeNumeracao[siglaNoAtual] = prefixo;
    
    const filhos = filhosPorPai[siglaNoAtual] || [];
    filhos.forEach((filho, index) => {
      const novoPrefixo = prefixo ? `${prefixo}.${index + 1}` : `${index + 1}`;
      percorrerEAtribuir(filho, novoPrefixo, new Set(caminhoAtual));
    });
  }

  // Inicia o processo a partir dos nós raiz.
  const raizes = filhosPorPai['root'] || [];
  raizes.forEach((raiz, index) => {
    percorrerEAtribuir(raiz, `${index + 1}`, new Set());
  });

  // Monta o resultado final com a nova coluna de numeração.
  return dadosPlanilha.map(([nome, sigla, paiSigla]) => {
    return [nome, sigla, paiSigla, mapaDeNumeracao[sigla] || ''];
  });
}

/**
 * Converte os dados visuais do ReactFlow (nós e arestas) em um formato de lista hierárquica
 * compatível com as outras funções do sistema.
 * @param {Array} nodes - O array de nós do ReactFlow.
 * @param {Array} edges - O array de arestas do ReactFlow.
 * @returns {Array<Array<string>>} Um array 2D no formato [Nome, Sigla, Pai_Sigla].
 */
function converterDadosVisuaisParaFormatoPlanilha(nodes, edges) {
  const nodesMap = new Map(nodes.map(node => [node.id, node]));
  const parentSiglaMap = new Map();

  // Mapeia o ID de cada nó filho à SIGLA do seu nó pai.
  edges.forEach(edge => {
    const parentNode = nodesMap.get(edge.source);
    if (parentNode) {
      parentSiglaMap.set(edge.target, parentNode.data.sigla);
    }
  });

  // Constrói a lista final no formato [Nome, Sigla, Pai_Sigla]
  const listaPlana = nodes.map(node => {
    const nome = node.data.nome;
    const sigla = node.data.sigla;
    const paiSigla = parentSiglaMap.get(node.id) || ''; // Se não encontrar pai, é um nó raiz.
    return [nome, sigla, paiSigla];
  });
  
  return listaPlana;
}

/**
 * Gera o arquivo JSON final para a API a partir dos dados já processados e numerados.
 * @param {Object} patriarca - O objeto do patriarca.
 * @param {Array<Array<string>>} dadosPlanilha - Os dados completos do organograma no formato [Nome, Sigla, Pai_Sigla, Numero].
 * @returns {object} Objeto com status de sucesso e mensagem.
 */
function gerarApiJsonDoOrganograma(patriarca, dadosPlanilha) {
  try {
    // Passo A: Criar mapas para acesso rápido por Sigla e por Número
    const mapaPorSigla = new Map();
    const mapaPorNumero = new Map();
    dadosPlanilha.forEach(([nome, sigla, paiSigla, numero]) => {
      const item = { Nome: nome, Sigla: sigla, Numero: numero };
      mapaPorSigla.set(sigla, item);
      mapaPorNumero.set(numero, item);
    });

    // Passo B: Identificar os Órgãos (nível 1.x)
    const orgaos = dadosPlanilha
      .filter(([nome, sigla, paiSigla, numero]) => numero && numero.startsWith('1.') && numero.split('.').length === 2)
      .map(([nome, sigla, paiSigla, numero]) => mapaPorSigla.get(sigla));

    // Passo C: Para cada órgão, encontrar todas as suas unidades descendentes
    const orgaosJson = orgaos.map(orgao => {
      const unidadesDoOrgao = [];
      dadosPlanilha.forEach(([nome, sigla, paiSigla, numero]) => {
        if (numero && numero.startsWith(orgao.Numero + '.')) {
          const partesNumero = numero.split('.');
          const numeroPai = partesNumero.slice(0, -1).join('.');
          let siglaUnidadePai = null;
          if (numeroPai !== orgao.Numero) {
            const pai = mapaPorNumero.get(numeroPai);
            if (pai) {
              siglaUnidadePai = pai.Sigla;
            }
          }
          unidadesDoOrgao.push({
            Nome: nome,
            Sigla: sigla,
            UnidadePai: siglaUnidadePai
          });
        }
      });
      return {
        Nome: orgao.Nome,
        Sigla: orgao.Sigla,
        Unidades: unidadesDoOrgao
      };
    });

    // Passo D: Montar o objeto JSON final
    const finalJson = {
      PatriarcaId: patriarca.idpatriarca,
      Orgaos: orgaosJson
    };

    // Etapa Final: Salvar o arquivo JSON para envio
    const jsonString = JSON.stringify(finalJson, null, 2);
    saveJsonToFile(jsonString, "Carga - Para Envio", `cargadeorgaos_${patriarca.sigla}.json`);

    return { success: true, message: 'JSON para API gerado com sucesso.' };
  } catch (error) {
    Logger.log('Erro em gerarApiJsonDoOrganograma: ' + error.message + ' Stack: ' + error.stack);
    return { success: false, message: 'Erro ao gerar JSON para API: ' + error.message };
  }
}

function _testeSalvarOrganogramaVisual(){

  var patriarca = {
    nome: 'PREFEITURA ALEXANDRE',
    sigla: 'PMALE',
    idpatriarca: 'f9d0506a-4978-4c15-8bba-49adbadd1e39',
    status: 'Em progresso',
    org_gerado: 'X',
    lot_gerado: '',
    token: '',
    datasolicitacao: ''
  };

  var retSetSelectedPatriarca = setSelectedPatriarca(patriarca.idpatriarca);

  const reactFlowFileName = `cargadeorgaos_${patriarca.sigla}_reactflow.json`;
  const reactFlowContent = findJsonFileContentByName("Carga - Para Envio", reactFlowFileName);
  
  const reconstructedItems = reconstruirHierarquiaDosNodes(reactFlowContent.nodes, reactFlowContent.edges, patriarca);

  const resultadoProcessamento = processAndSaveOrganograma(patriarca, reconstructedItems, 'salvarOrganogramaVisual');
  
}

function converterTextosParaCaixaAlta(dados) {
  return dados.map(linha => {
    // linha[0] = Nome, linha[1] = Sigla, linha[2] = Pai_Sigla, linha[3] = Numero
    const nome = linha[0] ? linha[0].toUpperCase() : '';
    const sigla = linha[1] ? linha[1].toUpperCase() : '';
    const paiSigla = linha[2] ? linha[2].toUpperCase() : '';
    const numero = linha[3]; // O número não é alterado.
    
    return [nome, sigla, paiSigla, numero];
  });
}

function ordenarDadosPorNumero(dados) {
  dados.sort((a, b) => {
    // A coluna 'Numero' está no índice 3.
    const numeroA = a[3] || '';
    const numeroB = b[3] || '';
    
    // localeCompare com a opção numeric:true trata os números dentro das strings corretamente.
    return numeroA.localeCompare(numeroB, undefined, { numeric: true, sensitivity: 'base' });
  });
  
  return dados;
}

/**
 * Orquestra o salvamento completo do organograma a partir do editor visual (ReactFlow).
 * @param {object} visualData Objeto contendo os nós (nodes) e arestas (edges) do ReactFlow.
 * @returns {object} Objeto com status de sucesso e mensagem.
 */
function salvarOrganogramaVisual(visualData) {
  try {
    const patriarca = getSelectedPatriarca();
    if (!patriarca) {
      throw new Error("Nenhum Patriarca selecionado para salvar o organograma.");
    }
    const { nodes, edges } = visualData;
    if (!nodes || !edges) {
      throw new Error("Dados visuais inválidos recebidos do editor.");
    }
    
    // 1. Converter dados visuais para formato de lista hierárquica [Nome, Sigla, Pai_Sigla]
    const dadosHierarquicos = converterDadosVisuaisParaFormatoPlanilha(nodes, edges);

    // 2: CHAMAR A FUNÇÃO DE VALIDAÇÃO CENTRAL
    const validacao = validarEstruturaOrganograma(dadosHierarquicos);
    if (!validacao.success) {
      Logger.log(`Validação falhou para o organograma visual: ${validacao.errors.join('; ')}`);
      return { success: false, message: 'Dados inválidos detectados! ' + validacao.errors.join('; ') };
    }

    // 2. Salvar o layout visual bruto para persistir as posições dos nós
    const reactFlowFileName = `cargadeorgaos_${patriarca.sigla}_reactflow.json`;
    saveJsonToFile(JSON.stringify(visualData, null, 2), "Carga - Para Envio", reactFlowFileName);
    Logger.log(`Layout visual do ReactFlow salvo como '${reactFlowFileName}'.`);


    // 3. Adicionar a numeração hierárquica (WBS), gerando a 4ª coluna 'Numero'
    const dadosNumerados = adicionarNumeracaoHierarquica(dadosHierarquicos);
    
    const dadosMaiusculos = converterTextosParaCaixaAlta(dadosNumerados);
    
    // 5: Ordenar os dados pela coluna 'Numero' antes de gravar
    const dadosOrdenados = ordenarDadosPorNumero(dadosMaiusculos);

    // 6. Gravar os dados completos e numerados na planilha
    const nomeAba = patriarca.sigla + '_O';
    const retGravarPlanilha = gravarOrganogramaEmPlanilha(nomeAba, dadosOrdenados);
    if (!retGravarPlanilha.success) {
      throw new Error(retGravarPlanilha.message);
    }
    Logger.log(`Dados do organograma gravados com sucesso na aba '${nomeAba}'.`);

    // 7. Gerar o JSON final para a API a partir dos dados recém-processados
    const retApiJson = gerarApiJsonDoOrganograma(patriarca, dadosOrdenados);
    if (!retApiJson.success) {
      throw new Error(retApiJson.message);
    }

    // 8. Atualizar o status do patriarca para refletir que o organograma foi trabalhado
    patriarca.status = "Em progresso";
    patriarca.organogramagerado = "X";
    const retAtualizarPatriarca = atualizarPatriarca(patriarca);
    if (!retAtualizarPatriarca.success) {
      // Loga o erro mas não impede o sucesso da operação principal de salvamento
      Logger.log(`Aviso: O organograma foi salvo, mas falhou ao atualizar o status do patriarca: ${retAtualizarPatriarca.message}`);
    }

    return { 
      success: true, 
      message: 'Organograma visual salvo com sucesso. A numeração foi recalculada e gravada.' 
    };

  } catch (error) {
    Logger.log('Erro em salvarOrganogramaVisual: ' + error.message + ' Stack: ' + error.stack);
    return { success: false, message: 'Erro ao salvar o organograma visual: ' + error.message };
  }
}

/**
 * Reconstrói a hierarquia dos dados da planilha a partir dos nodes e edges do ReactFlow.
 * Agora inclui corretamente a Pai_Sigla para cada item.
 * @param {Array} nodes - Nós do ReactFlow.
 * @param {Array} edges - Arestas do ReactFlow.
 * @param {Object} patriarca - Objeto do patriarca.
 * @returns {Array} Array de itens no formato compatível com a planilha.
 */
function reconstruirHierarquiaDosNodes(nodes, edges, patriarca) {
  const nodesById = new Map(nodes.map(node => [node.id, node]));
  const childrenByParentId = new Map();
  
  // --> CORREÇÃO: Adiciona mapeamento para encontrar o pai de cada nó
  const parentByChildId = new Map();
  
  edges.forEach(edge => {
    // Mapear filhos por pai (como já estava)
    if (!childrenByParentId.has(edge.source)) {
      childrenByParentId.set(edge.source, []);
    }
    childrenByParentId.get(edge.source).push(edge.target);
    
    // --> NOVO: Mapear pai por filho
    parentByChildId.set(edge.target, edge.source);
  });

  const rootNodeId = 'root';
  if (!nodesById.has(rootNodeId)) {
    throw new Error("Não foi possível encontrar o nó raiz (Patriarca) no organograma visual.");
  }

  const reconstructedItems = [];
  
  function dfs(nodeId, level) {
    const node = nodesById.get(nodeId);
    if (!node) return;

    // --> CORREÇÃO: Encontrar a sigla do pai
    let paiSigla = '';
    const parentNodeId = parentByChildId.get(nodeId);
    if (parentNodeId && nodeId !== 'root') {
      const parentNode = nodesById.get(parentNodeId);
      if (parentNode) {
        paiSigla = parentNode.data.sigla;
      }
    }
    // Se não tem pai ou o pai é o root, Pai_Sigla fica vazio (para o patriarca)

    reconstructedItems.push({
      text: node.data.nome,
      acronym: node.data.sigla,
      nestingLevel: level,
      id: nodeId,
      paiSigla: paiSigla, // --> ADICIONADO: Inclui a sigla do pai
      numero: node.data.numero || ''
    });

    const children = childrenByParentId.get(nodeId) || [];
    children.forEach(childId => {
      dfs(childId, level + 1);
    });
  }

  dfs(rootNodeId, 0);
  return reconstructedItems;
}

/**
 * Grava os dados formatados do organograma em uma aba específica da planilha de carga.
 * @param {string} nomeNovaAba - O nome da aba a ser criada (ex: "PMEXE_O").
 * @param {Array<Array<string>>} dadosFormatados - Os dados a serem gravados.
 */
function gravarOrganogramaEmPlanilha(nomeNovaAba, dadosFormatados) {
  try {
    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) throw new Error(`Erro ao abrir a planilha de carga: ${CONFIG.SPREADSHEET_PARAM}`);
    
    const spreadsheetCarga = SpreadsheetApp.openById(retLerArq.fileId);
    let existingSheet = spreadsheetCarga.getSheetByName(nomeNovaAba);
    if (existingSheet) spreadsheetCarga.deleteSheet(existingSheet);
    
    const novaAba = spreadsheetCarga.insertSheet(nomeNovaAba);
    
    // Cabeçalho atualizado com 4 colunas
    const header = ['Nome', 'Sigla', 'Pai_Sigla', 'Numero'];
    novaAba.getRange(1, 1, 1, header.length).setValues([header]).setFontWeight('bold');

    // Garante que a coluna 'Numero' (coluna D, a 4ª) seja formatada como Texto Puro.
    // Isso impede que o Google Sheets faça a conversão automática de "1.1" para uma data ou número.
    novaAba.getRange("D:D").setNumberFormat('@'); // '@' é o código para formato de texto.

    if (dadosFormatados.length > 0) {
      novaAba.getRange(2, 1, dadosFormatados.length, header.length).setValues(dadosFormatados);
      novaAba.autoResizeColumns(1, header.length);
    }
    Logger.log(`Dados do organograma gravados com sucesso na aba '${nomeNovaAba}'.`);
    return { success: true, sheetName: nomeNovaAba };
  } catch (error) {
    Logger.log('Erro em gravarOrganogramaEmPlanilha: ' + error.message);
    return { success: false, message: error.message };
  }
}

//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

/**
 * 
 * Funções de Lotação
 * 
*/

function processUploadedFileLotacao(base64Content, fileName, fileMimeType) {
  let fileId = null;
  
  try {
    const selectedPatriarca = getSelectedPatriarca();
    if (!selectedPatriarca) {
      return { success: false, message: 'Nenhum Patriarca selecionado. Por favor, selecione um Patriarca antes de processar o arquivo.', data: null };
    }

    Logger.log("chamada processUploadedFileLotacao - fileName: " + fileName + ", fileMimeType: " + fileMimeType);

    var textFile = fileMimeType;
    textFile = textFile + '\n';
    textFile = textFile + base64Content;
    saveTxtToFile(textFile, "Carga_Lotacao - Para Envio", 'encodedBlob_' + selectedPatriarca.sigla + '.txt');

    const decodedBlob = Utilities.newBlob(
      Utilities.base64Decode(base64Content), 
      fileMimeType, 
      fileName
    );

    let processedData = null;
    let convertedFile = null;

    if (fileMimeType === MimeType.MICROSOFT_EXCEL ||
        fileMimeType === MimeType.MICROSOFT_EXCEL_LEGACY ||
        fileMimeType === MimeType.GOOGLE_SPREADSHEET ||
        fileMimeType === MimeType.OPEN_DOCUMENT_SPREADSHEET) {
      // Cria um arquivo temporário do Excel no Drive para processamento
      convertedFile = Drive.Files.insert({ title: fileName, mimeType: MimeType.GOOGLE_SPREADSHEET }, decodedBlob, { convert: true });
      const spreadsheet = SpreadsheetApp.openById(convertedFile.id);
      const sheet = spreadsheet.getSheets()[0];
      const range = sheet.getDataRange();
      processedData = range.getValues();
      Logger.log("processUploadedFileLotacao - Excel processado! processedData: " + JSON.stringify(processedData));
      
    } else {
      return { success: false, message: 'Tipo de arquivo não suportado.', data: null };
    }
    
    // Deleta o arquivo temporário
    if (convertedFile && convertedFile.id) {
      DriveApp.getFileById(convertedFile.id).setTrashed(true);
    }
    
    return { success: true, message: 'Arquivo processado com sucesso!', data: processedData };

  } catch (error) {
    if (fileId) {
      DriveApp.getFileById(fileId).setTrashed(true);
    }
    Logger.log('Erro ao processar o arquivo enviado: ' + error.message);
    return { success: false, message: 'Erro no servidor: ' + error.message, data: null };
  }
}

function processSelectedTabs(fileName, selectedTabs) {
  try {
    const selectedPatriarca = getSelectedPatriarca();
    if (!selectedPatriarca) {
      return { success: false, message: 'Nenhum Patriarca selecionado. Por favor, selecione um Patriarca antes de processar as abas.' };
    }

    if (!selectedTabs || selectedTabs.length === 0) {
      return { success: false, message: 'Nenhuma aba selecionada para processamento.' };
    }

    // Abrir a planilha de carga
    const retLerArqCarga = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArqCarga.success) {
      return { success: false, message: `Erro ao abrir a planilha de carga: ${CONFIG.SPREADSHEET_PARAM}` };
    }

    const spreadsheetCarga = SpreadsheetApp.openById(retLerArqCarga.fileId);
    
    // MODIFICADO: Define o nome da nova aba para Lotação
    const nomeNovaAba = selectedPatriarca.sigla + '_L';

    // Verificar se a aba já existe e excluir
    let existingSheet = spreadsheetCarga.getSheetByName(nomeNovaAba);
    if (existingSheet) {
      spreadsheetCarga.deleteSheet(existingSheet);
      Logger.log(`Aba existente '${nomeNovaAba}' foi excluída.`);
    }

    // Criar nova aba
    const novaAba = spreadsheetCarga.insertSheet(nomeNovaAba);
    
    // Cabeçalho
    const dataProcessamento = new Date().toLocaleString('pt-BR');
    const cabecalho = [
      [`Processamento de Lotação - ${selectedPatriarca.nome} (${selectedPatriarca.sigla})`],
      [`Arquivo: ${fileName}`],
      [`Data/Hora: ${dataProcessamento}`],
      [`Abas processadas: ${selectedTabs.join(', ')}`],
      [''],
      ['Dados das abas selecionadas:']
    ];

    for (let i = 0; i < cabecalho.length; i++) {
      novaAba.getRange(i + 1, 1, 1, cabecalho[i].length).setValues([cabecalho[i]]);
    }
    novaAba.getRange(1, 1).setFontWeight('bold').setFontSize(14);
    novaAba.getRange(2, 1, 4, 1).setFontSize(10);
    novaAba.getRange(6, 1).setFontWeight('bold');

    let linhaAtual = 8;

    // Abrir arquivo de servidores (Google Sheets ou XLSX convertido)
    const retArqServidores = verificarEAbrirPlanilha(fileName);
    if(!retArqServidores.success){
      throw new Error(`Não foi possível abrir o arquivo '${fileName}'.`);
    }

    const { spreadsheetArqServidores, convertedFileId } = abrirPlanilhaGenerica(retArqServidores.fileId);

    // Loop pelas abas selecionadas
    selectedTabs.forEach((tabName, index) => {
      novaAba.getRange(linhaAtual, 1).setValue(`Aba ${index + 1}: ${tabName}`);
      linhaAtual++;
      let linhaplanilha = 8;

      const sheetServidor = spreadsheetArqServidores.getSheetByName(tabName);
      if(sheetServidor){        
        const lastRow = sheetServidor.getLastRow();

        if(lastRow > 0){
          // Ao ler o conteúdo da planiha, elimina as linhas em branco.
          const data = getCleanedData(sheetServidor);
         if (data.length > 0) {
          // Inclui o número da linha original como primeira coluna
          const dataComLinha = data.map((row, idx) => {
            return [idx + 1].concat(row);
          });

          // Adiciona um cabeçalho extra para indicar a coluna da linha original
          novaAba.getRange(linhaAtual, 1, 1, dataComLinha[0].length)
                .setValues([['LinhaOriginal'].concat(data[0].map((_, i) => `Coluna${i+1}`))]);
          linhaAtual++;

          // Grava os dados
          novaAba.getRange(linhaAtual, 1, dataComLinha.length, dataComLinha[0].length).setValues(dataComLinha);
          linhaAtual += dataComLinha.length + 1;
          } else {
            novaAba.getRange(linhaAtual, 2).setValue('Aba sem dados.');
            linhaAtual += 2;
          }
        } else {
          novaAba.getRange(linhaAtual,2).setValue('Aba sem dados.');
          linhaAtual += 2;
        }
      } else {
        novaAba.getRange(linhaAtual,2).setValue(`Aba '${tabName}' não encontrada no arquivo de servidores.`);
        linhaAtual += 2;
      }
    });

    novaAba.autoResizeColumns(1, 10);

    // Se foi criada uma cópia convertida, remove para não acumular no Drive
    if (convertedFileId) {
      try {
        //DriveApp.getFileById(convertedFileId).setTrashed(true);
        Logger.log("Arquivo temporário convertido excluído: " + convertedFileId);
      } catch (e) {
        Logger.log("Falha ao excluir cópia convertida: " + e.message);
      }
    }

    return { 
      success: true, 
      message: `${selectedTabs.length} aba(s) processada(s) com sucesso.`, 
      sheetName: nomeNovaAba 
    };

  } catch (error) {
    Logger.log('Erro ao processar abas selecionadas: ' + error.message);
    return { success: false, message: 'Erro no servidor: ' + error.message };
  }
}

function abrirPlanilhaGenerica(fileId){
  const file = DriveApp.getFileById(fileId);
  const mimeType = file.getMimeType();

  Logger.log("Abrindo arquivo com MIME: " + mimeType);

  // Se já for Google Sheets
  if(mimeType === MimeType.GOOGLE_SHEETS){
    return { spreadsheetArqServidores: SpreadsheetApp.openById(fileId), convertedFileId: null };
  }

  // Se for Excel (XLSX)
  if(mimeType === MimeType.MICROSOFT_EXCEL){
    const blob = file.getBlob();
    const resource = {
      title: file.getName(),
      mimeType: MimeType.GOOGLE_SHEETS
    };
    
    // Aqui sim converte para Google Sheets
    const convertedFile = Drive.Files.insert(resource, blob, {convert: true});

    return { spreadsheetArqServidores: SpreadsheetApp.openById(convertedFile.id), convertedFileId: convertedFile.id };
  }

  throw new Error("Tipo de arquivo não suportado: " + mimeType);
}

/**
 * Lê os dados da aba e remove linhas vazias
 * considerando apenas as colunas A, B e C.
 */
function getCleanedData(sheetServidor) {
  const lastRow = sheetServidor.getLastRow();
  const lastCol = 7; // sheetServidor.getLastColumn(); só é necessário selecionar até a coluna G. 

  if (lastRow === 0 || lastCol === 0) {
    return []; // nenhuma linha de dados
  }

  // Pega todos os dados da aba
  const data = sheetServidor.getRange(1, 1, lastRow, lastCol).getValues();

  // Filtra removendo linhas onde A, B e C estão vazias
  const filtered = data.filter((row, index) => {
    // mantém o cabeçalho (linha 1) sempre
    if (index === 0) return true;

    const colA = row[0]; // Coluna A
    const colB = row[1]; // Coluna B
    const colC = row[2]; // Coluna C

    return (colA && colA.toString().trim() !== '') ||
           (colB && colB.toString().trim() !== '') ||
           (colC && colC.toString().trim() !== '');
  });

  return filtered;
}

/**
 * Constrói um mapa de itens por ID para acesso rápido.
 * @param {Array<object>} itemsArray O array de itens do organograma.
 * @returns {Map<string, object>} Um mapa onde a chave é o ID do item e o valor é o objeto do item.
 */
function buildItemsMap(itemsArray) {
  const itemsMap = new Map();
  itemsArray.forEach(item => {
    itemsMap.set(item.id, item);
  });
  return itemsMap;
}

/**
 * Verifica se um item é ancestral de outro (ou o próprio item).
 * @param {object} possibleAncestor O item que pode ser um ancestral.
 * @param {object} descendant O item que pode ser um descendente.
 * @param {Map<string, object>} itemsMap Mapa de todos os itens por ID.
 * @returns {boolean} True se possibleAncestor é um ancestral de descendant (ou o próprio descendant), False caso contrário.
 */
function isAncestorOrSelf(possibleAncestor, descendant, itemsMap) {
  if (!possibleAncestor || !descendant) return false;
  if (possibleAncestor.id === descendant.id) return true; // É o mesmo item

  let current = descendant;
  while (current.parentId) {
    current = itemsMap.get(current.parentId);
    if (!current) break; // Pai não encontrado, hierarquia quebrada
    if (current.id === possibleAncestor.id) return true;
  }
  return false;
}

/**
 * Verifica se dois itens estão na mesma linha hierárquica (ancestral-descendente).
 * @param {object} item1 O primeiro item.
 * @param {object} item2 O segundo item.
 * @param {Map<string, object>} itemsMap Mapa de todos os itens por ID.
 * @returns {boolean} True se item1 é ancestral de item2, ou item2 é ancestral de item1, ou são o mesmo item. False caso contrário.
 */
function isInSameHierarchyLine(item1, item2, itemsMap) {
  if (!item1 || !item2) return false;
  return isAncestorOrSelf(item1, item2, itemsMap) || isAncestorOrSelf(item2, item1, itemsMap);
}


/**
 * Função de SpellChecker para português
 */
function verificarOrtografia(texto) {
  if (texto === undefined || texto === null) return [];
  if (typeof texto !== "string") texto = String(texto);
  if (texto.trim() === "") return [];

  var url = "https://api.languagetool.org/v2/check";

  var payload = {
    text: texto,
    language: 'pt-BR'
  };

  var options = {
    method: 'POST',
    payload: payload,
    muteHttpExceptions: true // evita exceção automática
  };

  var response = UrlFetchApp.fetch(url, options);
  var status = response.getResponseCode();
  var resultText = response.getContentText();

  Logger.log("Código HTTP: " + status);
  Logger.log("Resposta da API: " + resultText);

  // Se não for 200, retorna vazio
  if (status !== 200) {
    return [{ erro: "Falha na chamada da API", detalhe: resultText }];
  }

  // Tenta converter em JSON
  var result;
  try {
    result = JSON.parse(resultText);
  } catch (e) {
    return [{ erro: "Resposta inválida da API", detalhe: resultText }];
  }

  if (result.matches && result.matches.length > 0) {
    return result.matches.map(function(match) {
      return {
        palavra: texto.substring(match.offset, match.offset + match.length),
        sugestao: match.replacements.length > 0 ? match.replacements[0].value : null,
        mensagem: match.message
      };
    });
  }

  return [];
}

function validarDadosLotacao() {
  try {
    const patriarca = getSelectedPatriarca();
    if (!patriarca) throw new Error("Nenhum Patriarca selecionado.");

    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) throw new Error("Não foi possível abrir a planilha de carga.");
    
    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId);
    const lotacaoSheet = spreadsheet.getSheetByName(patriarca.sigla + '_L');
    const organogramaSheet = spreadsheet.getSheetByName(patriarca.sigla + '_O');

    if (!lotacaoSheet) throw new Error(`Aba de lotação '${patriarca.sigla}_L' não encontrada.`);
    if (!organogramaSheet) throw new Error(`Aba de organograma '${patriarca.sigla}_O' não encontrada.`);

    // 1. Mapear Órgãos e a Hierarquia de Unidades
    const orgaos = new Set();
    const unidades = new Map();
    const todasAsSiglas = new Set();
    const organogramaData = organogramaSheet.getDataRange().getValues();
    const siglaPatriarca = patriarca.sigla;

    for (let i = 1; i < organogramaData.length; i++) {
      const sigla = organogramaData[i][1]; // Coluna B: Sigla
      const siglaPai = organogramaData[i][2]; // Coluna C: Sigla_Pai

      if (!sigla) continue;
      todasAsSiglas.add(sigla);

      // Define como "Órgão" apenas os filhos diretos do Patriarca
      if (siglaPai === siglaPatriarca) {
        orgaos.add(sigla);
      }

      // Mapeia toda a hierarquia de unidades
      if (siglaPai) {
        if (!unidades.has(siglaPai)) {
          unidades.set(siglaPai, new Set());
        }
        unidades.get(siglaPai).add(sigla);
      }
    }

    // 2. Iterar e validar a aba de lotação
    const lotacaoData = lotacaoSheet.getDataRange().getValues();
    let currentAba = null;
    let inconsistenciasMap = {};

    for (let i = 7; i < lotacaoData.length; i++) {
      const row = lotacaoData[i];
      const firstCell = row[0] ? String(row[0]).trim() : '';

      const match = firstCell.match(/^Aba \d+: (.*)$/);
      if (match) {
        currentAba = match[1].trim();
        i += 3; // Pula as 3 linhas de cabeçalho fixo + a linha do match
        continue;
      }

      if (!currentAba || row.every(cell => cell === '') || (row[1] === 'Sigla' && row[6] === 'Sigla Setor')) {
        continue;
      }

      const linhaOriginal = row[0];
      const orgaoServidor = row[1]; // Coluna B: Órgão do servidor
      const siglaSetor = row[6]; // Coluna G: Setor/Unidade de lotação
      const cpf = row[4];
      const cargo = row[5];

      const addInconsistencia = (tipo, detalhe, indicador_erro = true) => {
        if (!inconsistenciasMap[currentAba]) {
          inconsistenciasMap[currentAba] = [];
        }
        inconsistenciasMap[currentAba].push({
          orgao: orgaoServidor,
          linha: linhaOriginal,
          tipo: tipo,
          detalhe: detalhe,
          indicador_erro: indicador_erro
        });
      };
      
      // Validação 1: O órgão do servidor (Coluna B) deve ser um órgão válido.
      if (!orgaos.has(orgaoServidor)) {
        addInconsistencia("Órgão Inválido", `O órgão "${orgaoServidor}" na coluna B não é um órgão válido (não é um filho direto de ${siglaPatriarca}).`);
      }

      // Validação 2: O setor de lotação (Coluna G) deve existir no organograma e pertencer à hierarquia do órgão.
      if (!todasAsSiglas.has(siglaSetor)) {
          addInconsistencia("Setor/Unidade Inválida", `A sigla de lotação "${siglaSetor}" na coluna G não existe no organograma.`);
      } else {
          // Valida se o setor pertence à hierarquia do órgão do servidor
          let paiAtual = siglaSetor;
          let pertence = false;
          while (paiAtual) {
              const entrada = Array.from(unidades.entries()).find(([_, filhos]) => filhos.has(paiAtual));
              paiAtual = entrada ? entrada[0] : null;
              if (paiAtual === orgaoServidor) {
                  pertence = true;
                  break;
              }
          }
          if (!pertence && orgaos.has(siglaSetor)) {
             // Permite lotação direta no próprio órgão
             if (siglaSetor !== orgaoServidor) {
                 addInconsistencia("Lotação Inválida", `O setor "${siglaSetor}" é um órgão, mas não corresponde ao órgão do servidor "${orgaoServidor}".`);
             }
          } else if (!pertence && !orgaos.has(siglaSetor)) {
              addInconsistencia("Hierarquia Inválida", `O setor/unidade "${siglaSetor}" não pertence à hierarquia do órgão "${orgaoServidor}".`);
          }
      }

      // Validações 3, 4 e 5 (CPF, Cargo) - sem alterações
      if (!cpf || String(cpf).trim() === '') {
        addInconsistencia("CPF Vazio", "O campo CPF é obrigatório e não está preenchido.");
      } else {
        const cpfLimpo = String(cpf).replace(/\D/g, '');
        if (cpfLimpo.length !== 11) {
          addInconsistencia("CPF Inválido", `O CPF "${cpf}" não possui 11 dígitos numéricos.`);
        }
      }

      if (!cargo || String(cargo).trim() === '') {
        addInconsistencia("Cargo Vazio", "O campo Cargo é obrigatório e não está preenchido.");
      }
      
      // Validação de Ortografia (placeholder)
      // ...
    }

    return {
      success: true,
      inconsistencias: inconsistenciasMap
    };

  } catch (e) {
    Logger.log("Erro em validarDadosLotacao: " + e.message + " em " + e.stack);
    return { success: false, message: e.message };
  }
}

function gerarJsonLotacao() {
  try {
    const patriarca = getSelectedPatriarca();
    if (!patriarca) throw new Error("Nenhum Patriarca selecionado.");

    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) throw new Error("Planilha de carga não encontrada.");
    
    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId);
    const lotacaoSheet = spreadsheet.getSheetByName(patriarca.sigla + '_L');
    if (!lotacaoSheet) throw new Error(`Aba de lotação '${patriarca.sigla}_L' não encontrada.`);
    
    const lotacaoData = lotacaoSheet.getDataRange().getValues();

    let currentAba = null;
    let orgaosMap = {};

    for (let i = 7; i < lotacaoData.length; i++) { // Começa a ler da linha 8 (índice 7)
      const row = lotacaoData[i];
      const firstCell = row[0] ? String(row[0]) : '';
      
      const match = firstCell.match(/^Aba \d+: (.*)$/);
      if (match) {
        currentAba = match[1].trim();
        i++; // pula linha de cabeçalho
        continue;
      }

      // pula linha sem valor
      if (row[2] === 'Patriarca:' && row[3] === '[Município Lotação]') continue;

      if (currentAba) {
        if (row.every(cell => cell === '')) continue; // linha vazia

        const orgaoSigla = row[1]; // Coluna B
        const cpf = String(row[4]).replace(/\D/g, '');
        const cargo = row[5];
        const unidade = row[6];

        // pula linha de cabeçalho da tabela
        if (orgaoSigla === 'Sigla Setor' && cpf === 'CPF') continue;

        if (cpf.length === 11 && unidade && cargo) {
          const lotacao = { Cpf: cpf, Unidade: unidade, Cargo: cargo };
          
          if (!orgaosMap[orgaoSigla]) {
            orgaosMap[orgaoSigla] = [];
          }
          orgaosMap[orgaoSigla].push(lotacao);
        }
      }
    }

    // Gerar os arquivos JSON
    let arquivosGerados = 0;
    for (const orgaoSigla in orgaosMap) {
      const lotacoes = orgaosMap[orgaoSigla];

      const jsonData = {
        PatriarcaId: patriarca.idpatriarca,
        Orgao: orgaoSigla,
        Lotacoes: lotacoes,
        Comissoes: [],
        Gestores: []
      };
      
      const jsonString = JSON.stringify(jsonData, null, 2);
      const fileName = `cargalotacao_${patriarca.sigla}_${orgaoSigla}.json`;

      saveJsonToFile(jsonString, "Carga - Para Envio", fileName);
      arquivosGerados++;
    }
    
    Logger.log("gerarJsonLotacao: " + `${arquivosGerados} arquivo(s) JSON de lotação gerado(s) com sucesso!` );

    patriarca.status = "Em progresso";
    patriarca.lot_gerado = "X";
    Logger.log("gerarJsonLotacao - atualizarPatriarca! " + JSON.stringify(patriarca));

    var retAtualizarPatriarca = atualizarPatriarca(patriarca);
    
    if(retAtualizarPatriarca.success){
      Logger.log("gerarJsonLotacao - atualizarPatriarca - Atualizado com sucesso!");
      return { success: true, message: `${arquivosGerados} arquivo(s) JSON de lotação gerado(s) com sucesso!` };
    }
    else{
      Logger.log("gerarJsonLotacao - " + retAtualizarPatriarca.message);
      return { success: false, message: retAtualizarPatriarca.message };
    }

  } catch (e) {
    Logger.log("Erro em gerarJsonLotacao: " + e.message);
    return { success: false, message: e.message };
  }
}

function testeNormalizacao() {
  var cargos = [
    "Prof(a) da area de aviação",
    "Prof(a) de Educação",
    "Prof(a) de fisica",
    "Médico(a) Veterinário",
    "ASG",
    "Estagiário(a) Nível Superior",
    "Secretário(a) Municipal de Educação"
  ];

  cargos.forEach(function(cargo) {
    Logger.log(cargo + " → " + normalizarCargo(cargo));
  });
}

// Exemplo de uso
function testeOrtografia() {
  var texto = "Eu goostaria de ir ao mercaado amanhã.";
  var erros = verificarOrtografia(texto);
  Logger.log(erros);
}

// Função principal: normaliza cargo
function normalizarCargo(cargo) {
  // 1️⃣ Maiúsculas
  cargo = cargo.toUpperCase();

  // 2️⃣ Substituir abreviações
  Object.keys(DICIONARIO_ABREVIACOES).forEach(function(abrev) {
    // Escapa caracteres especiais
    var abrevRegex = abrev.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
    var regex = new RegExp("\\b" + abrevRegex + "\\b", "g");
    cargo = cargo.replace(regex, DICIONARIO_ABREVIACOES[abrev]);
  });

  // 3️⃣ Corrigir casos de Prof(a) ou similares
  cargo = cargo.replace(/\bPROF\(A\)\b/g, "PROFESSOR(A)");

  // 4️⃣ Aplicar gênero palavra por palavra
  cargo = cargo.split(" ").map(function(palavra) {
    return DICIONARIO_GENERO[palavra] || palavra;
  }).join(" ");

  return cargo;
}

function debugGetOrganogramaGoogleCharts() {
  var response = getOrganogramaCompleto();
  
  console.log('=== DEBUG getOrganogramaCompleto() ===');
  console.log('response:', response);
  console.log('response.success:', response.success);
  console.log('response.data:', response.data);
  console.log('typeof response.data:', typeof response.data);
  console.log('Array.isArray(response.data):', Array.isArray(response.data));
  console.log('response.data.length:', response.data ? response.data.length : 'N/A');
  
  if (response.data && Array.isArray(response.data)) {
    console.log('Primeiro item:', response.data[0]);
    console.log('Total itens:', response.data.length);
  }
}

function getOrganogramaGoogleCharts() {
  var response = getOrganogramaCompleto();
  
  if (!response.success || !response.data) {
    throw new Error('Estrutura inválida de getOrganogramaCompleto()');
  }
  
  // Usa listaHierarquica (mais limpa) ou chartRows (formato Google Charts)
  var organogramaData = response.data.listaHierarquica || 
                       response.data.chartRows?.map(row => ({...row[0], superior: row[1] })) || [];
  
  if (!Array.isArray(organogramaData) || organogramaData.length === 0) {
    throw new Error('Nenhum dado válido encontrado');
  }
  
  console.log(`Processando ${organogramaData.length} linhas da listaHierarquica...`);
  
  var data = [['Nome', 'Superior', 'Tooltip']];
  var count = 0;
  
  organogramaData.forEach(row => {
    // Prioriza listaHierarquica (Nome/Sigla/UnidadePai)
    if (row.Nome && row.Sigla) {
      var nome = row.Sigla.trim() + ' - ' + row.Nome.trim();
      var superior = row.UnidadePai || '';
      var tooltip = row.Nome.trim();
      data.push([nome, superior, tooltip]);
      count++;
    }
    // Fallback chartRows [[Object], 'superior']
    else if (Array.isArray(row) && row[0] && row[1]) {
      var nome = row[0].Sigla.trim() + ' - ' + row[0].Nome.trim();
      var superior = row[1];
      var tooltip = row[0].Nome.trim();
      data.push([nome, superior, tooltip]);
      count++;
    }
  });
  
  return {
    success: true,
    data: data,
    count: count,
    message: `Organograma Google Charts: ${count} funcionários`
  };
}




/**
 * Função unificada que retorna um OBJETO JAVASCRIPT direto para o frontend,
 * contendo os dados para o gráfico e para a lista hierárquica.
 */
function getOrganogramaCompleto() {
  Logger.log("Iniciando getOrganogramaCompleto");
  try {
    const patriarca = getSelectedPatriarca();
    if (!patriarca) throw new Error("Nenhum Patriarca selecionado.");

    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) throw new Error("Planilha de carga não encontrada.");

    const spreadsheetCarga = SpreadsheetApp.openById(retLerArq.fileId);
    const nomeNovaAba = patriarca.sigla + '_O';
    let sheet = spreadsheetCarga.getSheetByName(nomeNovaAba);

    if (!sheet || sheet.getLastRow() < 2) {
      return { success: true, data: { chartRows: [], listaHierarquica: [] } };
    }
    
    const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, sheet.getLastColumn()).getValues();
    Logger.log("Lendo " + data.length + " linhas da aba " + nomeNovaAba);

    // --- CORREÇÃO CRÍTICA DO MAPEAMENTO DE COLUNAS ---
    // A planilha tem: A=Nome, B=Sigla, C=Pai_Sigla
    // Os índices baseados em 0 são: 0, 1, 2
    const colMap = { nome: 0, sigla: 1, unidadePai: 2 };

    // --- Processamento para o Gráfico ---
    const chartRows = data.map(row => {
      const nome = row[colMap.nome] || '[Sem Nome]';
      const sigla = row[colMap.sigla];
      const pai = row[colMap.unidadePai] || '';
      return [{ v: sigla, f: `<b>${sigla}</b><br>${nome}` }, pai];
    });

    // --- Processamento para a Lista Hierárquica ---
    const items = data.map(row => ({
      Nome: row[colMap.nome],
      Sigla: row[colMap.sigla],
      UnidadePai: row[colMap.unidadePai] || null
    }));
    
    const itemsMap = {};
    items.forEach(item => { if (item.Sigla) itemsMap[item.Sigla] = item; });
    
    const depthCache = {};
    function getDepth(sigla) {
      if (depthCache[sigla] !== undefined) return depthCache[sigla];
      const item = itemsMap[sigla];
      if (!item || !item.UnidadePai || !itemsMap[item.UnidadePai]) return (depthCache[sigla] = 0);
      return (depthCache[sigla] = getDepth(item.UnidadePai) + 1);
    }
    
    items.forEach(item => { item.nestingLevel = item.Sigla ? getDepth(item.Sigla) : 0; });
    
    Logger.log("Processamento concluído. Retornando objeto diretamente com dados corretos.");

    return {
      success: true,
      data: { chartRows: chartRows, listaHierarquica: items }
    };

  } catch (e) {
    Logger.log("ERRO CRÍTICO em getOrganogramaCompleto: " + e.message);
    return { success: false, message: "Erro em getOrganogramaCompleto: " + e.message };
  }
}

/**
 * Lê a planilha no NOVO formato e prepara os dados para o gráfico D3.js.
 */
function getChartDataTable() {
  try {
    const patriarca = getSelectedPatriarca();
    if (!patriarca) throw new Error("Nenhum Patriarca selecionado.");

    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) throw new Error("Não foi possível abrir a planilha de carga.");
    
    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId);
    const organogramaSheet = spreadsheet.getSheetByName(patriarca.sigla + '_O');
    if (!organogramaSheet) throw new Error(`Aba de organograma '${patriarca.sigla}_O' não encontrada.`);

    const data = organogramaSheet.getDataRange().getValues();
    if (data.length <= 1) return { success: false, message: "Organograma salvo está vazio." };

    const chartRows = [];
    // Pula o cabeçalho
    for (let i = 1; i < data.length; i++) {
      const nome = data[i][0];
      const sigla = data[i][1];
      const paiSigla = data[i][2] || '';
      
      // Formato do Google Charts: [ {v: 'ID_UNICO', f: 'HTML_DO_LABEL'}, 'ID_DO_PAI', 'TOOLTIP' ]
     
      chartRows.push([
        { v: sigla, f: `${sigla} - ${nome}` },
        paiSigla, // O ID do pai
        nome      // O Tooltip
      ]);
    }

    return { success: true, dataString: JSON.stringify(chartRows) };

  } catch (e) {
    Logger.log("Erro em getChartDataTable: " + e.message);
    return { success: false, message: e.message };
  }
}

function encodeRFC2047(str) {
  return "=?UTF-8?B?" + Utilities.base64Encode(str, Utilities.Charset.UTF_8) + "?=";
}

/**
 * 
 * Tratamento de arquivos
 * 
*/

function saveTxtToFile(textContent, folderName, fileName) {
  try {
    const rootFolder = DriveApp.getRootFolder();
    let subFolders = rootFolder.getFoldersByName(folderName);
    let targetFolder = subFolders.hasNext() ? subFolders.next() : rootFolder.createFolder(folderName);

    const existingFiles = targetFolder.getFilesByName(fileName);
    while (existingFiles.hasNext()) {
      existingFiles.next().setTrashed(true);
    }

    targetFolder.createFile(fileName, textContent, 'text/plain');
    Logger.log(`Arquivo '${fileName}' salvo com sucesso.`);
  } catch (e) {
    Logger.log("Erro ao salvar o arquivo TXT: " + e.message);
  }
}

function saveJsonToFile(jsonContent, folderName, fileName) {
  try {
    const rootFolder = DriveApp.getRootFolder();
    let subFolders = rootFolder.getFoldersByName(folderName);
    let targetFolder = subFolders.hasNext() ? subFolders.next() : rootFolder.createFolder(folderName);

    const existingFiles = targetFolder.getFilesByName(fileName);
    while (existingFiles.hasNext()) {
      existingFiles.next().setTrashed(true);
    }

    targetFolder.createFile(fileName, jsonContent, 'application/json');
    Logger.log(`Arquivo '${fileName}' salvo com sucesso.`);
  } catch (e) {
    Logger.log("Erro ao salvar o arquivo JSON: " + e.message);
  }
}

function testeGetJsonFilesAndContents(){

  // Teste para buscar arquivos do tipo organograma
  let resultOrg = getJsonFilesAndContents("Carga - Para Envio", "organograma", "PMALE");
  Logger.log("testeGetJsonFilesAndContents - Organograma: " + JSON.stringify(resultOrg));

  // Teste para buscar arquivos do tipo lotação
  let resultLot = getJsonFilesAndContents("Carga - Para Envio", "lotacao", "PMALE");
  Logger.log("testeGetJsonFilesAndContents - Lotação: " + JSON.stringify(resultLot));
}

function getJsonFilesAndContents(folderName, fileType, sigla) {
  var msg = '';
  var fileNames = [];

  // Verifica se o tipo de arquivo é válido
  if (fileType !== 'organograma' && fileType !== 'lotacao') {
    msg = 'Erro em getJsonFiles: o tipo do arquivo não é esperado!';
    Logger.log(msg);
    return { success: false, message: msg, data: [] };
  }

  try {
    var data = [];
    const organogramaPrefix = 'cargadeorgaos_' + sigla; // Prefixo esperado para organograma
    const lotacaoPrefix = 'cargalotacao_' + sigla;      // Prefixo esperado para lotação

    // Pega a pasta raiz e encontra a subpasta pelo nome
    const rootFolder = DriveApp.getRootFolder();
    let subFolders = rootFolder.getFoldersByName(folderName);

    if (!subFolders.hasNext()) {
      msg = 'Erro em getJsonFiles: pasta não encontrada!';
      Logger.log(msg);
      return { success: false, message: msg, data: [] };
    }

    let targetFolder = subFolders.next();

    // Pega todos os arquivos da pasta
    let files = targetFolder.getFiles();
    let existingFiles = [];

    // Filtra pelos nomes que começam com o prefixo desejado
    while (files.hasNext()) {
      let file = files.next();
      let fileName = file.getName();

      if (
        (fileType === 'organograma' && fileName.indexOf(organogramaPrefix) === 0) ||
        (fileType === 'lotacao' && fileName.indexOf(lotacaoPrefix) === 0)
      ) {

        var fileInfo = {
          id: file.getId(),
          name: fileName
        }

        var dataFile = readJsonFromDrive(fileInfo);

        fileNames.push(fileName);

        existingFiles.push({
          id: file.getId(),
          name: fileName,
          content: dataFile.success ? dataFile.datafile : ''
        });
      }
    }

    if (existingFiles.length === 0) {
      msg = 'Nenhum arquivo encontrado com o prefixo informado.';
    }

    return { success: true, message: msg, filenames: fileNames, data: existingFiles };
  } catch (error) {
    msg = 'Erro em getJsonFiles: ' + error.message;
    Logger.log(msg);
    return { success: false, message: error.message, fileNames: [], data: [] };
  }
}



function testeGetJsonFiles(){

  // Teste para buscar arquivos do tipo organograma
  let resultOrg = getJsonFiles("Carga - Para Envio", "organograma", "PMALE");
  Logger.log("Organograma: " + JSON.stringify(resultOrg));

  // Teste para buscar arquivos do tipo lotação
  let resultLot = getJsonFiles("Carga - Para Envio", "lotacao", "PMALE");
  Logger.log("Lotação: " + JSON.stringify(resultLot));
}

function getJsonFiles(folderName, fileType, sigla) {
  var msg = '';

  // Verifica se o tipo de arquivo é válido
  if (fileType !== 'organograma' && fileType !== 'lotacao') {
    msg = 'Erro em getJsonFiles: o tipo do arquivo não é esperado!';
    Logger.log(msg);
    return { success: false, message: msg, data: [] };
  }

  try {
    var data = [];
    const organogramaPrefix = 'cargadeorgaos_' + sigla; // Prefixo esperado para organograma
    const lotacaoPrefix = 'cargalotacao_' + sigla;      // Prefixo esperado para lotação

    // Pega a pasta raiz e encontra a subpasta pelo nome
    const rootFolder = DriveApp.getRootFolder();
    let subFolders = rootFolder.getFoldersByName(folderName);

    if (!subFolders.hasNext()) {
      msg = 'Erro em getJsonFiles: pasta não encontrada!';
      Logger.log(msg);
      return { success: false, message: msg, data: [] };
    }

    let targetFolder = subFolders.next();

    // Pega todos os arquivos da pasta
    let files = targetFolder.getFiles();
    let existingFiles = [];

    // Filtra pelos nomes que começam com o prefixo desejado
    while (files.hasNext()) {
      let file = files.next();
      let fileName = file.getName();

      if (
        (fileType === 'organograma' && fileName.indexOf(organogramaPrefix) === 0) ||
        (fileType === 'lotacao' && fileName.indexOf(lotacaoPrefix) === 0)
      ) {
        existingFiles.push({
          id: file.getId(),
          name: fileName,
          url: file.getUrl(),
          fileType: fileType
        });
      }
    }

    if (existingFiles.length === 0) {
      msg = 'Nenhum arquivo encontrado com o prefixo informado.';
    }

    return { success: true, message: msg, data: existingFiles };
  } catch (error) {
    msg = 'Erro em getJsonFiles: ' + error.message;
    Logger.log(msg);
    return { success: false, message: error.message, data: [] };
  }
}

function readJsonFromDrive(fileInfo) {
  var msg = '';

  // Validação dos parâmetros recebidos
  if (!fileInfo || !fileInfo.id) {
    msg = 'Erro em readJsonFromDrive: As informações do arquivo não foram passadas corretamente!';
    return { success: false, message: msg, datafile: '' };
  }

  try {
    // Recupera o arquivo JSON do Google Drive pelo ID
    var file = DriveApp.getFileById(fileInfo.id);

    // Lê o conteúdo do arquivo como string
    var jsonString = file.getBlob().getDataAsString();

    // Converte a string em objeto JSON
    var jsonData = JSON.parse(jsonString);

    // Log do conteúdo formatado
    //Logger.log("Conteúdo JSON:\n" + JSON.stringify(jsonData, null, 2));

    // Retorna o objeto JSON
    return { success: true, message: msg, datafile: jsonData };

  } catch (error) {
    msg = 'Erro em readJsonFromDrive: ' + error.message;
    Logger.log(msg);
    return { success: false, message: msg, datafile: '' };
  }
}

/**
  Funcionamento da API de carga

  Tadeu PRODEST: basicamente como está o funcionamento da carga do cargarh hoje em dia
  Tadeu PRODEST: 1 - gera um token ( que tem validade 1h) que vai servir de autorização
  Tadeu PRODEST: 2 - envia o json que faz validações basicas
  Tadeu PRODEST: 2.1 - se falhar te avisar na hora
  Tadeu PRODEST: 2.2 - se aceitar vai para a fila
  Tadeu PRODEST: 3 - voce fica batendo no endpoint de status para ver se terminou com sucesso ou se deu erro
  Tadeu PRODEST: 3.1 - se terminou com sucesso, maravilha
  Tadeu PRODEST: 3.2 - se deu erro, ele te avisa o problema para você corrigir e mandar de novo
  Tadeu PRODEST: No geral: vai ser um carga destrutiva, inicialmente é sem problema porque está vazio
  Tadeu PRODEST: se já tiver dado não consigo garantir que nada anterior será mantido
  Alexandre Wanick Mohamad: se passar de 1 hora, gero novo token
  Tadeu PRODEST: sim, mas em geral nem precisa porque vc manda em 2 segundos
  Tadeu PRODEST: o caso de vocês que é bem exporádico e rápido, eu nem sugiro fazer aplicação para gerar o token
  Tadeu PRODEST: manda pelo postman ou pelo próprio swagger
  Tadeu PRODEST: o admin, na parte de configuração de cliente tem um botão que gera esse token de 1h de validade
  Alexandre Wanick Mohamad: eu já fiz uma app para leitura, validação e geração dos arquivos json de organograma e lotação por secretaria
  Tadeu PRODEST: é manual, mas vai acontecer o que? umas 20 vezes na vida?
  Tadeu PRODEST: mais importante é garantir que os json estão sendo gerados da forma correta
  Tadeu PRODEST: só o envio, mas se quiser automatizar também nào tem problema
  Alexandre Wanick Mohamad: eu fiz o app, pois o pessoal aqui precisa conferir algumas coisas
  Tadeu PRODEST: é coisa de 2 linhas de código para gerar o token
*/

function deleteTokenCacheTime(idPatriarca){
  
  const cache = CacheService.getScriptCache();
  let tokenData = cache.get("cargarh_token_" + idPatriarca);
  
  if (tokenData) {
    cache.remove("cargarh_token_" + idPatriarca);
  }
}

/**
 * Verifica o cache ou a planilha por um token ativo.
 * Adiciona validações para evitar erros em linhas vazias.
 * @param {string} idPatriarca O ID do patriarca.
 * @returns {{success: boolean, message: string, token?: string, expiresIn?: number}}
 */
function checkTokenCacheTime(idPatriarca) {
  // 1. Tenta buscar no cache primeiro (mais rápido)
  try {
    const cache = CacheService.getScriptCache();
    const tokenDataJSON = cache.get(`cargarh_token_${idPatriarca}`);
    if (tokenDataJSON) {
      const tokenData = JSON.parse(tokenDataJSON);
      const agora = Math.floor(Date.now() / 1000);
      const tempoRestante = tokenData.expiraEm - agora;

      if (tempoRestante > 60) { // Adiciona uma margem de segurança de 1 minuto
        Logger.log(`Token válido encontrado no cache para ${idPatriarca}.`);
        return { success: true, message: 'Token do cache é válido.', token: tokenData.token, expiresIn: tempoRestante };
      }
    }
  } catch (e) {
    Logger.log(`Erro ao ler token do cache: ${e.message}`);
  }

  // 2. Se não encontrou no cache, tenta buscar na planilha (fallback)
  try {
    const sheet = SpreadsheetApp.openById(verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM).fileId).getSheetByName(CONFIG.SHEET_LISTAS);
    const range = sheet.getRange(CONFIG.TAB_PATRIARCA);
    const values = range.getValues();

    // Mapeamento de colunas baseado no intervalo G:N
    const COL_ID_INDEX = 2;       // Coluna I
    const COL_TOKEN_INDEX = 6;    // Coluna M
    const COL_DATA_INDEX = 7;     // Coluna N

    for (let i = 1; i < values.length; i++) {
      const row = values[i];
      // ---- PONTO DA CORREÇÃO IMPORTANTE ----
      // Ignora linhas vazias ou sem ID para evitar erros
      if (!row[COL_ID_INDEX] || row[COL_ID_INDEX].toString().trim() === '') {
        continue;
      }
      
      if (row[COL_ID_INDEX].toString() === idPatriarca.toString() && row[COL_TOKEN_INDEX]) {
        const dataCriacao = new Date(row[COL_DATA_INDEX]).getTime();
        if (isNaN(dataCriacao)) continue; // Pula se a data for inválida

        const agora = Date.now();
        const idadeTokenMs = agora - dataCriacao;
        const tempoRestanteMs = (3600 * 1000) - idadeTokenMs; // Assume que o token dura 1h

        if (tempoRestanteMs > 60000) { // Se ainda resta mais de 1 minuto
          const token = row[COL_TOKEN_INDEX];
          const tempoRestanteSeg = Math.floor(tempoRestanteMs / 1000);
          
          // Re-armazena no cache para otimizar a próxima chamada
          setNewToken(idPatriarca, token, tempoRestanteSeg);
          Logger.log(`Token válido recuperado da planilha para ${idPatriarca}.`);
          return { success: true, message: 'Token da planilha é válido.', token: token, expiresIn: tempoRestanteSeg };
        }
        break; // Achou o patriarca, mas o token está expirado, então para a busca.
      }
    }
  } catch (e) {
    Logger.log(`Erro ao buscar token na planilha: ${e.message}`);
  }

  // 3. Se não encontrou em nenhum lugar
  return { success: false, message: 'Nenhum token válido encontrado no cache ou na planilha.' };
}

function setNewToken(idPatriarca, newToken, expiresIn) {
  const cache = CacheService.getScriptCache();
  const agora = Math.floor(Date.now() / 1000);

  // Se não veio expiresIn, assume 1h
  expiresIn = expiresIn || 3600;

  // Coloca no cache (diminuindo 1 minuto para segurança)
  const cacheSeconds = Math.max(60, expiresIn - 60);
  const expiraEm = agora + cacheSeconds;

  cache.put(
    "cargarh_token_" + idPatriarca,
    JSON.stringify({ token: newToken, expiraEm }),
    cacheSeconds
  );

  Logger.log("Token obtido e salvo no cache. Expira em " + cacheSeconds + " segundos.");
  return {
    success: true,
    errorCode: 0,
    message: "Token obtido e salvo no cache. Expira em " + cacheSeconds + " segundos.",
    token: newToken,
    expiresIn: cacheSeconds
  };
}

/**
 * Função genérica para chamar APIs com tratamento de erros.
 * @param {string} url - URL completa da API
 * @param {object} options - Objeto de configuração para UrlFetchApp
 * @returns {object} { success, errorCode, message, responseText, statusCode }
 */
function fetchFromAPI_Sync(url, options) {
  // Garante que exceções HTTP (4xx, 5xx) não parem o script, permitindo-nos ler o código de status.
  options.muteHttpExceptions = true;

  let response, statusCode, responseHeaders, responseContent, body, msg = '', bodyParsed = {};

  Logger.log('Chamada fetchFromAPI_Sync');
  Logger.log('url: ' + url);
  Logger.log('options (modificado): ' + JSON.stringify(options));

  for (let attempt = 0; attempt < CONFIG.MAX_RETRIES; attempt++) {
    try {
      response = UrlFetchApp.fetch(url, options);
      statusCode = response.getResponseCode();
      responseHeaders = response.getAllHeaders();
      responseContent = response.getContentText(); // Obter como texto
      
      // Tenta parsear o JSON, mas permite corpo vazio ou não-JSON
      try {
        if (responseContent) {
          bodyParsed = JSON.parse(responseContent);
          body = responseContent; // Mantém o texto original para log e retorno
        } else {
          bodyParsed = {};
          body = "";
        }
      } catch (e) {
        Logger.log('Resposta não era JSON válido: ' + responseContent);
        bodyParsed = {};
        body = responseContent; // Salva a resposta não-JSON
      }

      Logger.log('Tentativa ' + (attempt + 1) + ': StatusCode ' + statusCode);
      Logger.log('response.body: ' + body);

      // 1. Sucesso (200 ou 201)
      if (statusCode === CONFIG.RESPONSE_CODE_SUCCESS_GENERIC || statusCode === CONFIG.RESPONSE_CODE_SUCCESS_CARGA) {
        return {
          success: true,
          errorCode: 0,
          message: CONFIG.RESPONSE_CODE_SUCCESS_MSG,
          responseText: body,
          statusCode: statusCode
        };
      }

      // 2. Erro 429 (Too Many Requests) - Tentar novamente
      if (statusCode === CONFIG.RESPONSE_CODE_TOO_MANY_REQUESTS) {
        if (attempt >= CONFIG.MAX_RETRIES - 1) {
          // Última tentativa falhou, sair do loop para retornar o erro
          msg = CONFIG.RESPONSE_CODE_TOO_MANY_REQUESTS_MSG;
          break;
        }

        let waitTimeMs = 0;
        const retryAfterHeader = responseHeaders['Retry-After'] || responseHeaders['retry-after'];

        if (retryAfterHeader) {
          // Servidor especificou um tempo de espera (em segundos)
          const waitSeconds = parseInt(retryAfterHeader, 10);
          waitTimeMs = (waitSeconds * 1000) + (Math.random() * 1000); // Adiciona jitter
          Logger.log('Erro 429. Cabeçalho Retry-After encontrado: ' + waitSeconds + 's. Aguardando ' + waitTimeMs + 'ms.');
        } else {
          // Calcular exponential backoff
          waitTimeMs = (CONFIG.INITIAL_BACKOFF_MS * Math.pow(2, attempt)) + (Math.random() * 1000); // Adiciona jitter
          Logger.log('Erro 429. Sem Retry-After. Aguardando ' + waitTimeMs + 'ms (Backoff Exponencial).');
        }

        Utilities.sleep(waitTimeMs);
        continue; // Próxima tentativa do loop 'for'
      }

      // 3. Outros Erros (400, 401, 500, etc.) - Não tentar novamente
      // Sai do loop para formatar e retornar o erro
      break;

    } catch (error) {
      // Captura erros de rede (ex: timeout, falha de DNS, serviço indisponível)
      Logger.log("Erro de rede em fetchFromAPI_Sync (Tentativa " + (attempt + 1) + "): " + error.message);
      statusCode = -1; // Código interno para erro de rede/timeout
      msg = error.message;
      body = '';
      
      if (attempt >= CONFIG.MAX_RETRIES - 1) {
        // Última tentativa falhou
        break;
      }

      // Tentar novamente em caso de erro de rede usando backoff
      const waitTimeMs = (CONFIG.INITIAL_BACKOFF_MS * Math.pow(2, attempt)) + (Math.random() * 1000);
      Logger.log('Erro de rede. Aguardando ' + waitTimeMs + 'ms antes de tentar novamente.');
      Utilities.sleep(waitTimeMs);
      // 'continue' é implícito
    }
  }

  // Se o loop terminar (por 'break' ou 'max_retries'), formatamos a mensagem de erro final.

  if (statusCode === -1) {
    // A mensagem 'msg' já foi definida no bloco catch de erro de rede.
  } else if (bodyParsed && bodyParsed.title && bodyParsed.detail) {
    // Formato de erro específico (JSON com título e detalhe)
    msg = 'Erro na chamada do método da API! ErrorCode: ' + statusCode + ', Título: ' + bodyParsed.title + ', Detalhe: ' + bodyParsed.detail;
  } else {
    // Tratamento de erros de chamada a API
    switch (statusCode) {
      case CONFIG.RESPONSE_CODE_BAD_REQUEST:
        msg = CONFIG.RESPONSE_CODE_BAD_REQUEST_MSG;
        break;
      case CONFIG.RESPONSE_CODE_UNAUTHORIZED: 
        msg = CONFIG.RESPONSE_CODE_UNAUTHORIZED_MSG; 
        break;
      case CONFIG.RESPONSE_CODE_FORBIDDEN:
        msg = CONFIG.RESPONSE_CODE_FORBIDDEN_MSG; 
        break;
      case CONFIG.RESPONSE_CODE_NOT_FOUND:
        msg = CONFIG.RESPONSE_CODE_NOT_FOUND_MSG;
        break;
      case CONFIG.RESPONSE_CODE_NOT_ACCEPTABLE:
        msg = CONFIG.RESPONSE_CODE_NOT_ACCEPTABLE_MSG;
        break;
      case CONFIG.RESPONSE_CODE_REQUEST_TIMEOUT:
        msg = CONFIG.RESPONSE_CODE_REQUEST_TIMEOUT_MSG;
        break;
      case CONFIG.RESPONSE_CODE_CONFLICT: 
        msg = CONFIG.RESPONSE_CODE_CONFLICT_MSG;
        break;
      case CONFIG.RESPONSE_CODE_UNPROCESSABLE_ENTITY:
        msg = CONFIG.RESPONSE_CODE_UNPROCESSABLE_ENTITY_MSG;
        break;
      case CONFIG.RESPONSE_CODE_METHOD_NOT_ALLOWED:
        msg = CONFIG.RESPONSE_CODE_METHOD_NOT_ALLOWED_MSG;
        break;
      case CONFIG.RESPONSE_CODE_TOO_MANY_REQUESTS:
        msg = CONFIG.RESPONSE_CODE_TOO_MANY_REQUESTS_MSG;
        break;
      case CONFIG.RESPONSE_CODE_INTERNAL_SERVER_ERROR:
        msg = CONFIG.RESPONSE_CODE_INTERNAL_SERVER_ERROR_MSG;
        break;
      case CONFIG.RESPONSE_CODE_BAD_GATEWAY:
        msg = CONFIG.RESPONSE_CODE_BAD_GATEWAY_MSG;
        break;
      case CONFIG.RESPONSE_CODE_SERVICE_UNAVAILABLE:
        msg = CONFIG.RESPONSE_CODE_SERVICE_UNAVAILABLE_MSG;
        break;
      case CONFIG.RESPONSE_CODE_GATEWAY_TIMEOUT:
        msg = CONFIG.RESPONSE_CODE_GATEWAY_TIMEOUT_MSG; 
        break;
      default:
        // Se a msg ainda estiver vazia, define um padrão
        if (!msg) {
          msg = "Erro inesperado ao chamar a API. StatusCode: " + statusCode;
        }
    }
  }

  // Retorno final de falha
  return {
    success: false,
    errorCode: statusCode,
    message: msg,
    responseText: body, // Retorna o último corpo de resposta recebido (pode ser o do erro)
    statusCode: statusCode
  };
}


/**
 * Obtém o token de acesso da API, com verificação explícita
 * de cada etapa e tratamento centralizado de erros.
 *
 * @param {string} idPatriarca O ID do patriarca para o qual o token será gerado.
 * @returns {{success: boolean, message: string, token?: string, expiresIn?: number}}
 */
function getAccessToken(idPatriarca) {
  const logContext = `getAccessToken(ID: ${idPatriarca})`;
  try {
    // Etapa 1: Verificar o cache antes de fazer uma nova chamada de rede.
    Logger.log(`${logContext}: Verificando token no cache...`);
    const respTokenCache = checkTokenCacheTime(idPatriarca);
    if (respTokenCache.success) {
      Logger.log(`${logContext}: Token válido encontrado no cache.`);
      return respTokenCache;
    }
    Logger.log(`${logContext}: Token não encontrado ou expirado no cache. Gerando novo...`);

    // Etapa 2: Preparar e executar a chamada à API para obter um novo token.
    const url = CONFIG.URL_GET_TOKEN;
    const payload = {
      'grant_type': 'client_credentials',
      'client_id': CONFIG.CLIENT_ID_CARGARH,
      'client_secret': CONFIG.CLIENT_SECRET_CARGARH,
      'scope': CONFIG.CLIENT_SCOPE_CARGARH
    };
    const options = { 'method': 'POST', 'payload': payload, 'muteHttpExceptions': true };

    const response = UrlFetchApp.fetch(url, options);
    const responseCode = response.getResponseCode();
    const responseText = response.getContentText();

    // CHECAGEM DE RETORNO 1: A chamada à API falhou?
    if (responseCode !== 200) {
      throw new Error(`Falha na API de autenticação. Código: ${responseCode}. Resposta: ${responseText}`);
    }

    // Etapa 3: Analisar a resposta e extrair o token.
    const responseData = JSON.parse(responseText);
    const token = responseData.access_token;
    const expiresIn = responseData.expires_in || 3600;

    // CHECAGEM DE RETORNO 2: O token veio na resposta?
    if (!token) {
      throw new Error('A resposta da API não continha um access_token válido.');
    }
    Logger.log(`${logContext}: Novo token obtido com sucesso.`);

    // Etapa 4: Salvar o novo token no cache.
    const cacheSaveResult = setNewToken(idPatriarca, token, expiresIn);
    // CHECAGEM DE RETORNO 3: O token foi salvo no cache?
    if (!cacheSaveResult.success) {
      // Este não é um erro fatal, mas é importante registrar.
      Logger.log(`AVISO: ${logContext}: Falha ao salvar o novo token no cache.`);
    }

    // Etapa 5: Atualizar o status do patriarca na planilha.
    const updateResult = atualizarStatusPatriarca(idPatriarca, 'Enviando Carga');
    // CHECAGEM DE RETORNO 4: A planilha foi atualizada?
    // (A função 'atualizarStatusPatriarca' já contém seu próprio try/catch, então apenas logamos).
    Logger.log(`${logContext}: Tentativa de atualização do status do patriarca concluída.`);
    
    // Etapa 6: Retornar sucesso com o novo token.
    return {
      success: true,
      message: 'Token obtido e cache atualizado.',
      token: token,
      expiresIn: expiresIn
    };

  } catch (error) {
    // Ponto central de captura para qualquer exceção lançada nas etapas acima.
    const errorMessage = `ERRO CRÍTICO em ${logContext}: ${error.message}`;
    Logger.log(`${errorMessage} Stack: ${error.stack}`);
    return { success: false, message: error.message };
  }
}

function formatDateTime(date) {
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
  const year = date.getFullYear();
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');

  var dateUS = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  var datePTbr = `${day}-${month}-${year} ${hours}:${minutes}:${seconds}`;  

  return { normal: datePTbr, invertida: dateUS, dia: day, mes: month, ano: year, hora: hours, minuto: minutes, segundo: seconds };
}

/**
 * Registra o envio inicial na aba 'Status_Envio'.
 * @param {object} patriarca - O objeto patriarca completo.
 * @param {string} guidCarga - O GUID da carga.
 */

function registrarEnvioInicial(patriarca, guidCarga) {
  try {
    if (!patriarca || !patriarca.idpatriarca) {
      throw new Error("Objeto Patriarca ou seu ID é inválido ao registrar o envio inicial.");
    }

    const nomeAba = CONFIG.SHEET_STATUS_ENVIO;
    const sheet = SpreadsheetApp.openById(verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM).fileId).getSheetByName(nomeAba);
    if (!sheet) throw new Error(`Aba '${nomeAba}' não encontrada.`);

    const statusInicialString = StatusCargaMap[CONFIG.STATUS_CARGA.AGUARDANDO_ORGANOGRAMA_CARGA_INICIAL] || 'Aguardando';

    sheet.appendRow([
      patriarca.idpatriarca, patriarca.nome, new Date(),
      CONFIG.TIPO_CARGA.INICIAL_ORGANOGRAMA, 'organograma',
      CONFIG.JSON_PATTERNS.ORGANOGRAMA.replace('{sigla}', patriarca.sigla),
      guidCarga, statusInicialString, false, '', 0, '', 'Envio realizado pela interface.'
    ]);

    Logger.log(`Registro de envio inicial criado para o Patriarca ID ${patriarca.idpatriarca}.`);
  } catch (error) {
    Logger.log(`ERRO em registrarEnvioInicial: ${error.message}`);
    throw error;
  }
}

/**
 * VERIFICA O STATUS DA CARGA, ATUALIZA A PLANILHA E RETORNA DADOS FORMATADOS PARA O FRONTEND.
 *
 * @param {string} guidCarga O GUID da carga a ser verificada.
 * @param {string} idPatriarca O ID do patriarca para obter o token.
 * @param {string} ambiente O ambiente ('HML' ou 'PRD').
 * @returns {{success: boolean, message: string, data?: object}} Objeto com dados para a UI.
 */
function verificarStatusCarga(guidCarga, idPatriarca, ambiente) {
  const logContext = `verificarStatusCarga(GUID: ${guidCarga})`;
  try {
    // A lógica de obtenção de token e chamada à API permanece a mesma.
    const patriarcaResponse = getPatriarca(idPatriarca);
    if (!patriarcaResponse.success) throw new Error(`Patriarca com ID ${idPatriarca} não encontrado.`);
    
    const tokenResponse = garantirTokenValido(patriarcaResponse.dados, ambiente);
    if (!tokenResponse.success) throw new Error(`Falha ao obter token: ${tokenResponse.message}`);
    
    const baseUrl = ambiente === 'HML' ? CONFIG.URL_CARGA_HML : CONFIG.URL_CARGA_PRD;
    const endpoint = CONFIG.API_ENDPOINTS.STATUS.replace('{guid}', guidCarga);
    const url = baseUrl + CONFIG.CARGA_V3 + endpoint;
    const options = { method: 'GET', headers: { 'Authorization': `Bearer ${tokenResponse.token}` }, muteHttpExceptions: true };

    const response = UrlFetchApp.fetch(url, options);
    const responseCode = response.getResponseCode();
    const responseText = response.getContentText();

    if (responseCode !== 200) {
      throw new Error(`Erro na API (${responseCode}): ${responseText}`);
    }

    const responseData = JSON.parse(responseText);
    const numericStatus = responseData.status;

    // Prepara os dados para a planilha
    const uiData = StatusCargaUIData[numericStatus] || { ...StatusCargaUIData.default, status: `Status ${numericStatus}` };
    const statusDataParaPlanilha = {
      status: uiData.status,
      finalizada: responseData.finalizada,
      mensagemErro: responseData.mensagemErro || '',
      observacoes: `Verificação automática em ${new Date().toLocaleString('pt-BR')}.`
    };
    
    // Atualiza a planilha em segundo plano
    atualizarStatusNaPlanilha(guidCarga, statusDataParaPlanilha);
    
    if (responseData.finalizada) {
      const novoStatus = (numericStatus === 6) ? 'Erro no Envio' : 'Carga processada';
      atualizarStatusPatriarca(idPatriarca, novoStatus);
    }
    
    // Prepara e retorna o objeto de dados para o frontend
    const dataParaFrontend = {
      ...uiData,
      finalizado: responseData.finalizada,
      mensagemErro: responseData.mensagemErro
    };

    return { success: true, message: 'Status obtido com sucesso.', data: dataParaFrontend };

  } catch (e) {
    const errorMsg = `Exceção em '${logContext}': ${e.message}`;
    Logger.log(`${errorMsg} Stack: ${e.stack}`);
    return { success: false, message: e.message, data: null };
  }
}

/**
 * Localiza a linha do patriarca pelo ID e atualiza a coluna de Status.
 *
 * @param {string} patriarcaId O ID do patriarca a ser atualizado.
 * @param {string} novoStatus O novo status a ser definido.
 */
function atualizarStatusPatriarca(patriarcaId, novoStatus) {
    try {
        // --- CORREÇÃO: Validação de entrada ---
        if (!patriarcaId) {
            Logger.log(`ERRO em atualizarStatusPatriarca: patriarcaId é nulo ou indefinido. Não é possível atualizar o status.`);
            return;
        }

        const sheet = SpreadsheetApp.openById(verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM).fileId).getSheetByName(CONFIG.SHEET_LISTAS);
        const range = sheet.getRange(CONFIG.TAB_PATRIARCA);
        const values = range.getValues();
        const startRow = range.getRow();

        const COL_ID_INDEX = 2; // Coluna I (G=0, H=1, I=2)
        const COL_STATUS_INDEX = 3; // Coluna J (G=0, H=1, I=2, J=3)

        for (let i = 1; i < values.length; i++) {
            if (values[i][COL_ID_INDEX] && values[i][COL_ID_INDEX].toString() === patriarcaId.toString()) { 
                const linhaParaAtualizar = startRow + i;
                sheet.getRange(linhaParaAtualizar, range.getColumn() + COL_STATUS_INDEX).setValue(novoStatus); 
                Logger.log(`Status do patriarca ${patriarcaId} (linha ${linhaParaAtualizar}) atualizado para '${novoStatus}'.`);
                return;
            }
        }
        Logger.log(`Patriarca com ID ${patriarcaId} não encontrado para atualização de status.`);
    } catch(e) {
        Logger.log(`ERRO em atualizarStatusPatriarca para ID ${patriarcaId}: ${e.message}`);
    }
}

/**
 * FUNÇÃO HÍBRIDA E DEFINITIVA para gerenciar a planilha 'Status_Envio'.
 * - Se 'guidCarga' for fornecido, ATUALIZA a linha existente.
 * - Se 'guidCarga' for nulo, CRIA uma nova linha para registrar uma falha pré-envio.
 *
 * @param {string | null} guidCarga O GUID da carga para localizar a linha, ou null para criar uma nova.
 * @param {object} statusData Objeto com os dados de status. O conteúdo esperado varia
 *                            dependendo se é uma criação ou atualização.
 * @returns {{success: boolean, message: string}} Resultado da operação.
 */
function atualizarStatusNaPlanilha(guidCarga, statusData) {
  try {
    const nomeAba = CONFIG.SHEET_STATUS_ENVIO;
    
    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) {
      throw new Error(`Erro ao abrir planilha: ${CONFIG.SPREADSHEET_PARAM}`);
    }
    
    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId);
    const sheet = spreadsheet.getSheetByName(nomeAba);
    if (!sheet) {
      throw new Error(`Aba '${nomeAba}' não encontrada.`);
    }

    if (guidCarga) {
      // CENÁRIO 1: ATUALIZAR linha existente pelo GUID
      const range = sheet.getRange(CONFIG.TAB_STATUS_CARGA);
      const values = range.getValues();
      let linhaEncontrada = -1;
      let tentativasAtuais = 0;

      for (let i = 1; i < values.length; i++) {
        if (values[i][6] === guidCarga) { // Coluna G (índice 6) é GuidCarga
          linhaEncontrada = i + range.getRow(); // Número real da linha
          tentativasAtuais = Number(values[i][10]) || 0;
          break;
        }
      }

      if (linhaEncontrada === -1) {
        throw new Error(`Carga com GUID ${guidCarga} não encontrada para atualização.`);
      }

      sheet.getRange(linhaEncontrada, 8).setValue(statusData.status);              // H - StatusCarga
      sheet.getRange(linhaEncontrada, 9).setValue(statusData.finalizada);          // I - StatusFinalizado
      sheet.getRange(linhaEncontrada, 10).setValue(statusData.mensagemErro || ''); // J - MensagemErro
      sheet.getRange(linhaEncontrada, 11).setValue(tentativasAtuais + 1);          // K - TentativasVerificacao
      sheet.getRange(linhaEncontrada, 12).setValue(new Date());                    // L - DataUltimaVerificacao
      sheet.getRange(linhaEncontrada, 13).setValue(statusData.observacoes || '');  // M - ObservacoesAdicionais
      
      Logger.log(`Linha ${linhaEncontrada} (GUID: ${guidCarga}) atualizada.`);

    } else {
      // CENÁRIO 2: CRIAR nova linha para falha pré-envio
      const patriarca = statusData.patriarca;
      const newRow = [
        patriarca.idpatriarca,          // A - IdPatriarca
        patriarca.nome,                 // B - NomePatriarca
        new Date(),                     // C - DataHoraEnvio (da falha)
        statusData.tipoCarga,           // D - TipoCarga
        'N/A',                          // E - TipoArquivo
        statusData.nomeArquivo || 'N/A',// F - NomeArquivo
        'FALHA ANTES DO ENVIO',       // G - GuidCarga
        statusData.status,              // H - StatusCarga
        true,                           // I - StatusFinalizado (a tentativa de envio falhou e foi finalizada)
        statusData.mensagemErro,        // J - MensagemErro
        1,                              // K - TentativasVerificacao
        new Date(),                     // L - DataUltimaVerificacao
        'Falha registrada antes de obter GUID da API.'  // M - ObservacoesAdicionais
      ];
      sheet.appendRow(newRow);
      Logger.log(`Nova linha de falha adicionada para o Patriarca ${patriarca.nome}.`);
    }

    return { success: true, message: 'Planilha de status atualizada.' };

  } catch (error) {
    Logger.log(`Erro em atualizarStatusNaPlanilha: ${error.message} Stack: ${error.stack}`);
    return { success: false, message: `Erro ao atualizar planilha: ${error.message}` };
  }
}

/**
 * Monitora o status de uma carga na API e atualiza a planilha.
 * É chamada periodicamente pelo frontend.
 *
 * @param {string} guid O GUID da carga a ser verificada.
 * @param {object} patriarca O objeto do patriarca.
 * @param {string} ambiente O ambiente de destino ('HML' ou 'PRD').
 * @returns {{success: boolean, message: string, data?: {status: number, finalizada: boolean, comErro: boolean, mensagemErro?: string}}}
 */
function monitorarStatusCarga(guid, patriarca, ambiente) {
  try {
    // Reutiliza sua função para verificar o status na API
    const resultadoVerificacao = verificarStatusCarga(guid, ambiente, patriarca.idpatriarca);
    
    if (!resultadoVerificacao.success) {
      Logger.log(`Falha ao verificar status para GUID ${guid}: ${resultadoVerificacao.message}`);
      // Não atualizamos a planilha se a própria verificação falhar, para não sobrescrever o último status válido.
      return { success: false, message: `Falha na consulta de status: ${resultadoVerificacao.message}` };
    }

    const statusApi = resultadoVerificacao.data;
    
    // Reutiliza sua função para atualizar a aba Status_Envio
    atualizarStatusNaPlanilha(guid, { statusApi: statusApi, patriarca: patriarca });

    // PONTO CRÍTICO: Se a carga foi finalizada, atualiza o status na aba 'Listas'
    if (statusApi.finalizada) {
      Logger.log(`Carga ${guid} finalizada. Status API: ${statusApi.status}. Atualizando Patriarca...`);
      let novoStatus = 'Processado'; // Status de sucesso
      if (statusApi.status === CONFIG.STATUS_CARGA.ERRO) {
        novoStatus = 'Erro no Envio';
      }
      atualizarStatusPatriarca(patriarca.idpatriarca, novoStatus);
    }
    
    return { success: true, data: statusApi };

  } catch (e) {
    const errorMsg = `Exceção crítica em 'monitorarStatusCarga': ${e.message}`;
    Logger.log(`${errorMsg} Stack: ${e.stack}`);
    return { success: false, message: errorMsg };
  }
}

/**
 * Função auxiliar para obter status atual da planilha
 */
function obterStatusAtualDaPlanilha(guidCarga) {
  try {
    const nomeAba = CONFIG.SHEET_STATUS_ENVIO;
    
    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) {
      return { success: false, message: `Erro ao abrir planilha: ${CONFIG.SPREADSHEET_PARAM}` };
    }
    
    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId);
    const sheet = spreadsheet.getSheetByName(nomeAba);
    if (!sheet) {
      return { success: false, message: `Aba '${nomeAba}' não encontrada` };
    }
    
    const range = sheet.getRange(CONFIG.TAB_STATUS_CARGA);
    const values = range.getValues();
    
    for (let i = 1; i < values.length; i++) {
      if (values[i][6] === guidCarga) {
        return {
          success: true,
          tentativas: values[i][10] || 0,
          dataUltimaVerificacao: values[i][11],
          statusCarga: values[i][7],
          finalizada: values[i][8]
        };
      }
    }
    
    return { success: false, message: 'Carga não encontrada' };
    
  } catch (error) {
    return { success: false, message: 'Erro: ' + error.message };
  }
}

/**
 * Registra aviso quando máximo de tentativas é atingido
 */
function registrarAvisoMaximoTentativas(guidCarga) {
  try {
    const nomeAba = CONFIG.SHEET_STATUS_ENVIO;
    
    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) return;
    
    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId);
    const sheet = spreadsheet.getSheetByName(nomeAba);
    if (!sheet) return;
    
    const range = sheet.getRange(CONFIG.TAB_STATUS_CARGA);
    const values = range.getValues();
    
    for (let i = 1; i < values.length; i++) {
      if (values[i][6] === guidCarga) {
        const linha = i + 1;
        sheet.getRange(linha, 13).setValue(
          'ATENÇÃO: Máximo de tentativas atingido. Contate a PRODEST para verificação manual.'
        );
        break;
      }
    }
  } catch (error) {
    Logger.log('Erro em registrarAvisoMaximoTentativas: ' + error.message);
  }
}

/**
 * Envia o arquivo JSON do organograma, utilizando um token e
 * validando o ID do patriarca antes de fazer a chamada.
 *
 * @param {object} patriarca O objeto do patriarca.
 * @param {string} ambiente O ambiente de destino.
 * @param {string} token O token de acesso `Bearer` já validado.
 * @returns {{success: boolean, message: string, data?: {guid: string}}}
 */
function enviarOrganogramaCargaInicial(patriarca, ambiente, token) {
  try {
    const nomeArquivoJson = CONFIG.JSON_PATTERNS.ORGANOGRAMA.replace('{sigla}', patriarca.sigla);
    const arquivoJsonContent = findJsonFileContentByName(CONFIG.FOLDER_CARGA_ENVIO, nomeArquivoJson);
    if (!arquivoJsonContent) throw new Error(`Arquivo '${nomeArquivoJson}' não encontrado.`);

    const url = (ambiente === 'HML' ? CONFIG.URL_CARGA_HML : CONFIG.URL_CARGA_PRD) + CONFIG.CARGA_V3 + CONFIG.API_ENDPOINTS.ORGANOGRAMA + patriarca.idpatriarca;
    const options = {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
      payload: JSON.stringify(arquivoJsonContent),
      muteHttpExceptions: true
    };
    
    //const response = UrlFetchApp.fetch(url, options);
    const response = fetchFromAPI_Sync(url, options);

    //if (response.getResponseCode() !== CONFIG.RESPONSE_CODE_SUCCESS_CARGA) {
    if (!response.success || (response.statusCode !== CONFIG.RESPONSE_CODE_SUCCESS_CARGA && response.statusCode !== CONFIG.RESPONSE_CODE_SUCCESS_GENERIC)) {
      throw new Error(`Erro na API de envio (${response.statusCode}): ${response.message}`);
    }

    const guidCarga = JSON.parse(response.getContentText());
    
    // --- ORDEM CORRETA DAS OPERAÇÕES ---
    // 1. Atualiza a aba 'Listas' com token, data e status
    atualizarPatriarca(patriarca.idpatriarca, {
      token: token,
      datasolicitacao: new Date(),
      status: 'Enviando Carga'
    });
    // 2. Registra a nova linha na aba 'Status_Envio'
    registrarEnvioInicial(patriarca, guidCarga);

    return { success: true, data: { guid: guidCarga } };
  } catch (e) {
    Logger.log(`Exceção em 'enviarOrganogramaCargaInicial': ${e.message}`);
    return { success: false, message: e.message };
  }
}

/**
 * Atualiza dados do patriarca após envio bem-sucedido
 */
function atualizarPatriarcaAposEnvio(patriarca, tipoArquivo, guidCarga) {
  try {
    const nomeAba = CONFIG.SHEET_LISTAS;
    
    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) return;
    
    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId);
    const sheet = spreadsheet.getSheetByName(nomeAba);
    if (!sheet) return;
    
    const range = sheet.getRange(CONFIG.TAB_PATRIARCA);
    const values = range.getValues();
    
    for (let i = 1; i < values.length; i++) {
      if (values[i][2] === patriarca.idpatriarca) { // Coluna C (índice 2) - Id
        const linha = i + 1;
        
        if (tipoArquivo === 'organograma') {
          // Coluna E (índice 4) - Org_gerado
          sheet.getRange(linha, 5).setValue(guidCarga);
        } else if (tipoArquivo === 'lotacao') {
          // Coluna F (índice 5) - Lot_Gerado
          sheet.getRange(linha, 6).setValue(guidCarga);
        }
        
        // Atualizar status
        sheet.getRange(linha, 4).setValue('Em Processamento'); // Coluna D - Status
        
        // Atualizar data de solicitação
        const now = new Date();
        const dataFormatada = Utilities.formatDate(now, Session.getScriptTimeZone(), "dd/MM/yyyy HH:mm:ss");
        sheet.getRange(linha, 8).setValue(dataFormatada); // Coluna H - DataSolicitacao
        
        break;
      }
    }
  } catch (error) {
    Logger.log('Erro em atualizarPatriarcaAposEnvio: ' + error.message);
  }
}

/**
 * Envia lotações de forma sequencial, aguardando finalização de cada uma
 */
function enviarLotacoesSequencial(patriarca, environment, listaOrgaosSelecionados) {
  try {
    // Validações iniciais
    if (!patriarca || !patriarca.idpatriarca) {
      return { success: false, message: 'Patriarca inválido' };
    }
    
    if (!listaOrgaosSelecionados || listaOrgaosSelecionados.length === 0) {
      return { success: false, message: 'Nenhum órgão selecionado para envio' };
    }
    
    // NOVO: Verificar se organograma foi finalizado
    const statusOrganograma = verificarStatusOrganogramaFinalizado(patriarca);
    if (!statusOrganograma.success || !statusOrganograma.finalizado) {
      return {
        success: false,
        message: 'Aguardando finalização do processamento do organograma antes de enviar lotações. Status: ' + statusOrganograma.message
      };
    }
    
    // NOVO: Validar token antes de iniciar envios
    const tokenValidacao = validarTokenParaEnvio(patriarca);
    if (!tokenValidacao.tokenValido) {
      return {
        success: false,
        message: 'Token inválido ou expirado: ' + tokenValidacao.message,
        requiredAction: tokenValidacao.requiredAction
      };
    }
    
    Logger.log(`✓ Token válido. Tempo restante: ${tokenValidacao.tempoRestante} minuto(s)`);
    
    const resultados = [];
    let totalSucesso = 0;
    let totalErro = 0;
    
    // Processar cada órgão sequencialmente
    for (let i = 0; i < listaOrgaosSelecionados.length; i++) {
      const orgaoSigla = listaOrgaosSelecionados[i];
      
      Logger.log(`Enviando lotação ${i + 1}/${listaOrgaosSelecionados.length}: ${orgaoSigla}`);
      
      // NOVO: Revalidar token antes de cada envio (caso o processo seja longo)
      if (i > 0) {
        const revalidacao = validarTokenParaEnvio(patriarca);
        if (!revalidacao.tokenValido) {
          resultados.push({
            orgao: orgaoSigla,
            success: false,
            message: 'Token expirou durante o processo: ' + revalidacao.message,
            ordem: i + 1
          });
          totalErro++;
          break; // Interrompe o processo
        }
      }
      
      // Enviar lotação do órgão
      const envioResult = enviarLotacaoOrgao(patriarca, environment, orgaoSigla);
      
      if (!envioResult.success) {
        resultados.push({
          orgao: orgaoSigla,
          success: false,
          message: envioResult.message,
          ordem: i + 1
        });
        totalErro++;
        
        Logger.log(`Erro no envio de ${orgaoSigla}. Continuando...`);
        continue;
      }
      
      // Aguardar finalização do processamento
      Logger.log(`Aguardando finalização do processamento de ${orgaoSigla}...`);
      const monitorResult = aguardarFinalizacaoLotacao(
        envioResult.guidCarga,
        patriarca,
        environment,
        orgaoSigla
      );
      
      resultados.push({
        orgao: orgaoSigla,
        success: monitorResult.success && monitorResult.comSucesso,
        guidCarga: envioResult.guidCarga,
        message: monitorResult.message,
        status: monitorResult.status,
        ordem: i + 1
      });
      
      if (monitorResult.success && monitorResult.comSucesso) {
        totalSucesso++;
      } else {
        totalErro++;
      }
      
      // Se deu erro, decidir se continua ou para
      if (!monitorResult.success || !monitorResult.comSucesso) {
        Logger.log(`Erro no processamento de ${orgaoSigla}. Interrompendo envio sequencial.`);
        break;
      }
    }
    
    return {
      success: true,
      message: `Envio sequencial concluído: ${totalSucesso} sucesso(s), ${totalErro} erro(s)`,
      resultados: resultados,
      totalEnviados: listaOrgaosSelecionados.length,
      totalProcessados: resultados.length,
      sucessos: totalSucesso,
      erros: totalErro
    };
    
  } catch (error) {
    Logger.log('Erro em enviarLotacoesSequencial: ' + error.message);
    return { success: false, message: 'Erro no envio sequencial: ' + error.message };
  }
}

/**
 * Verifica se organograma está finalizado com sucesso
 */

function verificarStatusOrganogramaFinalizado(patriarca) {
  try {
    const nomeAba = CONFIG.SHEET_STATUS_ENVIO;
    
    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) {
      return { success: false, message: 'Erro ao abrir planilha' };
    }
    
    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId);
    const sheet = spreadsheet.getSheetByName(nomeAba);
    if (!sheet) {
      return { success: false, message: 'Aba Status_Envio não encontrada' };
    }
    
    const range = sheet.getRange(CONFIG.TAB_STATUS_CARGA);
    const values = range.getValues();
    
    // Procurar pelo último envio de organograma deste patriarca
    for (let i = values.length - 1; i >= 1; i--) {
      const idPatriarca = values[i][0];         // Coluna A
      const tipoCarga = values[i][3];           // Coluna D
      const statusCarga = values[i][7];         // Coluna H
      const finalizada = values[i][8];          // Coluna I
      
      if (idPatriarca === patriarca.idpatriarca && 
          tipoCarga === CONFIG.TIPO_CARGA.INICIAL_ORGANOGRAMA) {
        
        if (finalizada === true && statusCarga === 'Finalizado') {
          return {
            success: true,
            finalizado: true,
            message: 'Organograma finalizado com sucesso'
          };
        } else if (statusCarga === 'Erro no Envio') {
          return {
            success: true,
            finalizado: false,
            comErro: true,
            message: 'Organograma finalizado com ERRO',
            status: statusCarga
          };
        } else {
          return {
            success: true,
            finalizado: false,
            message: 'Organograma ainda em processamento',
            status: statusCarga
          };
        }
      }
    }
    
    return {
      success: false,
      message: 'Nenhum envio de organograma encontrado para este patriarca'
    };
    
  } catch (error) {
    Logger.log('Erro em verificarStatusOrganogramaFinalizado: ' + error.message);
    return { success: false, message: 'Erro: ' + error.message };
  }
}

/**
 * Aguarda finalização do processamento de uma lotação
 * Verifica a cada 3 minutos, máximo 5 tentativas
 */
function aguardarFinalizacaoLotacao(guidCarga, patriarca, environment, orgaoSigla) {
  try {
    let tentativas = 0;
    const maxTentativas = CONFIG.STATUS_MAX_ATTEMPTS;
    
    while (tentativas < maxTentativas) {
      // Aguardar 3 minutos antes de verificar (exceto na primeira tentativa)
      if (tentativas > 0) {
        Logger.log(`Aguardando ${CONFIG.STATUS_CHECK_INTERVAL_MS / 1000 / 60} minutos antes da próxima verificação...`);
        Utilities.sleep(CONFIG.STATUS_CHECK_INTERVAL_MS);
      }
      
      tentativas++;
      Logger.log(`Tentativa ${tentativas}/${maxTentativas} - Verificando status de ${orgaoSigla}...`);
      
      // Verificar status
      const statusResult = monitorarStatusCarga(guidCarga, patriarca, environment);
      
      if (!statusResult.success) {
        Logger.log(`Erro ao verificar status (tentativa ${tentativas}): ${statusResult.message}`);
        
        // Se não for a última tentativa, continuar
        if (tentativas < maxTentativas) {
          continue;
        } else {
          return {
            success: false,
            message: `Erro ao verificar status após ${tentativas} tentativa(s): ${statusResult.message}`,
            tentativas: tentativas
          };
        }
      }
      
      // Se finalizou com sucesso
      if (statusResult.finalizado && statusResult.comSucesso) {
        Logger.log(`✓ Lotação do órgão ${orgaoSigla} processada com sucesso!`);
        return {
          success: true,
          comSucesso: true,
          message: `Lotação do órgão ${orgaoSigla} processada com sucesso`,
          status: statusResult.status,
          tentativas: tentativas
        };
      }
      
      // Se finalizou com erro
      if (statusResult.finalizado && !statusResult.comSucesso) {
        Logger.log(`✗ Lotação do órgão ${orgaoSigla} finalizada com ERRO: ${statusResult.erro}`);
        return {
          success: true,
          comSucesso: false,
          message: `Lotação do órgão ${orgaoSigla} finalizada com ERRO: ${statusResult.erro}`,
          status: statusResult.status,
          erro: statusResult.erro,
          tentativas: tentativas
        };
      }
      
      // Ainda processando
      Logger.log(`Status atual: ${statusResult.status} - Ainda processando...`);
    }
    
    // Máximo de tentativas atingido
    Logger.log(`⚠ Máximo de tentativas atingido para lotação do órgão ${orgaoSigla}`);
    return {
      success: false,
      message: `Máximo de ${maxTentativas} tentativas atingido para lotação do órgão ${orgaoSigla}. O processamento ainda está em andamento. Contate a PRODEST ou verifique o status manualmente mais tarde.`,
      tentativas: maxTentativas
    };
    
  } catch (error) {
    Logger.log('Erro em aguardarFinalizacaoLotacao: ' + error.message);
    return { success: false, message: 'Erro: ' + error.message };
  }
}

/**
 * Envia todas as lotações selecionadas sem aguardar finalização
 * Aguarda apenas o retorno 201 de cada envio
 * COMENTADO: Aguardando disponibilização completa da API
 */
function enviarLotacoesParalelo(patriarca, environment, listaOrgaosSelecionados) {
  try {
    // Validações iniciais
    if (!patriarca || !patriarca.idpatriarca) {
      return { success: false, message: 'Patriarca inválido' };
    }
    
    if (!listaOrgaosSelecionados || listaOrgaosSelecionados.length === 0) {
      return { success: false, message: 'Nenhum órgão selecionado para envio' };
    }
    
    // NOVO: Verificar se organograma foi finalizado
    const statusOrganograma = verificarStatusOrganogramaFinalizado(patriarca);
    if (!statusOrganograma.success || !statusOrganograma.finalizado) {
      return {
        success: false,
        message: 'Aguardando finalização do processamento do organograma antes de enviar lotações. Status: ' + statusOrganograma.message
      };
    }
    
    // NOVO: Validar token antes de iniciar envios
    const tokenValidacao = validarTokenParaEnvio(patriarca);
    if (!tokenValidacao.tokenValido) {
      return {
        success: false,
        message: 'Token inválido ou expirado: ' + tokenValidacao.message,
        requiredAction: tokenValidacao.requiredAction
      };
    }
    
    Logger.log(`✓ Token válido. Tempo restante: ${tokenValidacao.tempoRestante} minuto(s)`);
    
    const resultados = [];
    let totalSucesso = 0;
    let totalErro = 0;
    
    // Enviar todas as lotações
    for (let i = 0; i < listaOrgaosSelecionados.length; i++) {
      const orgaoSigla = listaOrgaosSelecionados[i];
      
      Logger.log(`Enviando lotação ${i + 1}/${listaOrgaosSelecionados.length}: ${orgaoSigla}`);
      
      // Enviar lotação do órgão
      const envioResult = enviarLotacaoOrgao(patriarca, environment, orgaoSigla);
      
      resultados.push({
        orgao: orgaoSigla,
        success: envioResult.success,
        guidCarga: envioResult.guidCarga || null,
        message: envioResult.message,
        statusCode: envioResult.statusCode,
        ordem: i + 1
      });
      
      if (envioResult.success) {
        totalSucesso++;
      } else {
        totalErro++;
      }
    }
    
    return {
      success: true,
      message: `Envio paralelo concluído: ${totalSucesso} enviado(s) com sucesso, ${totalErro} falha(s). Verifique o status de processamento posteriormente.`,
      resultados: resultados,
      totalEnviados: listaOrgaosSelecionados.length,
      sucessos: totalSucesso,
      falhas: totalErro
    };
    
  } catch (error) {
    Logger.log('Erro em enviarLotacoesParalelo: ' + error.message);
    return { success: false, message: 'Erro no envio paralelo: ' + error.message };
  }
}

/**
 * Envia lotação de um órgão específico para a API
 * COMENTADO: Aguardando disponibilização completa da API
 */
function enviarLotacaoOrgao(patriarca, environment, orgaoSigla) {
  try {
    // ATUALIZADO: Garantir token válido
    const tokenResponse = garantirTokenValido(patriarca);
    if (!tokenResponse.success) {
      return { 
        success: false, 
        message: 'Erro ao obter/validar token: ' + tokenResponse.message 
      };
    }
    
    if (tokenResponse.novo) {
      Logger.log('Novo token gerado para envio de ' + orgaoSigla);
    }
    
    // Nome do arquivo padrão
    const nomeArquivo = `cargalotacao_${patriarca.sigla}_${orgaoSigla}.json`;
    
    // Carregar JSON da lotação do órgão
    const jsonFile = buscarArquivoJson(nomeArquivo);
    if (!jsonFile.success) {
      return { 
        success: false, 
        message: `Arquivo JSON de lotação não encontrado: ${nomeArquivo}` 
      };
    }
    
    const dadosLotacao = JSON.parse(jsonFile.content);
    
    // Montar URL
    const baseUrl = environment === 'HML' ? CONFIG.URL_CARGA_HML : CONFIG.URL_CARGA_PRD;
    const url = baseUrl + CONFIG.CARGA_V3 + CONFIG.API_ENDPOINTS.LOTACOES + patriarca.idpatriarca;
    
    // Preparar requisição
    const options = {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + tokenResponse.token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      payload: JSON.stringify(dadosLotacao),
      muteHttpExceptions: true
    };
    
    // Salvar log da requisição
    const timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyyMMdd_HHmmss');
    saveTxtToFile(
      'URL: ' + url + '\n\nPayload:\n' + JSON.stringify(dadosLotacao, null, 2),
      CONFIG.FOLDER_CARGA_ENVIO,
      `log_requisicao_lotacao_${patriarca.sigla}_${orgaoSigla}_${timestamp}.txt`
    );
    
    // Enviar para API
    const response = fetchFromAPI_Sync(url, options);
    
    // Salvar log da resposta
    saveTxtToFile(
      'Status: ' + response.statusCode + '\n\nResponse:\n' + response.responseText,
      CONFIG.FOLDER_CARGA_ENVIO,
      `log_response_lotacao_${patriarca.sigla}_${orgaoSigla}_${timestamp}.txt`
    );
    
    // Verificar resposta
    if (!response.success || response.statusCode !== CONFIG.RESPONSE_CODE_SUCCESS_CARGA) {
      return {
        success: false,
        message: `Erro no envio de lotação ${orgaoSigla}. Status: ${response.statusCode}. ${response.message}`,
        statusCode: response.statusCode
      };
    }
    
    // Parsear resposta para obter o GUID
    let guidCarga = response.responseText.replace(/"/g, '').trim();
    
    // Registrar na planilha Status_Envio
    const registroResult = registrarEnvioInicial(
      patriarca,
      'lotacao',
      nomeArquivo,
      guidCarga,
      CONFIG.TIPO_CARGA.INICIAL_LOTACOES
    );
    
    if (!registroResult.success) {
      Logger.log('AVISO: Envio realizado mas falha ao registrar na planilha: ' + registroResult.message);
    }
    
    return {
      success: true,
      message: `Lotação do órgão ${orgaoSigla} enviada com sucesso!`,
      guidCarga: guidCarga,
      statusCode: 201
    };
    
  } catch (error) {
    Logger.log(`Erro em enviarLotacaoOrgao (${orgaoSigla}): ` + error.message);
    return { success: false, message: 'Erro ao enviar lotação: ' + error.message };
  }
}


/**
 * Obtém os dados para a tela de envio de lotações.
 * Lê os órgãos da aba "{sigla}_L", valida a existência dos arquivos JSON
 * correspondentes e retorna a lista de órgãos disponíveis para envio.
 *
 * @param {string} idPatriarca O ID do patriarca selecionado.
 * @returns {{success: boolean, message: string, data: {patriarca: object, orgaos: Array, travaEnvio: boolean}}}
 */
function obterDadosTelaLotacao(idPatriarca) {
  try {
    const patriarcaResult = getPatriarca(idPatriarca);
    if (!patriarcaResult.success) {
      throw new Error(`Patriarca com ID ${idPatriarca} não encontrado.`);
    }
    const patriarca = patriarcaResult.dados;

    // 1. Validar se a carga do organograma está finalizada (exemplo de validação)
    if (patriarca.status.toLowerCase() !== 'carga processada') {
      return { success: false, message: `O organograma do patriarca precisa estar com status "Carga processada" para continuar. Status atual: ${patriarca.status}.`, data: { travaEnvio: true } };
    }

    // 2. Ler a lista de órgãos da aba da planilha
    const nomeAbaOrgaos = `${patriarca.sigla}_L`;
    const spreadsheet = SpreadsheetApp.openById(verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM).fileId);
    const sheetOrgaos = spreadsheet.getSheetByName(nomeAbaOrgaos);

    if (!sheetOrgaos) {
      return { success: false, message: `Aba de órgãos '${nomeAbaOrgaos}' não foi encontrada. É necessário processar os arquivos de lotação primeiro.`, data: { travaEnvio: true } };
    }

    const dataOrgaos = sheetOrgaos.getDataRange().getValues();
    const orgaosDaPlanilha = dataOrgaos.slice(1) // Pula cabeçalho
      .map(row => ({ nome: row[0], sigla: row[1] })) // Assumindo Col A = Nome, Col B = Sigla
      .filter(orgao => orgao.sigla); // Remove linhas sem sigla

    if (orgaosDaPlanilha.length === 0) {
      return { success: false, message: `Nenhum órgão encontrado na aba '${nomeAbaOrgaos}'.`, data: { travaEnvio: true } };
    }

    // 3. Validar a existência de cada arquivo JSON de lotação
    const orgaosDisponiveis = [];
    const arquivosFaltantes = [];

    orgaosDaPlanilha.forEach(orgao => {
      const nomeArquivoLotacao = CONFIG.JSON_PATTERNS.LOTACAO
        .replace('{sigla}', patriarca.sigla)
        .replace('{orgao}', orgao.sigla);
      
      if (findJsonFileContentByName(CONFIG.FOLDER_CARGA_ENVIO, nomeArquivoLotacao)) {
        orgaosDisponiveis.push({ ...orgao, arquivo: nomeArquivoLotacao });
      } else {
        arquivosFaltantes.push(orgao.sigla);
      }
    });

    // 4. Se houver arquivos faltando, retornar erro e travar o envio
    if (arquivosFaltantes.length > 0) {
      const msgErro = `Arquivos de lotação não encontrados para os seguintes órgãos: ${arquivosFaltantes.join(', ')}. Por favor, refaça o processo de leitura dos arquivos de lotação antes de prosseguir.`;
      return { success: false, message: msgErro, data: { travaEnvio: true } };
    }

    // 5. Se tudo estiver correto, retornar os dados
    return { 
      success: true, 
      message: 'Órgãos carregados com sucesso.', 
      data: {
        patriarca: patriarca,
        orgaos: orgaosDisponiveis,
        travaEnvio: false
      }
    };

  } catch (error) {
    Logger.log(`ERRO CRÍTICO em obterDadosTelaLotacao: ${error.message}`);
    return { success: false, message: error.message, data: { travaEnvio: true } };
  }
}



/**
 * Reinicia o status de um patriarca para um novo envio de organograma.
 * Limpa o token, a data e define o status como "Em progresso".
 *
 * @param {string} idPatriarca O ID do patriarca a ser reiniciado.
 * @returns {{success: boolean, message: string}}
 */
function resetarStatusPatriarca(idPatriarca) {
  try {
    if (!idPatriarca) {
      throw new Error("ID do Patriarca não fornecido para o reset.");
    }
    Logger.log(`Iniciando reset de token para o Patriarca ID: ${idPatriarca}`);
    
    const dadosParaResetar = {
      status: 'Em progresso',
      token: '',
      dataSolicitacao: ''
    };
    
    const updateResult = atualizarPatriarca(idPatriarca, dadosParaResetar);
    if (!updateResult.success) {
      throw new Error(`Falha ao reiniciar o status: ${updateResult.message}`);
    }

    Logger.log(`Patriarca ID ${idPatriarca} reiniciado com sucesso.`);
    return { success: true, message: 'Patriarca reiniciado com sucesso! Pronto para um novo envio.' };

  } catch (error) {
    Logger.log(`ERRO CRÍTICO em resetarStatusPatriarca: ${error.message}`);
    return { success: false, message: error.message };
  }
}


/**
 * Limpa os dados de controle de envio na aba Listas
 * Deve ser chamada quando necessário resetar o processo
 */
function limparControlesEnvio(patriarca) {
  try {
    const nomeAba = CONFIG.SHEET_LISTAS;
    
    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) {
      return { success: false, message: `Erro ao abrir planilha: ${CONFIG.SPREADSHEET_PARAM}` };
    }
    
    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId);
    const sheet = spreadsheet.getSheetByName(nomeAba);
    if (!sheet) {
      return { success: false, message: `Aba '${nomeAba}' não encontrada` };
    }
    
    const range = sheet.getRange(CONFIG.TAB_PATRIARCA);
    const values = range.getValues();
    
    for (let i = 1; i < values.length; i++) {
      if (values[i][2] === patriarca.idpatriarca) { // Coluna C - Id
        const linha = i + 1;
        
        // Limpar Token (coluna G)
        sheet.getRange(linha, 7).setValue('');
        
        // Limpar DataSolicitacao (coluna H)
        sheet.getRange(linha, 8).setValue('');
        
        break;
      }
    }
    
    return {
      success: true,
      message: 'Controles de envio limpos com sucesso'
    };
    
  } catch (error) {
    Logger.log('Erro em limparControlesEnvio: ' + error.message);
    return { success: false, message: 'Erro ao limpar controles: ' + error.message };
  }
}

/**
 * Limpa os registros de uma carga específica da aba Status_Envio
 */
function limparRegistroStatusEnvio(guidCarga) {
  try {
    const nomeAba = CONFIG.SHEET_STATUS_ENVIO;
    
    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) {
      return { success: false, message: `Erro ao abrir planilha: ${CONFIG.SPREADSHEET_PARAM}` };
    }
    
    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId);
    const sheet = spreadsheet.getSheetByName(nomeAba);
    if (!sheet) {
      return { success: false, message: `Aba '${nomeAba}' não encontrada` };
    }
    
    const range = sheet.getRange(CONFIG.TAB_STATUS_CARGA);
    const values = range.getValues();
    
    for (let i = 1; i < values.length; i++) {
      if (values[i][6] === guidCarga) { // Coluna G - GuidCarga
        const linha = i + 1;
        // Deletar a linha
        sheet.deleteRow(linha);
        return {
          success: true,
          message: 'Registro removido com sucesso'
        };
      }
    }
    
    return {
      success: false,
      message: 'Registro não encontrado'
    };
    
  } catch (error) {
    Logger.log('Erro em limparRegistroStatusEnvio: ' + error.message);
    return { success: false, message: 'Erro ao limpar registro: ' + error.message };
  }
}

/**
 * Busca um arquivo JSON específico em uma pasta
 */
function buscarArquivoJson(nomeArquivo) {
  try {
    const nomePasta = CONFIG.FOLDER_CARGA_ENVIO; // 'Carga - Para Envio'
    
    const folders = DriveApp.getFoldersByName(nomePasta);
    if (!folders.hasNext()) {
      return { success: false, message: `Pasta '${nomePasta}' não encontrada` };
    }
    
    const folder = folders.next();
    const files = folder.getFilesByName(nomeArquivo);
    
    if (!files.hasNext()) {
      return { success: false, message: `Arquivo '${nomeArquivo}' não encontrado` };
    }
    
    const file = files.next();
    const content = file.getBlob().getDataAsString();
    
    return {
      success: true,
      content: content,
      fileId: file.getId(),
      fileName: nomeArquivo
    };
    
  } catch (error) {
    Logger.log('Erro em buscarArquivoJson: ' + error.message);
    return { success: false, message: 'Erro ao buscar arquivo: ' + error.message };
  }
}

/**
 * Valida se existe um token válido antes de enviar lotações
 * Retorna informações sobre o token e sua validade
 * @param {Object} patriarca - Dados do patriarca
 * @returns {Object} Resultado da validação
 */
function validarTokenParaEnvio(patriarca) {
  try {
    if (!patriarca || !patriarca.idpatriarca) {
      return { 
        success: false, 
        tokenValido: false,
        message: 'Patriarca inválido' 
      };
    }
    
    // Verificar se existe token em cache
    const respToken = checkTokenCacheTime(patriarca.idpatriarca);
    
    if (!respToken.success) {
      return {
        success: false,
        tokenValido: false,
        message: 'Token não encontrado. É necessário gerar um novo token antes de enviar lotações.',
        requiredAction: 'GERAR_TOKEN'
      };
    }
    
    // Verificar tempo de expiração
    const expiresIn = respToken.expiresIn; // em segundos
    
    if (expiresIn <= 0) {
      return {
        success: false,
        tokenValido: false,
        message: 'Token expirado. É necessário gerar um novo token.',
        requiredAction: 'GERAR_TOKEN'
      };
    }
    
    // Token válido mas expirando em menos de 5 minutos (300 segundos)
    if (expiresIn < 300) {
      return {
        success: false,
        tokenValido: false,
        message: `Token irá expirar em ${Math.floor(expiresIn / 60)} minuto(s). Aguarde a expiração e gere um novo token.`,
        requiredAction: 'AGUARDAR_EXPIRACAO',
        tempoRestante: expiresIn
      };
    }
    
    // Token válido com tempo suficiente
    const minutos = Math.floor(expiresIn / 60);
    return {
      success: true,
      tokenValido: true,
      message: `Token válido. Tempo restante: ${minutos} minuto(s).`,
      token: respToken.token,
      expiresIn: expiresIn,
      tempoRestante: minutos
    };
    
  } catch (error) {
    Logger.log('Erro em validarTokenParaEnvio: ' + error.message);
    return { 
      success: false, 
      tokenValido: false,
      message: 'Erro ao validar token: ' + error.message 
    };
  }
}

/**
 * Função de teste para isolar e depurar a lógica de obtenção de token.
 * Ela simula a chamada que o seu sistema faria ao iniciar o fluxo de envio.
 */
function testeGarantirTokenValido() {
  Logger.log("--- Iniciando teste da função garantirTokenValido ---");
  
  // 1. Criar um objeto patriarca de teste com os dados fornecidos.
  // Os campos 'clientId' e 'clientSecret' foram extraídos dos seus logs.
  const patriarcaDeTeste = {
    nome: 'Prefeitura de Testes',
    sigla: 'PMEXE',
    idpatriarca: '24663877-6b59-4ae4-8dcf-f0b4d9abebcc',
    status: 'Em progresso',
    organogramagerado: 'X',
    lotacaogerado: 'X',
    token: '',
    datasolicitacao: ''
  };

  Logger.log("Objeto Patriarca de Teste criado: " + JSON.stringify(patriarcaDeTeste, null, 2));

  deleteTokenCacheTime(patriarcaDeTeste.idpatriarca);

  try {
    // 2. Chamar a função `garantirTokenValido` com o objeto de teste.
    const resultado = garantirTokenValido(patriarcaDeTeste);

    // 3. Logar o resultado completo para análise.
    Logger.log("--- Resultado do teste ---");
    Logger.log("Sucesso: " + resultado.success);
    Logger.log("Mensagem: " + resultado.message);
    Logger.log("--------------------------");
    
    return resultado;

  } catch (e) {
    Logger.log("!!! ERRO CRÍTICO NO TESTE !!!");
    Logger.log("Erro: " + e.message);
    Logger.log("Stack Trace: " + e.stack);
    Logger.log("--------------------------");
    return { success: false, message: e.message };
  }
}

/**
 * Garante que existe um token válido, gerando um novo se necessário
 * @param {Object} patriarca - Dados do patriarca
 * @returns {Object} Token válido ou erro
 */
function garantirTokenValido(patriarca) {
  try {
    // Primeiro, verificar se já existe token válido
    const validacao = validarTokenParaEnvio(patriarca);
    
    if (validacao.tokenValido) {
      return {
        success: true,
        message: 'Token válido encontrado',
        token: validacao.token,
        expiresIn: validacao.expiresIn,
        novo: false
      };
    }
    
    // Se token não é válido, verificar se é por expiração próxima
    if (validacao.requiredAction === 'AGUARDAR_EXPIRACAO') {
      return {
        success: false,
        message: validacao.message,
        requiredAction: 'AGUARDAR'
      };
    }
    
    // Token não existe ou está expirado - gerar novo
    Logger.log('Token não válido. Gerando novo token...');
    const novoToken = getAccessToken(patriarca.idpatriarca);
    
    if (!novoToken.success) {
      return {
        success: false,
        message: 'Erro ao gerar novo token: ' + novoToken.message
      };
    }
    
    return {
      success: true,
      message: 'Novo token gerado com sucesso',
      token: novoToken.token,
      expiresIn: novoToken.expiresIn,
      novo: true
    };
    
  } catch (error) {
    Logger.log('Erro em garantirTokenValido: ' + error.message);
    return { 
      success: false, 
      message: 'Erro ao garantir token válido: ' + error.message 
    };
  }
}

/**
 * Função de teste para isolar e depurar a lógica de obtenção de token.
 * Ela simula a chamada que o seu sistema faria ao iniciar o fluxo de envio.
 */
function testeIniciarFluxoEnvioOrganograma() {
  Logger.log("--- Iniciando teste da função testeIniciarFluxoEnvioOrganograma ---");
  
  // 1. Criar um objeto patriarca de teste com os dados fornecidos.
  // Os campos 'clientId' e 'clientSecret' foram extraídos dos seus logs.
  const patriarcaDeTeste = {
    nome: 'Prefeitura de Testes',
    sigla: 'PMEXE',
    idpatriarca: '24663877-6b59-4ae4-8dcf-f0b4d9abebcc',
    status: 'Em progresso',
    organogramagerado: 'X',
    lotacaogerado: 'X',
    token: '',
    datasolicitacao: ''
  };

  Logger.log("Objeto Patriarca de Teste criado: " + JSON.stringify(patriarcaDeTeste, null, 2));

  //deleteTokenCacheTime(patriarcaDeTeste.idpatriarca);

  try {
    // 2. Chamar a função `iniciarFluxoEnvioOrganograma` com o objeto de teste.
    const resultado = iniciarFluxoEnvioOrganograma(patriarcaDeTeste, 'PRD');

    // 3. Logar o resultado completo para análise.
    Logger.log("--- Resultado do teste ---");
    Logger.log("Sucesso: " + resultado.success);
    Logger.log("Mensagem: " + resultado.message);
    if (resultado.data) {
      Logger.log("Dados retornados: " + JSON.stringify(resultado.data));
    } else {
      Logger.log("Nenhum dado retornado.");
    }
    Logger.log("--------------------------");
    
    return resultado;

  } catch (e) {
    Logger.log("!!! ERRO CRÍTICO NO TESTE !!!");
    Logger.log("Erro: " + e.message);
    Logger.log("Stack Trace: " + e.stack);
    Logger.log("--------------------------");
    return { success: false, message: e.message };
  }
}

/**
 * Orquestra o fluxo de envio, com validação de entrada
 * para prevenir a propagação de ID indefinido.
 *
 * @param {object} patriarca O objeto completo do patriarca.
 * @param {string} ambiente O ambiente de destino ('HML' ou 'PRD').
 * @returns {{success: boolean, message: string, data?: object}}
 */
function iniciarFluxoEnvioOrganograma(patriarca, ambiente) {
  try {
    if (!patriarca || !patriarca.idpatriarca) {
      throw new Error("Objeto Patriarca recebido pelo backend é inválido ou não contém 'idpatriarca'.");
    }
    
    const tokenResult = garantirTokenValido(patriarca);
    if (!tokenResult.success) return tokenResult;
    
    const envioResult = enviarOrganogramaCargaInicial(patriarca, ambiente, tokenResult.token);
    if (!envioResult.success) {
      atualizarPatriarca(patriarca.idpatriarca, { status: 'Erro no Envio' });
      return envioResult;
    }
    
    return { 
      success: true, 
      message: 'Envio iniciado com sucesso.',
      data: { guid: envioResult.data.guid, patriarca: patriarca }
    };
  } catch (e) {
    Logger.log(`ERRO CRÍTICO em iniciarFluxoEnvioOrganograma: ${e.message}`);
    if (patriarca && patriarca.idpatriarca) {
      atualizarPatriarca(patriarca.idpatriarca, { status: 'Erro Crítico' });
    }
    return { success: false, message: e.message };
  }
}

/**
 * Função auxiliar para converter valores do tipo Date para uma string formatada.
 * Trata casos em que o valor pode ser nulo, vazio ou não ser uma data.
 * @param {any} valor O valor da célula a ser convertido.
 * @returns {string|any} A data formatada como "dd/MM/yyyy HH:mm:ss" ou o valor original se não for uma data válida.
 */
function converterDataParaString(valor) {
  // 1. Verifica se o valor é um objeto do tipo Date
  // 2. Verifica se a data é válida (getTime() não retorna NaN)
  if (valor instanceof Date && !isNaN(valor.getTime())) {
    return Utilities.formatDate(valor, Session.getScriptTimeZone(), "dd/MM/yyyy HH:mm:ss");
  }
  
  // Se não for uma data válida (pode ser "", null, ou um texto), retorna o valor original.
  return valor;
}

/**
 * Obtém o status de todas as cargas enviadas, garantindo que as datas (mesmo as vazias) sejam
 * tratadas corretamente antes de serem retornadas ao frontend.
 */
function obterStatusCargas() {
  try {
    const nomeAba = CONFIG.SHEET_STATUS_ENVIO;
    const nomeTabela = CONFIG.TAB_STATUS_CARGA;
    
    const retLerArq = verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM);
    if (!retLerArq.success) {
      return { success: false, dados: [] };
    }
    
    const spreadsheet = SpreadsheetApp.openById(retLerArq.fileId);
    const sheet = spreadsheet.getSheetByName(nomeAba);
    if (!sheet) {
      return { success: false, dados: [] };
    }
    
    const range = sheet.getRange(nomeTabela);
    const values = range.getValues();
    const dados = [];
    
    for (let i = 1; i < values.length; i++) {
      
      const [colIdPatriarca, colNomePatriarca, colDataHoraEnvio, colTipoCarga, colTipoArquivo, colNomeArquivo, colGuidCarga, colStatus, colFinalizado, colMensagemErro, colTentativasVerificacao, colDataUltimaVerificacao, colObservacoes] = values[i];
      if (!colIdPatriarca || colIdPatriarca === '') break;
      
      dados.push({
        idPatriarca: colIdPatriarca, 
        nomePatriarca: colNomePatriarca, 
        dataHoraEnvio: converterDataParaString(colDataHoraEnvio), // <<< Tratamento robusto
        tipoCarga: colTipoCarga, 
        tipoArquivo: colTipoArquivo, 
        nomeArquivo: colNomeArquivo, 
        guidCarga: colGuidCarga, 
        status: colStatus, 
        finalizado: colFinalizado, 
        mensagemErro: colMensagemErro, 
        tentativasVerificacao: colTentativasVerificacao, 
        dataUltimaVerificacao: converterDataParaString(colDataUltimaVerificacao), // <<< Tratamento robusto
        observacoes: colObservacoes
      });
    }
    
    return { success: true, dados: dados };
    
  } catch (error) {
    Logger.log('Erro em obterStatusCargas: ' + error.message + ' Stack: ' + error.stack);
    return { success: false, dados: [], message: 'Erro no servidor: ' + error.message };
  }
}

function testeObterDetalhesDeEnvioPorPatriarca(){

  var ret = obterDetalhesDeEnvioPorPatriarca('24663877-6b59-4ae4-8dcf-f0b4d9abebcc');
}

/**
 * Obtém o histórico do último ciclo de envio de um patriarca.
 * Esta versão assume que as datas na planilha já são strings formatadas e as passa
 * diretamente para o frontend, sem conversão.
 * @param {string} idPatriarca O ID do patriarca a ser pesquisado.
 * @returns {Array<object>} Uma lista de objetos com os detalhes do envio.
 */
function obterDetalhesDeEnvioPorPatriarca(idPatriarca) {
  try {
    const sheet = SpreadsheetApp.openById(verificarEAbrirPlanilha(CONFIG.SPREADSHEET_PARAM).fileId)
                                .getSheetByName(CONFIG.SHEET_STATUS_ENVIO);
    if (!sheet) throw new Error(`Aba '${CONFIG.SHEET_STATUS_ENVIO}' não encontrada.`);

    const range = sheet.getDataRange();
    const values = range.getValues();
    const header = values[0];

    const colunas = {
      idPatriarca: header.indexOf("IdPatriarca"),
      nomePatriarca: header.indexOf("NomePatriarca"),
      dataHoraEnvio: header.indexOf("DataHoraEnvio"),
      tipoCarga: header.indexOf("TipoCarga"),
      tipoArquivo: header.indexOf("TipoArquivo"),
      nomeArquivo: header.indexOf("NomeArquivo"),
      guidCarga: header.indexOf("GuidCarga"),
      status: header.indexOf("StatusCarga"),
      finalizado: header.indexOf("StatusFinalizado"),
      mensagemErro: header.indexOf("MensagemErro"),
      tentativasVerificacao: header.indexOf("TentativasVerificacao"),
      dataUltimaVerificacao: header.indexOf("DataUltimaVerificacao"),
      observacoes: header.indexOf("ObservacoesAdicionais")
    };
    
    if (colunas.idPatriarca === -1 || colunas.dataHoraEnvio === -1 || colunas.tipoCarga === -1) {
      throw new Error("Colunas essenciais (IdPatriarca, DataHoraEnvio, TipoCarga) não encontradas.");
    }

    const enviosDoPatriarca = values.slice(1)
      .filter(row => row[colunas.idPatriarca] === idPatriarca)
      .sort((a, b) => new Date(b[colunas.dataHoraEnvio]) - new Date(a[colunas.dataHoraEnvio]));

    if (enviosDoPatriarca.length === 0) return [];

    const ultimoEnvioOrganograma = enviosDoPatriarca.find(row => row[colunas.tipoCarga] === 3);

    let registrosParaProcessar = enviosDoPatriarca;

    if (ultimoEnvioOrganograma) {
      const dataUltimoCiclo = new Date(ultimoEnvioOrganograma[colunas.dataHoraEnvio]);
      registrosParaProcessar = enviosDoPatriarca.filter(row => new Date(row[colunas.dataHoraEnvio]) >= dataUltimoCiclo);
    }
    
    // Mapeia os registros para o formato de objeto JSON sem converter as datas
    const dadosFormatados = registrosParaProcessar.map(row => {

      var resultado = getConfigValueByKey("TIPO_CARGA_TEXT", row[colunas.tipoCarga]);
      return {
        idPatriarca: row[colunas.idPatriarca],
        nomePatriarca: row[colunas.nomePatriarca],
        dataHoraEnvio: converterDataParaString(row[colunas.dataHoraEnvio]), // <<< VALOR PASSADO DIRETAMENTE
        tipoCarga: row[colunas.tipoCarga],
        tipoArquivo: resultado.value, //row[colunas.tipoArquivo],
        nomeArquivo: row[colunas.nomeArquivo],
        guidCarga: row[colunas.guidCarga],
        status: row[colunas.status],
        finalizado: row[colunas.finalizado],
        mensagemErro: row[colunas.mensagemErro],
        tentativasVerificacao: row[colunas.tentativasVerificacao],
        dataUltimaVerificacao: converterDataParaString(row[colunas.dataUltimaVerificacao]), // <<< VALOR PASSADO DIRETAMENTE
        observacoes: row[colunas.observacoes]
      };
    });

    return dadosFormatados;

  } catch (e) {
    Logger.log(`Erro em obterDetalhesDeEnvioPorPatriarca: ${e.message}`);
    return [];
  }
}
