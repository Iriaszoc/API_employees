# ============================================================
#  CLIENTE: FRIDA
#  Rox tiene el servidor — conectate a su IP
# ============================================================

$IP_ROX = "192.168.X.X"   # <-- SUSTITUIR con la IP real de Rox

$env:API_URL = "http://${IP_ROX}:8080"
Write-Host ""
Write-Host "========================================" -ForegroundColor DarkCyan
Write-Host "  Conectando como: FRIDA" -ForegroundColor Yellow
Write-Host "  Servidor de Rox: $env:API_URL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor DarkCyan
Write-Host ""

try {
    $resp = Invoke-WebRequest -Uri "$env:API_URL/empleados" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "Conexion exitosa con el servidor de Rox!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: No se pudo conectar a $env:API_URL" -ForegroundColor Red
    Write-Host "Verifica que Rox tiene el servidor corriendo y que la IP es correcta." -ForegroundColor Yellow
    Read-Host "Presiona Enter para intentar abrir la app de todos modos..."
}

python ..\cliente_python\main.py
