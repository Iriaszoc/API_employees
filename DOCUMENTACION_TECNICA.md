# 📘 Documentación Técnica — Sistema de Gestión de Empleados

> **Materia:** Tópicos para el Despliegue de Aplicaciones  
> **Proyecto Final**  
> **Tecnologías:** Go · MySQL · Docker · Python (CustomTkinter)

---

## 1. Descripción General

Este proyecto es un sistema CRUD completo para la gestión de empleados. Consta de tres capas bien diferenciadas:

| Capa | Tecnología | Rol |
|---|---|---|
| **Base de datos** | MySQL 8.0 (Docker) | Almacena 300,024 registros del dataset *Employees* |
| **API REST** | Go + Gorilla Mux (Docker) | Expone endpoints HTTP para el CRUD |
| **Cliente de escritorio** | Python + CustomTkinter | Interfaz gráfica que consume la API |

Todo el backend (MySQL + API Go) corre dentro de contenedores Docker, garantizando portabilidad y aislamiento. El cliente Python se ejecuta directamente en el host.

---

## 2. Arquitectura del Sistema

```
┌─────────────────────────────────────────────┐
│              HOST (Windows)                 │
│                                             │
│   ┌─────────────────────────────────────┐   │
│   │         Docker Network              │   │
│   │                                     │   │
│   │  ┌──────────────┐  ┌─────────────┐  │   │
│   │  │  api (Go)    │  │  db (MySQL) │  │   │
│   │  │  :8080       │──│  :3306      │  │   │
│   │  └──────────────┘  └─────────────┘  │   │
│   └────────────┬────────────────────────┘   │
│                │ localhost:8080              │
│   ┌────────────▼────────────────────────┐   │
│   │   Cliente Python (CustomTkinter)    │   │
│   └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

La API Go se comunica con MySQL usando el hostname interno `db` dentro de la red Docker. El cliente Python accede a la API desde fuera del contenedor vía `http://localhost:8080`.

---

## 3. Estructura del Proyecto

```
API_employees/
├── Dockerfile                  # Imagen para compilar y correr la API Go
├── docker-compose.yml          # Orquestación de los servicios db y api
├── go.mod                      # Módulo Go con dependencias declaradas
├── go.sum                      # Hashes de integridad de dependencias
├── main.go                     # Código fuente de la API REST en Go
│
├── init-db/                    # Scripts SQL que MySQL ejecuta al iniciar
│   ├── employees.sql           # DDL: crea las tablas de la BD
│   ├── load_employees.dump     # ~300k registros de empleados
│   ├── load_departments.dump
│   ├── load_dept_emp.dump
│   ├── load_dept_manager.dump
│   ├── load_salaries1.dump
│   ├── load_salaries2.dump
│   ├── load_salaries3.dump
│   └── load_titles.dump
│
└── cliente_python/             # Aplicación de escritorio
    ├── main.py                 # Punto de entrada
    ├── ui.py                   # Ventanas, formularios y tabla (CustomTkinter)
    ├── api_client.py           # Capa de comunicación HTTP con la API
    └── requirements.txt        # Dependencias Python
```

---

## 4. Base de Datos

### 4.1 Motor y dataset

