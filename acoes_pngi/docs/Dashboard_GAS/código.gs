const CONFIG = {
  LOGIN_PAGE: 'login',
  LOGOUT_PAGE: 'logout',
  DATA_SHEET_PAGE: 'Monitor de Ações',
  DASHBOARD_PAGE: 'dashboard',
  RESET_PASSWD_PAGE: 'reset-password',
  REMIND_PASSWD_PAGE: 'remind-password',
  SET_NEW_PASSWD_PAGE: 'set-new-password',

  SHEET_DASHBOARD: 'Dashboard',
  SHEET_LISTAS: 'Listas',
  SHEET_ACOES: 'Monitor de Ações',
  SHEET_LOG: 'Log',
  SHEET_TOKEN: 'Token',

  TAB_USUARIOS: 'I1:M100',
  TAB_USUARIO_PROJETO: 'W2:AA28',
  TAB_TOKEN: 'A2:E1000',
  TAB_PRAZOS: 'B4:M50',

  STATUS_TOKEN_SOLICITADO: 'Solicitado',
  STATUS_TOKEN_UTILIZADO: 'Utilizado',
  STATUS_TOKEN_EXPIRADO: 'Expirado',

  COL_PASSWD: 'K',
  IDX_COL_PASSWD: '11',

  // Células dos dropdowns
  DROPDOWN_EIXO: 'A3:A9',
  DROPDOWN_SITUACAO: 'C3:C9',
  DROPDOWN_MONITORAMENTO: 'G2:G26',
  DROPDOWN_PESSOAS: 'I2:M80',
  DROPDOWN_PRAZOS: 'F4:F1000',

  //cores para situações
  BC_SIT_Todos: '#ffffff',
  FC_SIT_Todos: '#000000',
  BC_SIT_Atrasado: '#cc0000',
  FC_SIT_Atrasado: '#ffffff',
  BC_SIT_Concluido: '#38761d',
  FC_SIT_Concluido: '#ffffff',
  BC_SIT_Repactuado: '#3d85c6',
  FC_SIT_Repactuado: '#ffffff',
  BC_SIT_EmAndamento: '#d9ead3',
  FC_SIT_EmAndamento: '#000000',
  BC_SIT_Cancelado: '#f1c232',
  FC_SIT_Cancelado: '#000000',
  BC_SIT_NaoIniciado: '#cccccc',
  FC_SIT_AguardandoFeed: '#ffffff',
  BC_SIT_AguardandoFeed: '#674ea7',
  FC_SIT_NaoIniciado: '#000000',

  SMTP_SERVER: 'seger.correio.es.gov.br',
  SMTP_PORT: '443',
  SMTP_SERVER_COMP: '/service/soap',
  EMAIL_SENDER: 'acoesgpp@seger.es.gov.br',
  EMAIL_SENDER_DISPLAY: 'Ações GPP',
  PASSWD_EMAIL_SENDER: 'GPP@acoes2025'

};


// ====== CONTROLE GLOBAL DE VERSÃO DE AÇÕES ======
function getOrInitGlobalAcoesVersion() {
  const props = PropertiesService.getScriptProperties();
  let version = props.getProperty('GLOBAL_ACOES_VERSION');
  if (version === null || version === undefined) {
    props.setProperty('GLOBAL_ACOES_VERSION', '0');
    return 0;
  }
  return parseInt(version, 10);
}

function incrementGlobalAcoesVersion() {
  const props = PropertiesService.getScriptProperties();
  let version = props.getProperty('GLOBAL_ACOES_VERSION');
  if (version === null || version === undefined) version = 0;
  else version = parseInt(version, 10) + 1;
  props.setProperty('GLOBAL_ACOES_VERSION', String(version));
  return version;
}

function getGlobalAcoesVersion() {
  return getOrInitGlobalAcoesVersion();
}

// ===== Controle de timeout do site =======

const SESSION_TIMEOUT = 30 * 60 * 1000; // 30 minutos

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

// ===================================================


// ========== ROTAS PRINCIPAIS ==========

function onEdit(e) {
  if (!e) return;
  var sheetName = e.range.getSheet().getName();
  
  if (sheetName === CONFIG.DATA_SHEET_PAGE) {
    incrementGlobalAcoesVersion();
      
    // Debug mais detalhado
    //console.log('onEdit chamado:', e);
    //console.log('Tipo de e:', typeof e);
    //console.log('e.range existe?', e && e.range);

    var emailUsuario = e.user.email;
    
    var user = getUserProperties();

    if (user && user.email) {
      emailUsuario = user.email;
    }
    
    const range = e.range;
    
    const editedValue = e.value;
    const oldValue = e.oldValue || '';
    
    Logger.log("OnEdit - e.oldValue: " + e.oldValue);
    Logger.log("OnEdit - e.value: " + e.value);
    
    gravarLogAlteracao(emailUsuario, range, oldValue, editedValue);

  }
}

function doGet(e) {
  setSiteProperty();

  Logger.log("doGet(e) - event: " + JSON.stringify(e));

  var page = e.parameter.page || CONFIG.LOGIN_PAGE;
  var token = e.parameter.token || '';
  Logger.log("doGet(e) - page: " + page + " token: " + token.trim());

  const valid_pages = ['login', 'dashboard', 'reset-password', 'remind-password', 'set-new-password'];
  var htmlFile = valid_pages.includes(page) ? page : CONFIG.LOGIN_PAGE;
  Logger.log("doGet(e) - htmlFile: " + htmlFile);

  var retUserProps = getUserProperties();

  Logger.log("doGet(e) - retUserProps: " + JSON.stringify(retUserProps));


  if ((retUserProps.sessionId !== null) && (retUserProps.sessionStart !== null)){
    var retValidTimeOut = validateTimeOutUserSession();
    
    Logger.log("doGet(e) - retValidTimeOut: " + JSON.stringify(retValidTimeOut));
    if (token.trim() !== ''){
      page = 'set-new-password';
      htmlFile = 'set-new-password';
    }
    //if ((retValidTimeOut.sessionExpired ==  true) || ((token.trim() === '') && (retUserProps.sessionId.trim() === ''))){
    //  page = 'login';
    //  htmlFile = 'login';
    //}
    //if ((retValidTimeOut.sessionExpired === false) && (token.trim() === '') && (retUserProps.sessionId.trim() === '')){
    //  page = 'dashboard';
    //  htmlFile = 'dashboard';
    //}
    if (retValidTimeOut.sessionExpired === true || (token.trim() === '' && retUserProps.sessionId.trim() === '')) {
      page = 'login';
      htmlFile = 'login';
    }
    if (retValidTimeOut.sessionExpired === false && token.trim() === '' && retUserProps.sessionId.trim() !== '') {
      page = 'dashboard';
      htmlFile = 'dashboard';
    }
  }else{
    page = 'login';
    htmlFile = 'login';
  }
  
  Logger.log("doGet(e) - page: " + page + ", htmlFile: " + htmlFile + ", getUrl(): " + ScriptApp.getService().getUrl());

  switch (page) {
    case 'remind-password':
      return HtmlService.createHtmlOutputFromFile('remind-password')
        .setTitle("Esqueci minha senha");
        //.setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);

    case 'set-new-password':
      if (!token) {
        return HtmlService.createHtmlOutput('<p>Token não informado.</p>');
      }
      const template = HtmlService.createTemplateFromFile('set-new-password');
      template.token = token;
      return template.evaluate()
        .setTitle("Nova senha");
        //.setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);

    case 'login':
      return HtmlService.createHtmlOutputFromFile('login')
        .setTitle("Login");
        //.setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);

    case 'dashboard':
      return HtmlService.createHtmlOutputFromFile('dashboard')
        .setTitle("Painel");
        //.setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);

    default:
      return HtmlService.createHtmlOutputFromFile('login')
        .setTitle("Login");
        //.setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
  }
}


// ====================================
// FUNÇÕES DE RETORNO DE VARIAVEIS DO CONFIG
// ====================================


function getEstilosParaSituacoes(situacoes) {
  const estilos = {};
  situacoes.forEach(s => {
    const { background, font } = getConfigKeysForSituacao(s);
    estilos[s] = `background-color: ${background}; color: ${font};`;
  });
  return estilos;
}

function getSituacaoColors() {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Listas');
    if (!sheet) throw new Error("Aba 'Listas' não encontrada");

    const data = sheet.getRange('C2:E').getValues(); // pula o cabeçalho
    const cores = [];

    for (let i = 0; i < data.length; i++) {
      const [acao, backgroundColor, fontColor] = data[i];

      if (acao && backgroundColor) {
        cores.push({
          acao: String(acao).trim(),
          backgroundColor: String(backgroundColor).trim(),
          fontColor: fontColor ? String(fontColor).trim() : '#ffffff'
        });
      }
    }

    return cores;
  } catch (e) {
    return [];
  }
}

function getConfigKeysForSituacao(situacao) {
  const map = {
    "TODOS": "Todos",
    "ATRASADA": "Atrasado",
    "CONCLUÍDA": "Concluido",
    "REPACTUADA": "Repactuado",
    "EM ANDAMENTO": "EmAndamento",
    "CANCELADA": "Cancelado",
    "NÃO INICIADA": "NaoIniciado",
    "AGUARDANDO FEED": "AguardandoFeed"
  };

  const keySuffix = map[situacao.toUpperCase()];
  
  if (!keySuffix) {
    console.warn(`Situação "${situacao}" não mapeada.`);
    return { success: false, background: null, font: null };
  }

  return {
    success: true,
    background: CONFIG[`BC_SIT_${keySuffix}`] || null,
    font: CONFIG[`FC_SIT_${keySuffix}`] || null
  };
}


// ====================================
// FUNÇÕES DE PROPRIEDADES DO USUÁRIO
// ====================================

function setSiteProperty() {
  const scriptProperties = PropertiesService.getScriptProperties();
  scriptProperties.setProperty('siteURL', ScriptApp.getService().getUrl());
  scriptProperties.setProperty('DATA_VERSION', 0);
  return { siteURL: ScriptApp.getService().getUrl() };
}

