<#
.SYNOPSIS
Teste Completo de TODAS as Aplicações do GPP Platform
Testa Views Web + Views API + Context Processors para cada app

.DESCRIPTION
Este script realiza testes completos de:
- Testes Unitários Django (context_processors de cada app)
- Views Web (renderização de templates)
- Views API (REST endpoints)
- Contexto para Next.js (API endpoints de contexto)

Aplicações Testadas:
1. carga_org_lot
2. acoes_pngi
3. Outras apps conforme disponível

.EXAMPLE
.\Test-AllApps-Complete.ps1
.\Test-AllApps-Complete.ps1 -Apps @('acoes_pngi', 'carga_org_lot')
.\Test-AllApps-Complete.ps1 -Verbose

#>

param(
    [string]$BaseURL = "http://localhost:8000",
    [string]$APIVersion = "v1",
    [string[]]$Apps = @('carga_org_lot', 'acoes_pngi'),
    [switch]$Verbose
)

# ============================================================================
# NAVEGAR PARA RAIZ DO PROJETO
# ============================================================================

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath

Write-Host "Mudando para diretório do projeto..." -ForegroundColor Cyan
Write-Host "Caminho do script: $scriptPath" -ForegroundColor Gray
Write-Host "Raíz do projeto: $projectRoot" -ForegroundColor Gray

Set-Location $projectRoot

if (-not (Test-Path "manage.py")) {
    Write-Host "✗ ERRO: manage.py não encontrado em $projectRoot" -ForegroundColor Red
    Write-Host "Por favor, execute o script da pasta raiz do projeto!" -ForegroundColor Red
    exit 1
}

Write-Host "✓ manage.py encontrado!" -ForegroundColor Green

# ============================================================================
# ATIVAR VIRTUALENV
# ============================================================================

$venvPath = Join-Path $projectRoot "venv"
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

if (-not (Test-Path $activateScript)) {
    Write-Host "✗ ERRO: Virtualenv não encontrado em $venvPath" -ForegroundColor Red
    Write-Host "Por favor, crie o virtualenv primeiro!" -ForegroundColor Red
    exit 1
}

Write-Host "Ativando virtualenv..." -ForegroundColor Cyan
& $activateScript

