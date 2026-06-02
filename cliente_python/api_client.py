import os
from typing import Any, Dict, List, Optional

import requests

BASE_URL = os.getenv("API_URL", "http://192.168.219.185:8080").rstrip("/")
TIMEOUT = float(os.getenv("API_TIMEOUT", "8"))


class APIError(Exception):
    pass


def _request(method: str, path: str, **kwargs) -> requests.Response:
    response = requests.request(
        method,
        f"{BASE_URL}{path}",
        timeout=TIMEOUT,
        **kwargs,
    )
    return response


def listar_empleados() -> List[Dict[str, Any]]:
    response = _request("GET", "/empleados")
    if response.status_code != 200:
        raise APIError(f"GET /empleados -> {response.status_code}: {response.text}")
    data = response.json()
    if isinstance(data, list):
        return data
    raise APIError("La API no devolvio una lista valida de empleados")


def obtener_empleado(emp_no: int) -> Optional[Dict[str, Any]]:
    response = _request("GET", f"/empleados/{emp_no}")
    if response.status_code == 404:
        return None
    if response.status_code != 200:
        raise APIError(f"GET /empleados/{emp_no} -> {response.status_code}: {response.text}")
    data = response.json()
    if isinstance(data, dict):
        return data
    raise APIError("La API no devolvio un empleado valido")


def crear_empleado(payload: Dict[str, Any]) -> Dict[str, Any]:
    response = _request(
        "POST",
        "/empleados",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    if response.status_code not in (200, 201):
        raise APIError(f"POST /empleados -> {response.status_code}: {response.text}")
    if response.content:
        return response.json()
    return {"message": "empleado creado"}


def actualizar_empleado(emp_no: int, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = _request(
        "PUT",
        f"/empleados/{emp_no}",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    if response.status_code not in (200, 204):
        raise APIError(f"PUT /empleados/{emp_no} -> {response.status_code}: {response.text}")
    if response.content:
        try:
            return response.json()
        except ValueError:
            return {"message": response.text.strip() or "empleado actualizado"}
    return {"message": "empleado actualizado"}


def eliminar_empleado(emp_no: int) -> None:
    response = _request("DELETE", f"/empleados/{emp_no}")
    if response.status_code not in (200, 204):
        raise APIError(f"DELETE /empleados/{emp_no} -> {response.status_code}: {response.text}")