function getCurrentVersion() {
  const props = PropertiesService.getScriptProperties();
  const version = props.getProperty('DATA_VERSION') || '0';
  Logger.log('Versão atual: ' + version);
  return { version: version };
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


function getDataHoraAtual() {
  // Obtém a data e hora atuais
  var agora = new Date();

  // Formata a data e hora usando toLocaleDateString e toLocaleTimeString
  var dataFormatada = agora.toLocaleDateString();
  var horaFormatada = agora.toLocaleTimeString();

  //Logger.log("Data: " + dataFormatada);
  //Logger.log("Hora: " + horaFormatada);

  // Formata a data e hora usando Utilities.formatDate
  var formatoPersonalizado = Utilities.formatDate(agora, "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");
  //Logger.log("Data e hora formatadas (personalizado): " + formatoPersonalizado);

  return {
    data: dataFormatada,
    hora: horaFormatada,
    dataHoraPersonalizada: formatoPersonalizado
  };
}

function getDataHoraComHoras(horas) {
  const agora = new Date();
  if (horas !== null && horas !== undefined) {
    agora.setHours(agora.getHours() + horas);
  }
  const dataHoraFormatada = agora.toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' });
  return dataHoraFormatada;
}

function setNewEmailToken(email, token){
try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_TOKEN);
    if (!sheet) throw new Error("Aba 'Token' não encontrada.");

    const data = sheet.getRange(CONFIG.TAB_TOKEN).getValues();
    
    var ultimaLinha = sheet.getLastRow();
    // Obtenha o valor da célula da última linha preenchida (por exemplo, coluna A).
    var valor = sheet.getRange(ultimaLinha, 1).getValue();
    // Escreva o valor na próxima linha.
    var proximaLinha = ultimaLinha + 1;

    var retData = getDataHoraAtual();
    var dataHoraAgora = retData.dataHoraPersonalizada;
    var retDataHoraExpiracao = getDataHoraComHoras(2);

    //data/hora solicitacao (A)
    //solicitante	(B)
    //token	(C)
    //data/hora expiração	(D)
    //status (E) = 'solicitado', 'utilizado' ,'expirado'

    sheet.getRange(proximaLinha, 1).setValue(dataHoraAgora);
    sheet.getRange(proximaLinha, 2).setValue(email);
    sheet.getRange(proximaLinha, 3).setValue(token);
    sheet.getRange(proximaLinha, 4).setValue(retDataHoraExpiracao);
    sheet.getRange(proximaLinha, 5).setValue('solicitado');

    return { success: true, message: '' };
    
  } catch (error) {
    return { success: false, message: 'Não foi possível gravar o novo token de envio de email. ' + error.message };
  }
}

function updateEmailToken(data, linha, status){
try {

    data.getRange(linha, 5).setValue(status);

    return { success: true, message: '' };
    
  } catch (error) {
    return { success: false, message: 'Não foi possível atualizar o token de envio de email. ' + error.message };
  }
}

function getValidToken(token){
  
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_TOKEN);
    if (!sheet) throw new Error("Aba 'Token' não encontrada.");

    const dados = sheet.getRange(CONFIG.TAB_TOKEN).getValues();
    var retorno = {};
    var bAchei = false;
    var valEmail = '';
    var valToken = '';
    // limpo o Token pois vem com Aspas no início e fim
    var tokenLimpo = String(token).trim().replace(/^["']|["']$/g, '');
    //Logger.log("tokenLimpo: " + tokenLimpo);
    //Logger.log("dados.length: " + (dados.length -1).toString());
    // pesquisa do último para o primeiro
    //for (let linha = dados.length - 1; linha >= 0 ; linha--) {
    for (let linha = 0; linha <= dados.length ; linha++) {

      valEmail = dados[linha][1];
      valToken = dados[linha][2];
      //Logger.log("Linha: " + linha.toString() + ", Token: " + String(tokenLimpo).trim() + ", valEmail: " + valEmail + ", valToken: " + String(valToken).trim());
      
      if (String(valToken).trim() === tokenLimpo) {
        bAchei = true;
        break;
      }        
    }
    retorno = { success : false, message : 'Token não encontrado!', email: '' };
    if (bAchei){
      retorno = { success : true, message : '', email: valEmail };
    }
    return retorno;
    
  } catch (error) {
    return { success: false, message: 'Não foi possível recuperar token de envio de email. ' + error.message, email: '' };
  }
}

function getAndValidateEmailToken(email, token){

  try {
    const sheetToken = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_TOKEN);
    if (!sheetToken) throw new Error("Aba 'Token' não encontrada.");

    const dados = sheetToken.getRange(CONFIG.TAB_TOKEN).getValues();
    var retorno = {};
    var bAchei = false;
    var bTokenSolicitado = false;
    var bTokenExpirado = false;
    var bTokenPrazoExpirado = false;
    var bTokenUtilizado = false;
    var valEmail = '';
    var valToken = '';
    var valDataExpiracao = '';
    var valStatus = '';
    var tokenLimpo = String(token).trim().replace(/^["']|["']$/g, '');
    
    //Logger.log("getAndValidateEmailToken - dados.length : " + dados.length.toString());
    if (dados.length >= 1){
      // pesquisa do último para o primeiro
      
      //for (let linha = dados.length - 1; linha >= 0 ; linha--) {
      for (let linha = 0; linha <= dados.length ; linha++) {
        valEmail = dados[linha][1];
        valToken = dados[linha][2];
        valDataExpiracao = dados[linha][3];
        valStatus = dados[linha][4];
        valStatus = valStatus.toLowerCase();

        //Logger.log("getAndValidateEmailToken - email(parametro) : " + email);
        //Logger.log("getAndValidateEmailToken - tokenLimpo(parametro) : " + tokenLimpo);
        //Logger.log("getAndValidateEmailToken - valEmail : " + valEmail);
        //Logger.log("getAndValidateEmailToken - String(valToken).trim() : " + String(valToken).trim());
        //Logger.log("getAndValidateEmailToken - valDataExpiracao : " + valDataExpiracao);
        //Logger.log("getAndValidateEmailToken - valStatus : " + valStatus);

        if(valEmail.trim() !== ''){
          // se o token é o mesmo passado como parâmetro e esse token ainda está como solicitado
          if((String(valToken).trim() === tokenLimpo) && (valStatus == 'solicitado')){
            if(valEmail == email){
              const agora = new Date();

              // Converter valDataExpiracao para Date, seja string ou Date
              let dataExpiracao;
              if (valDataExpiracao instanceof Date) {
                dataExpiracao = valDataExpiracao;
              } else if (typeof valDataExpiracao === 'string') {
                let partes = valDataExpiracao.match(/(\d{2})\/(\d{2})\/(\d{4}),?\s*(\d{2}):(\d{2}):(\d{2})/);
                if (partes) {
                  // partes: [tudo, dd, mm, yyyy, hh, mi, ss]
                  dataExpiracao = new Date(
                    parseInt(partes[3]),       // ano
                    parseInt(partes[2]) - 1,   // mês (0-based)
                    parseInt(partes[1]),       // dia
                    parseInt(partes[4]),       // hora
                    parseInt(partes[5]),       // min
                    parseInt(partes[6])        // seg
                  );
                } else {
                  dataExpiracao = new Date(valDataExpiracao);
                }
              } else {
                dataExpiracao = new Date(valDataExpiracao);
              }

              //Logger.log("agora: "+ agora.toLocaleString() + ", dataExpiracao: " + dataExpiracao.toLocaleString());

              if (agora.getTime() <= dataExpiracao.getTime()) {
              //if(valDataExpiracao <= agora){
                sheetToken.getRange(linha + 2, 5).setValue('utilizado');
                linha = -1;
                bAchei = true;
                bTokenSolicitado = true;
                break;
              }
              else{
                sheetToken.getRange(linha + 2, 5).setValue('expirado');
                linha = -1;
                bAchei = true;
                bTokenPrazoExpirado = true;
                break;
              }
            }
          }

          // se o token é o mesmo passado como parâmetro e esse token já foi utilizado
          if((String(valToken).trim() === tokenLimpo) && (valStatus == 'utilizado')){
            if(valEmail == email){
              linha = -1;
              bAchei = true;
              bTokenUtilizado = true;
              break;
            }
          }
          
          // se o token é o mesmo passado como parâmetro e esse token está expirado
          if((String(valToken).trim() === tokenLimpo) && (valStatus == 'expirado')){
            if(valEmail == email){
              linha = -1;
              bAchei = true;
              bTokenExpirado = true;
              break;
            }
          }
        }
      }
     
      if (!bAchei){
        retorno = { success : false, message : 'Token não encontrado!', valor: '' };
      }
      else{
        if (bTokenSolicitado){
          retorno = { success : true, message : '', valor: 'utilizado' };
        }
        if (bTokenPrazoExpirado){
          retorno = { success : false, message : 'Infelizmente o prazo para a troca de senha foi expirado! Faça nova solicitação em Esqueci minha senha.', valor: '' };
        }
        if (bTokenExpirado){
          retorno = { success : false, message : 'Este token está expirado! Faça nova solicitação em Esqueci minha senha.', valor: '' };
        }
        if (bTokenUtilizado){
          retorno = { success : false, message : 'Este token já foi utilizado para a troca da senha!', valor: '' };
        }
      }      
      Logger.log("retorno: "+ JSON.stringify(retorno))
      return retorno;
    }
    else{
      retorno = { success : false, message : 'Nenhuma solicitação de troca de senha foi não encontrada!', valor: '' };
      return retorno;
    }

  } catch (error) {
    return { success: false, message: 'Não foi possível recuperar e validar token de envio de email. ' + error.message, valor: ''};
  }
}

function encontrarLinhaPorValor(abaNome, intervalo, valorProcurado) {
  const planilha = SpreadsheetApp.getActiveSpreadsheet();
  const aba = planilha.getSheetByName(abaNome);
  const dados = aba.getRange(intervalo).getValues();

}


function setUserSessionIdProperties(sessionId, email, nome, tipo_usuario){
  const propriedades = PropertiesService.getUserProperties();
  if (sessionId == null || sessionId == undefined || (String(sessionId).trim() == ""))
  {
    sessionId = Utilities.getUuid();
  }
  propriedades.setProperty('sessionId', sessionId);
  propriedades.setProperty('email', email);
  propriedades.setProperty('email_to_passwd', email);
  propriedades.setProperty('nome', nome);
  propriedades.setProperty('url', ScriptApp.getService().getUrl());
  const now = new Date().getTime();
  propriedades.setProperty('sessionStart', String(now));
  propriedades.setProperty('tipo_usuario', tipo_usuario);
  return {sessionId: sessionId, email: email, nome: nome, url: ScriptApp.getService().getUrl(), sessionStart: now, tipo_usuario: tipo_usuario};
}

function getUserProperties() {
  const userProperties = PropertiesService.getUserProperties();
  var tipo_usuario = userProperties.getProperty('tipo_usuario');
  return {
    sessionId: userProperties.getProperty('sessionId'),
    email: userProperties.getProperty('email'),
    email_to_passwd: userProperties.getProperty('email_to_passwd'),
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

// ====================================
// FUNÇÕES DE LOAD DE PÁGINAS
// ====================================

function loadLogin() {
  return HtmlService.createHtmlOutputFromFile(CONFIG.LOGIN_PAGE)
    .setTitle("Login")
    //.setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .getContent();
}

function loadDashboard() {
  const user = getUserProperties();
  Logger.log("user: " + JSON.stringify(user));
  if (!user.sessionId) {
    return HtmlService.createHtmlOutputFromFile(CONFIG.LOGIN_PAGE)
      .setTitle("Login")
      //.setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
      .getContent();
  }
  return HtmlService.createHtmlOutputFromFile(CONFIG.DASHBOARD_PAGE)
    .setTitle("Ações MGI")
    //.setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .getContent();
}


function getUserState(email) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_LISTAS);
    if (!sheet) throw new Error("Aba 'Listas' não encontrada.");

    const data = sheet.getRange(CONFIG.TAB_USUARIOS).getValues();
    for (let i = 1; i < data.length; i++) {
      const [rowEmail, rowNome, rowSenha, rowStatus, tipo_usuario] = data[i];
      if (rowEmail && rowEmail.toLowerCase() === email.toLowerCase() ) {
        if (rowStatus && rowStatus.toLowerCase() === 'ativo'){
          return { success: true, message: '' };
        } else {
          return { success: false, message: 'O usuário (' + rowNome + ') está inativo.\nSolicite a ativação para poder continuar!' };
        }
      }
    }
    return { success: false, message: 'Email ou senha inválidos.' };
  } catch (error) {
    //throw new Error("Erro ao recuperar informações do usuário: " + error.message);
    return { success: false, message: "Erro ao recuperar informações do usuário: " + error.message };
  }
}

