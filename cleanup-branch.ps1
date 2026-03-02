<#
.SYNOPSIS
    Script de limpeza automatizada da branch refactor/iam-service-architecture

.DESCRIPTION
    Remove arquivos obsoletos, valida __init__.py e prepara para atualização de documentação.
    Relacionado à Issue #10

.NOTES
    Author: GPP Team
    Date: 2026-02-25
#>

# Cores para output
$ErrorActionPreference = "Continue"

function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-ColorOutput Green "="*80
Write-ColorOutput Green "LIMPEZA DA BRANCH refactor/iam-service-architecture"
Write-ColorOutput Green "="*80
Write-Output ""

# Confirmação
$confirmacao = Read-Host "Deseja continuar com a limpeza? (S/N)"
if ($confirmacao -ne "S" -and $confirmacao -ne "s") {
    Write-ColorOutput Yellow "Operação cancelada pelo usuário."
    exit
}

Write-Output ""
Write-ColorOutput Cyan "[1/4] Removendo arquivos de correção temporários..."

$fixFiles = @(
    "fix_alinhamento_response_data.py",
    "fix_master_todos_testes.py",
    "fix_pylance_errors.py",
    "fix_response_data_acesso.py",
    "fix_response_data_v3.py",
    "fix_situacao_DEFINITIVO_v2.py",
    "fix_situacao_FOCADO.py",
    "fix_test_api_final_v2.py",
    "fix_test_api_views_acoes.py",
    "fix_test_api_views_acoes_v2.py",
    "fix_test_api_views_final.py",
    "fix_testes_massivo.py",
    "fix_testes_massivo_v2.py",
    "fix_testes_massivo_v3.py",
    "fix_testes_massivo_v4.py",
    "fix_testes_massivo_v5_FINAL.py",
    "fix_testes_massivo_v6_DEFINITIVO.py",
    "fix_web_views_complete_fixed.py"
)

$removidos = 0
foreach ($file in $fixFiles) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-ColorOutput Green "  ✓ Removido: $file"
        $removidos++
    }
}
Write-Output "  Total de arquivos fix_*.py removidos: $removidos"

Write-Output ""
Write-ColorOutput Cyan "[2/4] Removendo arquivos de log e diagnóstico..."

$logFiles = @(
    ".coverage",
    "diagnostic_19_02_2026.txt",
    "último_Log_execucao_testes_20260212.txt",
    "test_results_api_views_acoes.txt",
    "urls-debug.txt"
)

$removidos = 0
foreach ($file in $logFiles) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-ColorOutput Green "  ✓ Removido: $file"
        $removidos++
    }
}
Write-Output "  Total de arquivos de log removidos: $removidos"

Write-Output ""
Write-ColorOutput Cyan "[3/4] Removendo arquivos temporários e notas..."

$tempFiles = @(
    "chatgpt.txt",
    "models_gerados.py",
    "patches_codigo.txt",
    "guia_correcao_completa.txt",
    "resumo_executivo.txt",
    "CORRECAO_MASSIVA_TESTES.md"
)

$removidos = 0
foreach ($file in $tempFiles) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-ColorOutput Green "  ✓ Removido: $file"
        $removidos++
    }
}
Write-Output "  Total de arquivos temporários removidos: $removidos"

Write-Output ""
Write-ColorOutput Cyan "[4/4] Validando arquivos __init__.py..."

$initFiles = @(
    "accounts/__init__.py",
    "accounts/services/__init__.py",
    "accounts/templatetags/__init__.py",
    "accounts/tests/__init__.py",
    "accounts/urls/__init__.py",
    "accounts/views/__init__.py",
    "core/__init__.py",
    "core/iam/__init__.py",
    "acoes_pngi/__init__.py",
    "acoes_pngi/services/__init__.py",
    "acoes_pngi/templatetags/__init__.py",
    "acoes_pngi/tests/__init__.py",
    "acoes_pngi/urls/__init__.py",
    "acoes_pngi/views/__init__.py",
    "acoes_pngi/utils/__init__.py"
)

Write-Output "  Verificando existência dos arquivos __init__.py..."
$missing = @()
foreach ($file in $initFiles) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        if ($size -eq 0) {
            Write-ColorOutput Yellow "  ⚠ Vazio: $file (pode precisar de exports)"
        } else {
            Write-ColorOutput Green "  ✓ OK: $file ($size bytes)"
        }
    } else {
        Write-ColorOutput Red "  ✗ Faltando: $file"
        $missing += $file
    }
}

if ($missing.Count -gt 0) {
    Write-Output ""
    Write-ColorOutput Yellow "  Criando arquivos __init__.py faltantes..."
    foreach ($file in $missing) {
        $dir = Split-Path $file -Parent
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
        New-Item -ItemType File -Path $file -Force | Out-Null
        Write-ColorOutput Green "  ✓ Criado: $file"
    }
}

Write-Output ""
Write-ColorOutput Green "="*80
Write-ColorOutput Green "LIMPEZA CONCLUÍDA!"
Write-ColorOutput Green "="*80
Write-Output ""
Write-ColorOutput Cyan "Próximos passos:"
Write-Output "  1. Revise os arquivos __init__.py vazios e adicione exports se necessário"
Write-Output "  2. Atualize a documentação conforme Issue #10"
Write-Output "  3. Execute os testes: pytest"
Write-Output "  4. Commit as mudanças: git add -A && git commit -m 'feat: Limpeza da branch refactor/iam-service-architecture'"
Write-Output ""
Write-ColorOutput Yellow "IMPORTANTE: Revise as mudanças antes de fazer commit!"
Write-Output "  git status"
Write-Output ""
