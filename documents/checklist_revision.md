# Checklist de revision del avance

## Roxana — Backend Go + Docker/MySQL/Despliegue
- [x] Variables de entorno leidas desde el entorno en `main.go` (no hardcodeadas).
- [x] `updateEmpleado` responde JSON en lugar de texto plano.
- [x] `getEmpleado` devuelve cuerpo JSON en el 404.
- [x] `createEmpleado` valida campos requeridos antes de insertar (devuelve 400 si faltan).
- [x] `Dockerfile` usa `golang:1.22-alpine` (no 1.26-alpine).
- [x] `docker-compose.yml` tiene `healthcheck` en el servicio `db`.
- [x] `docker-compose.yml` usa `service_healthy` en `depends_on` del servicio `api`.
- [x] Existe archivo `.env` con credenciales (NO commiteado).
- [x] `.gitignore` incluye la linea `.env`.
- [x] Existe `docker-compose.test.yml` sin volumenes persistentes.
- [x] Existe `DEPLOY.md` con guia de arranque documentada.
- [x] `docker-compose up --build` levanta sin errores en equipo limpio.

## Eli — Despliegue, GitHub Actions y evidencia
- [x] Existe `docker-compose.test.yml` listo para CI.
- [x] El workflow de GitHub Actions ejecuta pruebas y publica resumen.
- [x] El workflow sube logs como artefacto descargable.
- [x] Se tiene evidencia de arranque y pruebas en logs o capturas.
- [x] El equipo entiende el flujo de despliegue y verificación.

## Frida — Interfaz grafica del cliente Python
- [x] Existe ventana principal con tabla `Treeview` mostrando empleados.
- [x] Boton Refrescar carga los datos desde la API.
- [x] Boton Buscar por ID consulta un empleado especifico.
- [x] Boton Nuevo empleado abre formulario con los 6 campos.
- [x] Boton Editar pre-rellena el formulario con datos del registro seleccionado.
- [x] Boton Eliminar pide confirmacion antes de borrar.
- [x] Los errores de conexion se muestran en la interfaz (no crashea silenciosamente).
- [x] Existe `requirements.txt` con `requests>=2.31.0`.

## Pablo — api_client.py + Pruebas bash + GitHub Actions
- [x] Existe `cliente_python/api_client.py` con las 5 funciones (obtener_empleados, obtener_empleado, crear_empleado, actualizar_empleado, eliminar_empleado).
- [x] `api_client.py` fue compartido con Frida e integrado en la UI.
- [x] Existe `tests/test_api.sh` con los 8 casos de prueba (PASS/FAIL).
- [x] El script retorna exit code 1 si alguna prueba falla.
- [x] El script se ejecuta localmente sin errores (`bash tests/test_api.sh`).
- [x] Existe `.github/workflows/tests.yml` configurado.
- [x] El workflow levanta los servicios con `docker-compose.test.yml`.
- [x] El workflow publica el resumen de resultados en la pestana Summary de GitHub Actions.
- [x] El workflow sube el log como artefacto descargable.
- [x] El workflow falla el job si hay pruebas en FAIL.
- [x] El workflow se ejecuto al menos una vez en el repositorio de GitHub.

## Integracion final
- [x] Cliente Python se conecta a la API corriendo en Docker.
- [x] Flujo completo CRUD verificado desde la UI (Crear, Leer, Actualizar, Borrar).
- [x] Prueba en equipos separados en red de laboratorio.
- [x] GitHub Actions muestra ejecucion exitosa en el repositorio.
- [x] Toda la documentacion entregada esta alineada al comportamiento real del sistema.
