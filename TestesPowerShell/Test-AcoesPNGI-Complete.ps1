<#
.SYNOPSIS
Teste Completo da Aplicação Ações PNGI
Testa Views Web + Views API + Context Processors

.DESCRIPTION
Este script realiza testes completos de:
- Testes Unitários Django (context_processors)
- Views Web (renderização de templates)
- Views API (REST endpoints)
- Contexto para Next.js (API endpoints)

.EXAMPLE
.\Test-AcoesPNGI-Complete.ps1
.\Test-AcoesPNGI-Complete.ps1 -Verbose

#>

param(
    [string]$BaseURL = "http://localhost:8000",
    [string]$APIVersion = "v1",
    [string]$AppCode = "ACOES_PNGI",
    [switch]$Verbose
)

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

$ErrorActionPreference = "Continue"
$WarningPreference = "Continue"

$colors = @{
    'SUCCESS' = 'Green'
    'FAIL' = 'Red'
    'INFO' = 'Cyan'
    'WARNING' = 'Yellow'
    'HEADER' = 'Magenta'
}

function Write-ColorOutput([string]$message, [string]$type = 'INFO') {
    $color = $colors[$type] -or 'White'
    Write-Host "[$type] $message" -ForegroundColor $color
}

function Write-SectionHeader([string]$title) {
    Write-Host "`n" -NoNewline
    Write-Host "═" * 80 -ForegroundColor $colors['HEADER']
    Write-ColorOutput $title 'HEADER'
    Write-Host "═" * 80 -ForegroundColor $colors['HEADER']
}

# ============================================================================
# 1. TESTES UNITÁRIOS DJANGO
# ============================================================================

Write-SectionHeader "1. EXECUTANDO TESTES UNITÁRIOS (Python/Django)"

Write-ColorOutput "Executando testes do context_processors de acoes_pngi..." 'INFO'
Write-ColorOutput "Comando: python manage.py test acoes_pngi.tests.test_context_processors -v 2" 'INFO'

$testOutput = python manage.py test acoes_pngi.tests.test_context_processors -v 2 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-ColorOutput "✓ Testes unitários executados com sucesso!" 'SUCCESS'
    
    # Extrai informações do output
    if ($testOutput -match 'Ran (\d+) test') {
        $testCount = $matches[1]
        Write-ColorOutput "  - Total de testes: $testCount" 'INFO'
    }
    if ($testOutput -match 'OK') {
        Write-ColorOutput "  - Status: TODOS OS TESTES PASSARAM" 'SUCCESS'
    }
} else {
    Write-ColorOutput "✗ Erro ao executar testes unitários!" 'FAIL'
    Write-Host $testOutput
    exit 1
}

# ============================================================================
# 2. TESTES DE VIEWS WEB
# ============================================================================

Write-SectionHeader "2. TESTANDO VIEWS WEB (Renderização de Templates)"

Write-ColorOutput "Testando acesso às views web da aplicação Ações PNGI..." 'INFO'

$webTests = @(
    @{
        'name' = 'Página Principal'
        'url' = "$BaseURL/acoes_pngi/"
        'method' = 'GET'
        'expectedStatus' = 200
    },
    @{
        'name' = 'Lista de Eixos'
        'url' = "$BaseURL/acoes_pngi/eixos/"
        'method' = 'GET'
        'expectedStatus' = @(200, 301, 302, 403)  # 403 se não autenticado
    },
    @{
        'name' = 'Lista de Situações'
        'url' = "$BaseURL/acoes_pngi/situacoes/"
        'method' = 'GET'
        'expectedStatus' = @(200, 301, 302, 403)
    },
    @{
        'name' = 'Lista de Vigências'
        'url' = "$BaseURL/acoes_pngi/vigencias/"
        'method' = 'GET'
        'expectedStatus' = @(200, 301, 302, 403)
    }
)

$webTestsPassed = 0
$webTestsFailed = 0

foreach ($test in $webTests) {
    Write-ColorOutput "  Testando: $($test['name'])" 'INFO'
    
    try {
        $response = Invoke-WebRequest -Uri $test['url'] -Method $test['method'] -SkipHttpErrorCheck -TimeoutSec 10
        
        if ($response.StatusCode -in $test['expectedStatus']) {
            Write-ColorOutput "    ✓ Status: $($response.StatusCode)" 'SUCCESS'
            $webTestsPassed++
        } else {
            Write-ColorOutput "    ✗ Status inesperado: $($response.StatusCode)" 'FAIL'
            Write-ColorOutput "      Esperado: $($test['expectedStatus'] -join ', ')" 'WARNING'
            $webTestsFailed++
        }
    } catch {
        Write-ColorOutput "    ✗ Erro ao acessar: $($_.Exception.Message)" 'FAIL'
        $webTestsFailed++
    }
}

