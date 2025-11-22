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
    precio_unitario: float
    unidad: str

class InsumoUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    stock: Optional[int] = None
    stock_minimo: Optional[int] = None
    precio_unitario: Optional[float] = None
    unidad: Optional[str] = None

class MovimientoInventario(BaseModel):
    id_insumo: int
    tipo_movimiento: str
    cantidad: int
    motivo: Optional[str] = None
    usuario: str

# --- CONVENIOS ---
class ConvenioCreate(BaseModel):
    nombre_empresa: str
    rut_empresa: str
    contacto: str
    telefono: str
    email: str
    direccion: Optional[str] = None
    tipo_descuento: str
    valor_descuento: float
    fecha_inicio: str
    fecha_termino: Optional[str] = None
    observaciones: Optional[str] = None

class ConvenioUpdate(BaseModel):
    nombre_empresa: Optional[str] = None
    contacto: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    tipo_descuento: Optional[str] = None
    valor_descuento: Optional[float] = None
    fecha_inicio: Optional[str] = None
    fecha_termino: Optional[str] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None

class VehiculoConvenioCreate(BaseModel):
    id_convenio: int
    patente: str
    tipo_vehiculo: str
    modelo: Optional[str] = None
    color: Optional[str] = None

# --- TARIFAS ---
class TarifaUpdate(BaseModel):
    precio: float

# --- LIQUIDACIONES ---
class LiquidacionCreate(BaseModel):
    id_empleado: int
    periodo_inicio: str
    periodo_fin: str