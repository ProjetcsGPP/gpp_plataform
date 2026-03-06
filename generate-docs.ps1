<#
.SYNOPSIS
    Gera documentação completa da estrutura de apps
.DESCRIPTION
    Executa 'python manage.py generate_docs' e exibe o resultado
.EXAMPLE
    .\generate-docs.ps1
.EXAMPLE
    .\generate-docs.ps1 -Format markdown
#>

param(
    [ValidateSet('json', 'markdown', 'both')]
    [string]$Format = 'both',

    [string]$Output = 'docs/',

    [switch]$Open
)

Write-Host "`n📋 Gerando Documentação da Estrutura...`n" -ForegroundColor Cyan

try {
    # Executar comando Django
    $command = "python manage.py generate_docs --format $Format --output $Output"
    Write-Host "Executando: $command" -ForegroundColor Yellow
    Invoke-Expression $command

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Documentação gerada com sucesso!" -ForegroundColor Green

        # Exibir localização dos arquivos
        Write-Host "
📄 Arquivos criados:" -ForegroundColor Cyan
        if ($Format -in @('json', 'both')) {
            Write-Host "   • docs/app_structure.json" -ForegroundColor White
        }
        if ($Format -in @('markdown', 'both')) {
            Write-Host "   • docs/app_structure.md" -ForegroundColor White
        }

        # Abrir arquivo se solicitado
        if ($Open -and $Format -in @('markdown', 'both')) {
            Write-Host "
🔍 Abrindo documentação..." -ForegroundColor Cyan
            Start-Process "docs/app_structure.md"
        }

        Write-Host "
📚 Leia DOCUMENTATION_GUIDE.md para mais informações." -ForegroundColor Magenta
    } else {
        Write-Host "`n❌ Erro ao gerar documentação!" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "`n❌ Erro: $_" -ForegroundColor Red
    exit 1
}