function authenticateUser(email, password) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_LISTAS);
    if (!sheet) throw new Error("Aba 'Listas' não encontrada.");

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
    return { success: false, message: 'Email ou senha inválidos.' };
  } catch (error) {
    throw new Error("Erro ao autenticar: " + error.message);
  }
}

// ====================================
// FUNÇÕES DE REDEFINIÇÃO DE SENHA
// ====================================

function setAndGetSiteURL(email) {
  setEmailProperty(email);
  return getSiteProperty();
}


function loadResetPassword(email) {
  const template = HtmlService.createTemplateFromFile(CONFIG.RESET_PASSWD_PAGE);
  template.email = email; // passa o parâmetro para o template

  return template
    .evaluate()
    .setTitle("Redefinir senha")
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .getContent();
}

function loadRemindPassword(email) {
  setSiteProperty();
  if (email) {
    setEmailProperty(email);
  }
  return HtmlService.createHtmlOutputFromFile('remind-password')
    .setTitle("Esqueci minha senha")
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .getContent(); // <-- Adicionar este método
}


function removeAllUserProperties(){
  PropertiesService.getUserProperties().deleteAllProperties();
  //PropertiesService.getScriptProperties().deleteAllProperties();
  return { success: true };
}

function resetPassword(email, oldPassword, newPassword) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_LISTAS);

    // Verifica se a aba 'Listas' existe
    if (!sheet) throw new Error("Aba 'Listas' não encontrada.");

    // Lê os dados da faixa CONFIG.TAB_USUARIOS
    const data = sheet.getRange(CONFIG.TAB_USUARIOS).getValues();

    var bSenhaAntiga = false;
    var bTamNovaSenha = false;
    var bAcheiUser = false;
    var emailEncontrado = "";
    var bEmailAtivo = false;
    var nomeEncontrado = "";
    var tipo_usuario = "";
    var rowToUpdate = -1; // Índice da linha a ser atualizada

    for (let i = 1; i < data.length; i++) {
      const [rowEmail, rowNome, rowSenhaOld, rowStatus, rowTipoUsuario] = data[i];

      if (rowSenhaOld.toString() === oldPassword ){
          bSenhaAntiga = true;
      }

      if(newPassword.length >= 3){
        bTamNovaSenha = true;
      }

      // Verifica se o email e senha batem
      if (rowEmail && rowEmail.toLowerCase() === email.toLowerCase()) {
        bAcheiUser = true;

        // Verifica se o status é 'ativo'
        if (rowStatus && rowStatus.toLowerCase() === 'ativo') {
          bEmailAtivo = true;
          emailEncontrado = rowEmail;
          nomeEncontrado = rowNome;
          tipo_usuario = rowTipoUsuario;
          rowToUpdate = i + 1; // Ajusta índice para a linha correta na planilha (base 1)
          break;
        }
      }
    }

    //Logger.log('bAcheiUser: ' + bAcheiUser);
    //Logger.log('bEmailAtivo: ' + bEmailAtivo);
    //Logger.log('email: ' + emailEncontrado);

    if(!bTamNovaSenha){
      return { success: false, message: 'A senha nova deve ter no mínimo 3 caracteres.', sessionId: null };
    }

    if(!bSenhaAntiga){
      return { success: false, message: 'A senha atual não confere com a senha cadastrada.', sessionId: null };
    }

    if (bAcheiUser && !bEmailAtivo) {
      return { success: false, message: 'Email inativo.', sessionId: null };
    }

    if (!bAcheiUser) {
      return { success: false, message: 'Email ou senha inválidos.', sessionId: null };
    }

    if (bAcheiUser && bEmailAtivo && bSenhaAntiga && rowToUpdate !== -1) {
      // Atualiza a senha
      //COL_PASSWD: 'K',
      //IDX_COL_PASSWD: '11',

      var idx_col = parseInt(CONFIG.IDX_COL_PASSWD);
      sheet.getRange(rowToUpdate, idx_col).setValue(newPassword);

      if(sheet.getRange(rowToUpdate, idx_col).getValue() == newPassword){
        // set properties
        let retorno = setUserSessionIdProperties("", emailEncontrado, nomeEncontrado, tipo_usuario);
        // Guardar SessionId
        const sessionId = retorno.sessionId;

        return { success: true, message: 'Senha atualizada!', sessionId: sessionId };
      }

      return { success: false, message: 'A senha não foi atualizada!' };
    }

  } catch (error) {
    //Logger.log("Erro ao alterar a senha: " + error.message);
    throw new Error("Erro ao alterar a senha: " + error);
  }
}

// ====================================
// ====================================

