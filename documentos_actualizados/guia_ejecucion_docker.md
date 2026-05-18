# Guia de ejecucion con Docker

## Requisitos
- Docker Desktop instalado.
- Docker Compose disponible.

## Arranque
Desde la carpeta del proyecto donde esta `docker-compose.yml`:

```bash
docker-compose up --build
```

## Servicio esperado
- Base de datos MySQL en un contenedor.
- API en Go en `http://localhost:8080`.

## Verificacion rapida
1. Esperar a que MySQL termine de iniciar.
2. Confirmar que la API ya responde.
3. Probar:

```bash
curl http://localhost:8080/empleados
```

## Carga inicial
Al iniciar por primera vez, el contenedor de MySQL carga el esquema y los datos de empleados desde `init-db`.

## Apagado
```bash
docker-compose down
```

## Reinicio limpio
Si se quiere volver a cargar la base desde cero:
1. Detener contenedores.
2. Borrar volumen de MySQL.
3. Levantar de nuevo con `docker-compose up --build`.

## Nota
La ejecucion esta pensada para el avance actual del repositorio, no para una base nueva distinta.
