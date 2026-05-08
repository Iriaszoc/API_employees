# 🏢 Sistema de Gestión de Empleados (API REST + Docker)

Este proyecto es una API robusta desarrollada en **Go** que se conecta a una base de datos **MySQL** con más de **300,000 registros**. Todo el entorno está contenedorizado con **Docker** para facilitar el despliegue.

## 🚀 Cómo ponerlo en marcha

Para correr el proyecto en tu máquina local, solo necesitas tener Docker Desktop instalado y ejecutar:

```bash
docker-compose up --build


⚠️ Notas importantes sobre la base de datos
Al encender el sistema por primera vez, Docker cargará automáticamente el dataset de empleados (300,024 registros).

Tiempo de espera: La carga puede tardar entre 5 y 10 minutos dependiendo de tu equipo.

Señal de éxito: El sistema está listo cuando la terminal muestre: db-1 | ready for connections y api-1 | Servidor Go en puerto 8080....


Método,Endpoint,Descripción
GET,/empleados,Obtiene los primeros 10 empleados (Paginación básica).
GET,/empleados/{id},Busca un empleado específico por su emp_no.
POST,/empleados,Crea un nuevo registro de empleado.
PUT,/empleados/{id},Actualiza los datos de un empleado existente.
DELETE,/empleados/{id},Elimina un registro de la base de datos.