function verificaPrazoFinalAcao(){

  //To Do:
  // a rotina só verifica ações que estão com situação AGUARDANDO FEED, REPACTUADA e EM ANDAMENTO
  
  // Quando for o último dia do mês anterior ao prazo final 


  // Se Prazo + 7 dias = hoje e situação diferente de ATRASADA
  // então 
  //    altera a situação para ATRASADA. 
  //    Manda email de atraso


  //Em relação ao prazo final de cada ação:
  //O envio de email será para todos os participantes de cada ação, com cópia para Claudio, Agatha, Sabrini e Pedro (estamos vendo a possibilidade de criação de grupo de emails), mais a Emilia (MGI).
    //Se for necessário incluir //mais alguém do MGI, favor responder este email com os endereçõs de email que devo acrescentar.
  //A aplicação deverá validar sozinha, quando for o último dia do mês anterior ao prazo final e irá enviar um email (para todos os participantes citados acima) informando sobre o prazo final da ação.
  //A aplicação deverá validar sozinha, quando um ação estiver com o prazo vencido em 7 dias. Neste caso, irá enviar email (para todos os participantes citados acima) informando que prazo está vencido e solicitando atulização //das informações da ação. A a situação da ação irá ser atualizada para ATRASADA.
  //Irei preparar os layouts dos emails e enviarei para que vocês possam dar suas sugetões e aprovação.
  //Sempre que um email for enviado (um mes antes do vencimento e 7 dias após), a aplicação deverá controlar para não enviar outro email com o mesmo conteúdo.
  //Para que as regras acima sejam executadas, cada ação deve ter sua situação como: AGUARDANDO FEED, REPACTUADA ou EM ANDAMENTO. As outras situações (ATRASADA, CONCLUÍDA, CANCELADA ou NÃO INICIADA) não devem enviar emails.
//
  //Em relação aos monitoramentos de cada ação:
  //Atualmente, a planilha não contém uma data para próximo monitoramento, entretanto no site, foi definido um campo solicitando que cada participante que incluir um monitoramento, deverá preencher a próxima data esperada //para o monitoramento seguinte. Esta data será utilizada como base para o envio do email de avisando quando é esperado uma atualização do próximo monitoramento. 
  //O envio de email será para todos os participantes de cada ação, com cópia para Claudio, Agatha, Sabrini e Pedro (estamos vendo a possibilidade de criação de grupo de emails), mais a Emilia (MGI). Se for necessário incluir //mais alguém do MGI, favor responder este email com os endereçõs de email que devo acrescentar.
  //Quando houver data do proximo monitoramento, a aplicação deverá validar sozinha e enviar email um mês antes.
  //No caso do próximo monitoramento for definido em um tempo entre 15 dias e 30 dias da útima atualização, a aplicação irá enviar email assim que for identificado.
  //No caso do próximo monitoramento for definido em um tempo menor que 15 dias da útima atualização, não haverá envio de email.
  //Sempre que um email for enviado (sobre o prazo para o próximo monitoramento), a aplicação deverá controlar para não enviar outro email com o mesmo conteúdo.
  //Irei preparar os layouts dos emails e enviarei para que vocês possam dar suas sugetões e aprovação.
  //Para que as regras acima sejam executadas, cada ação deve ter sua situação como: AGUARDANDO FEED, REPACTUADA ou EM ANDAMENTO. As outras situações (ATRASADA, CONCLUÍDA, CANCELADA ou NÃO INICIADA) não devem enviar emails.


  try{
    var formato = "dd/MM/yyyy";
    var fusoHorario = Session.getScriptTimeZone(); 

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.DATA_SHEET_PAGE);

    // Verifica se a aba 'Monitor de Ações' existe
    if (!sheet) throw new Error("Aba 'Monitor de Ações' não encontrada.");

    const headerRange = sheet.getRange("B3:M3");
    const headers = headerRange.getValues()[0];

    // Lê os dados da faixa TAB_PRAZOS: 'B4:M50'
    var data = sheet.getRange(CONFIG.TAB_PRAZOS).getValues();
    
    // Aqui você remove as linhas em branco
    data = removerLinhasEmBranco(data);

    var hoje = new Date();
    var hojeSemHora = new Date(hoje.getFullYear(), hoje.getMonth(), hoje.getDate());
    hoje = Utilities.formatDate(hojeSemHora, Session.getScriptTimeZone(), "dd/MM/yyyy");
    var dataHoje = Utilities.parseDate(hoje, fusoHorario, formato);

    var arrayPrazo = [];
    var objSituacaoAcao = {};
    var numAcao = 0;
    var linha = 0;
    var situacaoAcao = '';
    hoje = Utilities.formatDate(hojeSemHora, Session.getScriptTimeZone(), "dd/MM/yyyy");

    for(linha = 0; linha < data.length; linha++){
      
      var linhaPlanilha = linha + 4;

      // EIXO	nº	ÁLIAS	AÇÕES	PRAZOS	SITUAÇÃO
      const [rowEixo, rowNumAcao, rowAlias, rowAcao, rowPrazo, rowSituacao] = data[linha];
      if (rowNumAcao.toString() !== ''){
        // Monitorar Ações com os status:
        //AGUARDANDO FEED, REPACTUADA e EM ANDAMENTO
        situacaoAcao = rowSituacao.toString().trim();
        objSituacaoAcao = {};

        if((situacaoAcao == 'EM ANDAMENTO') || (situacaoAcao == 'REPACTUADA')  || (situacaoAcao == 'AGUARDANDO FEED')){

          numAcao = parseInt(rowNumAcao.toString().trim(), 10);
          var dataFinal = Utilities.parseDate(rowPrazo, fusoHorario, formato);
          
          var prazoMesAnterior = new Date(dataFinal.getFullYear(), dataFinal.getMonth(), 1);
          prazoMesAnterior.setDate(prazoMesAnterior.getDate() - 1);

          var dataEmAtraso = new Date(dataFinal.getFullYear(), dataFinal.getMonth(), dataFinal.getDay());
          dataEmAtraso.setDate(dataEmAtraso.getDate() + 7);

          Logger.log("numAcao: " + numAcao.toString());
          Logger.log("prazoMesAnterior: " + prazoMesAnterior.toString());

          if(dataHoje = prazoMesAnterior){
            objSituacaoAcao = {
              linha: linhaPlanilha,
              eixo: rowEixo,
              numAcao: numAcao,
              descricaoAcao: rowAcao,
              situacaoAcao: situacaoAcao,
              dataFinal: dataFinal,
              enviarAvisoUmMes: true,
              atrasado: false
            }
          }

          if(dataFinal = dataEmAtraso){
            // Atualiza a situação da Ação para ATRASADA
            sheet.getRange(linhaPlanilha, 7).setValue('ATRASADA');

            objSituacaoAcao = {
              linha: linhaPlanilha,
              eixo: rowEixo,
              numAcao: numAcao,
              descricaoAcao: rowAcao,
              situacaoAcao: 'ATRASADA',
              dataFinal: dataFinal,
              enviarAvisoUmMes: false,
              atrasado: true
            }
          }
          // se enviarAvisoUmMes ou já ultrapassou o prazo final da Ação, adiciona ao array
          if((objSituacaoAcao.enviarAvisoUmMes) || (objSituacaoAcao.atrasado)){
            arrayPrazo.push(objSituacaoAcao);
          }
        }
      }
    } 

    // pega Lista de Participantes
    const ss = SpreadsheetApp.getActiveSpreadsheet();

    // === Carrega dados dos usuários da aba CONFIG.SHEET_LISTAS ===
    const tabUsuarios = CONFIG.SHEET_LISTAS;
    const sheetUsuarios = ss.getSheetByName(CONFIG.SHEET_LISTAS);
    if (!sheetUsuarios) return { success: false, message: `Aba '${tabUsuarios}' não encontrada.` };

    const usuariosData = sheetUsuarios.getRange(CONFIG.TAB_USUARIOS).getValues();
    const usuariosMap = {};
    const emailToNomeMap = {}; // Novo mapa para buscar nome pelo email

    // Assume-se que a primeira linha da aba de usuários é o cabeçalho com nome e email
    const headerUsuarios = usuariosData[0];
    const colNome = headerUsuarios.indexOf("Nome");
    const colEmail = headerUsuarios.indexOf("Email");

    for (let i = 1; i < usuariosData.length; i++) {
      const nome = (usuariosData[i][colNome] || "").toString().trim();
      const email = (usuariosData[i][colEmail] || "").toString().trim().toLowerCase();
      if (nome && email) {
        usuariosMap[nome.toLowerCase()] = email;
        emailToNomeMap[email] = nome; // Mapa reverso: email -> nome
      }
    }

    // varrer todo o arrayPrazo para adicionar os participantes para cada ação que está atrasada ou dentro do prazo
    arrayPrazo.forEach((objArray) => {
      // varrer as linhas da planilha até achar a Ação
      for (const item of data) {
        // Coleta os valores brutos das colunas K e M (índices relativos ao range B:M → K=9, M=11)
        const colB = 1;
        const colK = 9;
        const colM = 11;
        
        if (objArray.numAcao == item[colB]) {
          const participantesRaw = [item[colK], item[colM]]
            .filter(Boolean)
            .join(";");
            
          const participantes = participantesRaw
            .split(/[,;]+/)
            .map(part => {
              part = part.trim();
              
              // Caso esteja no formato: "Nome" <email>
              const match = part.match(/^(.+?)\s*<([^>]+)>$/);
              if (match) {
                const nome = match[1].replace(/["']/g, "").trim();
                const email = match[2].toLowerCase();
                return { nome: nome, email: email };
              }
              
              // Se for apenas email
              if (part.includes("@")) {
                const email = part.toLowerCase();
                const nome = emailToNomeMap[email] || ""; // Busca o nome pelo email
                return { nome: nome, email: email };
              }
              
              // Se for apenas nome (sem <>), tenta buscar no mapa
              const nomeLimpo = part.replace(/["']/g, "").toLowerCase();
              const email = usuariosMap[nomeLimpo];
              if (email) {
                return { nome: part.replace(/["']/g, "").trim(), email: email };
              }
              
              return null; // Retorna null para participantes inválidos
            })
            .filter(participante => participante !== null && participante.email.includes("@")) // remove inválidos
            .filter((participante, idx, arr) => 
              arr.findIndex(p => p.email === participante.email) === idx // remove duplicados baseado no email
            );
            
          objArray.participantes = participantes;
          break; // termina for (const item of data)
        }
      }
    });

    if(arrayPrazo.length > 0){
      return { success: true, message: '', arrayAcoesParaVencer: arrayPrazo };
    }
    else{
      return { success: true, message: 'Nenhuma ação está para expirar o prazo final.', arrayAcoesParaVencer: null };
    }
  }
  catch(e){
    var msgError = '';
    Logger.log("Erro ao Verificar Prazos Finais das Ações:");

    if (e instanceof Error) {
      Logger.log("Mensagem: " + e.message);
      Logger.log("Stack: " + e.stack);
      msgError = "Mensagem: " + e.message +  "Stack: " + e.stack;
    } else {
      msgError = "Erro genérico: " + JSON.stringify(e);
      Logger.log(msgError);
    }
      
    return { success: false, message: msgError, arrayAcoesParaVencer: null };
  }
}


// ====================================
// ====================================

function sendEmailEmAtraso(){
  try{
    // chama rotina de criação do Array de Atraso
    const resposta = verificaPrazoFinalAcao();

    if(resposta.success && resposta.arrayAcoesParaVencer.length > 0){
      resposta.arrayAcoesParaVencer.forEach(item => {

        const loginLink = `${ScriptApp.getService().getUrl()}?page=login`;

        const html = `
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
          <meta charset="UTF-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1.0" />
          <title>Ação em Atraso</title>
          <style>
            body {
              margin: 0;
              padding: 0;
              font-family: Arial, sans-serif;
              background-color: #f2f2f2;
            }
            .container {
              width: 100%;
              background-color: #f2f2f2;
              padding: 20px 0;
            }
            .content {
              max-width: 600px;
              margin: 0 auto;
              background-color: #ffffff;
              border-radius: 8px;
              overflow: hidden;
              box-shadow: 0 0 10px rgba(0,0,0,0.05);
            }
            .header {
              background-color: #d9534f; /* vermelho para alerta */
              color: #ffffff;
              padding: 20px;
              text-align: center;
            }
            .body {
              padding: 30px;
              color: #333333;
            }
            .body p {
              font-size: 16px;
              line-height: 1.6;
            }
            .footer {
              padding: 20px;
              font-size: 12px;
              text-align: center;
              color: #888888;
            }
          </style>
        </head>
        <body>
          <div class="container">
            <div class="content">
              <div class="header">
                <h1>Ação em Atraso</h1>
              </div>
              <div class="body">
                <p>Olá, ${nomeEncontrado}!</p>
                <p>
                  Identificamos que a ação <strong>#${numAcao} - ${descAcao}</strong> está em atraso.
                  O prazo definido para conclusão era <strong>${prazoAcao}</strong> e já está vencido, entretanto o estado da ação, ainda não foi atualizado.
                </p>
                <p>
                  Solicitamos que atualize a situação atual da ação ou repactue o prazo final.
                </p>
                <p>Atenciosamente,<br>Equipe GPP</p>
              </div>
              <div class="footer">
                <p>Por favor, não responda este e-mail. Esta caixa não é monitorada.</p>
                <p>&copy; ${new Date().getFullYear()} GPP.</p>
              </div>
            </div>
          </div>
        </body>
        </html>
        `;
      

        const subject = "Redefinição de senha do site de Ações do PNGI do Espírito Santo";

        var retorno = sendZimbraHtmlEmail(emailEncontrado, subject, htmlBody);

        if (retorno.success){
          Logger.log("Email sent successfully!");

          return {
            success: true,
            message: 'Link de redefinição enviado para o email',
            resetLink: resetLink // Em produção, isso seria enviado por email
          };
        }

      })
    }
  
  }
  catch (error) {
    Logger.log("Erro ao enviar email de ação em atraso: " + error.message);
    throw new Error("Erro ao enviar email de ação em atraso: " + error.message);
  }
}

function sendResetLink(email) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_LISTAS);

    // Verifica se a aba 'Listas' existe
    if (!sheet) throw new Error("Aba 'Listas' não encontrada.");

    // Lê os dados da faixa G1:J100
    const data = sheet.getRange(CONFIG.TAB_USUARIOS).getValues();

    var bAcheiUser = false;
    var emailEncontrado = "";
    var nomeEncontrado = "";
    var bEmailAtivo = false;
    var rowToUpdate = -1; // Índice da linha a ser atualizada

    for (let i = 1; i < data.length; i++) {
      const [rowEmail, rowNome, rowSenhaOld, rowStatus] = data[i];

      // Verifica se o email e senha batem
      if (rowEmail && rowEmail.toLowerCase() === email.toLowerCase()) {
        bAcheiUser = true;

        // Verifica se o status é 'ativo'
        if (rowStatus && rowStatus.toLowerCase() === 'ativo') {
          bEmailAtivo = true;
          emailEncontrado = rowEmail;
          nomeEncontrado = rowNome;
          rowToUpdate = i + 1; // Ajusta índice para a linha correta na planilha (base 1)
          break;
        }
      }
    }

    //Logger.log('bAcheiUser: ' + bAcheiUser);
    //Logger.log('bEmailAtivo: ' + bEmailAtivo);
    //Logger.log('email: ' + emailEncontrado);

    if (bAcheiUser && !bEmailAtivo) {
      return { success: false, message: 'Email inativo.', sessionId: null };
    }

    if (bAcheiUser && bEmailAtivo && rowToUpdate !== -1) {

      const resetToken = Utilities.getUuid();
      
      var retNewToken = setNewEmailToken(email, resetToken);

      if(!retNewToken.success){
        return {
              success: false,
              message: retNewToken.message,
              resetLink: ''
            };
      }
            
      // Aqui você enviaria o email com o link de reset
      // Por simplicidade, vamos apenas retornar o token
      const resetLink = `${ScriptApp.getService().getUrl()}?page=set-new-password&token=${encodeURIComponent(resetToken)}`;
      
      const htmlBody = `<!DOCTYPE html>
                        <html lang="pt-BR">
                        <head>
                          <meta charset="UTF-8" />
                          <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                          <title>Redefinição de Senha</title>
                          <style>
                            body {
                              margin: 0;
                              padding: 0;
                              font-family: Arial, sans-serif;
                              background-color: #f2f2f2;
                            }
                            .container {
                              width: 100%;
                              background-color: #f2f2f2;
                              padding: 20px 0;
                            }
                            .content {
                              max-width: 600px;
                              margin: 0 auto;
                              background-color: #ffffff;
                              border-radius: 8px;
                              overflow: hidden;
                              box-shadow: 0 0 10px rgba(0,0,0,0.05);
                            }
                            .header {
                              background-color: #004aad;
                              color: #ffffff;
                              padding: 20px;
                              text-align: center;
                            }
                            .body {
                              padding: 30px;
                              color: #333333;
                            }
                            .body p {
                              font-size: 16px;
                              line-height: 1.6;
                            }
                            .btn {
                              display: inline-block;
                              margin-top: 20px;
                              padding: 12px 24px;
                              background-color: #004aad;
                              color: #ffffff !important;
                              text-decoration: none;
                              border-radius: 5px;
                              font-weight: bold;
                            }
                            .footer {
                              padding: 20px;
                              font-size: 12px;
                              text-align: center;
                              color: #888888;
                            }
                          </style>
                        </head>
                        <body>
                          <div class="container">
                            <div class="content">
                              <div class="header">
                                <h1>Redefinição de Senha</h1>
                              </div>
                              <div class="body">
                                <p>Olá, ` + nomeEncontrado + `!</p>
                                <p>Recebemos uma solicitação para redefinir a sua senha. Para continuar com a redefinição, clique no link abaixo:</p>
                                <p style="text-align: center;">
                                  <a href="` + resetLink + `" class="btn">Redefinir Senha</a>
                                </p>
                                <p>Se você não solicitou esta alteração, por favor ignore este e-mail. Sua senha permanecerá a mesma.</p>
                                <p>Atenciosamente,<br>Equipe GPP</p>
                              </div>
                              <div class="footer">
                                <p> Por favor, não responda este e-mail. Esta caixa não é monitorada. </p>
                                <p id="ano"></p>
                              </div>
                            </div>
                          </div>
                          <script>
                            const dataAtual = new Date();
                            const anoAtual = dataAtual.getFullYear();
                            document.getElementById("ano").innerHTML = &copy + anoAtual + ' GPP.'
                          </script>
                        </body>
                        </html>`;

      const subject = "Redefinição de senha do site de Ações do PNGI do Espírito Santo";

      var retorno = sendZimbraHtmlEmail(emailEncontrado, subject, htmlBody);

      if (retorno.success){
        Logger.log("Email sent successfully!");

        return {
          success: true,
          message: 'Link de redefinição enviado para o email',
          resetLink: resetLink // Em produção, isso seria enviado por email
        };
      }
    }
    
    Logger.log("Erro no envio de email - sendResetLink");

    return {
      success: false,
      message: 'Algumas das informações para redefinição de senha não foram encontradas!',
      resetLink: ''
    };

  } catch (error) {
    Logger.log("Erro ao enviar email de redefinição de senha: " + error.message);
    throw new Error("Erro ao enviar email de redefinição de senha: " + error.message);
  }
}

function resetPasswordWithToken(email, token, novaSenha) {
  //Logger.log("resetPasswordWithToken - email: " + email + ", token: " + token + " novaSenha: " + novaSenha);
  
  if (!email || !token || !novaSenha){
    return {succes: false, message: 'Alguma das informações necessárias para atualizar a senha não foi passada!'};
  } 

  var retUser = getUserState(email);
  //Logger.log("resetPasswordWithToken - getUserState - retUser: " + JSON.stringify(retUser));
  if(retUser.success){

    var retorno = getAndValidateEmailToken(email, token);
    ;;Logger.log("getAndValidateEmailToken - retorno: " + JSON.stringify(retorno));

    if(retorno.success){
      var retAtualizar = atualizarSenhaDoUsuario(email, novaSenha);
      ;;Logger.log("atualizarSenhaDoUsuario - retAtualizar: " + JSON.stringify(retAtualizar));

      if (!retAtualizar.success){
        return {success: false, message: retAtualizar.message};
      }
      return {success: true, message: ''};
    }
    return {success: false, message: retorno.message};
  }
  else{
    return {success: false, message: retUser.message};
  }
}



/**
 * Atualiza a senha do usuário (dummy - substitua pelo seu backend real)
 */
function atualizarSenhaDoUsuario(email, novaSenha) {
  
  try {
    const sheetAtuSenha = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_LISTAS);

    // Verifica se a aba 'Listas' existe
    if (!sheetAtuSenha) throw new Error("Aba 'Listas' não encontrada.");

    // Lê os dados da faixa G1:J100
    const data = sheetAtuSenha.getRange(CONFIG.TAB_USUARIOS).getValues();

    for (let i = 1; i < data.length; i++) {
      if (data[i][0] === email) {
        
        var idx_col = parseInt(CONFIG.IDX_COL_PASSWD);
        sheetAtuSenha.getRange(i + 1, idx_col).setValue(novaSenha);
        
        //PropertiesService.getScriptProperties().deleteProperty('reset_' + token);
        
        Logger.log(`Senha do usuário ${email} redefinida para: ${novaSenha}`);
        return { success: true, message: 'Senha redefinida com sucesso' };
      }
    }
    
    return { success: false, message: 'Usuário não encontrado' };
  } catch (error) {
    console.error('Erro ao redefinir senha:', error);
    return { success: false, message: 'Erro interno do servidor' };
  }
}

// ====================================
// FUNÇÕES DE RECUPERAÇÃO E PREENCHIMENTO DE DROPDOWN
// ====================================


function getConfigValue(variavel){

  if (CONFIG.hasOwnProperty(variavel)) {
    return { success: true, configKey: variavel, value: CONFIG[variavel] };
  }
  else {
    console.warn(`Chave "${key}" não encontrada em CONFIG.`);
    return { success: false, configKey: variavel, value: null };
  }
}

function getOptionsForDropdown(configDropdown, bTodosOption = false, bSort = false) {

  let options = [];
  const configkey = CONFIG[configDropdown];

  Logger.log("configDropdown: " + configDropdown);  
  Logger.log("configkey: " + configkey);

  if (configkey !== null && configkey !== undefined && String(configkey).trim() !== ''){

    const dataSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_LISTAS);
    data = dataSheet.getRange(configkey).getValues();
    
    if (data.length === 0) {
      dataSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_ACOES);
      data = dataSheet.getRange(configkey).getValues();
    }    

    Logger.log("data: " + data);

    let numOpcoes = data.length;

    if (bTodosOption){
      options.push('Todos');
    }
    
    for (let i = 0; i < data.length; i++) {
      const value = data[i][0];
      if (value) options.push(value);
    }
    
    if (bSort) {
      return options.sort((a, b) => {
        if (a === 'Todos') return -1;
        if (b === 'Todos') return 1;
        return a.localeCompare(b);
      });
    }
    
  }
  else{
    options.push('Valores não carregados para a opção: ' + configDropdown);
  }
  Logger.log("resultado da execução: " + options);  

  return options;
}

