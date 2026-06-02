# 🏢 Sistema de Gestión de Empleados
### Presentación del Proyecto Final
**Materia:** Tópicos para el Despliegue de Aplicaciones

---

## ¿Qué construimos?

> Un sistema CRUD completo, **contenerizado con Docker**, que gestiona una base de datos real de **300,024 empleados** a través de una **API REST en Go** y una **interfaz gráfica en Python**.

---

## 🧩 Las 3 piezas del sistema

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   🖥️  Cliente Python          →    Interfaz visual      │
│          ↕  HTTP                                        │
│   🚀  API REST (Go)           →    Lógica del negocio   │
│          ↕  SQL                                         │
│   🗄️  MySQL (Docker)          →    300k empleados       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🐋 ¿Por qué Docker?

**Sin Docker** → "En mi máquina sí funciona" 😅

**Con Docker** → Mismo entorno en cualquier computadora, siempre.

```yaml
# Un solo comando levanta TODO el backend:
docker compose up -d
```

Docker nos da:
- ✅ Entorno **reproducible** (mismo MySQL, misma versión, mismas configs)
- ✅ **Aislamiento** entre servicios
- ✅ **Persistencia** de datos con volúmenes nombrados
- ✅ Red interna privada entre contenedores

---

## 🔌 Los 5 endpoints de la API

| Operación | Método | Ruta | ¿Qué hace? |
|---|---|---|---|
| **Listar** | `GET` | `/empleados` | Devuelve los primeros 30 registros |
| **Buscar** | `GET` | `/empleados/{id}` | Busca un empleado por número |
| **Crear** | `POST` | `/empleados` | Registra un nuevo empleado |
| **Actualizar** | `PUT` | `/empleados/{id}` | Modifica nombre y género |
| **Eliminar** | `DELETE` | `/empleados/{id}` | Borra el registro |

---

## 🔑 Decisión clave: el healthcheck

**El problema:** Docker iniciaba la API Go *antes* de que MySQL terminara de cargar.  
**Resultado:** La API crasheaba al no poder conectarse a la BD.

**La solución:**

```yaml
# En docker-compose.yml
db:
  healthcheck:
    test: ["CMD", "mysqladmin", "ping", ...]
    retries: 10
    start_period: 30s        # ← tiempo para que MySQL inicialice

api:
  depends_on:
    db:
      condition: service_healthy   # ← API espera a que DB esté SANA
```

> 💡 Este patrón es **fundamental** en arquitecturas de microservicios.

---

## 🐹 ¿Por qué Go para la API?

| Característica | Beneficio |
|---|---|
| Compilado a binario nativo | Imagen Docker muy ligera |
| Alta concurrencia nativa | Maneja múltiples peticiones sin bloqueos |
| Tipado estático | Menos errores en tiempo de ejecución |
| `database/sql` estándar | Conexión segura a MySQL sin ORM |

---

## 🐍 El cliente Python

**Tecnología:** CustomTkinter (interfaz gráfica moderna sobre tkinter)

**Diseño:**
- Modo oscuro con tema azul
- Tabla con scroll para ver los empleados
- Formularios modales para crear/editar
- Barra de estado en tiempo real (🟢 / 🔴)

**Separación de responsabilidades:**

```
main.py       →  Solo arranca la ventana principal
ui.py         →  Solo lógica de la interfaz visual
api_client.py →  Solo comunicación HTTP con la API
```

---

## 📦 El dataset

El dataset **MySQL Employees** es un estándar académico de pruebas:

- **300,024 empleados** con nombre, género, fecha de nacimiento y contratación
- Tablas relacionadas: departamentos, salarios, títulos, gerentes
- Datos **sintéticos** (no corresponden a personas reales)
- La carga inicial tarda ~5 min por el volumen de datos

---

## 🛠️ Cómo ejecutarlo

```powershell
# 1. Levantar backend (primera vez: esperar ~5 min)
docker compose up -d

# 2. Instalar dependencias Python (solo la primera vez)
pip install -r cliente_python/requirements.txt

# 3. Abrir la interfaz
python cliente_python/main.py
```

---

## 📊 Flujo completo de una operación

```
Usuario hace clic en "Nuevo Empleado"
         ↓
ui.py abre formulario modal (EmployeeForm)
         ↓
Usuario llena datos y presiona "Guardar"
         ↓
ui.py llama a api_client.crear_empleado(payload)
         ↓
api_client.py hace POST http://localhost:8080/empleados
         ↓
API Go recibe el request → valida JSON → ejecuta INSERT en MySQL
         ↓
MySQL confirma la inserción → Go devuelve 201 Created
         ↓
api_client.py devuelve el resultado a ui.py
         ↓
ui.py cierra el formulario y refresca la tabla
         ↓
Usuario ve el nuevo empleado en la lista ✅
```

---

## ✅ Resultados

| Métrica | Valor |
|---|---|
| Registros en base de datos | **300,024 empleados** |
| Endpoints funcionales | **5 / 5** |
| Servicios en Docker | **2** (db + api) |
| Tiempo de arranque (2ª vez) | **< 15 segundos** |
| Puerto de la API | **8080** |

---

## 🔮 Mejoras propuestas

1. **Autenticación JWT** — proteger los endpoints con tokens
2. **Paginación** — `/empleados?page=2&limit=50` en lugar de `LIMIT 30` fijo
3. **Dockerfile multi-stage** — separar la fase de build del runtime para imagen más pequeña
4. **Variables de entorno** — sacar las credenciales del código fuente a un `.env`
5. **CI/CD con GitHub Actions** — build y deploy automático al hacer push

---

*Proyecto desarrollado para la materia Tópicos para el Despliegue de Aplicaciones — 2026*
