import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from api_client import APIError, actualizar_empleado, crear_empleado, eliminar_empleado, listar_empleados, obtener_empleado


class EmployeeForm(tk.Toplevel):
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
            ("emp_no", "Numero de empleado"),
            ("birth_date", "Fecha de nacimiento (YYYY-MM-DD)"),
            ("first_name", "Nombre"),
            ("last_name", "Apellido"),
            ("gender", "Genero (M/F)"),
            ("hire_date", "Fecha de ingreso (YYYY-MM-DD)"),
        ]
        self.entries = {}
        container = ttk.Frame(self, padding=12)
        container.grid(row=0, column=0, sticky="nsew")

        for row, (key, label) in enumerate(fields):
            ttk.Label(container, text=label).grid(row=row, column=0, sticky="w", pady=4)
            entry = ttk.Entry(container, width=30)
            entry.grid(row=row, column=1, sticky="ew", pady=4)
            value = self.values.get(key, "")
            if value is not None:
                entry.insert(0, str(value))
            if key == "emp_no" and readonly_emp_no:
                entry.configure(state="readonly")
            self.entries[key] = entry

        button_row = ttk.Frame(container)
        button_row.grid(row=len(fields), column=0, columnspan=2, pady=(10, 0), sticky="e")
        ttk.Button(button_row, text="Guardar", command=self._save).grid(row=0, column=0, padx=4)
        ttk.Button(button_row, text="Cancelar", command=self.destroy).grid(row=0, column=1)

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


class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.master = master
        self.master.title("Clientes de empleados")
        self.master.geometry("920x560")
        self.pack(fill="both", expand=True)
        self._build_styles()
        self._build_ui()
        self.refresh_employees()

    def _build_styles(self):
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Status.TLabel", font=("Segoe UI", 10))

    def _build_ui(self):
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 10))
        ttk.Label(header, text="Sistema CRUD de Empleados", style="Header.TLabel").pack(side="left")
        ttk.Button(header, text="Refrescar", command=self.refresh_employees).pack(side="right")
        ttk.Button(header, text="Buscar por ID", command=self.search_employee).pack(side="right", padx=6)
        ttk.Button(header, text="Eliminar", command=self.delete_selected).pack(side="right", padx=6)
        ttk.Button(header, text="Editar", command=self.edit_selected).pack(side="right", padx=6)
        ttk.Button(header, text="Nuevo empleado", command=self.create_employee).pack(side="right", padx=6)

        columns = ("emp_no", "first_name", "last_name", "gender", "birth_date", "hire_date")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=18)
        headings = {
            "emp_no": "ID",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "gender": "Genero",
            "birth_date": "Nacimiento",
            "hire_date": "Ingreso",
        }
        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=130 if column != "emp_no" else 90, anchor="center")
        self.tree.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(in_=self.tree, relx=1.0, rely=0, relheight=1.0, anchor="ne")

        self.status_var = tk.StringVar(value="Listo")
        status = ttk.Label(self, textvariable=self.status_var, style="Status.TLabel")
        status.pack(fill="x", pady=(10, 0))

    def _set_status(self, message, is_error=False):
        self.status_var.set(message)
        style = self.master.style if hasattr(self.master, "style") else None
        if is_error:
            self.status_var.set(f"Error: {message}")

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
            self._set_status(f"Se cargaron {len(employees)} empleados")
        except Exception as exc:
            self._set_status(str(exc), is_error=True)
            messagebox.showerror("Error", str(exc))

    def search_employee(self):
        emp_no = simpledialog.askinteger("Buscar empleado", "Ingresa el numero de empleado:", parent=self.master)
        if emp_no is None:
            return
        try:
            employee = obtener_empleado(emp_no)
            self._clear_tree()
            if employee is None:
                self._set_status(f"No se encontro el empleado {emp_no}", is_error=True)
                messagebox.showinfo("Sin resultados", f"No se encontro el empleado {emp_no}")
                return
            self.tree.insert("", "end", values=self._employee_row(employee))
            self._set_status(f"Empleado {emp_no} cargado")
        except Exception as exc:
            self._set_status(str(exc), is_error=True)
            messagebox.showerror("Error", str(exc))

    def create_employee(self):
        def save(payload):
            try:
                crear_empleado(payload)
                form.destroy()
                self.refresh_employees()
            except APIError as exc:
                messagebox.showerror("Error", str(exc))

        form = EmployeeForm(self.master, "Nuevo empleado", on_save=save)

    def edit_selected(self):
        emp_no = self._selected_emp_no()
        if emp_no is None:
            messagebox.showinfo("Selecciona un registro", "Primero selecciona un empleado en la tabla.")
            return

        try:
            employee = obtener_empleado(emp_no)
            if employee is None:
                messagebox.showinfo("Sin resultados", f"No se encontro el empleado {emp_no}")
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
            except APIError as exc:
                messagebox.showerror("Error", str(exc))

        form = EmployeeForm(self.master, "Editar empleado", values=employee, readonly_emp_no=True, on_save=save)

    def delete_selected(self):
        emp_no = self._selected_emp_no()
        if emp_no is None:
            messagebox.showinfo("Selecciona un registro", "Primero selecciona un empleado en la tabla.")
            return
        if not messagebox.askyesno("Confirmar", f"Deseas eliminar el empleado {emp_no}?"):
            return
        try:
            eliminar_empleado(emp_no)
            self.refresh_employees()
            self._set_status(f"Empleado {emp_no} eliminado")
        except Exception as exc:
            self._set_status(str(exc), is_error=True)
            messagebox.showerror("Error", str(exc))
