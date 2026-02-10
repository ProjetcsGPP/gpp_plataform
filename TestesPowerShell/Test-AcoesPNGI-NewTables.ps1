<#
.SYNOPSIS
Teste Focado nas Novas Tabelas - Ações PNGI
Testa Ações, Prazos, Destaques, Alinhamento e Responsáveis

.DESCRIPTION
Script de teste específico para as novas entidades:
- Ações (com filtros e custom actions)
- Prazos (com filtro de ativos)
- Destaques
- Tipos de Anotação de Alinhamento
- Anotações de Alinhamento
- Usuários Responsáveis
- Relações Ação-Responsável

.PARAMETER BaseURL
URL base do servidor

.PARAMETER Token
Token JWT para autenticação (opcional, testa sem token se não fornecido)

.EXAMPLE
.\Test-AcoesPNGI-NewTables.ps1
.\Test-AcoesPNGI-NewTables.ps1 -Token "seu-token-jwt"

#>

param(
    [string]$BaseURL = "http://localhost:8000",
    [string]$Token = ""
)

$API_BASE = "$BaseURL/api/v1/acoes_pngi"

function Write-TestHeader([string]$title) {
    Write-Host "`n" -NoNewline
    Write-Host ("═" * 70) -ForegroundColor Cyan
    Write-Host $title -ForegroundColor Cyan
    Write-Host ("═" * 70) -ForegroundColor Cyan
}

function Test-Endpoint {
    param(
        [string]$Url,
        [string]$Name,
        [string]$Method = "GET",
        [hashtable]$Body = $null
    )
    
    Write-Host "`n  Testando: $Name" -ForegroundColor Yellow
    Write-Host "  URL: $Url" -ForegroundColor Gray
    
    try {
        $headers = @{
            'Content-Type' = 'application/json'
        }
        
        if ($Token) {
            $headers['Authorization'] = "Bearer $Token"
        }
        
        $params = @{
            Uri = $Url
            Method = $Method
            Headers = $headers
            SkipHttpErrorCheck = $true
            TimeoutSec = 10
        }
        
        if ($Body) {
            $params['Body'] = ($Body | ConvertTo-Json)
        }
        
        $response = Invoke-WebRequest @params
        
        $statusColor = switch ($response.StatusCode) {
            { $_ -in 200..299 } { 'Green' }
            { $_ -in 400..499 } { 'Yellow' }
            default { 'Red' }
        }
        
        Write-Host "    ✓ Status: $($response.StatusCode)" -ForegroundColor $statusColor
        
        if ($response.StatusCode -in 200..299) {
            try {
                $content = $response.Content | ConvertFrom-Json
                if ($content.count -ne $null) {
                    Write-Host "    ℹ Registros: $($content.count)" -ForegroundColor Cyan
                }
                if ($content.results -ne $null) {
                    Write-Host "    ℹ Results: $($content.results.Count) itens" -ForegroundColor Cyan
                }
            } catch {
                # Ignora erro de parse
            }
        }
        
        return @{ Success = $true; StatusCode = $response.StatusCode; Data = $content }
    }
    catch {
        Write-Host "    ✗ Erro: $($_.Exception.Message)" -ForegroundColor Red
        return @{ Success = $false; Error = $_.Exception.Message }
    }
}

# ============================================================================
# TESTES DAS NOVAS ENTIDADES
# ============================================================================

Write-Host "`n📊 TESTE DAS NOVAS TABELAS - AÇÕES PNGI" -ForegroundColor Magenta
Write-Host "URL Base: $BaseURL" -ForegroundColor Gray
Write-Host "Token: $(if ($Token) { 'Fornecido' } else { 'Não fornecido (testando endpoints públicos)' })" -ForegroundColor Gray

# ============================================================================
# 1. AÇÕES
# ============================================================================

Write-TestHeader "1. AÇÕES (ACOES)"

Test-Endpoint -Url "$API_BASE/acoes/" -Name "Listar Ações"
Test-Endpoint -Url "$API_BASE/acoes/?search=teste" -Name "Buscar Ações (search)"
Test-Endpoint -Url "$API_BASE/acoes/?ordering=strapelido" -Name "Ordenar Ações (ordering)"
Test-Endpoint -Url "$API_BASE/acoes/?idvigenciapngi=1" -Name "Filtrar por Vigência"

Write-Host "`n  Testando Actions:" -ForegroundColor Magenta
# Assumindo que existe acao com id=1 (ajustar se necessário)
Test-Endpoint -Url "$API_BASE/acoes/1/prazos_ativos/" -Name "Prazos Ativos da Ação #1"
Test-Endpoint -Url "$API_BASE/acoes/1/responsaveis_list/" -Name "Responsáveis da Ação #1"

# ============================================================================
# 2. PRAZOS
# ============================================================================

Write-TestHeader "2. PRAZOS DE AÇÕES"

