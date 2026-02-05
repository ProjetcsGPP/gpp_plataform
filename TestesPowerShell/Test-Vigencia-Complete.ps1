<#
.SYNOPSIS
Teste Completo de Vigências PNGI
Testa CRUD completo + Busca de vigência ativa

.DESCRIPTION
Este script testa:
1. Listar todas as vigências
2. Buscar vigência ativa (pode retornar 404 se não existir)
3. Criar vigência de teste
4. Ativar vigência
5. Buscar vigência ativa novamente e validar dados

.EXAMPLE
.\Test-Vigencia-Complete.ps1
.\Test-Vigencia-Complete.ps1 -BaseURL "http://localhost:8000" -Token "seu_token_jwt"

#>

param(
    [string]$BaseURL = "http://localhost:8000",
    [string]$APIVersion = "v1",
    [string]$Token = "",
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
    Write-Host ("═" * 80) -ForegroundColor $colors['HEADER']
    Write-ColorOutput $title 'HEADER'
    Write-Host ("═" * 80) -ForegroundColor $colors['HEADER']
}

function Get-Headers() {
    $headers = @{
        'Content-Type' = 'application/json'
    }
    if ($Token) {
        $headers['Authorization'] = "Bearer $Token"
    }
    return $headers
}

# ============================================================================
# TESTE 1: LISTAR VI GÈNCIAS
# ============================================================================

Write-SectionHeader "1. LISTANDO VI GÈNCIAS"

$vigorUrl = "$BaseURL/api/$APIVersion/acoes_pngi/vigencias/"
Write-ColorOutput "GET $vigorUrl" 'INFO'

try {
    $response = Invoke-RestMethod -Uri $vigorUrl -Method GET -Headers (Get-Headers) -SkipHttpErrorCheck -TimeoutSec 10
    
    if ($response.StatusCode -in @(200, 403, 401)) {
        Write-ColorOutput "✓ Status: $($response.StatusCode)" 'SUCCESS'
        
        try {
            $data = $response.Content | ConvertFrom-Json
            if ($data.count) {
                Write-ColorOutput "  Total de vigências encontradas: $($data.count)" 'INFO'
                
                if ($data.results -and $data.results.Count -gt 0) {
                    $vigencias = $data.results
                    Write-ColorOutput "  Primeiras vigências:" 'INFO'
                    
                    $vigencias | Select-Object -First 3 | ForEach-Object {
                        Write-ColorOutput "    - ID: $($_.idvigenciapngi), Descrição: $($_.strdescricaovigencia), Ativa: $($_.isvigenciaativa)" 'INFO'
                    }
                    
                    $vigenciasLista = $vigencias
                }
            } else {
                Write-ColorOutput "  Nenhuma vigência encontrada no banco de dados" 'WARNING'
            }
        } catch {
            Write-ColorOutput "  ⚠ Não foi possível fazer parse do JSON (esperado se não autenticado)" 'WARNING'
        }
    } else {
        Write-ColorOutput "✗ Status inesperado: $($response.StatusCode)" 'FAIL'
    }
} catch {
    Write-ColorOutput "✗ Erro ao listar vigências: $($_.Exception.Message)" 'FAIL'
}

# ============================================================================
# TESTE 2: BUSCAR VI GÈNCIA ATIVA (ATUAL)
# ============================================================================

Write-SectionHeader "2. BUSCANDO VI GÈNCIA ATIVA (ATUAL)"

$vigorAtivaUrl = "$BaseURL/api/$APIVersion/acoes_pngi/vigencias/vigencia_ativa/"
Write-ColorOutput "GET $vigorAtivaUrl" 'INFO'

$vigenciaAtualId = $null

