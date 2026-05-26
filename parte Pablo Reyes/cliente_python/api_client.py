import os
import requests

BASE_URL = os.getenv("API_URL", "http://localhost:8080")

class APIError(Exception):
    pass


def obtener_empleados():
    """Devuelve la lista de empleados (array JSON)."""
    r = requests.get(f"{BASE_URL}/empleados")
    if r.status_code != 200:
        raise APIError(f"GET /empleados -> {r.status_code}: {r.text}")
    return r.json()


def obtener_empleado(emp_no):
    """Devuelve un empleado por id o None si no existe."""
    r = requests.get(f"{BASE_URL}/empleados/{emp_no}")
    if r.status_code == 404:
        return None
    if r.status_code != 200:
        raise APIError(f"GET /empleados/{emp_no} -> {r.status_code}: {r.text}")
    return r.json()


def crear_empleado(data: dict):
    """Crea un empleado. `data` debe contener las claves requeridas."""
    r = requests.post(f"{BASE_URL}/empleados", json=data)
    if r.status_code not in (200, 201):
        raise APIError(f"POST /empleados -> {r.status_code}: {r.text}")
    return r.json()


def actualizar_empleado(emp_no, data: dict):
    """Actualiza campos de un empleado."""
    r = requests.put(f"{BASE_URL}/empleados/{emp_no}", json=data)
    if r.status_code not in (200, 201, 204):
        raise APIError(f"PUT /empleados/{emp_no} -> {r.status_code}: {r.text}")
    # Si el endpoint devuelve JSON lo retornamos, si no, devolvemos un mensaje simple
    if r.content:
        try:
            return r.json()
        except Exception:
            return {"message": r.text}
    return {"message": "ok"}


def eliminar_empleado(emp_no):
    """Elimina un empleado. Devuelve True si se eliminó, False si no existía."""
    r = requests.delete(f"{BASE_URL}/empleados/{emp_no}")
    if r.status_code in (200, 204):
        return True
    if r.status_code == 404:
        return False
    raise APIError(f"DELETE /empleados/{emp_no} -> {r.status_code}: {r.text}")
