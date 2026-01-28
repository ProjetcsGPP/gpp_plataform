# ============================================================================
# Script de Testes de Permissões - Ações PNGI
# Versão: 2.0 - Segura e com boas práticas
# ============================================================================

[CmdletBinding()]
param()

# Configurações
$BASE_URL = "http://localhost:8000"
$API_URL = "$BASE_URL/api/v1/acoes_pngi"

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

# ============================================================================
# FUNÇÃO: Fazer Login e Obter Token
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
    
    # Converter SecureString para texto plano (apenas para envio HTTPS)
    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password)
    try {
        $PlainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
        
        $loginUrl = "$BASE_URL/api/token/"
        $body = @{
            email = $Email
            password = $PlainPassword
        } | ConvertTo-Json
        
        try {
            $response = Invoke-RestMethod -Uri $loginUrl -Method Post `
                -Body $body -ContentType "application/json"
            
            Write-Success "✓ Token obtido com sucesso"
            return $response.access
        }
        catch {
            Write-ErrorMessage "✗ Erro ao obter token: $($_.Exception.Message)"
            return $null
        }
    }
    finally {
        # Limpar senha da memória
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
# FUNÇÃO: Testar Permissões do Usuário
# ============================================================================

function Test-UserPermissions {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Token
    )
    
    Write-Info "`n========================================="
    Write-Info "TESTANDO ENDPOINT DE PERMISSÕES"
    Write-Info "========================================="
    
    $url = "$API_URL/permissions/"
    $result = Test-Endpoint -Method "GET" -Url $url -Token $Token `
        -Description "Buscar permissões do usuário"
    
    if ($result.Success) {
        $perms = $result.Data
        
        Write-Info "`nDados do Usuário:"
        Write-Host "  Email: $($perms.email)" -ForegroundColor White
        Write-Host "  Nome: $($perms.name)" -ForegroundColor White
        Write-Host "  Role: $($perms.role)" -ForegroundColor Yellow
        Write-Host "  Superuser: $($perms.is_superuser)" -ForegroundColor White
        
        Write-Info "`nPermissões:"
        $perms.permissions | ForEach-Object {
            Write-Host "  - $_" -ForegroundColor White
        }
        
        Write-Info "`nGrupos:"
        Write-Host "  Gerenciar Config: $($perms.groups.can_manage_config)" -ForegroundColor White
        Write-Host "  Gerenciar Ações: $($perms.groups.can_manage_acoes)" -ForegroundColor White
        Write-Host "  Deletar: $($perms.groups.can_delete)" -ForegroundColor White
        
        Write-Info "`nPermissões Específicas:"
        Write-Host "  Eixo:" -ForegroundColor Yellow
        Write-Host "    Add: $($perms.specific.eixo.add)" -ForegroundColor White
        Write-Host "    Change: $($perms.specific.eixo.change)" -ForegroundColor White
        Write-Host "    Delete: $($perms.specific.eixo.delete)" -ForegroundColor White
        Write-Host "    View: $($perms.specific.eixo.view)" -ForegroundColor White
        
        return $perms
    }
    
    return $null
}

# ============================================================================
# FUNÇÃO: Testar CRUD de Eixos
# ============================================================================

