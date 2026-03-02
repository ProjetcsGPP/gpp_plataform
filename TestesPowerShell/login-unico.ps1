# login-unico.ps1
$email = "alexandre.mohamad@seger.es.gov.br"
$password = "Awm2@11712"  # ← ALTERE!
$app_code = "ACOES_PNGI"

$body = @{
    email = $email
    password = $password
    app_code = $app_code
} | ConvertTo-Json

Write-Host "🔐 LOGIN REAL → http://127.0.0.1:8000/accounts/api/auth/login/" -ForegroundColor Green

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/accounts/api/auth/login/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

Write-Host "✅ SUCESSO!" -ForegroundColor Green
Write-Host "👤 $($response.user.name) ($($response.user.role))" -ForegroundColor Yellow
Write-Host "🔑 Access: $($response.access_token.Substring(0,30))..." -ForegroundColor Gray
Write-Host "`n📋 TOKEN para testes: Bearer $($response.access_token)" -ForegroundColor Cyan