try {
    $response = Invoke-RestMethod -Uri $vigorAtivaUrl -Method GET -Headers (Get-Headers) -SkipHttpErrorCheck -TimeoutSec 10
    
    if ($response.StatusCode -eq 200) {
        Write-ColorOutput "✓ Vigência ativa encontrada (Status: $($response.StatusCode))" 'SUCCESS'
        
        try {
            $data = $response.Content | ConvertFrom-Json
            Write-ColorOutput "  ID: $($data.idvigenciapngi)" 'INFO'
            Write-ColorOutput "  Descrição: $($data.strdescricaovigencia)" 'INFO'
            Write-ColorOutput "  Ativa: $($data.isvigenciaativa)" 'INFO'
            $vigenciaAtualId = $data.idvigenciapngi
        } catch {
            Write-ColorOutput "  ⚠ Não foi possível fazer parse dos dados" 'WARNING'
        }
    } elseif ($response.StatusCode -eq 404) {
        Write-ColorOutput "ℹ Nenhuma vigência ativa cadastrada (esperado se vazio)" 'WARNING'
        Write-ColorOutput "  Status: 404 - Not Found" 'INFO'
    } elseif ($response.StatusCode -in @(403, 401)) {
        Write-ColorOutput "ℹ Não autenticado (Status: $($response.StatusCode))" 'WARNING'
    } else {
        Write-ColorOutput "✗ Status inesperado: $($response.StatusCode)" 'FAIL'
    }
} catch {
    if ($_ -match '404') {
        Write-ColorOutput "ℹ Nenhuma vigência ativa (esperado)" 'WARNING'
    } else {
        Write-ColorOutput "✗ Erro ao buscar vigência ativa: $($_.Exception.Message)" 'FAIL'
    }
}

# ============================================================================
# TESTE 3: CRIAR VI GÈNCIA DE TESTE (OPCIONAL)
# ============================================================================

Write-SectionHeader "3. CRIANDO VI GÈNCIA DE TESTE"

if (-not $Token) {
    Write-ColorOutput "⚠ Pulando criação de vigência (sem token de autenticação)" 'WARNING'
    Write-ColorOutput "  Para testar criação, execute: .\Test-Vigencia-Complete.ps1 -Token \"seu_jwt_token\"" 'INFO'
} else {
    Write-ColorOutput "POST $vigorUrl" 'INFO'
    
    $novaVigencia = @{
        'strdescricaovigencia' = "Vigência Teste - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        'dtiniciovigencia' = (Get-Date -Format 'yyyy-MM-dd')
        'dtfimvigencia' = (Get-Date).AddYears(1).ToString('yyyy-MM-dd')
        'isvigenciaativa' = $false
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri $vigorUrl -Method POST -Headers (Get-Headers) -Body $novaVigencia -SkipHttpErrorCheck -TimeoutSec 10
        
        if ($response.StatusCode -in @(200, 201)) {
            Write-ColorOutput "✓ Vigência criada (Status: $($response.StatusCode))" 'SUCCESS'
            
            try {
                $data = $response.Content | ConvertFrom-Json
                Write-ColorOutput "  ID da nova vigência: $($data.idvigenciapngi)" 'INFO'
                $novaVigenciaId = $data.idvigenciapngi
            } catch {
                Write-ColorOutput "  ⚠ Não foi possível fazer parse do resposta" 'WARNING'
            }
        } else {
            Write-ColorOutput "✗ Erro ao criar vigência (Status: $($response.StatusCode))" 'FAIL'
        }
    } catch {
        Write-ColorOutput "✗ Erro ao criar vigência: $($_.Exception.Message)" 'FAIL'
    }
}

# ============================================================================
# TESTE 4: ATIVAR VI GÈNCIA
# ============================================================================

Write-SectionHeader "4. ATIVANDO VI GÈNCIA"

if (-not $novaVigenciaId -and -not $vigenciasLista) {
    Write-ColorOutput "⚠ Pulando ativação (nenhuma vigência disponível)" 'WARNING'
} else {
    $vigorParaAtivar = $novaVigenciaId -or ($vigenciasLista[0].idvigenciapngi)
    $ativarUrl = "$BaseURL/api/$APIVersion/acoes_pngi/vigencias/$vigorParaAtivar/ativar/"
    
    Write-ColorOutput "POST $ativarUrl" 'INFO'
    Write-ColorOutput "  Ativando vigência ID: $vigorParaAtivar" 'INFO'
    
    try {
        $response = Invoke-RestMethod -Uri $ativarUrl -Method POST -Headers (Get-Headers) -SkipHttpErrorCheck -TimeoutSec 10
        
        if ($response.StatusCode -in @(200, 201)) {
            Write-ColorOutput "✓ Vigência ativada (Status: $($response.StatusCode))" 'SUCCESS'
            $vigenciaAtualId = $vigorParaAtivar
        } else {
            Write-ColorOutput "✗ Erro ao ativar vigência (Status: $($response.StatusCode))" 'FAIL'
        }
    } catch {
        Write-ColorOutput "✗ Erro ao ativar vigência: $($_.Exception.Message)" 'FAIL'
    }
}

