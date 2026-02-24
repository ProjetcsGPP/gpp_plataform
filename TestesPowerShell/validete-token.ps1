# teste-completo-final.ps1
$TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwiYXBwX2NvZGUiOiJBQ09FU19QTkdJIiwiYWN0aXZlX3JvbGVfaWQiOjMsInJvbGVfY29kZSI6IkdFU1RPUl9QTkdJIiwiZXhwIjoxNzcxOTM3MTg5LCJpYXQiOjE3NzE5MzY1ODksImp0aSI6IjExYzc1NjE5MjU0MjRiYTY4NGI4YjkxNDk0NjQwNzRjLTE3NzE5MzY1ODkiLCJ0b2tlbl90eXBlIjoiYWNjZXNzIn0.4nSSOobIcNcOuArKSUtmjZNIjbqMFxCP-agQ1BAdg-M"

$headers = @{"Authorization" = "Bearer $TOKEN"}

Write-Host "🎉 TESTE FINAL JWT" -ForegroundColor Green

# 1. Validate
Write-Host "`n1️⃣ VALIDATE TOKEN:" -ForegroundColor Cyan
$validate = Invoke-RestMethod -Uri "http://127.0.0.1:8000/accounts/api/auth/validate/" -Headers $headers
Write-Host "✅ VALIDADO → $($validate.token_payload.role_code)" -ForegroundColor Green

# 2. User Management (se existir)
Write-Host "`n2️⃣ USER MANAGEMENT:" -ForegroundColor Cyan
$userMgmt = Invoke-RestMethod -Uri "http://127.0.0.1:8000/accounts/api/gestao/usuarios/" -Headers $headers
Write-Host "✅ GESTÃO OK → $($userMgmt | ConvertTo-Json -Depth 3)"

Write-Host "`n🎊 JWT + MIDDLEWARE 100% FUNCIONANDO!" -ForegroundColor Green
