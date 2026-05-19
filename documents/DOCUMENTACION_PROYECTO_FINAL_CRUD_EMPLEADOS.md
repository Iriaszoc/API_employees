# Documento Maestro de Proyecto Final

## 1. Datos Generales
- Materia: Topicos para el Despliegue de Aplicaciones
- Tipo de proyecto: Sistema CRUD Cliente-Servidor
- Dominio: Gestion de empleados
- Fecha limite de revision parcial: fin de mes de mayo de 2026
- Entrega final: Fin de semestre (integracion en equipos y en equipos de computo separados)

## 2. Objetivo del Documento
Definir de forma completa, clara y ejecutable los requisitos, alcance, arquitectura, contrato de API, plan de implementacion, pruebas y criterios de aceptacion del proyecto final.

Este documento transforma los lineamientos de clase en una especificacion de trabajo para reducir ambiguedad, evitar retrabajo y asegurar cumplimiento tecnico en el tiempo establecido.

## 2.1 Tecnologia principal del proyecto
- Backend: Go.
- Interfaz de usuario: Python.
- Contenedores: Docker y Docker Compose.
- Base de datos: MySQL.

Con esta definicion se separan claramente las responsabilidades: Go se encarga de la API y la logica del servidor, Python se encarga de la interfaz de escritorio que consume esa API, y Docker estandariza el despliegue del entorno con MySQL.

## 3. Estado del avance para fin de mes
Esta seccion resume lo que ya quedo definido para la revision parcial y lo que aun falta implementar antes de la entrega de avance.

### 3.1 Lo que ya esta definido
- El proyecto sera un CRUD de empleados con arquitectura cliente-servidor.
- La API respondera en JSON.
- Se usarán los metodos HTTP GET, POST, PUT y DELETE.
- El backend se implementara en Go.
- El cliente sera de escritorio en Python.
- La persistencia se manejara con MySQL dentro de contenedores Docker.
- El repositorio ya cuenta con un avance base de backend, docker-compose y carga inicial de datos.
- El documento ya incluye requisitos funcionales, no funcionales, arquitectura y contrato preliminar de API.

### 3.2 Lo que falta para la entrega de avance
- Completar y corregir el backend en Go con respuestas JSON consistentes y manejo correcto de codigos HTTP.
- Ajustar las rutas CRUD para que queden estables y documentadas.
- Revisar la capa de acceso a MySQL y dejarla parametrizada por variables de entorno.
- Desarrollar el cliente de escritorio en Python que consuma la API.
- Conectar cliente y servidor con pruebas reales dentro de Docker.
- Agregar validaciones de entrada y manejo de errores completos.
- Preparar un enlace de acceso al cliente para revision del profesor, si aplica.
- Revisar y pulir la documentacion final antes de enviarla por correo.

### 3.3 Lo que se enviara en el avance
- Documento de avance actualizado.
- Enlace al cliente funcional.
- Sin credenciales de acceso, porque el sistema no contempla login en esta entrega.
- Resumen breve de que ya funciona y que esta en desarrollo.

### 3.4 Evidencia de pruebas para la entrega
Si, conviene incluir los tests del programa como evidencia de avance. Lo ideal es enviar:
- capturas o salida de consola de las pruebas realizadas,
- casos de prueba que validen crear, leer, actualizar y eliminar,
- evidencia de que el cliente si consulta la API,
- y si es posible, un archivo o seccion donde se explique como ejecutar esas pruebas.

Esto ayuda al profesor a verificar que no solo existe la documentacion, sino tambien el funcionamiento real del sistema.

## 4. Contexto y Alcance
### 4.1 Contexto
El proyecto exige construir un sistema CRUD para el manejo de una base de datos de empleados, utilizando arquitectura Cliente-Servidor y comunicacion HTTP.