function _testeGetOptionsForDropdownForDates()
{
  var ret = getOptionsForDropdownForDates(true, true, true);

  Logger.log('Primeira chamada com bShowExpiredDeadlines = true: ' + JSON.stringify(ret));
  
  var ret1 = getOptionsForDropdownForDates(true, true, false);

  Logger.log('Primeira chamada com bShowExpiredDeadlines = false: ' + JSON.stringify(ret1));

}

function getOptionsForDropdownForDates(bTodosOption = false, bSort = false, bShowExpiredDeadlines = true) {

  let options = [];
  
  const dataSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_LISTAS);
  data = dataSheet.getRange(CONFIG.DROPDOWN_PRAZOS).getValues();
  
  if (data.length === 0) {
    dataSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_ACOES);
    data = dataSheet.getRange(CONFIG.DROPDOWN_PRAZOS).getValues();
  }    

  let numOpcoes = data.length;

  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0'); 
  const day = String(today.getDate()).padStart(2, '0');
  const todayFormatted = `${year}-${month}-${day}`; 
  
  for (let i = 0; i < data.length; i++) {
    const value = data[i][0];
    if (value){
      // Converte "dd/mm/yyyy" para "yyyy-mm-dd" para comparação
      var deadline = value.split('/').reverse().join('-');

      if (!bShowExpiredDeadlines){
        if(deadline >= todayFormatted){
          options.push(value);
        }
      } else {
        options.push(value);
      }        
    }
  }

  // retirar elementos duplicados
  const arraySemDuplicatas = options.filter((valor, indice, self) => {
    return self.indexOf(valor) === indice;
  });

  // retirar opção 'Todos' para ordenar
  let filteredValues = arraySemDuplicatas.filter(value => value !== 'Todos');

  if (bSort){

    filteredValues.sort((a, b) => {
      // Converte "dd/mm/yyyy" para "yyyy-mm-dd" para comparação
      const aa = a.split('/').reverse().join('-');
      const bb = b.split('/').reverse().join('-');
      
      // Usa localeCompare() para ordenar
      return aa.localeCompare(bb); 
    });
    
    options = [];
    options = [...filteredValues];
    
    // adiciona na primeira posição
    if (bTodosOption){
      options.unshift('Todos');
    }
  } else if (bSort) {

    // adiciona na primeira posição
    if (bTodosOption){
      options.unshift('Todos');
    }

    return options.sort((a, b) => {
      if (a === 'Todos') return -1;
      if (b === 'Todos') return 1;
      return a.localeCompare(b);
    });
  }
  
  return options;
}



// ====================================
// FUNÇÕES DE RECUPERAÇÃO DOS PROJETOS
// ====================================

function removerLinhasEmBranco(sheetData) {
  const cleanedData = [];
  let lastRow = 0;

  // loop nas linhas de sheetData do final para o início
  for (let i = sheetData.length; i > 0; i--) {
    const row = sheetData[i];

    if (row != undefined){
      //const cleanedRow = [];

      let contColVazia = 0;

      // loop nas colunas da linha
      for (let j = 0; j < row.length; j++) {
        const cellValue = row[j];

        // Verifica se as células estão vazias ou null/undefined
        if (cellValue !== null && cellValue !== undefined && String(cellValue).trim() !== '' && String(cellValue).trim() !== 'Não atribuído') {
          //cleanedRow.push(cellValue);
          lastRow = i;         
          break;
        }
        else if (String(cellValue).trim() == 'Não atribuído' || String(cellValue).trim() == '') {
          contColVazia ++;
        }
        if (contColVazia > 2){
          break;
        }
      }
    }
    if (lastRow > 0){
      break;
    }
  }
  
  for (let i = 0; i <= lastRow; i++) {
    const linhaOriginal = sheetData[i];
    const novaLinha = linhaOriginal.slice(0, linhaOriginal.length);
    cleanedData.push(novaLinha);
  }
  return cleanedData;
}