function Test-EixoCRUD {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Token,
        
        [Parameter(Mandatory = $true)]
        [object]$Permissions
    )
    
    Write-Info "`n========================================="
    Write-Info "TESTANDO CRUD DE EIXOS"
    Write-Info "========================================="
    
    $baseUrl = "$API_URL/eixos/"
    
    # 1. LIST (GET)
    $canView = $Permissions.specific.eixo.view
    Test-Endpoint -Method "GET" -Url $baseUrl -Token $Token `
        -Description "Listar Eixos (requer view_eixo)" `
        -ExpectSuccess $canView | Out-Null
    
    # 2. LIST LIGHT (GET)
    Test-Endpoint -Method "GET" -Url "${baseUrl}list_light/" -Token $Token `
        -Description "Listar Eixos (light)" `
        -ExpectSuccess $canView | Out-Null
    
    # 3. CREATE (POST)
    $canAdd = $Permissions.specific.eixo.add
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $newEixo = @{
        strdescricaoeixo = "Eixo Teste PowerShell $timestamp"
        stralias = "ETP"
    }
    
    $createResult = Test-Endpoint -Method "POST" -Url $baseUrl -Token $Token `
        -Body $newEixo `
        -Description "Criar Eixo (requer add_eixo)" `
        -ExpectSuccess $canAdd
    
    if ($createResult.Success -and $createResult.Data.ideixo) {
        $eixoId = $createResult.Data.ideixo
        Write-Success "Eixo criado com ID: $eixoId"
        
        # 4. RETRIEVE (GET by ID)
        Test-Endpoint -Method "GET" -Url "${baseUrl}${eixoId}/" -Token $Token `
            -Description "Buscar Eixo por ID (requer view_eixo)" `
            -ExpectSuccess $canView | Out-Null
        
        # 5. UPDATE (PATCH)
        $canChange = $Permissions.specific.eixo.change
        $updateData = @{
            strdescricaoeixo = "Eixo Teste ATUALIZADO"
        }
        
        Test-Endpoint -Method "PATCH" -Url "${baseUrl}${eixoId}/" -Token $Token `
            -Body $updateData `
            -Description "Atualizar Eixo (requer change_eixo)" `
            -ExpectSuccess $canChange | Out-Null
        
        # 6. DELETE
        $canDelete = $Permissions.specific.eixo.delete
        Test-Endpoint -Method "DELETE" -Url "${baseUrl}${eixoId}/" -Token $Token `
            -Description "Deletar Eixo (requer delete_eixo)" `
            -ExpectSuccess $canDelete | Out-Null
    }
}

# ============================================================================
# FUNÇÃO: Testar CRUD de Situações
# ============================================================================

function Test-SituacaoCRUD {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Token,
        
        [Parameter(Mandatory = $true)]
        [object]$Permissions
    )
    
    Write-Info "`n========================================="
    Write-Info "TESTANDO CRUD DE SITUAÇÕES"
    Write-Info "========================================="
    
    $baseUrl = "$API_URL/situacoes/"
    
    $canView = $Permissions.specific.situacaoacao.view
    $canAdd = $Permissions.specific.situacaoacao.add
    $canChange = $Permissions.specific.situacaoacao.change
    $canDelete = $Permissions.specific.situacaoacao.delete
    
    # LIST
    Test-Endpoint -Method "GET" -Url $baseUrl -Token $Token `
        -Description "Listar Situações (requer view_situacaoacao)" `
        -ExpectSuccess $canView | Out-Null
    
    # CREATE
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $newSituacao = @{
        strdescricaosituacao = "Situação Teste $timestamp"
        stralias = "SIT_$timestamp"
    }
    
    $createResult = Test-Endpoint -Method "POST" -Url $baseUrl -Token $Token `
        -Body $newSituacao `
        -Description "Criar Situação (requer add_situacaoacao)" `
        -ExpectSuccess $canAdd
    
    if ($createResult.Success -and $createResult.Data.idsituacaoacao) {
        $sitId = $createResult.Data.idsituacaoacao
        
        # UPDATE
        $updateData = @{
            strdescricaosituacao = "Situação Atualizada $timestamp"
        }
        
        Test-Endpoint -Method "PATCH" -Url "${baseUrl}${sitId}/" -Token $Token `
            -Body $updateData `
            -Description "Atualizar Situação (requer change_situacaoacao)" `
            -ExpectSuccess $canChange | Out-Null
        
        # DELETE
        Test-Endpoint -Method "DELETE" -Url "${baseUrl}${sitId}/" -Token $Token `
            -Description "Deletar Situação (requer delete_situacaoacao)" `
            -ExpectSuccess $canDelete | Out-Null
    }
}

# ============================================================================
# FUNÇÃO: Testar CRUD de Vigências
# ============================================================================

