# teste-jwt-FINAL.ps1
$BASE_URL = "http://127.0.0.1:8000/accounts/api"  # Base
$LOGIN_URL = "$BASE_URL/auth/login/"               # Completo
$VALIDATE_URL = "$BASE_URL/auth/validate/"         # Completo
$REFRESH_URL = "$BASE_URL/auth/refresh/"           # Completo
$LOGOUT_URL = "$BASE_URL/auth/logout/"             # Completo

# 1. LOGIN
Write-Host "1️⃣ LOGIN → $LOGIN_URL" -ForegroundColor Cyan
$loginBody = @{
    email = "alexandre.mohamad@seger.es.gov.br"
    password = "Awm2@11712"  # ALTERE sua senha!
    app_code = "ACOES_PNGI"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri $LOGIN_URL -Method POST -ContentType "application/json" -Body $loginBody -TimeoutSec 10
    $ACCESS_TOKEN = $loginResponse.access_token
    $REFRESH_TOKEN = $loginResponse.refresh_token
    
    Write-Host "✅ LOGIN OK!" -ForegroundColor Green
    Write-Host "👤 $($loginResponse.user.name) ($($loginResponse.user.role))" -ForegroundColor Green
} catch {
    Write-Host "❌ LOGIN FALHOU:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# 2. VALIDATE
Write-Host "`n2️⃣ VALIDATE → $VALIDATE_URL" -ForegroundColor Cyan
$headers = @{"Authorization" = "Bearer $ACCESS_TOKEN"}

$validateResponse = Invoke-RestMethod -Uri $VALIDATE_URL -Method GET -Headers $headers
Write-Host "✅ TOKEN VÁLIDO → $($validateResponse.token_payload.app_code)" -ForegroundColor Green

# 3. REFRESH
Write-Host "`n3️⃣ REFRESH → $REFRESH_URL" -ForegroundColor Cyan
$refreshBody = @{refresh_token = $REFRESH_TOKEN} | ConvertTo-Json
$refreshResponse = Invoke-RestMethod -Uri $REFRESH_URL -Method POST -ContentType "application/json" -Body $refreshBody
Write-Host "✅ REFRESH OK!" -ForegroundColor Green

# 4. LOGOUT
Write-Host "`n4️⃣ LOGOUT → $LOGOUT_URL" -ForegroundColor Cyan
$logoutBody = @{refresh_token = $REFRESH_TOKEN} | ConvertTo-Json
Invoke-RestMethod -Uri $LOGOUT_URL -Method POST -ContentType "application/json" -Headers $headers -Body $logoutBody
Write-Host "✅ LOGOUT OK!" -ForegroundColor Green

Write-Host "`n🎉 JWT Universal FUNCIONANDO PERFEITAMENTE!" -ForegroundColor Green