### 4.1.1 Minuta de lineamientos de clase
- El profesor indicó que la API debe responder en JSON.
- Se confirmó uso de métodos HTTP básicos: GET, POST, PUT y DELETE.
- Se solicitó manejo de códigos HTTP de éxito y error en cada operación.
- Se estableció que el dominio funcional es gestión de empleados con operaciones de manipulación de datos.
- Se descartó autenticación y seguridad avanzada para esta etapa (no se implementará login ni tokens en esta entrega).
- El backend deberá implementarse en Go (Java está prohibido por la cátedra; el equipo recomienda usar Go para entrega rápida).
- Se exigió cliente de escritorio (sin web ni móvil).
- Se fijó fecha de revisión parcial para fin de mes.
- El equipo acordó trabajar el frontend en Python y el backend en Go.
- El despliegue del proyecto se apoyara en Docker y Docker Compose.

### 4.2 Alcance incluido
- API REST (backend) con operaciones Create, Read, Update, Delete.
- Cliente de escritorio nativo que consume la API.
- Respuestas de la API en JSON.
- Manejo correcto de codigos HTTP.
- Persistencia de datos en base relacional MySQL dentro de contenedores.

### 4.3 Alcance excluido
- No se implementa autenticación, login, JWT, OAuth o control de acceso avanzado.
- No se implementan clientes web ni móviles.
- No se contempla microservicios ni arquitectura distribuida compleja.
- No se implementarán mecanismos de seguridad adicionales en esta fase; el alcance funcional es estrictamente el CRUD de empleados.
## 4. Restricciones Tecnicas Obligatorias
### 4.1 Backend
- Lenguaje obligatorio: Go (por requisición de la cátedra). Java está prohibido.
- Recomendación: usar Go 1.22+ y empaquetar la aplicación en una imagen Docker para despliegue reproducible.

### 4.2 Frontend
- Debe ser aplicacion de escritorio nativa.
- No se aceptan interfaces web ni aplicaciones moviles.
- Lenguaje libre (propuesta aprobada por equipo: Python con Tkinter o CustomTkinter).

### 4.3 Persistencia
- MySQL dentro de contenedores Docker.
- El esquema y los scripts de carga deben mantenerse sincronizados con el backend y el contrato de API.

### 4.4 Tiempo
- Proyecto con horizonte de 1 mes para llegar a una revision estable.

## 5. Requisitos Funcionales
### RF-01: Alta de empleado
El sistema debe permitir registrar un empleado nuevo mediante una solicitud HTTP POST al servidor.

### RF-02: Consulta de empleados
El sistema debe permitir listar todos los empleados (GET) y consultar por identificador unico (GET por id).

### RF-03: Actualizacion de empleado
El sistema debe permitir modificar datos de un empleado existente (PUT por id), incluyendo cambios de puesto y departamento.

### RF-04: Eliminacion de empleado
El sistema debe permitir borrar un empleado por identificador (DELETE por id).

### RF-05: Formato de respuesta
Toda respuesta del servidor debe serializarse en JSON.

### RF-06: Codigos de estado HTTP
El servidor debe retornar codigos HTTP estandar segun resultado de operacion:
- Exito general: 200
- Creacion: 201
- Solicitud invalida: 400
- Recurso no encontrado: 404
- Error interno: 500

### RF-07: Interaccion cliente-servidor
El cliente de escritorio debe consumir endpoints HTTP y representar resultados al usuario.

### RF-08: Separacion de responsabilidades
El cliente no debe ejecutar SQL directo. Toda manipulacion de datos se realiza por API.

## 6. Requisitos No Funcionales
### RNF-01: Simplicidad operativa
El sistema debe poder ejecutarse en un entorno de laboratorio sin dependencias complejas.

### RNF-02: Mantenibilidad
El codigo debe separarse por capas (rutas, logica de negocio, acceso a datos).

### RNF-03: Portabilidad backend
El servidor en Go debe compilarse como binario unico para simplificar despliegue.

### RNF-04: Respuesta consistente
Las respuestas JSON deben mantener una estructura homogenea en exito y error.

### RNF-05: Confiabilidad minima
Debe existir validacion basica de datos de entrada para evitar inserciones invalidas.

## 7. Casos de Uso Principales
### CU-01 Registrar empleado
1. Usuario abre cliente.
2. Captura datos del empleado.
3. Cliente envia POST /empleados.
4. API valida y guarda.
5. API responde JSON + codigo 201.
6. Cliente notifica exito.

### CU-02 Consultar lista de empleados
1. Usuario solicita listado.
2. Cliente envia GET /empleados.
3. API responde arreglo JSON con registros.
4. Cliente muestra tabla/lista.

