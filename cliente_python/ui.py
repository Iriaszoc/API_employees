import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import customtkinter as ctk 

from api_client import (
    APIError,
    actualizar_empleado,
    crear_empleado,
    eliminar_empleado,
    listar_empleados,
    obtener_empleado,
)

# --- Configuración estética global ---
ctk.set_appearance_mode("Dark")       # Modos: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")    # Temas: "blue", "green", "dark-blue"


class EmployeeForm(ctk.CTkToplevel):
    def __init__(self, master, title, values=None, readonly_emp_no=False, on_save=None):
        super().__init__(master)
        self.title(title)
        self.resizable(False, False)
        self.on_save = on_save
        self.values = values or {}
        
        self._build_form(readonly_emp_no)
        self._center()
        self.transient(master)
        self.grab_set()

    def _build_form(self, readonly_emp_no):
        fields = [
            ("emp_no", "Número de empleado:"),
            ("birth_date", "Fecha de nacimiento (YYYY-MM-DD):"),
            ("first_name", "Nombre(s):"),
            ("last_name", "Apellido(s):"),
            ("gender", "Género (M/F):"),
            ("hire_date", "Fecha de ingreso (YYYY-MM-DD):"),
        ]
        self.entries = {}
        
        # Contenedor principal con esquinas redondeadas
        container = ctk.CTkFrame(self, corner_radius=15)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        for row, (key, label_text) in enumerate(fields):
            lbl = ctk.CTkLabel(container, text=label_text, font=("Segoe UI", 12, "bold"), anchor="w")
            lbl.grid(row=row, column=0, sticky="w", pady=8, padx=(10, 20))
            
            entry = ctk.CTkEntry(container, width=220, font=("Segoe UI", 12))
            entry.grid(row=row, column=1, sticky="ew", pady=8, padx=(0, 10))
            
            value = self.values.get(key, "")
            if value is not None:
                entry.insert(0, str(value))
            if key == "emp_no" and readonly_emp_no:
                entry.configure(state="readonly")
            self.entries[key] = entry

        # Botones del formulario
        button_row = ctk.CTkFrame(container, fg_color="transparent")
        button_row.grid(row=len(fields), column=0, columnspan=2, pady=(20, 10), sticky="e")
        
        btn_save = ctk.CTkButton(button_row, text="Guardar", command=self._save, width=100, font=("Segoe UI", 12, "bold"))
        btn_save.grid(row=0, column=0, padx=6)
        
        btn_cancel = ctk.CTkButton(button_row, text="Cancelar", fg_color="gray", hover_color="#555555", command=self.destroy, width=100)
        btn_cancel.grid(row=0, column=1, padx=6)

    def _center(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (width // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (height // 2)
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")

    def _save(self):
        payload = {key: entry.get().strip() for key, entry in self.entries.items()}
        if self.on_save:
            self.on_save(payload)


class App(ctk.CTkFrame):
    def __init__(self, master):
        self.master = master
        self.master.title("Dashboard Ejecutivo de Empleados")
        
        # Centrar la aplicación principal en pantalla de manera responsiva
        ancho, alto = 1000, 640
        x = (self.master.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.master.winfo_screenheight() // 2) - (alto // 2)
        self.master.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        super().__init__(master, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._build_ui()
        self._apply_treeview_theme()
        self.refresh_employees()

    def _apply_treeview_theme(self):
        """Estiliza la tabla interna nativa para que combine con el modo oscuro"""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        font=("Segoe UI", 11), 
                        rowheight=32, 
                        background="#2A2D2E", 
                        fieldbackground="#2A2D2E", 
                        foreground="#FFFFFF")
        style.configure("Treeview.Heading", 
                        font=("Segoe UI", 11, "bold"), 
                        background="#1F2122", 
                        foreground="#FFFFFF", 
                        relief="flat")
        style.map("Treeview", background=[("selected", "#1F6AA5")], foreground=[("selected", "#FFFFFF")])

    def _build_ui(self):
        # --- ENCABEZADO SUPERIOR MODERNO ---
        header = ctk.CTkFrame(self, height=70, corner_radius=10)
        header.pack(fill="x", pady=(0, 15))
        
        title_lbl = ctk.CTkLabel(header, text="👥 Panel de Empleados", font=("Segoe UI", 20, "bold"))
        title_lbl.pack(side="left", padx=20, pady=15)
        
        # Botones de Acción alineados de izquierda a derecha con diseño pulido
        ctk.CTkButton(header, text="➕ Nuevo Empleado", command=self.create_employee, width=140, font=("Segoe UI", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkButton(header, text="Editar", fg_color="#4A5568", hover_color="#2D3748", command=self.edit_selected, width=100).pack(side="left", padx=5)
        ctk.CTkButton(header, text="Eliminar", fg_color="#991B1B", hover_color="#7F1D1D", command=self.delete_selected, width=100).pack(side="left", padx=5)
        ctk.CTkButton(header, text="Buscar por ID", fg_color="#4A5568", hover_color="#2D3748", command=self.search_employee, width=120).pack(side="left", padx=5)
        
        ctk.CTkButton(header, text="Refrescar", fg_color="transparent", border_width=1, border_color="#1F6AA5", command=self.refresh_employees, width=110).pack(side="right", padx=20)

        # --- ÁREA CENTRAL: TABLA CONTENEDORA ---
        table_container = ctk.CTkFrame(self, corner_radius=10)
        table_container.pack(fill="both", expand=True)

        columns = ("emp_no", "first_name", "last_name", "gender", "birth_date", "hire_date")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings")
        
        headings = {
            "emp_no": "No. Empleado",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "gender": "Género",
            "birth_date": "F. Nacimiento",
            "hire_date": "F. Ingreso",
        }
        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=140 if column != "emp_no" else 110, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True, padx=15, pady=15)

        # Barra de desplazamiento integrada
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=15)

        # --- BARRA DE ESTADO INFERIOR DINÁMICA ---
        self.status_var = tk.StringVar(value="🟢 Sistema en línea y listo.")
        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, font=("Segoe UI", 12), text_color="#A0AEC0", anchor="w")
        self.status_label.pack(fill="x", pady=(10, 0), padx=5)

    def _set_status(self, message, is_error=False):
        if is_error:
            self.status_var.set(f"🔴 Error: {message}")
            self.status_label.configure(text_color="#F87171")
        else:
            self.status_var.set(f"🍏 {message}")
            self.status_label.configure(text_color="#34D399")

    def _selected_emp_no(self):
        selection = self.tree.selection()
        if not selection:
            return None
        values = self.tree.item(selection[0], "values")
        if not values:
            return None
        return int(values[0])

    def _employee_row(self, employee):
        return (
            employee.get("emp_no", ""),
            employee.get("first_name", ""),
            employee.get("last_name", ""),
            employee.get("gender", ""),
            employee.get("birth_date", ""),
            employee.get("hire_date", ""),
        )

    def _clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def refresh_employees(self):
        try:
            employees = listar_empleados()
            self._clear_tree()
            for employee in employees:
                self.tree.insert("", "end", values=self._employee_row(employee))
            self._set_status(f"Se cargaron exitosamente {len(employees)} empleados.")
        except Exception as exc:
            self._set_status(str(exc), is_error=True)
            messagebox.showerror("Error de Comunicación", f"No se pudo conectar con la API:\n{str(exc)}")

    def search_employee(self):
        emp_no = simpledialog.askinteger("Buscar Empleado", "Ingresa el número de empleado único:", parent=self.master)
        if emp_no is None:
            return
        try:
            employee = obtener_empleado(emp_no)
            self._clear_tree()
            if employee is None:
                self._set_status(f"No se encontró el ID {emp_no}", is_error=True)
                messagebox.showinfo("Sin resultados", f"El empleado {emp_no} no existe.")
                return
            self.tree.insert("", "end", values=self._employee_row(employee))
            self._set_status(f"Ficha del empleado {emp_no} cargada.")
        except Exception as exc:
            self._set_status(str(exc), is_error=True)
            messagebox.showerror("Error", str(exc))

    def create_employee(self):
        def save(payload):
            try:
                crear_empleado(payload)
                form.destroy()
                self.refresh_employees()
                self._set_status("Nuevo empleado registrado correctamente.")
            except APIError as exc:
                messagebox.showerror("Error de Validación", str(exc))

        form = EmployeeForm(self.master, "Añadir Nuevo Empleado", on_save=save)

    def edit_selected(self):
        emp_no = self._selected_emp_no()
        if emp_no is None:
            messagebox.showinfo("Registro Requerido", "Por favor, selecciona un empleado en la tabla.")
            return

        try:
            employee = obtener_empleado(emp_no)
            if employee is None:
                messagebox.showinfo("No Encontrado", f"No se encontró el empleado {emp_no}")
                return
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        def save(payload):
            try:
                actualizar_empleado(emp_no, {
                    "first_name": payload.get("first_name", ""),
                    "last_name": payload.get("last_name", ""),
                    "gender": payload.get("gender", ""),
                })
                form.destroy()
                self.refresh_employees()
                self._set_status(f"Datos del empleado {emp_no} actualizados.")
            except APIError as exc:
                messagebox.showerror("Error al Actualizar", str(exc))

        form = EmployeeForm(self.master, f"Modificar Empleado #{emp_no}", values=employee, readonly_emp_no=True, on_save=save)

    def delete_selected(self):
        emp_no = self._selected_emp_no()
        if emp_no is None:
            messagebox.showinfo("Registro Requerido", "Selecciona un empleado para eliminar.")
            return
        if not messagebox.askyesno("Confirmar Eliminación", f"¿Deseas eliminar permanentemente al empleado #{emp_no}?"):
            return
        try:
            eliminar_empleado(emp_no)
            self.refresh_employees()
            self._set_status(f"El empleado #{emp_no} fue removido.")
        except Exception as exc:
            self._set_status(str(exc), is_error=True)
            messagebox.showerror("Error al Eliminar", str(exc))