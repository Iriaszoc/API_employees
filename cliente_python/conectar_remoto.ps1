# ============================================================
#  CONECTAR AL SERVIDOR DE TU COMPAÑERA
#  Sustituye la IP aqui abajo cuando te la comparta
# ============================================================

$IP = "192.168.X.X"   # <-- PON AQUI LA IP DE TU COMPAÑERA

$env:API_URL = "http://${IP}:8080"
Write-Host "Conectando a: $env:API_URL" -ForegroundColor Cyan

python main.py
