# Parte Pablo Reyes — Entregables

Esta carpeta contiene los siguientes archivos:
- Cliente HTTP reutilizable (`cliente_python/api_client.py`)
- Scripts de pruebas automatizadas (`tests/test_api.sh`)
- Plantilla de `docker-compose.test.yml` para CI (en `API_employees/docker-compose.test.yml`)
- Plantilla de GitHub Actions (mover a `.github/workflows/tests.yml` en el repo) en `.github/workflows/tests.yml`
- Scripts de ejecución local y recolección de logs (`run_tests_local.sh`, `collect_logs.sh`)
- Documentación y evidencia (`evidencia_pruebas.md`)

## Instrucciones rápidas

1. Levantar servicios de prueba (desde la raíz del repo):

```bash
# Levantar el compose de pruebas definido en API_employees/docker-compose.test.yml
docker-compose -f API_employees/docker-compose.test.yml up --build -d
```

2. Ejecutar las pruebas locales:

```bash
./"parte Pablo Reyes"/run_tests_local.sh
```

3. Para integrar en GitHub Actions, mover `parte Pablo Reyes/.github/workflows/tests.yml` a `.github/workflows/tests.yml` en la raíz del repositorio y ajustar rutas si es necesario.