# Verificar que virtualenv foi ativado
if (-not $env:VIRTUAL_ENV) {
    Write-Host "✗ ERRO: Falha ao ativar virtualenv" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Virtualenv ativado!" -ForegroundColor Green
Write-Host "  Versão Python: $(python --version)" -ForegroundColor Gray

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

$ErrorActionPreference = "Continue"
$WarningPreference = "Continue"

# Define cores disponíveis no PowerShell
$colors = @{
    'SUCCESS' = 'Green'
    'FAIL' = 'Red'
    'INFO' = 'Cyan'
    'WARNING' = 'Yellow'
    'HEADER' = 'Magenta'
}

$appConfig = @{
    'carga_org_lot' = @{
        'name' = 'Carga e Organização de Lotes'
        'code' = 'CARGA_ORG_LOT'
        'paths' = @(
            '/carga_org_lot/'
            '/carga_org_lot/lotamentos/'
            '/carga_org_lot/otmizacoes/'
        )
        'apiEndpoints' = @(
            '/api/v1/carga_org_lot/lotamentos/'
            '/api/v1/carga_org_lot/otmizacoes/'
            '/api/v1/carga_org_lot/context/full/'
        )
    }
    'acoes_pngi' = @{
        'name' = 'Ações PNGI'
        'code' = 'ACOES_PNGI'
        'paths' = @(
            '/acoes_pngi/'
            '/acoes_pngi/eixos/'
            '/acoes_pngi/situacoes/'
            '/acoes_pngi/vigencias/'
        )
        'apiEndpoints' = @(
            '/api/v1/acoes_pngi/eixos/'
            '/api/v1/acoes_pngi/situacoes/'
            '/api/v1/acoes_pngi/vigencias/'
            '/api/v1/acoes_pngi/context/full/'
        )
    }
}

function Write-ColorOutput([string]$message, [string]$type = 'INFO') {
    $color = $colors[$type]
    if ($null -eq $color) {
        $color = 'White'
    }
    Write-Host "[$type] $message" -ForegroundColor $color
}

function Write-SectionHeader([string]$title) {
    Write-Host "`n" -NoNewline
    Write-Host ("═" * 80) -ForegroundColor $colors['HEADER']
    Write-ColorOutput $title 'HEADER'
    Write-Host ("═" * 80) -ForegroundColor $colors['HEADER']
}

function Write-AppHeader([string]$appName, [string]$appDisplayName) {
    Write-Host "`n" -NoNewline
    Write-Host ("=" * 80) -ForegroundColor 'Cyan'
    Write-ColorOutput "📋 APP: $appDisplayName ($appName)" 'INFO'
    Write-Host ("=" * 80) -ForegroundColor 'Cyan'
}

# ============================================================================
# TESTES PARA UMA APLICAÇÃO
# ============================================================================

function Test-AppUnit([string]$appName) {
    Write-ColorOutput "[Unit Tests] Executando testes Django para $appName..." 'INFO'
    
    $appTestPath = "${appName}.tests.test_context_processors"
    Write-ColorOutput "Comando: python manage.py test $appTestPath -v 2" 'INFO'
    Write-ColorOutput "Diretório: $(Get-Location)" 'INFO'
    
    try {
        $testOutput = python manage.py test $appTestPath -v 2 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✓ Testes unitários executados com sucesso!" 'SUCCESS'
            return @{
                'passed' = $true
                'message' = 'Testes unitários passaram'
                'details' = $testOutput
            }
        } else {
            Write-ColorOutput "✗ Erro ao executar testes!" 'FAIL'
            if ($Verbose) {
                Write-Host $testOutput
            } else {
                Write-Host "Erro: $($testOutput | Select-Object -First 5)" -ForegroundColor Red
            }
            return @{
                'passed' = $false
                'message' = 'Testes unitários falharam'
                'details' = $testOutput
            }
        }
    }
    catch {
        Write-ColorOutput "✗ Erro: $($_.Exception.Message)" 'FAIL'
        return @{
            'passed' = $false
            'message' = 'Erro ao executar testes'
            'details' = $_.Exception.Message
        }
    }
}

function Test-WebViews([string]$appName, [string[]]$paths) {
    Write-ColorOutput "[Web Views] Testando renderização de templates..." 'INFO'
    
    $passed = 0
    $failed = 0
    
    foreach ($path in $paths) {
        $url = "$BaseURL$path"
        Write-ColorOutput "  Acessando: $path" 'INFO'
        
        try {
            $response = Invoke-WebRequest -Uri $url -Method GET -SkipHttpErrorCheck -TimeoutSec 10
            
            if ($response.StatusCode -in @(200, 301, 302, 403)) {
                Write-ColorOutput "    ✓ Status: $($response.StatusCode)" 'SUCCESS'
                $passed++
            } else {
                Write-ColorOutput "    ✗ Status inesperado: $($response.StatusCode)" 'FAIL'
                $failed++
            }
        } catch {
            Write-ColorOutput "    ✗ Erro: $($_.Exception.Message)" 'FAIL'
            $failed++
        }
    }
    
    return @{
        'passed' = $passed
        'failed' = $failed
    }
}

function Test-APIEndpoints([string]$appName, [string[]]$endpoints) {
    Write-ColorOutput "[API REST] Testando endpoints da API..." 'INFO'
    
    $passed = 0
    $failed = 0
    
    foreach ($endpoint in $endpoints) {
        $url = "$BaseURL$endpoint"
        Write-ColorOutput "  Acessando: $endpoint" 'INFO'
        
        try {
            $headers = @{
                'Content-Type' = 'application/json'
            }
            
            $response = Invoke-WebRequest -Uri $url -Method GET -Headers $headers -SkipHttpErrorCheck -TimeoutSec 10
            
            if ($response.StatusCode -in @(200, 403, 401)) {
                Write-ColorOutput "    ✓ Status: $($response.StatusCode)" 'SUCCESS'
                $passed++
            } else {
                Write-ColorOutput "    ✗ Status inesperado: $($response.StatusCode)" 'FAIL'
                $failed++
            }
        } catch {
            if ($_ -match '(403|401|Unauthorized)') {
                Write-ColorOutput "    ℹ Não autenticado (esperado)" 'WARNING'
                $passed++
            } else {
                Write-ColorOutput "    ✗ Erro: $($_.Exception.Message)" 'FAIL'
                $failed++
            }
        }
    }
    
    return @{
        'passed' = $passed
        'failed' = $failed
    }
}

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

