# Estado actual del avance

## Base tecnica ya existente
El repositorio clonado ya trae:
- API en Go.
- Dockerfile.
- docker-compose.yml.
- Base de datos MySQL.
- Script de inicializacion con la base `employees`.
- Rutas CRUD basicas para empleados.
- Documentacion tecnica minima del proyecto.

## Lo que ya funciona de forma general
- Levantamiento del entorno con Docker Compose.
- Conexion del backend a MySQL.
- Consulta de empleados.
- Creacion de empleados.
- Actualizacion de empleados.
- Eliminacion de empleados.

## Esquema que usa el avance actual
El backend actual trabaja sobre la tabla `employees` con campos:
- `emp_no`
- `birth_date`
- `first_name`
- `last_name`
- `gender`
- `hire_date`

## Lo que aun necesita ajuste
- Respuestas JSON homogéneas en todos los endpoints.
- Manejo formal de codigos HTTP.
- Validaciones de entrada mas estrictas.
- Limpieza de errores en update y delete.
- Cliente de escritorio en Python.
- Pruebas documentadas y evidencia para entrega.
- GitHub Actions o alguna automatizacion de verificacion.

## Observacion importante
Este avance no usa un modelo nuevo de empleados; usa la base `employees` ya cargada. Por eso toda nueva documentacion en esta carpeta debe hablar el mismo lenguaje que el backend actual.
