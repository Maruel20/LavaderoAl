from pydantic import BaseModel
from typing import Optional

# --- LOGIN ---
class LoginRequest(BaseModel):
    username: str
    password: str

# --- EMPLEADOS ---
class EmpleadoCreate(BaseModel):
    nombre: str
    rut: str
    telefono: str
    email: str
    porcentaje_comision: int

# --- SERVICIOS ---
class ServicioCreate(BaseModel):
    patente: str
    tipo_vehiculo: str
    tipo_servicio: str
    monto_total: int
    id_empleado: int
    # La comisión la calculamos en el backend, no la envíe el front

# --- INVENTARIO ---
class InsumoCreate(BaseModel):
    nombre: str
    categoria: str
    stock: int
    stock_minimo: int
    precio_unitario: int
    unidad: str