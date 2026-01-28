[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Token
)

$API_URL = "http://localhost:8000/api/v1/acoes_pngi"

function Test-CreateWithDebug {
    param(
        [string]$Url,
        [object]$Body
    )
    
    $headers = @{
        "Authorization" = "Bearer $Token"
        "Content-Type" = "application/json"
    }
    
    Write-Host "`nTestando: $Url" -ForegroundColor Cyan
    Write-Host "Body: $($Body | ConvertTo-Json)" -ForegroundColor Yellow
    
    try {
        $response = Invoke-RestMethod -Uri $Url -Method Post `
            -Headers $headers -Body ($Body | ConvertTo-Json) -ErrorAction Stop
        
        Write-Host "✓ Sucesso!" -ForegroundColor Green
        $response | ConvertTo-Json -Depth 5
    }
    catch {
        Write-Host "✗ Erro: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
        
        # Tentar ler o erro detalhado
        try {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $errorBody = $reader.ReadToEnd() | ConvertFrom-Json
            Write-Host "Detalhes do erro:" -ForegroundColor Red
            $errorBody | ConvertTo-Json -Depth 5
        }
        catch {
            Write-Host "Não foi possível ler detalhes do erro" -ForegroundColor Red
        }
    }
}

# Testar Situação
Write-Host "`n=== TESTANDO SITUAÇÃO ===" -ForegroundColor Magenta
$sitBody = @{
    strdescricaosituacao = "TESTE"
}
Test-CreateWithDebug -Url "$API_URL/situacoes/" -Body $sitBody

# Testar Vigência
Write-Host "`n=== TESTANDO VIGÊNCIA ===" -ForegroundColor Magenta
$vigBody = @{
    strdescricaovigenciapngi = "Teste 2026"
    datiniciovigencia = "2026-01-01"
    datfinalvigencia = "2026-12-31"
    isvigenciaativa = $false
}
Test-CreateWithDebug -Url "$API_URL/vigencias/" -Body $vigBody