### CU-03 Editar datos de empleado
1. Usuario selecciona empleado.
2. Modifica puesto/departamento/salario.
3. Cliente envia PUT /empleados/{id}.
4. API actualiza y responde 200.

### CU-04 Eliminar empleado
1. Usuario selecciona empleado.
2. Confirma borrado.
3. Cliente envia DELETE /empleados/{id}.
4. API elimina y responde 200.

## 8. Arquitectura Propuesta
Arquitectura de 3 componentes:
1. Cliente de escritorio Python (UI + consumo HTTP).
2. API REST en Go (controlador de reglas CRUD).
3. Base de datos MySQL dentro de contenedores Docker (persistencia en volumen).

Flujo:
1. UI captura accion del usuario.
2. Cliente transforma accion a request HTTP JSON.
3. API procesa solicitud y opera sobre BD.
4. API devuelve status code + payload JSON.
5. Cliente actualiza interfaz.

Implementación en contenedores:
- El backend, el cliente (opcionalmente empaquetado) y la base de datos pueden orquestarse con `docker-compose.yml` en la raíz del proyecto. Esto facilita reproducibilidad entre laptops y la demo en red.

## 9. Diseno Tecnico del Backend (Go)
### 9.1 Stack sugerido
- Lenguaje: Go 1.22+
- HTTP: net/http
- Router: net/http o chi (opcional)
- Driver MySQL: github.com/go-sql-driver/mysql
- Serializacion JSON: encoding/json

### 9.2 Estructura sugerida
La estructura actual del repositorio es plana (un solo `main.go`). Como mejora recomendada para la entrega final:
```text
API_employees/
  main.go                  <- API actual (handlers, rutas y DB en un solo archivo)
  go.mod
  go.sum
  Dockerfile
  docker-compose.yml
  init-db/
    employees.sql          <- Schema de MySQL
    *.dump                 <- Datos de 300,024 empleados
  cliente_python/          <- A crear por Frida
    main.py
    api_client.py
    ui.py
    requirements.txt
  tests/                   <- A crear por Pablo
    test_api.sh
  .github/workflows/       <- A crear por Pablo
    tests.yml
```

### 9.3 Modelo de datos empleado
Campos minimos recomendados:
- id (integer, primary key, autoincrement)
- numero_empleado (text, unico)
- nombre (text, requerido)
- apellido (text, requerido)
- puesto (text, requerido)
- departamento (text, requerido)
- salario (real, requerido, mayor que 0)
- fecha_ingreso (text/date, requerido)
- activo (integer/boolean, default 1)

Nota: el avance actual del repo usa el esquema base de `employees` con campos como `emp_no`, `birth_date`, `first_name`, `last_name`, `gender` y `hire_date`. Si se mantiene ese dataset, el contrato del cliente y la API deben usar esos nombres; si se migra a un CRUD propio de empleados, se debe crear un esquema nuevo y documentarlo antes de codificar el frontend.

### 9.4 Schema real del proyecto (MySQL)
El archivo `init-db/employees.sql` contiene el schema real cargado en Docker. La tabla principal usada por la API es:
```sql
-- Tabla principal usada por todos los endpoints
CREATE TABLE employees (
    emp_no      INT             NOT NULL,
    birth_date  DATE            NOT NULL,
    first_name  VARCHAR(14)     NOT NULL,
    last_name   VARCHAR(16)     NOT NULL,
    gender      ENUM ('M','F')  NOT NULL,
    hire_date   DATE            NOT NULL,
    PRIMARY KEY (emp_no)
);
```
El dataset inicial contiene 300,024 registros cargados desde los archivos `*.dump` en `init-db/`.

## 10. Contrato de API REST
Base URL local sugerida: `http://localhost:8080`

### 10.1 Estructura de respuesta estandar
Exito:
```json
{
  "status": "ok",
  "message": "Operacion exitosa",
  "data": {}
}
```

Error:
```json
{
  "status": "error",
  "message": "Descripcion del error",
  "error": {
    "code": "NOT_FOUND",
    "details": "No existe empleado con id=15"
  }
}
```

