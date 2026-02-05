<#
.SYNOPSIS
Debug Full Output - Captura saída COMPLETA dos testes
Útil para diagnosticar erros truncados

.DESCRIPTION
Este script executa os testes e SALVA a saída completa em arquivo
para análise detalhada.

.EXAMPLE
.\Test-Debug-Full-Output.ps1

#>

# Navegaçao
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath

Set-Location $projectRoot

# Ativar venv
$venvPath = Join-Path $projectRoot "venv"
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
& $activateScript

Write-Host "════════════════════════════════════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "[DEBUG] Capturando Saída Completa dos Testes" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════════════════════════════" -ForegroundColor Magenta

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = Join-Path $projectRoot "test_output_$timestamp.log"

Write-Host "`n[INFO] Saída será salva em: $logFile" -ForegroundColor Yellow
Write-Host "[INFO] Executando testes com -v 3 (máximo verbosity)...`n" -ForegroundColor Yellow

# Executar testes com captura
python manage.py test acoes_pngi.tests.test_context_processors -v 3 2>&1 | Tee-Object -FilePath $logFile

Write-Host "`n" -ForegroundColor Magenta
Write-Host "════════════════════════════════════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "[INFO] Arquivo de log criado:" -ForegroundColor Cyan
Write-Host "  📄 $logFile" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════════════════════════" -ForegroundColor Magenta

Write-Host "`n[INFO] Abrindo arquivo no editor...\n" -ForegroundColor Yellow
Start-Process "notepad.exe" -ArgumentList $logFile