function Test-VigenciaCRUD {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Token,
        
        [Parameter(Mandatory = $true)]
        [object]$Permissions
    )
    
    Write-Info "`n========================================="
    Write-Info "TESTANDO CRUD DE VIGÊNCIAS"
    Write-Info "========================================="
    
    $baseUrl = "$API_URL/vigencias/"
    
    $canView = $Permissions.specific.vigenciapngi.view
    $canAdd = $Permissions.specific.vigenciapngi.add
    $canChange = $Permissions.specific.vigenciapngi.change
    $canDelete = $Permissions.specific.vigenciapngi.delete
    
    # LIST
    Test-Endpoint -Method "GET" -Url $baseUrl -Token $Token `
        -Description "Listar Vigências (requer view_vigenciapngi)" `
        -ExpectSuccess $canView | Out-Null
    
    # VIGÊNCIA ATIVA
    Test-Endpoint -Method "GET" -Url "${baseUrl}vigencia_ativa/" -Token $Token `
        -Description "Buscar Vigência Ativa (requer view_vigenciapngi)" `
        -ExpectSuccess $canView | Out-Null
    
    # CREATE
    $year = (Get-Date).Year
    $newVigencia = @{
        strciclo = "Teste $year"
        dataini = "$year-01-01"
        datafim = "$year-12-31"
        isvigenciaativa = $false
    }
    
    $createResult = Test-Endpoint -Method "POST" -Url $baseUrl -Token $Token `
        -Body $newVigencia `
        -Description "Criar Vigência (requer add_vigenciapngi)" `
        -ExpectSuccess $canAdd
    
    if ($createResult.Success -and $createResult.Data.idvigenciapngi) {
        $vigId = $createResult.Data.idvigenciapngi
        
        # UPDATE
        $updateData = @{
            strciclo = "Teste $year ATUALIZADO"
        }
        
        Test-Endpoint -Method "PATCH" -Url "${baseUrl}${vigId}/" -Token $Token `
            -Body $updateData `
            -Description "Atualizar Vigência (requer change_vigenciapngi)" `
            -ExpectSuccess $canChange | Out-Null
        
        # ATIVAR (requer role Coordenador ou Gestor)
        $isCoordOrGestor = $Permissions.role -in @('GESTOR_PNGI', 'COORDENADOR_PNGI')
        Test-Endpoint -Method "POST" -Url "${baseUrl}${vigId}/ativar/" -Token $Token `
            -Description "Ativar Vigência (requer Coordenador+)" `
            -ExpectSuccess $isCoordOrGestor | Out-Null
        
        # DELETE
        Test-Endpoint -Method "DELETE" -Url "${baseUrl}${vigId}/" -Token $Token `
            -Description "Deletar Vigência (requer delete_vigenciapngi)" `
            -ExpectSuccess $canDelete | Out-Null
    }
}

# ============================================================================
# FUNÇÃO PRINCIPAL - Invoke-AllTests
# ============================================================================

function Invoke-AllTests {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Email,
        
        [Parameter(Mandatory = $true)]
        [SecureString]$Password
    )
    
    Write-Host "`n" -NoNewline
    Write-Host "=========================================" -ForegroundColor Magenta
    Write-Host "   TESTES DE PERMISSÕES - AÇÕES PNGI    " -ForegroundColor Magenta
    Write-Host "=========================================" -ForegroundColor Magenta
    
    # 1. Obter token
    $token = Get-AuthToken -Email $Email -Password $Password
    
    if (-not $token) {
        Write-ErrorMessage "Não foi possível obter token. Abortando testes."
        return
    }
    
    # 2. Buscar permissões do usuário
    $permissions = Test-UserPermissions -Token $token
    
    if (-not $permissions) {
        Write-ErrorMessage "Não foi possível obter permissões. Abortando testes."
        return
    }
    
    # 3. Testar CRUD de cada modelo
    Test-EixoCRUD -Token $token -Permissions $permissions
    Test-SituacaoCRUD -Token $token -Permissions $permissions
    Test-VigenciaCRUD -Token $token -Permissions $permissions
    
    # Resumo final
    Write-Host "`n" -NoNewline
    Write-Host "=========================================" -ForegroundColor Magenta
    Write-Host "         TESTES CONCLUÍDOS               " -ForegroundColor Magenta
    Write-Host "=========================================" -ForegroundColor Magenta
}

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

# Solicitar credenciais de forma segura
Write-Host "`nInforme as credenciais para teste:" -ForegroundColor Cyan
$email = Read-Host "Email do usuário"
$senhaSecure = Read-Host "Senha" -AsSecureString

# Executar testes
Invoke-AllTests -Email $email -Password $senhaSecure

# Limpar variáveis sensíveis
Remove-Variable -Name senhaSecure -ErrorAction SilentlyContinue