### 10.2 Endpoint: Crear empleado
- Metodo: POST
- Ruta: /empleados
- Request body:
```json
{
  "numero_empleado": "EMP-001",
  "nombre": "Juan",
  "apellido": "Perez",
  "puesto": "Analista",
  "departamento": "TI",
  "salario": 15000,
  "fecha_ingreso": "2026-04-20",
  "activo": true
}
```
- Respuestas:
  - 201 Created
  - 400 Bad Request (datos incompletos o invalidos)
  - 409 Conflict (numero_empleado duplicado)
  - 500 Internal Server Error

### 10.3 Endpoint: Listar empleados
- Metodo: GET
- Ruta: /empleados
- Respuestas:
  - 200 OK
  - 500 Internal Server Error

### 10.4 Endpoint: Obtener empleado por id
- Metodo: GET
- Ruta: /empleados/{id}
- Respuestas:
  - 200 OK
  - 404 Not Found
  - 500 Internal Server Error

### 10.5 Endpoint: Actualizar empleado
- Metodo: PUT
- Ruta: /empleados/{id}
- Request body: mismo esquema que alta (campos editables)
- Respuestas:
  - 200 OK
  - 400 Bad Request
  - 404 Not Found
  - 500 Internal Server Error

### 10.6 Endpoint: Eliminar empleado
- Metodo: DELETE
- Ruta: /empleados/{id}
- Respuestas:
  - 200 OK
  - 404 Not Found
  - 500 Internal Server Error

## 11. Diseno Tecnico del Cliente de Escritorio (Python)
### 11.1 Stack sugerido
- Python 3.11+
- Tkinter o CustomTkinter
- requests para consumo HTTP

### 11.2 Reglas de arquitectura del cliente
- No incluir SQL ni acceso directo a BD.
- Toda operacion se hace via requests a API.
- Implementar capa de cliente API separada de la capa UI.

### 11.3 Estructura sugerida
```text
/frontend
  /app/main.py
  /app/ui/main_window.py
  /app/ui/forms/empleado_form.py
  /app/services/api_client.py
  /app/models/empleado.py
  requirements.txt
```

### 11.4 Pantallas minimas
- Pantalla principal con tabla/lista de empleados.
- Formulario de alta/edicion.
- Dialogo de confirmacion para eliminar.
- Mensajes de error y exito legibles.

## 12. Validaciones Minimas
### 12.1 En cliente
- Campos obligatorios no vacios.
- Salario numerico mayor a 0.
- Confirmacion previa a borrado.

### 12.2 En servidor (obligatorio, aunque cliente valide)
- numero_empleado unico.
- Campos requeridos presentes.
- id valido en rutas parametrizadas.
- Respuesta 400 para payload invalido.

## 13. Plan de Implementacion (1 Mes)
### Semana 1 (20 abril - 26 abril)
- Definir estructura de repositorio.
- Crear esquema de BD.
- Implementar API base y endpoint de salud.
- Implementar POST y GET general.

### Semana 2 (27 abril - 3 mayo)
- Completar GET por id, PUT y DELETE.
- Estandarizar respuestas JSON y manejo de errores.
- Probar endpoints con cliente HTTP (curl/Postman).

### Semana 3 (4 mayo - 10 mayo)
- Construir interfaz de escritorio.
- Integrar cliente con endpoints.
- Gestionar mensajes de estado y errores.

### Semana 4 (11 mayo - fin de mes)
- Pruebas integrales.
- Correccion de defectos.
- Empaquetado y guia de ejecucion.
- Preparar demo de revision parcial.

## 14. Plan de Pruebas
### 14.1 Pruebas API
- Crear empleado valido -> 201.
- Crear empleado sin campo requerido -> 400.
- Consultar id inexistente -> 404.
- Actualizar id existente -> 200.
- Eliminar id inexistente -> 404.

### 14.2 Pruebas cliente
- Alta desde formulario refleja registro en lista.
- Edicion de departamento/puesto se persiste.
- Eliminacion pide confirmacion y actualiza vista.
- Manejo visual de errores del servidor.

### 14.3 Pruebas de integracion
- Cliente y servidor en maquinas separadas dentro de la red de laboratorio.
- Validar conectividad por IP y puerto.