function getProjetsInternal(){
  
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(CONFIG.DATA_SHEET_PAGE);
    if (!sheet) return { success: false, message: "Aba 'Monitor de Ações' não encontrada." };
    
    const headerRange = sheet.getRange("B3:AQ3");
    const headers = headerRange.getValues()[0];

    const dataRange = sheet.getRange("B4:AQ35");
    let data = dataRange.getValues();

    // Aqui você remove as linhas em branco
    data = removerLinhasEmBranco(data);

    // === Carrega dados dos usuários da aba CONFIG.SHEET_LISTAS ===
    const tabUsuarios = CONFIG.SHEET_LISTAS;
    const sheetUsuarios = ss.getSheetByName(CONFIG.SHEET_LISTAS);
    if (!sheetUsuarios) return { success: false, message: `Aba '${tabUsuarios}' não encontrada.` };

    const usuariosData = sheetUsuarios.getRange(CONFIG.TAB_USUARIOS).getValues();
    const usuariosMap = {};

    // Assume-se que a primeira linha da aba de usuários é o cabeçalho com nome e email
    const headerUsuarios = usuariosData[0];
    const colNome = headerUsuarios.indexOf("Nome");
    const colEmail = headerUsuarios.indexOf("Email");

    for (let i = 1; i < usuariosData.length; i++) {
      const nome = (usuariosData[i][colNome] || "").toString().trim();
      const email = (usuariosData[i][colEmail] || "").toString().trim().toLowerCase();
      if (nome && email) {
        usuariosMap[nome.toLowerCase()] = email;
      }
    }

    let projetos = [];

    data.forEach((row) => {
      if (row.join("").trim() === "") return;

      const projeto = {};

      headers.forEach((h, idx) => {
        if (typeof h === "string" && h.trim() !== "") {
          projeto[h] = row[idx];
        }
      });

      // Coleta os valores brutos das colunas K e M (índices relativos ao range B:AQ → K=9, M=11)
      const colK = 9;
      const colM = 11;

      const participantesRaw = [row[colK], row[colM]]
        .filter(Boolean)
        .join(";");

      const participantes = participantesRaw
        .split(/[,;]+/)
        .map(part => {
          part = part.trim();

          // Caso esteja no formato: "Nome" <email>
          const match = part.match(/<([^>]+)>/);
          if (match) return match[1].toLowerCase(); // retorna apenas o e-mail

          // Se for apenas nome (sem <>), tenta buscar no mapa
          const nomeLimpo = part.replace(/["']/g, "").toLowerCase();
          return usuariosMap[nomeLimpo] || ""; // retorna e-mail ou string vazia
        })
        .filter(email => email.includes("@")) // remove inválidos
        .filter((email, idx, arr) => arr.indexOf(email) === idx); // remove duplicados

      projeto.participantes = participantes;

      projetos.push(projeto);
    });

    return { success: true, projetos: projetos };

  }
  catch (error) {
    return { success: false, message: "Erro interno: " + error.message };
  }
}

function getProjects() {

  const props = getUserProperties();
  const sessionId = props.sessionId;
  const email = props.email;
  const nome = props.nome;

  const siteProps = getCurrentVersion();
  const versaoAtual = siteProps.version;
  Logger.log("getProjects.versaoAtual: " + versaoAtual);

  if (!sessionId || !email || !nome) {
    return {
      gzip: null,
      data: null,
      success: false,
      versaoAtual : versaoAtual,
      message: "Sessão inválida. Acesso negado."
    };
  }

  let retValidaTempo = validateTimeOutUserSession();
  if (retValidaTempo.sessionExpired){   
    return {
      gzip: null,
      data: null,
      success: false,
      versaoAtual : versaoAtual,
      message: "Sessão expirada.",
      loginRedirect: true
    };
  }

  let resposta = [];

  resposta = getProjetsInternal();

  if(resposta.success){
    Logger.log("Total de projetos: " + resposta.projetos.length);
    Logger.log("Exemplo de projeto: " + JSON.stringify(resposta.projetos[0]));
    
    let projetos = [];
    projetos = resposta.projetos;

    const jsonString = JSON.stringify({ success: true, projetos });

    // Cria um Blob com tipo MIME apropriado
    const blob = Utilities.newBlob(jsonString, 'application/json');

    // Comprime o blob
    const compressedBlob = Utilities.gzip(blob);

    // Codifica o conteúdo do blob GZIP em base64
    const encoded = Utilities.base64Encode(compressedBlob.getBytes());

    return { success: true, gzip: true, data: encoded, versaoAtual : versaoAtual, message: '' };
  }
  else{
    
    return { success: false, gzip: false, message: projetos.message, data: null, versaoAtual : versaoAtual};
  }

}

function getProjectDetail(numProject){
  
  try {
    
    let resposta = [];
    resposta = getProjetsInternal();
    
    if(resposta.success){

      let projetos = [];
      projetos = resposta.projetos;

      // Pesquisa específica
      const projetoEncontrado = projetos.find(p => p["nº"] == numProject); // ou === se quiser tipo exato

      if (!projetoEncontrado) {
        return { success: false, message: "Projeto não encontrado" };
      }
  
      // Compressão de dados para retorno
      const jsonString = JSON.stringify({ success: true, projeto: projetoEncontrado });
      //Logger.log("jsonString :" + jsonString);
      const blob = Utilities.newBlob(jsonString, 'application/json');
      const gzBlob = Utilities.gzip(blob);
      const base64 = Utilities.base64Encode(gzBlob.getBytes());
      return { gzip: true, data: base64 };
    }
    else{
      
      return { success: false, message: "Erro em getProjetsInternal()" };
    }
  }
  catch (error) {
    return { success: false, message: "Erro interno: " + error.message };
  }
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

function registrarMonitoramento(sheet, row, timestamp, user) {
  try {
    const valorG =  sheet.getRange(row, 7).getValue(); // Coluna G = 7

    // Pega o valor da coluna N (número do monitoramento)
    const valorN = sheet.getRange(row, 14).getValue(); // Coluna N = 14
    
    // Converte para número se necessário
    let numeroMonitoramento = valorN;
    if (typeof valorN === 'string') {
      // Remove caracteres não numéricos (como °) e converte para número
      numeroMonitoramento = parseInt(valorN.replace(/[^0-9]/g, ''));
    }
    
    //Logger.log('registrarMonitoramento - Valor da coluna N: ', valorN, 'Número do monitoramento: ', numeroMonitoramento);
    
    // Verifica se é um número válido entre 1 e 24
    if (isNaN(numeroMonitoramento) || numeroMonitoramento < 1 || numeroMonitoramento > 24) {
      Logger.log('Número de monitoramento inválido:', numeroMonitoramento);
      return;
    }
    
    // Calcula a coluna correspondente (U=21, ..., AQ=43)
    // Monitoramento 1° = coluna U (21), 2° = coluna V (22), ..., 24° = coluna AQ (43)
    const colunaDestino = 20 + numeroMonitoramento; // U=21, então 20 + 1 = 21   

    const data = new Date(sheet.getRange(row, 15).getValue());

    const options = {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      timeZone: 'America/Sao_Paulo' // Garante o fuso horário correto
    };

    const dataFormatada = data.toLocaleDateString('pt-BR', options);

    // Pega os valores das colunas N, O, P, Q
    const valorN_formatado = formatarDataOuTexto('N', sheet.getRange(row, 14).getValue());
    const valorO_formatado = dataFormatada;
    //Logger.log('valorO_formatado: ' + valorO_formatado);
    const valorP_formatado = formatarDataOuTexto('P', sheet.getRange(row, 16).getValue());
    const valorQ_formatado = formatarDataOuTexto('Q', sheet.getRange(row, 17).getValue());
    
    // Concatena os valores
    const valorConcatenado = `Em ${timestamp}, ${user} atualizou: Monitoramento: ${valorN_formatado} Próxima data: ${valorO_formatado}, Próxima ação: ${valorP_formatado}, Responsável: ${valorQ_formatado}`;
    
    // Insere na coluna correspondente ao monitoramento
    sheet.getRange(row, colunaDestino).setValue(valorConcatenado);
    
    //Logger.log(`Monitoramento ${numeroMonitoramento}° registrado na coluna ${convertColumnToLetter(colunaDestino)} (${colunaDestino})`);
    //Logger.log('Valor concatenado:', valorConcatenado);
    
  } catch (error) {
    Logger.log('Erro ao registrar monitoramento:', error);
  }
}

  function gravarLogAlteracao(emailUsuario, range, oldValue, editedValue) {

    const col = range.getColumn();
    const row = range.getRow();
    
    const colLetter = convertColumnToLetter(col);
    //Logger.log('gravarLogAlteracao - row: ' + range.getRow() + ', col: ' + range.getColumn() + ', colLetter: ' + colLetter);

    
    const monitorSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.DATA_SHEET_PAGE);
    if (!monitorSheet) {
      Logger.log('Sheet de Monitor não encontrada');
      return;
    }
    
    const logSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_LOG);
    if (!logSheet) {
      Logger.log('Sheet de log não encontrada');
      return;
    }

    if ((colLetter == 'G') || (colLetter == 'N') || (colLetter == 'O') || (colLetter == 'P') || (colLetter == 'Q')) {
    
      const timestamp = new Date();
      const user = emailUsuario || 'Desconhecido';
      const fieldName = monitorSheet.getRange(3, col).getValue() || 'Campo não identificado';

      var valorConvertidoAntigo = '';
      var valorConvertidoNovo = '';

      // CORREÇÃO: Passar o colLetter para a função
      if (colLetter == 'O'){
        valorConvertidoAntigo = formatDateForJS(new Date((parseFloat(oldValue).toFixed(0) - 25568) * 86400000)); 
        valorConvertidoNovo = formatDateForJS(new Date((parseFloat(editedValue).toFixed(0) - 25568) * 86400000));
      }else{
        valorConvertidoAntigo = oldValue;
        valorConvertidoNovo = editedValue;
      }

      const timestampFormatado = Utilities.formatDate(timestamp, Session.getScriptTimeZone(), "dd/MM/yyyy HH:mm:ss");

      // DEBUG: verificar os valores antes de inserir
      //Logger.log('gravarLogAlteracao - Coluna:' + colLetter);
      //Logger.log('gravarLogAlteracao - Valor antigo original:' + oldValue +  ' Tipo: ' + typeof oldValue);
      //Logger.log('gravarLogAlteracao - Valor novo original:'+  editedValue +' Tipo: ' + typeof editedValue);
      //Logger.log('gravarLogAlteracao - Valor antigo convertido:' + valorConvertidoAntigo);
      //Logger.log('gravarLogAlteracao - Valor novo convertido:' + valorConvertidoNovo);

      logSheet.appendRow([
        timestampFormatado,  // Timestamp formatado
        user,
        row,
        colLetter,
        fieldName,
        valorConvertidoAntigo,  // Valor ANTIGO
        valorConvertidoNovo  // Valor NOVO
      ]);

      // Só executa se a edição for nas colunas N, O, P ou Q
      if (['N', 'O', 'P', 'Q'].includes(colLetter)) {
        registrarMonitoramento(monitorSheet, row, timestampFormatado, user);
      }
    }
  }

// ====================================
// FUNÇÃO DE GRAVAÇÃO PELO SITE
// ====================================

function findProjectDetail(numAcao){
  try {
    let resposta = getProjetsInternal();
    if(resposta.success){
      let projetos = resposta.projetos;
      // O range usado em getProjetsInternal é "B4:AQ35", ou seja, começa na linha 4 da planilha.
      for(let i = 0; i < projetos.length; i++){
        if(projetos[i]["nº"] == numAcao.toString()){
          // Retorna também o número da linha correspondente na planilha
          return {success: true, message: "", acao: projetos[i], rowNum: i + 4}; // linha real da planilha
        }
      }
      return { success: false, message: "Ação não encontrada!" };
    } else {      
      return { success: false, message: "Erro em getProjetsInternal()!" };
    }
  }
  catch (error) {
    return { success: false, message: "Erro interno: " + error.message };
  }
}