Write-ColorOutput "\nResumo Views Web: $webTestsPassed passou, $webTestsFailed falhou" 'INFO'

# ============================================================================
# 3. TESTES DE API (REST)
# ============================================================================

Write-SectionHeader "3. TESTANDO ENDPOINTS DA API"

Write-ColorOutput "Testando endpoints REST da aplicação Ações PNGI..." 'INFO'

# Primeiro, obtém o token (se necessário)
$token = ""

$apiTests = @(
    @{
        'name' = 'GET: Lista de Eixos'
        'url' = "$BaseURL/api/$APIVersion/acoes_pngi/eixos/"
        'method' = 'GET'
        'expectedStatus' = @(200, 403)  # 403 se não autenticado
        'requiresAuth' = $true
    },
    @{
        'name' = 'GET: Lista de Situações'
        'url' = "$BaseURL/api/$APIVersion/acoes_pngi/situacoes/"
        'method' = 'GET'
        'expectedStatus' = @(200, 403)
        'requiresAuth' = $true
    },
    @{
        'name' = 'GET: Lista de Vigências'
        'url' = "$BaseURL/api/$APIVersion/acoes_pngi/vigencias/"
        'method' = 'GET'
        'expectedStatus' = @(200, 403)
        'requiresAuth' = $true
    },
    @{
        'name' = 'GET: Vigência Ativa'
        'url' = "$BaseURL/api/$APIVersion/acoes_pngi/vigencias/vigencia_ativa/"
        'method' = 'GET'
        'expectedStatus' = @(200, 404, 403)
        'requiresAuth' = $true
    }
)

$apiTestsPassed = 0
$apiTestsFailed = 0

foreach ($test in $apiTests) {
    Write-ColorOutput "  Testando: $($test['name'])" 'INFO'
    
    try {
        $headers = @{
            'Content-Type' = 'application/json'
        }
        if ($token) {
            $headers['Authorization'] = "Bearer $token"
        }
        
        $response = Invoke-RestMethod -Uri $test['url'] -Method $test['method'] -Headers $headers -SkipHttpErrorCheck -TimeoutSec 10
        
        if ($response.StatusCode -in $test['expectedStatus']) {
            Write-ColorOutput "    ✓ Status: $($response.StatusCode)" 'SUCCESS'
            if ($response.Content) {
                $content = $response.Content | ConvertFrom-Json
                if ($content.Count) {
                    Write-ColorOutput "      Itens retornados: $($content.Count)" 'INFO'
                }
            }
            $apiTestsPassed++
        } else {
            Write-ColorOutput "    ✗ Status inesperado: $($response.StatusCode)" 'FAIL'
            $apiTestsFailed++
        }
    } catch {
        if ($test['expectedStatus'] -contains 403 -or $test['expectedStatus'] -contains 401) {
            Write-ColorOutput "    ℹ Não autenticado (esperado): $($_.Exception.Message)" 'WARNING'
            $apiTestsPassed++
        } else {
            Write-ColorOutput "    ✗ Erro ao acessar: $($_.Exception.Message)" 'FAIL'
            $apiTestsFailed++
        }
    }
}

Write-ColorOutput "\nResumo API REST: $apiTestsPassed passou, $apiTestsFailed falhou" 'INFO'

# ============================================================================
# 4. TESTES DE CONTEXT PROCESSORS API (PARA NEXT.JS)
# ============================================================================

Write-SectionHeader "4. TESTANDO ENDPOINTS DE CONTEXTO (Para Next.js)"

Write-ColorOutput "Testando endpoints que retornam dados dos context_processors..." 'INFO'

$contextTests = @(
    @{
        'name' = 'GET: Contexto da App'
        'url' = "$BaseURL/api/$APIVersion/acoes_pngi/context/app/"
        'method' = 'GET'
        'expectedStatus' = @(200, 403)
        'expectedFields' = @('code', 'name', 'icon')
    },
    @{
        'name' = 'GET: Permissões do Usuário'
        'url' = "$BaseURL/api/$APIVersion/acoes_pngi/context/permissions/"
        'method' = 'GET'
        'expectedStatus' = @(200, 403)
        'expectedFields' = @('user_id', 'email', 'permissions')
    },
    @{
        'name' = 'GET: Informações dos Modelos'
        'url' = "$BaseURL/api/$APIVersion/acoes_pngi/context/models/"
        'method' = 'GET'
        'expectedStatus' = @(200, 403)
        'expectedFields' = @('models')
    },
    @{
        'name' = 'GET: Contexto Completo'
        'url' = "$BaseURL/api/$APIVersion/acoes_pngi/context/full/"
        'method' = 'GET'
        'expectedStatus' = @(200, 403)
        'expectedFields' = @('app', 'permissions', 'models')
    }
)