### 14.4 Integracion continua (CI)
- El workflow se ubica en `.github/workflows/tests.yml`.
- En cada push o Pull Request el workflow:
  - Levanta MySQL y la API con `docker-compose.test.yml`.
  - Ejecuta el script `tests/test_api.sh` que reporta PASS/FAIL por caso.
  - Publica el resumen de resultados en la pestana Summary del workflow.
  - Sube el log completo como artefacto descargable.
  - Falla el job si algun caso reporta FAIL, bloqueando el merge del PR.
- La instruccion completa del workflow y el script bash se encuentran en `faltantes_y_reparto_equipo.md`, seccion "GitHub Actions".

## 15. Estrategia de Despliegue
### 15.1 Backend
- Build local (desarrollo):
```bash
go build -o servidor_empleados ./cmd/server
```
- Recomendado: construir una imagen Docker para despliegue y pruebas reproducibles:
```bash
# Desde la raíz del directorio /api
docker build -t proyecto-crud-api:latest .
```
- Orquestar con docker-compose (`docker-compose.yml` en la raíz) para levantar API + BD en un solo comando.

### 15.2 Frontend
- Ejecutar con Python instalado o empaquetar con PyInstaller.
- Se puede contenerizar el cliente para estandarizar entornos, pero no es obligatorio para la entrega parcial.
- Configurar `API_BASE_URL` en archivo de settings o mediante variable de entorno; evitar hardcodear URLs.

### 15.3 Configuracion recomendada
Variables de entorno del servidor:
- APP_PORT=8080
- DB_HOST=db
- DB_PORT=3306
- DB_USER=root
- DB_PASSWORD=password123
- DB_NAME=employees
- APP_ENV=dev

## 16. Criterios de Aceptacion
Se considera cumplido el proyecto cuando:
1. Existen endpoints CRUD funcionales sobre empleados.
2. Todas las respuestas de API son JSON.
3. Se usan codigos HTTP correctos segun caso.
4. El cliente de escritorio consume API sin SQL directo.
5. Se demuestra flujo completo Crear-Leer-Actualizar-Borrar.
6. Se presenta evidencia de pruebas basicas.
7. Se cumple la revision parcial en la fecha comprometida.

## 17. Riesgos y Mitigaciones
- Riesgo: Demora por curva de aprendizaje de backend nuevo.
  - Mitigacion: Usar Go y comenzar con vertical slice (POST+GET) en semana 1.

- Riesgo: Acoplamiento UI-datos.
  - Mitigacion: Capa api_client dedicada y contratos JSON estables.

- Riesgo: Fallas por diferencias de entorno.
  - Mitigacion: Configuracion por variables y checklist de despliegue.

- Riesgo: Manejo inconsistente de errores.
  - Mitigacion: Middleware o helper unico para respuestas de error.

## 18. Distribucion Real de Trabajo por Integrante

| Integrante | Tarea | Carga | Entregables principales |
|---|---|---|---|
| Roxana Irias Hernandez | Backend Go (handlers, validaciones, variables de entorno) + Docker/MySQL/Despliegue | Alta | `main.go`, `docker-compose.yml`, `docker-compose.test.yml`, `.env`, `DEPLOY.md` |
| Martha Elizabeth Castorena Rivera | Documentacion formal del proyecto | Media | `API_CONTRACT.md`, `CHANGELOG.md`, `README.md` actualizado |
| Frida Paulina Sepulveda Becerra | Interfaz grafica del cliente Python (Tkinter) | Media | `cliente_python/ui.py`, `main.py`, `requirements.txt` |
| Pablo Alberto Reyes Gutierrez | Capa HTTP del cliente + Script de pruebas bash + CI/CD GitHub Actions | Media | `cliente_python/api_client.py`, `tests/test_api.sh`, `.github/workflows/tests.yml` |

## 19. Checklist de Entrega Parcial (fin de mes)
- [ ] API CRUD completa operativa (5 endpoints respondiendo JSON).
- [ ] Cliente desktop funcional: lista, crea, edita y elimina desde la UI.
- [ ] MySQL inicia correctamente con los datos de 300,024 empleados.
- [ ] Documento tecnico actualizado y alineado al codigo real.
- [ ] Script `tests/test_api.sh` ejecuta sin errores.
- [ ] Workflow de GitHub Actions configurado en el repositorio.
- [ ] `DEPLOY.md` probado en equipo limpio.

