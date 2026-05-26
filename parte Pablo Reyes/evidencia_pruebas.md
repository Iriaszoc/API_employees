# Evidencia de pruebas — Pablo Reyes

Esta guía explica cómo generar evidencia de ejecución de las pruebas automatizadas.

1) Levantar servicios de prueba:

```bash
docker-compose -f API_employees/docker-compose.test.yml up --build -d
```

2) Ejecutar las pruebas:

```bash
./"parte Pablo Reyes"/run_tests_local.sh
```

3) Guardar logs:

```bash
./"parte Pablo Reyes"/collect_logs.sh
```

4) Ejemplos de comandos `curl` útiles para comprobar manualmente:

- Listar empleados:

```bash
curl http://localhost:8080/empleados
```

- Consultar empleado por id:

```bash
curl http://localhost:8080/empleados/10001
```

- Crear empleado (ejemplo):

```bash
curl -X POST -H "Content-Type: application/json" -d '{"emp_no":999999, "birth_date":"1990-01-01", "first_name":"Pablo", "last_name":"Reyes", "gender":"M", "hire_date":"2026-05-20"}' http://localhost:8080/empleados
```

- Actualizar empleado:

```bash
curl -X PUT -H "Content-Type: application/json" -d '{"first_name":"PabloU", "last_name":"Reyes", "gender":"M"}' http://localhost:8080/empleados/999999
```

- Eliminar empleado:

```bash
curl -X DELETE http://localhost:8080/empleados/999999
```

5) Guardar la salida de los tests como evidencia (copiar la salida del script, y adjuntar `logs_*.txt`).