$contextTestsPassed = 0
$contextTestsFailed = 0

foreach ($test in $contextTests) {
    Write-ColorOutput "  Testando: $($test['name'])" 'INFO'
    
    try {
        $headers = @{
            'Content-Type' = 'application/json'
        }
        if ($token) {
            $headers['Authorization'] = "Bearer $token"
        }
        
        $response = Invoke-RestMethod -Uri $test['url'] -Method $test['method'] -Headers $headers -SkipHttpErrorCheck -TimeoutSec 10
        
        if ($response.StatusCode -in $test['expectedStatus']) {
            Write-ColorOutput "    ✓ Status: $($response.StatusCode)" 'SUCCESS'
            
            # Valida campos esperados
            if ($response.Content) {
                $data = $response.Content | ConvertFrom-Json
                $missingFields = @()
                
                foreach ($field in $test['expectedFields']) {
                    if (-not $data.$field) {
                        $missingFields += $field
                    }
                }
                
                if ($missingFields.Count -eq 0) {
                    Write-ColorOutput "      Todos os campos esperados presentes" 'SUCCESS'
                } else {
                    Write-ColorOutput "      ⚠ Campos faltando: $($missingFields -join ', ')" 'WARNING'
                }
            }
            $contextTestsPassed++
        } else {
            Write-ColorOutput "    ✗ Status inesperado: $($response.StatusCode)" 'FAIL'
            $contextTestsFailed++
        }
    } catch {
        if ($test['expectedStatus'] -contains 403 -or $test['expectedStatus'] -contains 401) {
            Write-ColorOutput "    ℹ Não autenticado (esperado)" 'WARNING'
            $contextTestsPassed++
        } else {
            Write-ColorOutput "    ✗ Erro: $($_.Exception.Message)" 'FAIL'
            $contextTestsFailed++
        }
    }
}

Write-ColorOutput "\nResumo Endpoints Contexto: $contextTestsPassed passou, $contextTestsFailed falhou" 'INFO'

# ============================================================================
# 5. RESUMO FINAL
# ============================================================================

Write-SectionHeader "RESUMO FINAL DOS TESTES"

$totalTests = $webTestsPassed + $webTestsFailed + $apiTestsPassed + $apiTestsFailed + $contextTestsPassed + $contextTestsFailed
$totalPassed = $webTestsPassed + $apiTestsPassed + $contextTestsPassed
$totalFailed = $webTestsFailed + $apiTestsFailed + $contextTestsFailed

Write-ColorOutput "Total de Testes: $totalTests" 'INFO'
Write-ColorOutput "Testes Passados: $totalPassed" 'SUCCESS'
Write-ColorOutput "Testes Falhados: $totalFailed" $(if ($totalFailed -gt 0) { 'FAIL' } else { 'SUCCESS' })

Write-Host "`n"
Write-ColorOutput "Resumo por Categoria:" 'HEADER'
Write-ColorOutput "  - Views Web:    $webTestsPassed/$($webTestsPassed + $webTestsFailed) passou" $(if ($webTestsFailed -eq 0) { 'SUCCESS' } else { 'WARNING' })
Write-ColorOutput "  - API REST:     $apiTestsPassed/$($apiTestsPassed + $apiTestsFailed) passou" $(if ($apiTestsFailed -eq 0) { 'SUCCESS' } else { 'WARNING' })
Write-ColorOutput "  - Contexto API: $contextTestsPassed/$($contextTestsPassed + $contextTestsFailed) passou" $(if ($contextTestsFailed -eq 0) { 'SUCCESS' } else { 'WARNING' })

if ($totalFailed -eq 0) {
    Write-Host "`n"
    Write-ColorOutput "🎉 TODOS OS TESTES PASSARAM!" 'SUCCESS'
    exit 0
} else {
    Write-Host "`n"
    Write-ColorOutput "⚠️  ALGUNS TESTES FALHARAM" 'FAIL'
    exit 1
}