## 20. Checklist de Entrega Final
- [ ] Integracion estable cliente-servidor en equipos separados (IP de red de laboratorio).
- [ ] Demo completa del flujo CRUD desde la UI de Python.
- [ ] Control de errores visible en la interfaz (mensajes claros al usuario).
- [ ] `api_client.py` separado de la capa visual (`ui.py`).
- [ ] GitHub Actions muestra pruebas en verde en el repositorio.
- [ ] Documentacion final consolidada: `API_CONTRACT.md`, `CHANGELOG.md`, `DEPLOY.md`, `README.md`.

## 21. Definicion de Terminado (DoD)
Una historia/tarea se considera terminada si:
1. Cumple funcionalidad objetivo.
2. Pasa pruebas manuales definidas.
3. Maneja errores esperados.
4. Esta integrada sin romper flujos existentes.
5. Queda documentada en este archivo.

## 22. Proximo Paso Inmediato Recomendado

El backend base ya existe. El orden de trabajo recomendado para terminar el proyecto:

1. **Roxana**: corregir `main.go` (JSON en updateEmpleado, 404 con cuerpo, validaciones en POST, variables de entorno) y actualizar `docker-compose.yml` con healthcheck y `.env`.
2. **Pablo**: implementar `api_client.py` en paralelo y preparar `tests/test_api.sh`.
3. **Frida**: construir `ui.py` con Tkinter; integrar `api_client.py` de Pablo cuando este disponible.
4. **Martha**: redactar `API_CONTRACT.md` y `README.md` con base en el codigo existente.
5. **Pablo**: configurar `.github/workflows/tests.yml` una vez que `docker-compose.test.yml` de Roxana este listo.
6. Prueba de integracion final: cliente + API en equipos separados en la red del laboratorio.

## 23. Matriz de Trazabilidad (Requisito -> API -> Prueba)
| Requisito | Endpoint principal | Resultado esperado | Caso de prueba |
|---|---|---|---|
| RF-01 Alta de empleado | POST /empleados | 201 con status ok | Crear empleado valido |
| RF-02 Consulta empleados | GET /empleados, GET /empleados/{id} | 200 con data | Listado y consulta por id |
| RF-03 Actualizacion | PUT /empleados/{id} | 200 con registro actualizado | Cambiar puesto/departamento |
| RF-04 Eliminacion | DELETE /empleados/{id} | 200 con confirmacion | Eliminar registro existente |
| RF-05 JSON obligatorio | Todos | Body en JSON | Verificacion de schema de respuesta |
| RF-06 Codigos HTTP | Todos | 200/201/400/404/500 segun caso | Suite manual de codigos |
| RF-07 Cliente consume API | Cliente desktop + API | Operacion completa desde UI | Prueba end-to-end |
| RF-08 Sin SQL en cliente | Capa services/api_client.py | Solo consumo HTTP | Revision de arquitectura |

## 24. Documentacion Complementaria
La documentacion operativa del equipo se encuentra en la carpeta `documentos_actualizados/`:

| Archivo | Contenido |
|---|---|
| `faltantes_y_reparto_equipo.md` | Guia paso a paso por integrante con codigo de referencia |
| `API_CONTRACT.md` | Contrato formal de cada endpoint (a crear por Martha) |
| `DEPLOY.md` | Guia de arranque con Docker (a crear por Roxana) |
| `CHANGELOG.md` | Registro de cambios del proyecto (a crear por Martha) |
| `checklist_revision.md` | Lista de verificacion para la revision parcial |
| `README.md` | Indice de la carpeta de documentacion |

Los archivos que se crearan en la raiz del repositorio (`reporox/API_employees/`) son:
- `API_CONTRACT.md` — Martha
- `DEPLOY.md` — Roxana
- `CHANGELOG.md` — Martha
- `tests/test_api.sh` — Pablo
- `.github/workflows/tests.yml` — Pablo
- `cliente_python/api_client.py` — Pablo
- `cliente_python/ui.py` — Frida
- `cliente_python/main.py` — Frida
- `cliente_python/requirements.txt` — Frida
