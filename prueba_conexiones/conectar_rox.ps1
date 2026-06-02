# ============================================================
#  CLIENTE: ROX  (el servidor corre en TU maquina)
#  Te conectas a tu propio localhost
# ============================================================

$env:API_URL = "http://localhost:8080"
Write-Host ""
Write-Host "========================================" -ForegroundColor DarkCyan
Write-Host "  Conectando como: ROX (servidor local)" -ForegroundColor Yellow
Write-Host "  Servidor:        $env:API_URL" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor DarkCyan
Write-Host ""

# Verificar que el servidor este corriendo
try {
    $resp = Invoke-WebRequest -Uri "$env:API_URL/empleados" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "Servidor local detectado y funcionando!" -ForegroundColor Green
} catch {
    Write-Host "ADVERTENCIA: El servidor no responde en localhost:8080" -ForegroundColor Red
    Write-Host "Asegurate de haber ejecutado: docker compose up -d" -ForegroundColor Yellow
    Read-Host "Presiona Enter para continuar..."
}

python ..\cliente_python\main.py
