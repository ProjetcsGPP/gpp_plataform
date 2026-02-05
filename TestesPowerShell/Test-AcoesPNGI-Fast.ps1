<#
.SYNOPSIS
Teste Rápido e sem Pausas da Aplicação Ações PNGI
Executa apenas os testes unitários (SEM PAUSAS)

.DESCRIPTION
Este script realiza testes RÁPIDOS sem nenhuma pausa:
- Testes Unitários Django (context_processors)
- Sem renderização de views
- Sem testes web
- Sem testes API
- Execução em tempo real sem buffering

.EXAMPLE
.\Test-AcoesPNGI-Fast.ps1
.\Test-AcoesPNGI-Fast.ps1 -Verbose

#>

param(
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

$appName = 'acoes_pngi'
$appDisplayName = 'Ações PNGI'
echo Off

# ============================================================================
# EXECUTAR TESTES COM STREAMING DE SAÍDA EM TEMPO REAL
# ============================================================================

Write-Host "`n════════════════════════════════════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "[TEST] TESTES UNITÁRIOS - $appDisplayName ($appName)" -ForegroundColor Magenta
Write-Host "════════════════════════════════════════════════════════════════════════════════" -ForegroundColor Magenta

$appTestPath = "${appName}.tests.test_context_processors"
Write-Host "[INFO] Executando: python manage.py test $appTestPath -v 2" -ForegroundColor Cyan
Write-Host "[INFO] Localização: $(Get-Location)" -ForegroundColor Gray
Write-Host "`n"

# Executar com streaming de saída EM TEMPO REAL (sem buffering)
$process = Start-Process -FilePath python `
    -ArgumentList @(
        "manage.py",
        "test",
        $appTestPath,
        "-v", "2"
    ) `
    -NoNewWindow `
    -PassThru `
    -RedirectStandardOutput "$projectRoot\test_output_fast.txt" `
    -RedirectStandardError "$projectRoot\test_error_fast.txt"

# Aguardar processo completar
$process.WaitForExit()
$exitCode = $process.ExitCode

# Ler saída do arquivo
Write-Host (Get-Content -Path "$projectRoot\test_output_fast.txt" -Raw)

if (Test-Path "$projectRoot\test_error_fast.txt") {
    $errors = Get-Content -Path "$projectRoot\test_error_fast.txt" -Raw
    if ($errors.Length -gt 0) {
        Write-Host $errors -ForegroundColor Yellow
    }
}

# ============================================================================
# RESULTADO FINAL
# ============================================================================

Write-Host "`n"
Write-Host "════════════════════════════════════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "[RESULTADO FINAL]" -ForegroundColor Magenta
Write-Host "════════════════════════════════════════════════════════════════════════════════" -ForegroundColor Magenta

if ($exitCode -eq 0) {
    Write-Host "`n✅ SUCESSO! Todos os testes passaram!" -ForegroundColor Green
    Write-Host "Pronto para deploy!" -ForegroundColor Green
    Write-Host "`nArquivos de saída:" -ForegroundColor Gray
    Write-Host "  - $projectRoot\test_output_fast.txt" -ForegroundColor Gray
    Write-Host "  - $projectRoot\test_error_fast.txt" -ForegroundColor Gray
    exit 0
} else {
    Write-Host "`n❌ FALHA! Alguns testes falharam (Exit Code: $exitCode)" -ForegroundColor Red
    Write-Host "Verifique os logs acima para mais detalhes." -ForegroundColor Red
    Write-Host "`nArquivos de saída:" -ForegroundColor Gray
    Write-Host "  - $projectRoot\test_output_fast.txt" -ForegroundColor Gray
    Write-Host "  - $projectRoot\test_error_fast.txt" -ForegroundColor Gray
    exit 1
}
