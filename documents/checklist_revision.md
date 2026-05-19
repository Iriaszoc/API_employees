# Checklist de revision del avance

## Roxana — Backend Go + Docker/MySQL/Despliegue
- [ ] Variables de entorno leidas desde el entorno en `main.go` (no hardcodeadas).
- [ ] `updateEmpleado` responde JSON en lugar de texto plano.
- [ ] `getEmpleado` devuelve cuerpo JSON en el 404.
- [ ] `createEmpleado` valida campos requeridos antes de insertar (devuelve 400 si faltan).
- [ ] `Dockerfile` usa `golang:1.22-alpine` (no 1.26-alpine).
- [ ] `docker-compose.yml` tiene `healthcheck` en el servicio `db`.
- [ ] `docker-compose.yml` usa `service_healthy` en `depends_on` del servicio `api`.
- [ ] Existe archivo `.env` con credenciales (NO commiteado).
- [ ] `.gitignore` incluye la linea `.env`.
- [ ] Existe `docker-compose.test.yml` sin volumenes persistentes.
- [ ] Existe `DEPLOY.md` con guia de arranque documentada.
- [ ] `docker-compose up --build` levanta sin errores en equipo limpio.

## Martha — Documentacion formal
- [ ] Existe `API_CONTRACT.md` con los 5 endpoints documentados.
- [ ] Los campos del contrato coinciden con el modelo real (`emp_no`, `birth_date`, `first_name`, `last_name`, `gender`, `hire_date`).
- [ ] Los codigos HTTP del contrato coinciden con el backend corregido.
- [ ] Existe `CHANGELOG.md` con todos los cambios del equipo registrados.
- [ ] `README.md` tiene el bloque de codigo cerrado correctamente.
- [ ] `README.md` incluye seccion de Requisitos previos, Ejemplos de uso y enlace a `DEPLOY.md`.

## Frida — Interfaz grafica del cliente Python
- [ ] Existe ventana principal con tabla `Treeview` mostrando empleados.
- [ ] Boton Refrescar carga los datos desde la API.
- [ ] Boton Buscar por ID consulta un empleado especifico.
- [ ] Boton Nuevo empleado abre formulario con los 6 campos.
- [ ] Boton Editar pre-rellena el formulario con datos del registro seleccionado.
- [ ] Boton Eliminar pide confirmacion antes de borrar.
- [ ] Los errores de conexion se muestran en la interfaz (no crashea silenciosamente).
- [ ] Existe `requirements.txt` con `requests>=2.31.0`.

## Pablo — api_client.py + Pruebas bash + GitHub Actions
- [ ] Existe `cliente_python/api_client.py` con las 5 funciones (obtener_empleados, obtener_empleado, crear_empleado, actualizar_empleado, eliminar_empleado).
- [ ] `api_client.py` fue compartido con Frida e integrado en la UI.
- [ ] Existe `tests/test_api.sh` con los 8 casos de prueba (PASS/FAIL).
- [ ] El script retorna exit code 1 si alguna prueba falla.
- [ ] El script se ejecuta localmente sin errores (`bash tests/test_api.sh`).
- [ ] Existe `.github/workflows/tests.yml` configurado.
- [ ] El workflow levanta los servicios con `docker-compose.test.yml`.
- [ ] El workflow publica el resumen de resultados en la pestana Summary de GitHub Actions.
- [ ] El workflow sube el log como artefacto descargable.
- [ ] El workflow falla el job si hay pruebas en FAIL.
- [ ] El workflow se ejecuto al menos una vez en el repositorio de GitHub.

## Integracion final
- [ ] Cliente Python se conecta a la API corriendo en Docker.
- [ ] Flujo completo CRUD verificado desde la UI (Crear, Leer, Actualizar, Borrar).
- [ ] Prueba en equipos separados en red de laboratorio.
- [ ] GitHub Actions muestra ejecucion exitosa en el repositorio.
- [ ] Toda la documentacion entregada esta alineada al comportamiento real del sistema.