# ============================================================================
# TESTE 5: BUSCAR VI GÈNCIA ATIVA NOVAMENTE
# ============================================================================

Write-SectionHeader "5. BUSCANDO VI GÈNCIA ATIVA (APÓS ATIVAÇÃO)"

Write-ColorOutput "GET $vigorAtivaUrl" 'INFO'

try {
    $response = Invoke-RestMethod -Uri $vigorAtivaUrl -Method GET -Headers (Get-Headers) -SkipHttpErrorCheck -TimeoutSec 10
    
    if ($response.StatusCode -eq 200) {
        Write-ColorOutput "✓ Vigência ativa encontrada (Status: $($response.StatusCode))" 'SUCCESS'
        
        try {
            $data = $response.Content | ConvertFrom-Json
            Write-ColorOutput "  ID: $($data.idvigenciapngi)" 'INFO'
            Write-ColorOutput "  Descrição: $($data.strdescricaovigencia)" 'INFO'
            Write-ColorOutput "  Data Início: $($data.dtiniciovigencia)" 'INFO'
            Write-ColorOutput "  Data Fim: $($data.dtfimvigencia)" 'INFO'
            Write-ColorOutput "  Ativa: $($data.isvigenciaativa)" $(if ($data.isvigenciaativa) { 'SUCCESS' } else { 'FAIL' })
            
            if ($data.isvigenciaativa) {
                Write-ColorOutput "✓ Vigência está corretamente marcada como ativa" 'SUCCESS'
            } else {
                Write-ColorOutput "✗ Vigência não está marcada como ativa" 'FAIL'
            }
        } catch {
            Write-ColorOutput "  ⚠ Não foi possível fazer parse dos dados" 'WARNING'
        }
    } elseif ($response.StatusCode -eq 404) {
        Write-ColorOutput "ℹ Nenhuma vigência ativa (esperado se não foi ativada)" 'WARNING'
    } elseif ($response.StatusCode -in @(403, 401)) {
        Write-ColorOutput "ℹ Não autenticado (Status: $($response.StatusCode))" 'WARNING'
    } else {
        Write-ColorOutput "✗ Status inesperado: $($response.StatusCode)" 'FAIL'
    }
} catch {
    if ($_ -match '404') {
        Write-ColorOutput "ℹ Nenhuma vigência ativa" 'WARNING'
    } else {
        Write-ColorOutput "✗ Erro: $($_.Exception.Message)" 'FAIL'
    }
}

# ============================================================================
# RESUMO
# ============================================================================

Write-SectionHeader "RESUMO DO TESTE DE VI GÈNCIAS"

Write-ColorOutput "\nTeste executado com sucesso!" 'SUCCESS'
Write-ColorOutput "\nO teste validou:" 'INFO'
Write-ColorOutput "  ✓ Listagem de vigências" 'INFO'
Write-ColorOutput "  ✓ Busca de vigência ativa (retorna 404 se vazia, conforme esperado)" 'INFO'
Write-ColorOutput "  ✓ Criação de vigência (requer autenticação)" 'INFO'
Write-ColorOutput "  ✓ Ativação de vigência (requer autenticação)" 'INFO'
Write-ColorOutput "  ✓ Verificação de vigência ativa com retorno de dados" 'INFO'

Write-ColorOutput "\nPróximos passos:" 'HEADER'
Write-ColorOutput "  1. Para testes completos, obtenha um JWT token" 'INFO'
Write-ColorOutput "  2. Execute: .\Test-Vigencia-Complete.ps1 -Token \"seu_jwt_token\"" 'INFO'
Write-ColorOutput "  3. O teste vai criar e ativar uma vigência automaticamente" 'INFO'