function saveAcao(user, numAcao, updateSituacao, updateData, objOriginal) {
  Logger.log("user: " + JSON.stringify(user));
  Logger.log("numAcao: " + numAcao);
  Logger.log("updateSituacao: " + JSON.stringify(updateSituacao));
  Logger.log("updateData: " + JSON.stringify(updateData));
  Logger.log("objOriginal: " + JSON.stringify(objOriginal));

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.DATA_SHEET_PAGE);
  if (!sheet) throw new Error("Aba 'Monitor' não encontrada");

  var bSuccess = false;
  var msgError = "";
  var errorCode = 0;
  // errorCode = 1000(tempo expirado)
  // errorCode = 1001(Usuário não é válido para salvar!)
  // errorCode = 1002(erro de gravação)
  // errorCode = 1003(ação não encontrada)
  // errorCode = 1004(objeto original já alterado)

  // validar o tempo de exipração
  let retValidaTempo = validateTimeOutUserSession();
  if (retValidaTempo.sessionExpired){
    msgError = "Sua sessão expirou. Por favor, faça login novamente.";

    Logger.log(msgError);
    errorCode = 1000;

    return {
      success: false,
      errorCode: errorCode,
      message: msgError
    };
  }
  
  // Validar usuário
  const validarUser = getUserProperties();
  if (validarUser.sessionId !== user.sessionId) {
    msgError = "Usuário não é válido para salvar!";
    
    errorCode = 1001;

    return {
      success: false,
      errorCode: errorCode,
      message: msgError
    };
  }

  // Buscar ação e linha
  const respFindAcao = findProjectDetail(numAcao);

  Logger.log("objOriginal: " + JSON.stringify(objOriginal));

  if (respFindAcao.success && respFindAcao.rowNum) {

    // pegar valores das céluas para comparar ao objOriginal
    // se forem iguais, ok continu
    // se forem diferentes, retorna errorCode = 1004(objeto original já alterado)
    
    //originalFormState = {
    //  numAcao: document.getElementById('editAcaoId')?.value || '',
    //  situacao: document.getElementById('editSituacao')?.value || '',
    //  monitoramento: document.getElementById('editMonitoramento')?.value || '',
    //  data: document.getElementById('editProxDataMonitoramento')?.value || '',
    //  acoes: document.getElementById('editProxAcoes')?.value || ''
    //};

    const rowNum = respFindAcao.rowNum;


    const colNumG = convertLetterToColumn('G');
    const rangeG = sheet.getRange(rowNum, colNumG);
    const oldValueG = rangeG.getValue();

    const colNumN = convertLetterToColumn('N');
    const rangeN = sheet.getRange(rowNum, colNumN);
    const oldValueN = rangeN.getValue();
    
    const colNumO = convertLetterToColumn('O');
    const rangeO = sheet.getRange(rowNum, colNumO);
    const oldValueO = rangeO.getValue();
    
    const colNumP = convertLetterToColumn('P');
    const rangeP = sheet.getRange(rowNum, colNumP);
    const oldValueP = rangeP.getValue();
    
    const colNumQ = convertLetterToColumn('Q');
    const rangeQ = sheet.getRange(rowNum, colNumQ);
    const oldValueQ = rangeQ.getValue();
    

    console.log("saveAcao - Antes de comparar");
    console.log("objOriginal.numAcao.toString(): " + objOriginal.numAcao.toString() + ", numAcao: " + numAcao.toString());
    console.log("objOriginal.situacao: " + objOriginal.situacao + ", numoldValueGAcao: " + oldValueG);
    console.log("objOriginal.monitoramento: " + objOriginal.monitoramento + ", oldValueN: " + oldValueN);


    if ((objOriginal.numAcao.toString() !== numAcao.toString()) || (oldValueG !== objOriginal.situacao) || (oldValueN !== objOriginal.monitoramento))
    {
      msgError = "Não foi possível atualizar a Ação pois outra pessoa já atualizou primeiro.";
      
      errorCode = 1004;

      return {
        success: false,
        errorCode: errorCode,
        message: msgError
      };
    }


    try {
      // SITUAÇÃO
      if (updateSituacao && typeof updateSituacao.situacao === "string" && updateSituacao.situacao.trim() !== "") {
        rangeG.setValue(updateSituacao.situacao.trim());
        gravarLogAlteracao(user.email, rangeG, oldValueG, updateSituacao.situacao.trim());
        
        bSuccess = true;
      }

      // MONITORAMENTO, DATA, PRÓXIMAS AÇÕES, RESPONSÁVEL
      if (updateData && typeof updateData.monitoramento === "string" && updateData.monitoramento.trim() !== "") {
        // Monitoramento
        rangeN.setValue(updateData.monitoramento.trim());
        gravarLogAlteracao(user.email, rangeN, oldValueN, updateData.monitoramento.trim());

        // Data
        rangeO.setValue(updateData.data ? updateData.data.trim() : "");
        gravarLogAlteracao(user.email, rangeO, oldValueO, updateData.data ? updateData.data.trim() : "");

        // Próximas ações
        rangeP.setValue(updateData.proximasacoes ? updateData.proximasacoes.trim() : "");
        gravarLogAlteracao(user.email, rangeP, oldValueP, updateData.proximasacoes ? updateData.proximasacoes.trim() : "");

        // Responsável
        rangeQ.setValue(validarUser.nome);
        gravarLogAlteracao(user.email, rangeQ, oldValueQ, validarUser.nome);

        bSuccess = true;
      }

    } catch (e) {
      errorCode = 1001;
      Logger.log("Erro ao Gravar a Ação:");
      if (e instanceof Error) {
        Logger.log("Mensagem: " + e.message);
        Logger.log("Stack: " + e.stack);
        msgError = "Mensagem: " + e.message +  "Stack: " + e.stack;
      } else {
        msgError = "Erro genérico: " + JSON.stringify(e);
        Logger.log(msgError);
      }

    }
  } else {
    msgError = respFindAcao.message;
    errorCode = 1002;
    Logger.log("respFindAcao.success = false: " + msgError);
  }

  Logger.log("bSuccess: " + bSuccess + " errorCode: " + errorCode + " msgError: " + msgError);

  return {
    success: bSuccess,
    errorCode: errorCode,
    message: msgError
  };
}


// ====================================
// FUNÇÕES DE FORMATAÇÃO DE DATAS E STRINGS
// ====================================

function formatDateForJS(date) {
  if (!date || typeof date === 'string') return date;
  return Utilities.formatDate(new Date(date), Session.getScriptTimeZone(), "dd-MM-yyyy");
}

function formatarDataOuTexto(colLetter, valor) {
  
  // Se for null, undefined ou string vazia, retorna como está
  if (!valor || valor === '') return valor;

  if((colLetter == 'G') || (colLetter == 'N') || (colLetter == 'P') || (colLetter == 'Q'))  {
    return valor;
  }

  if(colLetter == 'O') {
    
    var numeroValor = 0 ;

    if (valor instanceof Date && !isNaN(valor)) {
      //Logger.log("formatarDataOuTexto - Date");
      valor =  formatCellAsDate();
    }
    
  }
  
  return valor; // Retorna o valor original se não conseguir formatar
}

// ================================
// Função privada!
// ================================

function getZimbraConfiguration_(){
  var url = '';
  var account = '';
  var passwd = '';
  var success = false;
  var msgreturn = '';
  var retorno = {};

  try{
    url = 'https://' + CONFIG.SMTP_SERVER + ':' + CONFIG.SMTP_PORT + CONFIG.SMTP_SERVER_COMP;
    account = CONFIG.EMAIL_SENDER;
    passwd = CONFIG.PASSWD_EMAIL_SENDER;
    displayAccount = CONFIG.EMAIL_SENDER_DISPLAY;
    success = true;
  }
  catch(e){
    msgreturn = 'Erro ao recuperar as informações de configuração de envio de e-mail: ' + e.message;
  }
  retorno = {success: success, msgreturn: msgreturn, url: url, displayAccount: displayAccount, account: account, password: passwd };
  
  //Logger.log(JSON.stringify(retorno));
  return retorno;
}

// ================================
// Função privada!
// ================================

function encodeRFC2047(str) {
  return "=?UTF-8?B?" + Utilities.base64Encode(str, Utilities.Charset.UTF_8) + "?=";
}

function getZimbraAuth_() {
  
  var msgError = '';
  var retorno = {};

  var retAuth = getZimbraConfiguration_();

  if(!retAuth.success){
    retorno = { sucess: false, message: retAuth.msgreturn, url: '', authToken: '' };
    //Logger.log(JSON.stringify(retorno));
    return retorno;
  }

  var url = retAuth.url;

  var payload = {
    Body: {
      AuthRequest: {
        _jsns: "urn:zimbraAccount",
        account: {
          _content: retAuth.account,
          by: "name"
        },
        password: retAuth.password,
        persistAuthTokenCookie: false
      }
    }
  };

  var options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  var response = null;
  var retjson = '';
  var authToken = '';
  
  try {
    response = UrlFetchApp.fetch(url, options);
    
    retjson = JSON.parse(response.getContentText());
    //Logger.log('retjson: ' + JSON.stringify(retjson));

    authToken = retjson.Body.AuthResponse.authToken[0]._content;
  } catch (e) {
    //Logger.log("Erro ao fazer requisição: " + e);
    return { sucess: false, message: "Erro ao fazer requisição: " + e, url: '', authToken: '' };
  }

  if (authToken.trim() !== '') {
    retorno = { sucess: true, message: msgError, url: retAuth.url, name: displayAccount, sender: retAuth.account, authToken: authToken };
  }
  else{
    msgError = 'Token não encontrado: ' + retjson;
    retorno = { sucess: false, message: msgError, url: '', sender: '', authToken: '' };
  }

  //Logger.log('retorno: ' + JSON.stringify(retorno));
  return retorno;
}


function sendZimbraHtmlEmail(destinatario, assunto, htmlContent) {
  var retAuth = getZimbraAuth_();
  var retorno = {};

  if (retAuth.success === false) {
    return { success: false, message: 'Erro ao enviar e-mail: ' + retAuth.message };
  }

  var url = retAuth.url;
  var authToken = retAuth.authToken;
  var fromEmail = encodeRFC2047(retAuth.name);
  fromEmail = fromEmail + '<' + retAuth.sender + '>';

  var payload = {
    Header: {
      context: {
        _jsns: "urn:zimbra",
        authToken: authToken
      }
    },
    Body: {
      SendMsgRequest: {
        _jsns: "urn:zimbraMail",
        m: {
          e: [
            { t: "f", a: fromEmail },
            { t: "t", a: destinatario },
            { t: "r", a: "no-reply@seger.es.gov.br" }
          ],
          su: {
            _content: assunto
          },
          mp: {
            ct: "text/html",
            content: htmlContent
          }
        }
      }
    }
  };

  var options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  try {
    var response = UrlFetchApp.fetch(url, options);
    var result = response.getContentText();

    retorno = { success: true, message: '' }
    return retorno;

  } catch (e) {
    return { success: false, message: 'Erro ao enviar e-mail: ' + e };
  }
}



// *******************************************************************************************************************
// Funções de teste
// *******************************************************************************************************************

