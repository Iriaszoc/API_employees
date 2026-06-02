# 📡 Guía de Conexión — Prueba en Red Local

> **Rox** corre el servidor (Docker). **Frida, Pablo y Emartha** se conectan a ella.  
> Todos trabajarán sobre la **misma base de datos en tiempo real**.

---

## 📋 Resumen rápido

| Integrante | Rol | Script | Cambia la IP? |
|---|---|---|---|
| **Rox** | Servidor | `conectar_rox.ps1` | No |
| **Frida** | Cliente | `conectar_frida.ps1` | Sí |
| **Pablo** | Cliente | `conectar_pablo.ps1` | Sí |
| **Emartha** | Cliente | `conectar_emartha.ps1` | Sí |

---

---

## ROX — Configuración del Servidor

> Rox es quien levanta Docker. Los demás se conectan a su IP.

### Paso 1 — Levantar el servidor Docker

Abre PowerShell en la carpeta `API_employees` y ejecuta:

```powershell
docker compose up -d
```

Espera hasta ver:
```
Container api_employees-db-1   Started  
Container api_employees-api-1  Started  
```

### Paso 2 — Abrir el puerto 8080 en el firewall

Para que Frida, Pablo y Emartha puedan conectarse, ejecuta en **PowerShell como Administrador**:

```powershell
netsh advfirewall firewall add rule name="API Empleados 8080" dir=in action=allow protocol=TCP localport=8080
```

### Paso 3 — Obtener tu IP local y compartirla

```powershell
ipconfig
```

Busca **Dirección IPv4** en tu adaptador activo (WiFi o Ethernet). Ejemplo:
```
Dirección IPv4. . . : 192.168.1.45
```

**Comparte esa IP con Frida, Pablo y Emartha.**

### Paso 4 — Abrir tu propio cliente

En la carpeta `prueba_conexiones`:

```powershell
.\conectar_rox.ps1
```

---

---

## FRIDA — Configuración del Cliente

### Paso 1 — Instalar dependencias Python (solo la primera vez)

En PowerShell, desde la carpeta `cliente_python`:

```powershell
pip install -r requirements.txt
```

### Paso 2 — Poner la IP de Rox en el script

Abre `conectar_frida.ps1` y cambia esta línea:

```powershell
$IP_ROX = "192.168.X.X"   # <-- pon aqui la IP de Rox
```

Por la IP real, por ejemplo:

```powershell
$IP_ROX = "192.168.1.45"
```

### Paso 3 — Ejecutar

Desde la carpeta `prueba_conexiones`:

```powershell
.\conectar_frida.ps1
```

---

---

## PABLO — Configuración del Cliente

### Paso 1 — Instalar dependencias Python (solo la primera vez)

```powershell
pip install -r requirements.txt
```

### Paso 2 — Poner la IP de Rox en el script

Abre `conectar_pablo.ps1` y cambia:

```powershell
$IP_ROX = "192.168.X.X"   # <-- pon aqui la IP de Rox
```

### Paso 3 — Ejecutar

```powershell
.\conectar_pablo.ps1
```

---

---

## MARTHA — Configuración del Cliente

### Paso 1 — Instalar dependencias Python (solo la primera vez)

```powershell
pip install -r requirements.txt
```

### Paso 2 — Poner la IP de Rox en el script

Abre `conectar_emartha.ps1` y cambia:

```powershell
$IP_ROX = "192.168.X.X"   # <-- pon aqui la IP de Rox
```

### Paso 3 — Ejecutar

```powershell
.\conectar_emartha.ps1
```

---

---

## Solución de problemas

### "No se pudo conectar a 192.168.X.X:8080"

| Causa probable | Solución |
|---|---|
| Rox no levantó Docker | Rox ejecuta `docker compose up -d` |
| Firewall de Rox bloqueando | Rox ejecuta el comando `netsh` del Paso 2 |
| IP incorrecta | Verificar con `ipconfig` en la laptop de Rox |
| No están en la misma red WiFi | Todos conectarse al mismo router o hotspot |

### Verificar el servidor manualmente

Cambia la IP por la de Rox y ejecuta desde cualquier cliente:

```powershell
Invoke-WebRequest -Uri "http://192.168.X.X:8080/empleados" -TimeoutSec 5
```

Si devuelve JSON con empleados → todo bien.

---

## Prueba de que los 3 están conectados a la vez

1. **Frida** crea un empleado nuevo (p.ej. `emp_no: 777777`, nombre: `Frida`)
2. **Pablo** presiona **Refrescar** → debe aparecer el empleado de Frida
3. **Emartha** lo edita desde su cliente
4. Todos refrescan → ven el cambio de Emartha

Esto demuestra que los 4 están sobre **la misma base de datos en tiempo real**. 🎯

---

## Para apagar (solo Rox, al terminar)

```powershell
docker compose down
```

> `docker compose down -v` borra también los datos de la BD. No usar salvo que quieras reiniciar todo.
