# ============================================================================
# Script de Teste de Performance - Cache de Permissões
# Versão: 1.0
# Objetivo: Validar e medir performance do cache de permissões (15min)
# ============================================================================

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$BaseUrl = "http://localhost:8000",
    
    [Parameter(Mandatory = $false)]
    [int]$Iterations = 5
)

$API_URL = "$BaseUrl/api/v1/acoes_pngi"
$AUTH_URL = "$BaseUrl/api/v1/auth"

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

function Write-Highlight {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Magenta
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
        
        $body = @{
            email = $Email
            password = $PlainPassword
        } | ConvertTo-Json
        
        try {
            $response = Invoke-RestMethod -Uri $loginUrl -Method Post `
                -Body $body -ContentType "application/json" -ErrorAction Stop
            
            Write-Success "✓ Token JWT obtido com sucesso"
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
# FUNÇÃO: Testar Performance do Cache
# ============================================================================

function Test-CachePerformance {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Token,
        
        [Parameter(Mandatory = $false)]
        [int]$Iterations = 5
    )
    
    Write-Highlight "`n========================================="
    Write-Highlight "  TESTE DE PERFORMANCE - CACHE 15MIN"
    Write-Highlight "========================================="
    
    $url = "$API_URL/permissions/"
    $headers = @{
        "Authorization" = "Bearer $Token"
        "Content-Type" = "application/json"
    }
    
    Write-Info "`n🔍 Endpoint: GET $url"
    Write-Info "📊 Iterações: $Iterations"
    Write-Info "⏱️  Cache configurado: 15 minutos (900 segundos)"
    
    # Array para armazenar tempos
    $times = @()
    
    # Loop de iterações
    for ($i = 1; $i -le $Iterations; $i++) {
        Write-Host "`n" -NoNewline
        if ($i -eq 1) {
            Write-Warning "$iª Chamada (SEM CACHE - primeira chamada)"
        }
        else {
            Write-Success "$iª Chamada (COM CACHE)"
        }
        
        # Medir tempo
        $start = Get-Date
        
        try {
            $response = Invoke-RestMethod -Uri $url -Headers $headers -ErrorAction Stop
            
            $end = Get-Date
            $duration = ($end - $start).TotalMilliseconds
            $times += $duration
            
            # Exibir resultado
            $icon = if ($i -eq 1) { "🔵" } else { "🟢" }
            Write-Host "  $icon Tempo: " -NoNewline -ForegroundColor White
            Write-Host "$([math]::Round($duration, 2)) ms" -ForegroundColor Yellow
            Write-Host "  👤 Usuário: $($response.email)" -ForegroundColor White
            Write-Host "  🔑 Permissões: $($response.permissions.Count) encontradas" -ForegroundColor White
            
            if ($i -eq 1) {
                Write-Host "  💾 Status: Dados buscados do BANCO DE DADOS" -ForegroundColor Yellow
            }
            else {
                Write-Host "  🗄️  Status: Dados servidos do CACHE (Redis/memória)" -ForegroundColor Green
            }
        }
        catch {
            Write-ErrorMessage "  ✗ Erro na chamada $i"
            Write-ErrorMessage "     $($_.Exception.Message)"
        }
        
        # Pausa entre chamadas
        if ($i -lt $Iterations) {
            Start-Sleep -Milliseconds 200
        }
    }
    
    # ========================================================================
    # ANÁLISE ESTATÍSTICA
    # ========================================================================
    
    Write-Highlight "`n========================================="
    Write-Highlight "       ANÁLISE DE PERFORMANCE"
    Write-Highlight "========================================="
    
    $firstCall = $times[0]
    $cachedCalls = $times[1..($times.Length - 1)]
    $avgCached = ($cachedCalls | Measure-Object -Average).Average
    $minCached = ($cachedCalls | Measure-Object -Minimum).Minimum
    $maxCached = ($cachedCalls | Measure-Object -Maximum).Maximum
    
    Write-Host "`n📊 ESTATÍSTICAS:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  1ª Chamada (SEM cache):" -ForegroundColor Yellow
    Write-Host "    ⏱️  Tempo: $([math]::Round($firstCall, 2)) ms" -ForegroundColor White
    Write-Host ""
    Write-Host "  Chamadas seguintes (COM cache):" -ForegroundColor Green
    Write-Host "    📊 Média: $([math]::Round($avgCached, 2)) ms" -ForegroundColor White
    Write-Host "    ⬇️  Mínimo: $([math]::Round($minCached, 2)) ms" -ForegroundColor White
    Write-Host "    ⬆️  Máximo: $([math]::Round($maxCached, 2)) ms" -ForegroundColor White
    
    # Calcular melhoria
    $improvement = (($firstCall - $avgCached) / $firstCall) * 100
    $speedup = $firstCall / $avgCached
    
    Write-Host "`n🚀 GANHO DE PERFORMANCE:" -ForegroundColor Magenta
    Write-Host "    📊 Redução de tempo: $([math]::Round($improvement, 2))%" -ForegroundColor Green
    Write-Host "    ⚡ Speedup: $([math]::Round($speedup, 2))x mais rápido" -ForegroundColor Green
    
    if ($improvement -gt 50) {
        Write-Success "`n  ✅ EXCELENTE! Cache está funcionando perfeitamente!"
    }
    elseif ($improvement -gt 20) {
        Write-Warning "`n  ⚠️  BOM. Cache melhorando performance moderadamente."
    }
    else {
        Write-ErrorMessage "`n  ❌ ATENÇÃO! Cache pode não estar funcionando corretamente."
    }
    
    # ========================================================================
    # COMPARAÇÃO VISUAL
    # ========================================================================
    
    Write-Host "`n📊 GRÁFICO DE TEMPOS (ms):" -ForegroundColor Cyan
    Write-Host ""
    
    $maxTime = $times | Measure-Object -Maximum | Select-Object -ExpandProperty Maximum
    $scale = 50 / $maxTime  # Escala para 50 caracteres
    
    for ($i = 0; $i -lt $times.Length; $i++) {
        $time = $times[$i]
        $barLength = [math]::Round($time * $scale)
        $bar = "█" * $barLength
        
        $label = if ($i -eq 0) { "Sem cache" } else { "Com cache" }
        $color = if ($i -eq 0) { "Yellow" } else { "Green" }
        
        Write-Host "  $($i + 1). " -NoNewline -ForegroundColor White
        Write-Host "$bar" -NoNewline -ForegroundColor $color
        Write-Host " $([math]::Round($time, 2)) ms ($label)" -ForegroundColor Gray
    }
    
    Write-Host ""
}

# ============================================================================
# FUNÇÃO: Testar Múltiplos Endpoints com Cache
# ============================================================================

function Test-MultipleEndpointsCache {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Token
    )
    
    Write-Highlight "`n========================================="
    Write-Highlight "  TESTE: MÚLTIPLOS ENDPOINTS COM CACHE"
    Write-Highlight "========================================="
    
    $endpoints = @(
        @{ Name = "Permissões"; Url = "$API_URL/permissions/" },
        @{ Name = "Eixos (light)"; Url = "$API_URL/eixos/list_light/" },
        @{ Name = "Vigência Ativa"; Url = "$API_URL/vigencias/vigencia_ativa/" }
    )
    
    $headers = @{
        "Authorization" = "Bearer $Token"
        "Content-Type" = "application/json"
    }
    
    foreach ($endpoint in $endpoints) {
        Write-Info "`n🔍 Testando: $($endpoint.Name)"
        Write-Host "   URL: $($endpoint.Url)" -ForegroundColor Gray
        
        # Primeira chamada
        $start1 = Get-Date
        try {
            $response1 = Invoke-RestMethod -Uri $endpoint.Url -Headers $headers -ErrorAction Stop
            $duration1 = ((Get-Date) - $start1).TotalMilliseconds
            Write-Host "   1ª: " -NoNewline -ForegroundColor Yellow
            Write-Host "$([math]::Round($duration1, 2)) ms" -ForegroundColor White
        }
        catch {
            if ($_.Exception.Response.StatusCode.value__ -eq 404) {
                Write-Warning "   ⚠️  404 - Recurso não encontrado (esperado para alguns endpoints)"
            }
            else {
                Write-ErrorMessage "   ✗ Erro: $($_.Exception.Message)"
            }
            continue
        }
        
        # Segunda chamada (com cache)
        Start-Sleep -Milliseconds 100
        $start2 = Get-Date
        try {
            $response2 = Invoke-RestMethod -Uri $endpoint.Url -Headers $headers -ErrorAction Stop
            $duration2 = ((Get-Date) - $start2).TotalMilliseconds
            Write-Host "   2ª: " -NoNewline -ForegroundColor Green
            Write-Host "$([math]::Round($duration2, 2)) ms" -ForegroundColor White
            
            $improvement = (($duration1 - $duration2) / $duration1) * 100
            if ($improvement -gt 0) {
                Write-Success "   ✓ Melhoria: $([math]::Round($improvement, 2))%"
            }
        }
        catch {
            Write-ErrorMessage "   ✗ Erro na 2ª chamada"
        }
    }
}

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

