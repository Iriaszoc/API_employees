# Contrato API actual

## Base URL
`http://localhost:8080`

## Modelo de empleado usado por el avance
```json
{
  "emp_no": 10001,
  "birth_date": "1953-09-02",
  "first_name": "Georgi",
  "last_name": "Facello",
  "gender": "M",
  "hire_date": "1986-06-26"
}
```

## Endpoints actuales

### GET /empleados
Obtiene una lista limitada de empleados.

Respuesta esperada:
- `200 OK`
- JSON con arreglo de registros.

Ejemplo:
```json
[
  {
    "emp_no": 10001,
    "birth_date": "1953-09-02",
    "first_name": "Georgi",
    "last_name": "Facello",
    "gender": "M",
    "hire_date": "1986-06-26"
  }
]
```

### GET /empleados/{id}
Busca un empleado por `emp_no`.

Respuestas:
- `200 OK` si existe.
- `404 Not Found` si no existe.

### POST /empleados
Crea un empleado.

Body esperado:
```json
{
  "emp_no": 99999,
  "birth_date": "1990-01-01",
  "first_name": "Ana",
  "last_name": "Lopez",
  "gender": "F",
  "hire_date": "2026-05-17"
}
```

### PUT /empleados/{id}
Actualiza datos de un empleado existente.

Body esperado:
```json
{
  "first_name": "Ana",
  "last_name": "Lopez",
  "gender": "F"
}
```

### DELETE /empleados/{id}
Elimina el empleado indicado por `emp_no`.

## Estado del contrato
Este contrato refleja lo que ya existe en el avance actual. Falta estandarizar:
- estructura de errores,
- formato uniforme de respuesta,
- validaciones por campo,
- y manejo consistente de codigos HTTP.

## Regla de uso
Si el backend cambia las columnas o las rutas, este archivo debe actualizarse antes de tocar el cliente.