Write-SectionHeader "TESTE COMPLETO DO GPP PLATFORM"
Write-ColorOutput "URL Base: $BaseURL" 'INFO'
Write-ColorOutput "Versão da API: $APIVersion" 'INFO'
Write-ColorOutput "Aplicações a Testar: $($Apps -join ', ')" 'INFO'
Write-ColorOutput "Diretório: $(Get-Location)" 'INFO'

$globalResults = @{}
$totalTestsPassed = 0
$totalTestsFailed = 0

foreach ($app in $Apps) {
    if (-not $appConfig.ContainsKey($app)) {
        Write-ColorOutput "⚠️  App '$app' não encontrada nas configurações" 'WARNING'
        continue
    }
    
    $config = $appConfig[$app]
    Write-AppHeader $app $config['name']
    
    # 1. Testes Unitários
    Write-SectionHeader "1. TESTES UNITÁRIOS"
    $unitResult = Test-AppUnit $app
    
    # 2. Views Web
    Write-SectionHeader "2. VIEWS WEB"
    $webResult = Test-WebViews $app $config['paths']
    
    # 3. API Endpoints
    Write-SectionHeader "3. ENDPOINTS DA API"
    $apiResult = Test-APIEndpoints $app $config['apiEndpoints']
    
    # Armazena resultado
    $globalResults[$app] = @{
        'unit' = $unitResult
        'web' = $webResult
        'api' = $apiResult
    }
    
    $totalTestsPassed += $unitResult.passed + $webResult.passed + $apiResult.passed
    $totalTestsFailed += $webResult.failed + $apiResult.failed
}

# ============================================================================
# RESUMO FINAL
# ============================================================================

Write-SectionHeader "RESUMO FINAL - TODAS AS APLICAÇÕES"

Write-ColorOutput "Resultados por Aplicação:" 'HEADER'

foreach ($app in $Apps) {
    if (-not $globalResults.ContainsKey($app)) {
        continue
    }
    
    $result = $globalResults[$app]
    $appName = $appConfig[$app]['name']
    
    Write-Host "`n$appName ($app):"
    Write-ColorOutput "  ✓ Unit Tests: $(if ($result['unit'].passed) {'PASSOU'} else {'FALHOU'})" $(if ($result['unit'].passed) { 'SUCCESS' } else { 'FAIL' })
    Write-ColorOutput "  ✓ Web Views:  $($result['web'].passed) passou, $($result['web'].failed) falhou" $(if ($result['web'].failed -eq 0) { 'SUCCESS' } else { 'WARNING' })
    Write-ColorOutput "  ✓ API REST:   $($result['api'].passed) passou, $($result['api'].failed) falhou" $(if ($result['api'].failed -eq 0) { 'SUCCESS' } else { 'WARNING' })
}

Write-Host "`n"
Write-ColorOutput "Total de Testes Passados: $totalTestsPassed" 'SUCCESS'
Write-ColorOutput "Total de Testes Falhados: $totalTestsFailed" $(if ($totalTestsFailed -gt 0) { 'FAIL' } else { 'SUCCESS' })

if ($totalTestsFailed -eq 0) {
    Write-Host "`n"
    Write-ColorOutput "🎉 TODOS OS TESTES PASSARAM!" 'SUCCESS'
    Write-ColorOutput "Pronto para deploy!" 'SUCCESS'
    exit 0
} else {
    Write-Host "`n"
    Write-ColorOutput "⚠️  ALGUNS TESTES FALHARAM - REVISAR LOGS ACIMA" 'FAIL'
    exit 1
}
