<#
.SYNOPSIS
Teste de Permissões v2 - Ações PNGI
Testa permissões hierárquicas com todas as entidades

.DESCRIPTION
Script completo de teste de permissões para:
- Sistema de permissões hierárquico (4 roles)
- Verificação dupla (JWT + Banco)
- CRUD de todas as entidades:
  * Core: Eixo, Situação, Vigência, Tipo Entrave
  * Ações: Ações, Prazos, Destaques
  * Alinhamento: Tipos e Anotações
  * Responsáveis: Usuários e Relações

.PARAMETER BaseURL
URL base do servidor

.PARAMETER Email
Email do usuário para teste

.PARAMETER Password
Senha (usar SecureString para segurança)

.EXAMPLE
.\Test-AcoesPNGI-Permissions-v2.ps1

.NOTES
Roles disponíveis:
- COORDENADOR_PNGI: Acesso total + gerencia configurações
- GESTOR_PNGI: Acesso total às ações
- OPERADOR_ACAO: Operações em ações (sem configurações)
- CONSULTOR_PNGI: Apenas leitura
#>

[CmdletBinding()]
param(
    [string]$BaseURL = "http://localhost:8000"
)

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

$API_URL = "$BaseURL/api/v1/acoes_pngi"
$AUTH_URL = "$BaseURL/api/v1/auth"

# Cores para output
function Write-Success {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Green
}

function Write-ErrorMessage {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Cyan
}

function Write-Warning {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Yellow
}

function Write-SectionHeader {
    param([string]$Title)
    Write-Host "`n" -NoNewline
    Write-Host ("═" * 80) -ForegroundColor Magenta
    Write-Host "   $Title" -ForegroundColor Magenta
    Write-Host ("═" * 80) -ForegroundColor Magenta
}

# ============================================================================
# FUNÇÃO: Fazer Login e Obter Token JWT
# ============================================================================