function Invoke-CacheTests {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Email,
        
        [Parameter(Mandatory = $true)]
        [SecureString]$Password,
        
        [Parameter(Mandatory = $false)]
        [int]$Iterations = 5
    )
    
    Write-Host "`n" -NoNewline
    Write-Highlight "=========================================="
    Write-Highlight "   TESTE DE CACHE DE PERMISSÕES - PNGI   "
    Write-Highlight "=========================================="
    
    # 1. Autenticação
    $token = Get-AuthToken -Email $Email -Password $Password
    
    if (-not $token) {
        Write-ErrorMessage "`n❌ Não foi possível obter token. Abortando testes."
        return
    }
    
    # 2. Teste de performance do cache
    Test-CachePerformance -Token $token -Iterations $Iterations
    
    # 3. Teste de múltiplos endpoints
    Test-MultipleEndpointsCache -Token $token
    
    # Resumo final
    Write-Host "`n" -NoNewline
    Write-Highlight "=========================================="
    Write-Highlight "            TESTES CONCLUÍDOS            "
    Write-Highlight "=========================================="
    
    Write-Info "`n📝 OBSERVAÇÕES:"
    Write-Host "  • Cache de permissões: 15 minutos (900s)" -ForegroundColor White
    Write-Host "  • Primeira chamada sempre mais lenta (busca BD)" -ForegroundColor White
    Write-Host "  • Chamadas seguintes usam cache (mais rápidas)" -ForegroundColor White
    Write-Host "  • Cache é limpo quando roles são alterados" -ForegroundColor White
    Write-Host ""
}

# ============================================================================
# EXECUÇÃO
# ============================================================================

Write-Host "`nScript de Teste de Cache - Ações PNGI" -ForegroundColor Cyan
Write-Host "Servidor: $BaseUrl" -ForegroundColor Gray
Write-Host "Iterações: $Iterations" -ForegroundColor Gray

$email = Read-Host "`nEmail do usuário"
$senhaSecure = Read-Host "Senha" -AsSecureString

Invoke-CacheTests -Email $email -Password $senhaSecure -Iterations $Iterations

# Limpar variáveis sensíveis
Remove-Variable -Name senhaSecure -ErrorAction SilentlyContinue
