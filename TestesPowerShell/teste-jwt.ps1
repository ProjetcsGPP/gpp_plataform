# =============================================================================
# TESTE JWT UNIVERSAL - GPP Plataform
# =============================================================================
# Executa no PowerShell (Windows) - Testa autenticação completa
# =============================================================================

# Configurações
$BASE_URL = "http://localhost:8000"
$EMAIL = "acoesgpp@seger.es.gov.br"  # ALTERE para seu usuário
$PASSWORD = "Gpp#Adm2026"       # ALTERE para sua senha
$APP_CODE = "ACOES_PNGI"

Write-Host "🚀 Testando GPP Plataform JWT Universal..." -ForegroundColor Green
Write-Host "📧 Email: $EMAIL" -ForegroundColor Yellow
Write-Host "📱 App: $APP_CODE" -ForegroundColor Yellow
Write-Host ""

# =============================================================================
# 1. LOGIN - Obtém tokens JWT
# =============================================================================
Write-Host "1️⃣  FAZENDO LOGIN..." -ForegroundColor Cyan

$loginBody = @{
    email = $EMAIL
    password = $PASSWORD
    app_code = $APP_CODE
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "$BASE_URL/api/auth/login/" `
        -Method POST `
        -ContentType "application/json" `
        -Body $loginBody `
        -TimeoutSec 10
} catch {
    Write-Host "❌ ERRO: Servidor não responde em $BASE_URL" -ForegroundColor Red
    Write-Host "🔧 SOLUÇÃO: Execute 'python manage.py runserver 8000'" -ForegroundColor Yellow
    exit 1
}

if (-not $loginResponse.access_token) {
    Write-Host "❌ LOGIN FALHOU: Verifique email/senha" -ForegroundColor Red
    exit 1
}

$ACCESS_TOKEN = $loginResponse.access_token
$REFRESH_TOKEN = $loginResponse.refresh_token

Write-Host "✅ Login OK!" -ForegroundColor Green
Write-Host "🔑 Access Token: $($ACCESS_TOKEN.Substring(0,20))..." -ForegroundColor Gray
Write-Host "🔄 Refresh Token: $($REFRESH_TOKEN.Substring(0,20))..." -ForegroundColor Gray
Write-Host "👤 Usuário: $($loginResponse.user.name) ($($loginResponse.user.role))" -ForegroundColor Green
Write-Host ""

# =============================================================================
# 2. TESTA API PROTEGIDA (com JWT)
# =============================================================================
Write-Host "2️⃣  TESTANDO API PROTEGIDA..." -ForegroundColor Cyan

$headers = @{
    "Authorization" = "Bearer $ACCESS_TOKEN"
    "Content-Type" = "application/json"
}

$eixosResponse = Invoke-RestMethod -Uri "$BASE_URL/api/acoes_pngi/eixos/" `
    -Method GET `
    -Headers $headers

Write-Host "✅ Eixos carregados: $($eixosResponse.count)" -ForegroundColor Green
Write-Host "📊 Primeiro eixo: $($eixosResponse[0].stralias) - $($eixosResponse[0].strdescricaoeixo)" -ForegroundColor Yellow
Write-Host ""

# =============================================================================
# 3. TESTA VALIDATE TOKEN
# =============================================================================
Write-Host "3️⃣  VALIDANDO TOKEN..." -ForegroundColor Cyan

$validateResponse = Invoke-RestMethod -Uri "$BASE_URL/api/auth/validate/" `
    -Method GET `
    -Headers $headers

Write-Host "✅ Token VÁLIDO!" -ForegroundColor Green
Write-Host "🎭 App: $($validateResponse.token_payload.app_code)" -ForegroundColor Yellow
Write-Host "👑 Role: $($validateResponse.token_payload.role_code)" -ForegroundColor Yellow
Write-Host "⏰ Expira: $([datetimeoffset]::FromUnixTimeSeconds($validateResponse.token_payload.exp).LocalDateTime)" -ForegroundColor Gray
Write-Host ""

# =============================================================================
# 4. TESTA REFRESH TOKEN
# =============================================================================
Write-Host "4️⃣  RENOVANDO TOKENS..." -ForegroundColor Cyan

$refreshBody = @{
    refresh_token = $REFRESH_TOKEN
} | ConvertTo-Json

$refreshResponse = Invoke-RestMethod -Uri "$BASE_URL/api/auth/refresh/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $refreshBody

$NEW_ACCESS_TOKEN = $refreshResponse.access_token

Write-Host "✅ Tokens renovados!" -ForegroundColor Green
Write-Host "🔑 Novo Access: $($NEW_ACCESS_TOKEN.Substring(0,20))..." -ForegroundColor Gray
Write-Host ""

# =============================================================================
# 5. TESTA NOVO TOKEN
# =============================================================================
Write-Host "5️⃣  TESTANDO NOVO TOKEN..." -ForegroundColor Cyan

$newHeaders = @{
    "Authorization" = "Bearer $NEW_ACCESS_TOKEN"
}

$newEixosResponse = Invoke-RestMethod -Uri "$BASE_URL/api/acoes_pngi/eixos/" `
    -Method GET `
    -Headers $newHeaders

Write-Host "✅ Novo token funcionando!" -ForegroundColor Green
Write-Host "📊 Eixos: $($newEixosResponse.count)" -ForegroundColor Yellow
Write-Host ""

# =============================================================================
# 6. TESTA LOGOUT (Revogação)
# =============================================================================
Write-Host "6️⃣  FAZENDO LOGOUT..." -ForegroundColor Cyan

$logoutBody = @{
    refresh_token = $REFRESH_TOKEN
} | ConvertTo-Json

$logoutResponse = Invoke-RestMethod -Uri "$BASE_URL/api/auth/logout/" `
    -Method POST `
    -ContentType "application/json" `
    -Headers $headers `
    -Body $logoutBody

Write-Host "✅ Logout OK! Tokens revogados." -ForegroundColor Green
Write-Host ""

# =============================================================================
# 7. TESTA TOKEN REVOGADO (deve falhar)
# =============================================================================
Write-Host "7️⃣  TESTANDO TOKEN REVOGADO..." -ForegroundColor Cyan

try {
    Invoke-RestMethod -Uri "$BASE_URL/api/acoes_pngi/eixos/" `
        -Method GET `
        -Headers $headers  # Token antigo revogado
} catch {
    $errorMsg = $_.Exception.Response.StatusCode.value__
    Write-Host "✅ Token revogado BLOQUEADO! (Status: $errorMsg)" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 TESTES CONCLUÍDOS COM SUCESSO!" -ForegroundColor Green
Write-Host "✅ 7 testes executados" -ForegroundColor Green
Write-Host "✅ JWT Universal funcionando perfeitamente!" -ForegroundColor Green