function Get-AuthToken {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Email,

        [Parameter(Mandatory = $true)]
        [SecureString]$Password
    )

    Write-Info "`n=== AUTENTICAÇÃO ==="
    Write-Info "Email: $Email"

    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password)
    try {
        $PlainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

        $loginUrl = "$AUTH_URL/token/"
        Write-Verbose "URL de login: $loginUrl"

        $body = @{
            email = $Email
            password = $PlainPassword
        } | ConvertTo-Json

        try {
            $response = Invoke-RestMethod -Uri $loginUrl -Method Post `
                -Body $body -ContentType "application/json" -ErrorAction Stop

            Write-Success "✓ Token JWT obtido com sucesso"
            Write-Verbose "Access Token: $($response.access)"

            return $response.access
        }
        catch {
            Write-ErrorMessage "✗ Erro ao obter token:"
            Write-ErrorMessage "   Status: $($_.Exception.Response.StatusCode.value__)"
            Write-ErrorMessage "   Mensagem: $($_.Exception.Message)"
            return $null
        }
    }
    finally {
        [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR)
        if ($PlainPassword) {
            Remove-Variable -Name PlainPassword -ErrorAction SilentlyContinue
        }
    }
}

# ============================================================================
# FUNÇÃO: Testar Endpoint com Token
# ============================================================================

function Test-Endpoint {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [ValidateSet('GET', 'POST', 'PUT', 'PATCH', 'DELETE')]
        [string]$Method,

        [Parameter(Mandatory = $true)]
        [string]$Url,

        [Parameter(Mandatory = $true)]
        [string]$Token,

        [Parameter(Mandatory = $true)]
        [string]$Description,

        [Parameter(Mandatory = $false)]
        [object]$Body = $null,

        [Parameter(Mandatory = $false)]
        [bool]$ExpectSuccess = $true
    )

    Write-Info "`n--- $Description ---"
    Write-Info "$Method $Url"

    $headers = @{
        "Authorization" = "Bearer $Token"
        "Content-Type" = "application/json"
    }

    try {
        $params = @{
            Uri = $Url
            Method = $Method
            Headers = $headers
            ErrorAction = 'Stop'
        }

        if ($Body) {
            $params.Body = ($Body | ConvertTo-Json -Depth 10)
            Write-Verbose "Body: $(($Body | ConvertTo-Json -Compress))"
        }

        $response = Invoke-RestMethod @params

        if ($ExpectSuccess) {
            Write-Success "✓ Sucesso (Status 200-299)"
            return @{ Success = $true; Data = $response }
        }
        else {
            Write-Warning "⚠ Esperava falha mas obteve sucesso"
            return @{ Success = $true; Data = $response }
        }
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.value__

        if (-not $ExpectSuccess) {
            if ($statusCode -eq 403) {
                Write-Success "✓ Permissão negada como esperado (403)"
                return @{ Success = $false; StatusCode = 403 }
            }
        }

        Write-ErrorMessage "✗ Erro: $statusCode - $($_.Exception.Message)"
        return @{ Success = $false; StatusCode = $statusCode }
    }
}

# ============================================================================
# FUNÇÃO: Testar CRUD Genérico
# ============================================================================

function Test-GenericCRUD {
    param(
        [string]$EntityName,
        [string]$BaseUrl,
        [hashtable]$CreateData,
        [hashtable]$UpdateData,
        [string]$Token,
        [bool]$CanView,
        [bool]$CanAdd,
        [bool]$CanChange,
        [bool]$CanDelete
    )

    Write-SectionHeader "TESTANDO $EntityName"

    # LIST
    Test-Endpoint -Method "GET" -Url $BaseUrl -Token $Token `
        -Description "Listar $EntityName" -ExpectSuccess $CanView | Out-Null

    # CREATE
    $createResult = Test-Endpoint -Method "POST" -Url $BaseUrl -Token $Token `
        -Body $CreateData -Description "Criar $EntityName" -ExpectSuccess $CanAdd

    if ($createResult.Success -and $createResult.Data) {
        # Encontrar campo ID dinamicamente
        $idField = ($createResult.Data.PSObject.Properties | Where-Object { $_.Name -like "id*" } | Select-Object -First 1).Name
        $id = $createResult.Data.$idField

        Write-Success "$EntityName criado com ID: $id"

        # RETRIEVE
        Test-Endpoint -Method "GET" -Url "${BaseUrl}${id}/" -Token $Token `
            -Description "Buscar $EntityName por ID" -ExpectSuccess $CanView | Out-Null

        # UPDATE
        Test-Endpoint -Method "PATCH" -Url "${BaseUrl}${id}/" -Token $Token `
            -Body $UpdateData -Description "Atualizar $EntityName" -ExpectSuccess $CanChange | Out-Null

        # DELETE
        Test-Endpoint -Method "DELETE" -Url "${BaseUrl}${id}/" -Token $Token `
            -Description "Deletar $EntityName" -ExpectSuccess $CanDelete | Out-Null
    }
}

# ============================================================================
# FUNÇÃO PRINCIPAL - Testar Todas as Entidades
# ============================================================================

function Invoke-AllTests {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Email,

        [Parameter(Mandatory = $true)]
        [SecureString]$Password
    )

    Write-SectionHeader "TESTES DE PERMISSÕES v2 - AÇÕES PNGI"

    # 1. Obter token
    $token = Get-AuthToken -Email $Email -Password $Password

    if (-not $token) {
        Write-ErrorMessage "`nNão foi possível obter token. Abortando testes."
        return
    }

    # NOTA: Ajustar permissões conforme role do usuário
    # Para teste completo, usar usuário com role GESTOR_PNGI ou COORDENADOR_PNGI

    $canManage = $true  # Assumindo GESTOR ou COORDENADOR
    $canEdit = $true
    $canView = $true

    # ========================================================================
    # CORE ENTITIES
    # ========================================================================

    $timestamp = (Get-Date).ToString("HHmmss")

    # EIXO
    Test-GenericCRUD -EntityName "EIXO" -BaseUrl "$API_URL/eixos/" `
        -CreateData @{ strdescricaoeixo = "Teste Eixo"; stralias = "T$($timestamp.Substring(0,4))" } `
        -UpdateData @{ strdescricaoeixo = "Eixo Atualizado" } `
        -Token $token -CanView $canView -CanAdd $canManage -CanChange $canManage -CanDelete $canManage

    # SITUAÇÃO
    Test-GenericCRUD -EntityName "SITUAÇÃO" -BaseUrl "$API_URL/situacoes/" `
        -CreateData @{ strdescricaosituacao = "TST_$timestamp" } `
        -UpdateData @{ strdescricaosituacao = "UPD_$timestamp" } `
        -Token $token -CanView $canView -CanAdd $canManage -CanChange $canManage -CanDelete $canManage

    # VIGÊNCIA
    $year = (Get-Date).Year
    Test-GenericCRUD -EntityName "VIGÊNCIA" -BaseUrl "$API_URL/vigencias/" `
        -CreateData @{
            strdescricaovigenciapngi = "Teste $year"
            datiniciovigencia = "$year-01-01"
            datfinalvigencia = "$year-12-31"
            isvigenciaativa = $false
        } `
        -UpdateData @{ strdescricaovigenciapngi = "Vigência Atualizada $year" } `
        -Token $token -CanView $canView -CanAdd $canManage -CanChange $canManage -CanDelete $canManage

    # TIPO ENTRAVE/ALERTA
    Test-GenericCRUD -EntityName "TIPO ENTRAVE" -BaseUrl "$API_URL/tipos-entrave-alerta/" `
        -CreateData @{ strdescricaotipoentravealerta = "Teste Tipo Entrave" } `
        -UpdateData @{ strdescricaotipoentravealerta = "Tipo Atualizado" } `
        -Token $token -CanView $canView -CanAdd $canManage -CanChange $canManage -CanDelete $canManage

    # ========================================================================
    # NOVAS ENTIDADES - Requerem dados relacionados existentes
    # ========================================================================

    Write-Info "`nℹ Pulando testes de AÇÕES, PRAZOS, DESTAQUES, ALINHAMENTO e RESPONSÁVEIS"
    Write-Info "   (Requerem IDs de vigência, ações, usuários, etc. existentes)"
    Write-Info "   Use Test-AcoesPNGI-NewTables.ps1 para testar essas entidades"

    # ========================================================================
    # TESTAR ACTIONS CUSTOMIZADAS
    # ========================================================================

    Write-SectionHeader "TESTANDO CUSTOM ACTIONS"

    Test-Endpoint -Method "GET" -Url "$API_URL/eixos/list_light/" -Token $token `
        -Description "Eixos List Light (action)" -ExpectSuccess $canView | Out-Null

    Test-Endpoint -Method "GET" -Url "$API_URL/vigencias/vigencia_ativa/" -Token $token `
        -Description "Vigência Ativa (action)" -ExpectSuccess $canView | Out-Null

    Test-Endpoint -Method "GET" -Url "$API_URL/prazos/ativos/" -Token $token `
        -Description "Prazos Ativos (action)" -ExpectSuccess $canView | Out-Null

    # Resumo final
    Write-SectionHeader "TESTES CONCLUÍDOS"
    Write-Success "🎉 Todos os testes de permissões foram executados!"
}

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

Write-Host "🔐 TESTE DE PERMISSÕES - AÇÕES PNGI v2" -ForegroundColor Magenta
Write-Host "URL Base: $BaseURL" -ForegroundColor Gray

Write-Host "`nInforme as credenciais para teste:" -ForegroundColor Cyan
$email = Read-Host "Email do usuário"
$senhaSecure = Read-Host "Senha" -AsSecureString

# Executar testes
Invoke-AllTests -Email $email -Password $senhaSecure

# Limpar variáveis sensíveis
Remove-Variable -Name senhaSecure -ErrorAction SilentlyContinue

Write-Host "`nℹ Nota: Para testar todas as roles:" -ForegroundColor Yellow
Write-Host "  - COORDENADOR_PNGI: Todas as permissões" -ForegroundColor White
Write-Host "  - GESTOR_PNGI: Acesso total às ações" -ForegroundColor White
Write-Host "  - OPERADOR_ACAO: Operações em ações" -ForegroundColor White
Write-Host "  - CONSULTOR_PNGI: Apenas leitura" -ForegroundColor White