- **Motor:** MySQL 8.0 ejecutándose en Docker
- **Dataset:** [MySQL Employees Sample Database](https://github.com/datacharmer/test_db) — datos sintéticos, no corresponden a personas reales
- **Registros:** 300,024 empleados

### 4.2 Esquema de tablas (DDL simplificado)

```sql
CREATE TABLE employees (
    emp_no      INT             NOT NULL,   -- PK
    birth_date  DATE            NOT NULL,
    first_name  VARCHAR(14)     NOT NULL,
    last_name   VARCHAR(16)     NOT NULL,
    gender      ENUM('M','F')   NOT NULL,
    hire_date   DATE            NOT NULL,
    PRIMARY KEY (emp_no)
);

-- Tablas relacionadas (solo estructura, no expuestas por la API)
CREATE TABLE departments   ( dept_no CHAR(4) PK, dept_name VARCHAR(40) );
CREATE TABLE dept_emp      ( emp_no INT, dept_no CHAR(4), from_date DATE, to_date DATE );
CREATE TABLE dept_manager  ( emp_no INT, dept_no CHAR(4), from_date DATE, to_date DATE );
CREATE TABLE titles        ( emp_no INT, title VARCHAR(50), from_date DATE, to_date DATE );
CREATE TABLE salaries      ( emp_no INT, salary INT, from_date DATE, to_date DATE );
```

### 4.3 Inicialización automática

Docker ejecuta automáticamente todos los archivos dentro de `init-db/` al crear el volumen por primera vez. El orden lo controla `employees.sql` usando `SOURCE`:

```sql
source /docker-entrypoint-initdb.d/load_departments.dump;
source /docker-entrypoint-initdb.d/load_employees.dump;
-- ... etc
```

> ⚠️ La carga completa puede tardar **5-10 minutos** la primera vez.

---

## 5. API REST (Go)

### 5.1 Dependencias (`go.mod`)

```
github.com/gorilla/mux       v1.8.1   -- Router HTTP
github.com/go-sql-driver/mysql v1.10.0 -- Driver MySQL para database/sql
```

### 5.2 Modelo de datos

```go
type Empleado struct {
    ID        int    `json:"emp_no"`
    BirthDate string `json:"birth_date"`
    FirstName string `json:"first_name"`
    LastName  string `json:"last_name"`
    Gender    string `json:"gender"`
    HireDate  string `json:"hire_date"`
}
```

### 5.3 Endpoints CRUD

| Método | Ruta | Descripción | Cuerpo |
|---|---|---|---|
| `GET` | `/empleados` | Lista los primeros 30 empleados | — |
| `GET` | `/empleados/{id}` | Obtiene un empleado por `emp_no` | — |
| `POST` | `/empleados` | Crea un nuevo empleado | JSON `Empleado` |
| `PUT` | `/empleados/{id}` | Actualiza `first_name`, `last_name`, `gender` | JSON parcial |
| `DELETE` | `/empleados/{id}` | Elimina el empleado indicado | — |

### 5.4 Ejemplos de uso

```bash
# Listar empleados
GET http://localhost:8080/empleados

# Buscar por ID
GET http://localhost:8080/empleados/10001

# Crear empleado
POST http://localhost:8080/empleados
Content-Type: application/json
{
  "emp_no": 999999,
  "birth_date": "1995-05-20",
  "first_name": "Juan",
  "last_name": "Pérez",
  "gender": "M",
  "hire_date": "2024-01-15"
}

# Actualizar
PUT http://localhost:8080/empleados/999999
Content-Type: application/json
{ "first_name": "Juan Carlos", "last_name": "Pérez", "gender": "M" }

# Eliminar
DELETE http://localhost:8080/empleados/999999
```

### 5.5 Conexión a la base de datos

```go
dsn := "root:password123@tcp(db:3306)/employees"
db, err = sql.Open("mysql", dsn)
```

El hostname `db` es resuelto automáticamente por la red interna de Docker Compose.

---

## 6. Contenedorización (Docker)

### 6.1 Dockerfile (API Go)

```dockerfile
FROM golang:1.24-alpine          # Imagen base ligera con Go 1.24

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download              # Descarga dependencias (cacheado por Docker)

COPY . .
RUN go mod tidy && go build -o main .   # Compila el binario

EXPOSE 8080
CMD ["./main"]
```

**Estrategia de capas:** Se copian primero `go.mod` y `go.sum` para aprovechar el caché de Docker. Solo se recompila si el código fuente cambia.

### 6.2 docker-compose.yml

```yaml
services:
  db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_DATABASE: employees
      MYSQL_ROOT_PASSWORD: password123
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql          # Persistencia de datos
      - ./init-db:/docker-entrypoint-initdb.d  # Scripts de inicialización
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-ppassword123"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 30s                 # Da tiempo a MySQL para iniciar

  api:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      db:
        condition: service_healthy      # API espera a que MySQL esté listo
    restart: on-failure

volumes:
  db_data:                              # Volumen nombrado para persistencia
```

**Punto clave:** El `healthcheck` en `db` + `condition: service_healthy` en `api` garantiza que la API Go no intente conectarse a MySQL antes de que esté completamente listo. Sin esto, el contenedor de Go crashea al arrancar.

---

## 7. Cliente Python

### 7.1 Dependencias

```
requests>=2.31.0       # Peticiones HTTP a la API
customtkinter>=5.2.0   # Widgets modernos sobre tkinter
```

### 7.2 Capa de comunicación (`api_client.py`)

Funciones puras que abstraen las llamadas HTTP. Cada función lanza `APIError` si la respuesta no es exitosa:

```python
BASE_URL = os.getenv("API_URL", "http://localhost:8080")

def listar_empleados() -> List[Dict]:  # GET /empleados
def obtener_empleado(emp_no: int) -> Optional[Dict]:  # GET /empleados/{id}
def crear_empleado(payload: Dict) -> Dict:  # POST /empleados
def actualizar_empleado(emp_no: int, payload: Dict) -> Dict:  # PUT /empleados/{id}
def eliminar_empleado(emp_no: int) -> None:  # DELETE /empleados/{id}
```

La URL base es configurable vía variable de entorno `API_URL`, lo que facilita apuntar a distintos ambientes.

### 7.3 Interfaz gráfica (`ui.py`)

- **Modo oscuro** con tema azul (CustomTkinter)
- **Tabla** (`ttk.Treeview`) estilizada para combinar con el modo oscuro
- **Barra de estado** inferior con indicadores visuales (🟢/🔴)
- **Formulario modal** (`EmployeeForm`) reutilizable tanto para crear como editar

---

## 8. Despliegue y Ejecución

### Prerrequisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo
- Python 3.9+ instalado

### Paso 1 — Levantar el backend

```powershell
cd API_employees
docker compose up -d
```

La primera vez descarga imágenes y carga ~300k registros. Puede tardar varios minutos.

### Paso 2 — Instalar dependencias Python

```powershell
cd cliente_python
pip install -r requirements.txt
```

### Paso 3 — Ejecutar el cliente

```powershell
python main.py
```

### Comandos útiles

```powershell
# Ver estado de los contenedores
docker compose ps

# Ver logs en tiempo real
docker compose logs -f

# Apagar los contenedores (conserva los datos)
docker compose down

# Apagar y BORRAR datos (elimina el volumen)
docker compose down -v
```

---

## 9. Correcciones Aplicadas al Proyecto Original

Durante la preparación para ejecución local se detectaron y corrigieron los siguientes problemas:

| # | Archivo | Problema original | Solución aplicada |
|---|---|---|---|
| 1 | `Dockerfile` | `golang:1.26-alpine` no existe en Docker Hub | Cambiado a `golang:1.24-alpine` |
| 2 | `go.mod` | `go 1.26.3` es una versión inválida | Cambiado a `go 1.24` |
| 3 | `Dockerfile` | `go build` fallaba porque Go 1.24 exige `go mod tidy` previo | Agregado `go mod tidy &&` antes del build |
| 4 | `docker-compose.yml` | Sin healthcheck: la API Go arrancaba antes que MySQL y crasheaba | Agregado `healthcheck` en `db` + `condition: service_healthy` en `api` |
| 5 | `docker-compose.yml` | Atributo `version` obsoleto genera warning en Docker Compose moderno | Eliminado el atributo `version: '3.8'` |

---

## 10. Posibles Mejoras Futuras

- [ ] Paginación real en `GET /empleados` (actualmente `LIMIT 30` fijo)
- [ ] Autenticación con JWT en la API
- [ ] Variables de entorno para credenciales (en lugar de hardcoded en el DSN)
- [ ] Tests unitarios para los handlers Go
- [ ] Dockerfile multi-stage para reducir el tamaño de la imagen final
- [ ] Búsqueda por nombre en el cliente Python