function testeSendZimbraEmail(){

  const resetLink = `https://link_do_site.com.br?page=remind-password&blablabla`; //`${ScriptApp.getService().getUrl()}?page=remind-password&token=${resetToken}`;
  
  const htmlBody = `<!DOCTYPE html>
                    <html lang="pt-BR">
                    <head>
                      <meta charset="UTF-8" />
                      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                      <title>E-mail de link para redefinição de Senha</title>
                      <style>
                        body {
                          margin: 0;
                          padding: 0;
                          font-family: Arial, sans-serif;
                          background-color: #f2f2f2;
                        }
                        .container {
                          width: 100%;
                          background-color: #f2f2f2;
                          padding: 20px 0;
                        }
                        .content {
                          max-width: 600px;
                          margin: 0 auto;
                          background-color: #ffffff;
                          border-radius: 8px;
                          overflow: hidden;
                          box-shadow: 0 0 10px rgba(0,0,0,0.05);
                        }
                        .header {
                          background-color: #004aad;
                          color: #ffffff;
                          padding: 20px;
                          text-align: center;
                        }
                        .body {
                          padding: 30px;
                          color: #333333;
                        }
                        .body p {
                          font-size: 16px;
                          line-height: 1.6;
                        }
                        .btn {
                          display: inline-block;
                          margin-top: 20px;
                          padding: 12px 24px;
                          background-color: #004aad;
                          color: #ffffff !important;
                          text-decoration: none;
                          border-radius: 5px;
                          font-weight: bold;
                        }
                        .footer {
                          padding: 20px;
                          font-size: 12px;
                          text-align: center;
                          color: #888888;
                        }
                      </style>
                    </head>
                    <body>
                      <div class="container">
                        <div class="content">
                          <div class="header">
                            <h1>Redefinição de Senha</h1>
                          </div>
                          <div class="body">
                            <p>Olá,</p>
                            <p>Recebemos uma solicitação para redefinir a sua senha. Para continuar com a redefinição, clique no botão abaixo:</p>
                            <p style="text-align: center;">
                              <a href="` + resetLink + `" class="btn">Redefinir Senha</a>
                            </p>
                            <p>Se você não solicitou esta alteração, por favor ignore este e-mail. Sua senha permanecerá a mesma.</p>
                            <p>Atenciosamente,<br>Equipe GPP</p>
                          </div>
                          <div class="footer">
                            <p id="ano"></p> 
                          </div>
                        </div>
                      </div>
                      <script>
                        const dataAtual = new Date();
                        const anoAtual = dataAtual.getFullYear();
                        document.getElementById("ano").innerHTML = &copy + anoAtual + ' GPP.'
                      </script>
                    </body>
                    </html>`;

  var retSendEmail = sendZimbraHtmlEmail('alexandrewmohamad@gmail.com', 'Link para redefinição de senha', htmlBody);
  Logger.log(retSendEmail);
}


function testarResetPasswordWithToken(){
  var email = "alexandre.mohamad@seger.es.gov.br";
  var token = "97ded042-61bf-47f1-87c7-16a297a83391";
  var novaSenha = "222";
  var retorno = resetPasswordWithToken(email, token, novaSenha );

  Logger.log("retorno: " + JSON.stringify(retorno) );
  
}

function testeauthenticateUser(){
  Logger.log("Teste de usuário encontrado!");
  let email = "claudio.campos@seger.es.gov.br";
  let password = "111";
  
  Logger.log("email parâmetro: " + email);
  Logger.log("password parâmetro: " + password);
  let resposta = {};
  resposta = authenticateUser(email, password);
  Logger.log("success: " + resposta.success);
  Logger.log("sessionId: " + resposta.sessionId);

  Logger.log("===========================================");

  Logger.log("Teste de usuário NÃO ENCONTRADO!");
  email = "andeeeerson.costa@enap.gov.br";
  password = "123";
  
  Logger.log("email parâmetro: " + email);
  Logger.log("password parâmetro: " + password);
  resposta = {};
  resposta = authenticateUser(email, password);
  Logger.log("success: " + resposta.success);
  Logger.log("sessionId: " + resposta.sessionId);

  Logger.log("===========================================");
  
  Logger.log("Teste de usuário INATIVO!");
  email = "anderson.costa@enap.gov.br";
  password = "123";
  
  Logger.log("email parâmetro: " + email);
  Logger.log("password parâmetro: " + password);
  resposta = {};
  resposta = authenticateUser(email, password);
  Logger.log("success: " + resposta.success);
  Logger.log("sessionId: " + resposta.sessionId);
}


function testarResetPassword(){
  
  Logger.log("Teste de alteração de senha!");
  let email = "alexandre.mohamad@seger.es.gov.br";
  let oldPassword = "111";
  let newPassword = "222";
  
  Logger.log("email parâmetro: " + email);
  Logger.log("oldPassword parâmetro: " + oldPassword);
  Logger.log("newPassword parâmetro: " + newPassword);

  let resposta = {};
  resposta = resetPassword(email, oldPassword, newPassword);
  Logger.log("success: " + resposta.success);
  Logger.log("message: " + resposta.message);
  Logger.log("sessionId: " + resposta.sessionId);
}

function testarSendResetLink(){
  Logger.log("Teste de Envio de Link - Esqueci minha senha!");
  let email = "alexandre.mohamad@seger.es.gov.br";

  Logger.log("email parâmetro: " + email);
  let resposta = {};
  resposta = sendResetLink(email);
  
  Logger.log("success: " + resposta.success);
  Logger.log("message: " + resposta.message);
  Logger.log("resetLink: " + resposta.resetLink);
}

function testeGetProjects(){  
  Logger.log("Teste de recuperação dos projetos");
  let resposta = {};
  resposta = getProjects();
  
  Logger.log("resposta.gzip: " + resposta.gzip);

}

function testarGetOptionsForDropdown(){
  let bTodosOption = false;

  Logger.log("Teste de Popular Combo Eixo SEM opção Todos");
  let resposta = getOptionsForDropdown('DROPDOWN_EIXO', bTodosOption, true);

  Logger.log("Tamanho do array: " + resposta.length.toString());
  for (i = 0; i < resposta.length ; i ++){
    Logger.log("Opção do Eixo SEM opção Todos: " + [i].toString() + ": " + resposta[i]);
  }
  
  bTodosOption = true;
  Logger.log("Teste de Popular Combo Eixo COM opção Todos");
  resposta = getOptionsForDropdown('DROPDOWN_EIXO', bTodosOption, true);

  for (i = 0; i < resposta.length ; i ++){
    Logger.log("Opção do Eixo COM opção Todos:  " + [i].toString() + ": " + resposta[i]);
  }

  bTodosOption = false;
  Logger.log("Teste de Popular Combo SITUAÇÃO SEM opção Todos");
  resposta = getOptionsForDropdown('DROPDOWN_SITUACAO', bTodosOption, true);

  Logger.log("Tamanho do array: " + resposta.length.toString());
  for (i = 0; i < resposta.length ; i ++){
    Logger.log("Opção de Situação SEM opção Todos: " + [i].toString() + ": " + resposta[i]);
  }
  
  bTodosOption = true;
  Logger.log("Teste de Popular Combo SITUAÇÃO COM opção Todos");
  resposta = getOptionsForDropdown('DROPDOWN_SITUACAO', bTodosOption, true);

  for (i = 0; i < resposta.length ; i ++){
    Logger.log("Opção de Situação COM opção Todos: " + [i].toString() + ": " + resposta[i]);
  }

  bTodosOption = false;
  Logger.log("Teste de Popular Combo MONITORAMENTO SEM opção Todos");
  resposta = getOptionsForDropdown('DROPDOWN_MONITORAMENTO', bTodosOption, true);

  Logger.log("Tamanho do array: " + resposta.length.toString());
  for (i = 0; i < resposta.length ; i ++){
    Logger.log("Opção de MONITORAMENTO SEM opção Todos: " + [i].toString() + ": " + resposta[i]);
  }
  
  bTodosOption = true;
  Logger.log("Teste de Popular Combo MONITORAMENTO COM opção Todos");
  resposta = getOptionsForDropdown('DROPDOWN_MONITORAMENTO', bTodosOption, true);

  for (i = 0; i < resposta.length ; i ++){
    Logger.log("Opção de MONITORAMENTO COM opção Todos: " + [i].toString() + ": " + resposta[i]);
  }


  bTodosOption = false;
  Logger.log("Teste de Popular Combo DROPDOWN_PESSOAS SEM opção Todos");
  resposta = getOptionsForDropdown('DROPDOWN_PESSOAS', bTodosOption, true);

  Logger.log("Tamanho do array: " + resposta.length.toString());
  for (i = 0; i < resposta.length ; i ++){
    Logger.log("Opção de DROPDOWN_PESSOAS SEM opção Todos: " + [i].toString() + ": " + resposta[i]);
  }
  
  bTodosOption = true;
  Logger.log("Teste de Popular Combo DROPDOWN_PESSOAS COM opção Todos");
  resposta = getOptionsForDropdown('DROPDOWN_PESSOAS', bTodosOption, true);

  for (i = 0; i < resposta.length ; i ++){
    Logger.log("Opção de DROPDOWN_PESSOAS COM opção Todos: " + [i].toString() + ": " + resposta[i]);
  }

}

function testarGetConfigKeysForSituacao() {

  let situacao = "em Andamento";
  Logger.log("Teste deGetConfigKeysForSituacao = Em Andamento");
  let resposta = getConfigKeysForSituacao(situacao);

  Logger.log("backgroud-color: " + resposta.background);
  Logger.log("color: " + resposta.font);

}

function testarGetProjectDetail() {
  let numProject = 3;
  Logger.log("Parâmetro numProject: " + numProject);

  Logger.log("Teste de GetProjectDetail");
  let resposta = getProjectDetail(numProject);

  if (!resposta || !resposta.gzip || !resposta.data) {
    Logger.log("Erro ou resposta inesperada: " + JSON.stringify(resposta));
    return;
  }
}

  
function testarEdicaoAbaMonitor() {

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.DATA_SHEET_PAGE);
  if (!sheet) throw new Error("Aba 'Monitor' não encontrada");

  Logger.log("Teste de EdicaoAbaMonitor");
  
  Logger.log("Editar situação na linha 4");
  var colNum = convertLetterToColumn('G');
  const valorSituacao = sheet.getRange(4, colNum).getValue();
  
  Logger.log("Situação Atual: " + valorSituacao);

  if (valorSituacao == 'ATRASADA'){
    sheet.getRange(4, colNum).setValue('CONCLUÍDA');
    Logger.log("Situação Nova: " + 'CONCLUÍDA');
  }
  
  if (valorSituacao == 'CONCLUÍDA'){
    sheet.getRange(4, colNum).setValue('ATRASADA');
    Logger.log("Situação Nova: " + 'ATRASADA');
  }
}

function testarFindProjectDetail(){
  
  Logger.log("Teste de FindProjectDetail");
  const resposta = findProjectDetail(3);
  
  Logger.log("resposta: " + resposta.success);
  Logger.log("ação: " + JSON.stringify(resposta.acao));
}

function testarVerificaPrazoFinalAcao(){

  Logger.log("Teste de VerificaPrazoFinalAcao");
  const resposta = verificaPrazoFinalAcao();
  
  Logger.log("resposta.success: " + resposta.success);
  Logger.log("resposta.message: " + resposta.message);
  Logger.log("resposta.arrayAcoesParaVencer: " + JSON.stringify(resposta.arrayAcoesParaVencer));  

}