Test-Endpoint -Url "$API_BASE/prazos/" -Name "Listar Prazos"
Test-Endpoint -Url "$API_BASE/prazos/ativos/" -Name "Listar Apenas Prazos Ativos (action)"
Test-Endpoint -Url "$API_BASE/prazos/?idacao=1" -Name "Filtrar Prazos por Ação"
Test-Endpoint -Url "$API_BASE/prazos/?isacaoprazoativo=true" -Name "Filtrar Prazos Ativos"

# ============================================================================
# 3. DESTAQUES
# ============================================================================

Write-TestHeader "3. DESTAQUES DE AÇÕES"

Test-Endpoint -Url "$API_BASE/destaques/" -Name "Listar Destaques"
Test-Endpoint -Url "$API_BASE/destaques/?idacao=1" -Name "Filtrar Destaques por Ação"
Test-Endpoint -Url "$API_BASE/destaques/?ordering=-datdatadestaque" -Name "Ordenar por Data (desc)"

# ============================================================================
# 4. TIPOS DE ANOTAÇÃO DE ALINHAMENTO
# ============================================================================

Write-TestHeader "4. TIPOS DE ANOTAÇÃO DE ALINHAMENTO"

Test-Endpoint -Url "$API_BASE/tipos-anotacao-alinhamento/" -Name "Listar Tipos"
Test-Endpoint -Url "$API_BASE/tipos-anotacao-alinhamento/?search=monitoramento" -Name "Buscar Tipos"
Test-Endpoint -Url "$API_BASE/tipos-anotacao-alinhamento/?ordering=strdescricaotipoanotacaoalinhamento" -Name "Ordenar Tipos"

# ============================================================================
# 5. ANOTAÇÕES DE ALINHAMENTO
# ============================================================================

Write-TestHeader "5. ANOTAÇÕES DE ALINHAMENTO"

Test-Endpoint -Url "$API_BASE/anotacoes-alinhamento/" -Name "Listar Anotações"
Test-Endpoint -Url "$API_BASE/anotacoes-alinhamento/?idacao=1" -Name "Filtrar por Ação"
Test-Endpoint -Url "$API_BASE/anotacoes-alinhamento/?idtipoanotacaoalinhamento=1" -Name "Filtrar por Tipo"
Test-Endpoint -Url "$API_BASE/anotacoes-alinhamento/?search=monitoramento" -Name "Buscar Anotações"
Test-Endpoint -Url "$API_BASE/anotacoes-alinhamento/?ordering=-datdataanotacaoalinhamento" -Name "Ordenar por Data (desc)"

# ============================================================================
# 6. USUÁRIOS RESPONSÁVEIS
# ============================================================================

Write-TestHeader "6. USUÁRIOS RESPONSÁVEIS"

Test-Endpoint -Url "$API_BASE/usuarios-responsaveis/" -Name "Listar Responsáveis"
Test-Endpoint -Url "$API_BASE/usuarios-responsaveis/?strorgao=SEGER" -Name "Filtrar por Órgão"
Test-Endpoint -Url "$API_BASE/usuarios-responsaveis/?search=silva" -Name "Buscar Responsável"
Test-Endpoint -Url "$API_BASE/usuarios-responsaveis/?ordering=idusuario__name" -Name "Ordenar por Nome"

# ============================================================================
# 7. RELAÇÕES AÇÃO-RESPONSÁVEL
# ============================================================================

Write-TestHeader "7. RELAÇÕES AÇÃO-RESPONSÁVEL"

Test-Endpoint -Url "$API_BASE/relacoes-acao-responsavel/" -Name "Listar Relações"
Test-Endpoint -Url "$API_BASE/relacoes-acao-responsavel/?idacao=1" -Name "Filtrar por Ação"
Test-Endpoint -Url "$API_BASE/relacoes-acao-responsavel/?search=teste" -Name "Buscar Relações"

# ============================================================================
# RESUMO FINAL
# ============================================================================

Write-Host "`n" -NoNewline
Write-Host ("═" * 70) -ForegroundColor Magenta
Write-Host "TESTE DAS NOVAS TABELAS CONCLUÍDO" -ForegroundColor Magenta
Write-Host ("═" * 70) -ForegroundColor Magenta

Write-Host "`nEntidades Testadas:" -ForegroundColor Cyan
Write-Host "  ✓ Ações (com filtros e actions)" -ForegroundColor Green
Write-Host "  ✓ Prazos (com action 'ativos')" -ForegroundColor Green
Write-Host "  ✓ Destaques" -ForegroundColor Green
Write-Host "  ✓ Tipos de Anotação" -ForegroundColor Green
Write-Host "  ✓ Anotações de Alinhamento" -ForegroundColor Green
Write-Host "  ✓ Usuários Responsáveis" -ForegroundColor Green
Write-Host "  ✓ Relações Ação-Responsável" -ForegroundColor Green

Write-Host "`nℹ Nota: Ajuste os IDs de teste (idacao=1, etc) conforme seus dados." -ForegroundColor Yellow
Write-Host "ℹ Para testes autenticados, passe o token JWT com -Token 'seu-token'" -ForegroundColor Yellow
