# ============================================================
#  CLIENTE: PABLO
#  Rox tiene el servidor — tú te conectas a su IP
# ============================================================

$IP_ROX = "192.168.219.185"   # IP de Rox

$env:API_URL = "http://${IP_ROX}:8080"
Write-Host ""
Write-Host "========================================" -ForegroundColor DarkCyan
Write-Host "  Conectando como: PABLO" -ForegroundColor Yellow
Write-Host "  Servidor de Rox: $env:API_URL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor DarkCyan
Write-Host ""

# Verificar conexion antes de abrir la UI
try {
    $resp = Invoke-WebRequest -Uri "$env:API_URL/empleados" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "Conexion exitosa con el servidor de Rox!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: No se pudo conectar a $env:API_URL" -ForegroundColor Red
    Write-Host "Verifica que Rox tiene el servidor corriendo y que la IP es correcta." -ForegroundColor Yellow
    Read-Host "Presiona Enter para intentar abrir la app de todos modos..."
}

$mainPy = Join-Path $PSScriptRoot "..\cliente_python\main.py"
python $mainPy
