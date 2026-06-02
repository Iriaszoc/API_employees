# Cliente Python (CustomTkinter)

Interfaz de escritorio moderna y funcional para consumir la API de empleados.
Esta versión cuenta con un diseño oscuro (Dark Mode), responsivo y profesional usando `customtkinter`.

## Requisitos
- Python 3.10 o superior.
- Paquete `requests`.
- Paquete `customtkinter`.
- La API del proyecto corriendo en `http://localhost:8080` (o configurar la variable `API_URL` como se indica en la carpeta `prueba_conexiones`).

## Instalación
```bash
pip install -r requirements.txt
```

## Ejecución
Si el servidor de la base de datos corre en tu máquina (Localhost):
```bash
python main.py
```
O si vas a conectarte a la máquina de Roxana, usa los scripts `.ps1` ubicados en la carpeta `prueba_conexiones`.

## Funcionalidades Integradas
- **Listar empleados** con tabla y barras de desplazamiento.
- **Buscar por ID** mediante cuadro de diálogo interactivo.
- **Crear empleado** con formulario en ventana flotante (Toplevel).
- **Editar empleado** precargando los datos actuales.
- **Eliminar empleado** con validación y confirmación.
- Soporte visual para errores HTTP y problemas de conexión a la API.
