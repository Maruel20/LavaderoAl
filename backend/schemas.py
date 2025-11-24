from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re

# --- LOGIN ---
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UsuarioCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    rol: Optional[str] = Field(default='usuario')

    @validator('username')
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('El username solo puede contener letras, números y guiones bajos')
        return v

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return v

# --- EMPLEADOS ---
class EmpleadoCreate(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    rut: str = Field(..., min_length=9, max_length=12)
    telefono: str = Field(..., min_length=9, max_length=15)
    email: EmailStr
    porcentaje_comision: int = Field(..., ge=0, le=100)

    @validator('rut')
    def validate_rut(cls, v):
        # Validar formato básico de RUT chileno (XX.XXX.XXX-X o XXXXXXXX-X)
        v = v.replace('.', '').replace('-', '')
        if not re.match(r'^\d{7,8}[\dkK]$', v):
            raise ValueError('Formato de RUT inválido. Debe ser formato chileno (ej: 12345678-9)')
        return v

    @validator('telefono')
    def validate_telefono(cls, v):
        # Validar teléfono chileno (+56 9 XXXX XXXX o 9 XXXX XXXX)
        v_clean = v.replace('+', '').replace(' ', '').replace('-', '')
        if not re.match(r'^(56)?9\d{8}$', v_clean):
            raise ValueError('Formato de teléfono inválido. Debe ser formato chileno (ej: +56912345678 o 912345678)')
        return v

# --- SERVICIOS ---
class ServicioCreate(BaseModel):
    patente: str = Field(..., min_length=6, max_length=10)
    tipo_vehiculo: str = Field(..., min_length=3, max_length=50)
    tipo_servicio: str = Field(..., min_length=3, max_length=50)
    monto_total: int = Field(..., gt=0)
    id_empleado: int = Field(..., gt=0)
    # La comisión la calculamos en el backend, no la envíe el front

    @validator('patente')
    def validate_patente(cls, v):
        # Validar formato de patente chilena (XXXX99 o XXXX-99)
        v_clean = v.upper().replace('-', '').replace(' ', '')
        if not re.match(r'^[A-Z]{4}\d{2}$|^[A-Z]{2}\d{4}$', v_clean):
            raise ValueError('Formato de patente inválido. Debe ser formato chileno (ej: ABCD12 o AB1234)')
        return v_clean

# --- INVENTARIO ---
class InsumoCreate(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    categoria: str = Field(..., min_length=3, max_length=50)
    stock: int = Field(..., ge=0)
    stock_minimo: int = Field(..., ge=0)
    precio_unitario: float = Field(..., gt=0)
    unidad: str = Field(..., min_length=1, max_length=20)

    @validator('stock_minimo')
    def validate_stock_minimo(cls, v, values):
        if v < 0:
            raise ValueError('El stock mínimo no puede ser negativo')
        return v

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
    nombre_empresa: str = Field(..., min_length=3, max_length=100)
    rut_empresa: str = Field(..., min_length=9, max_length=12)
    contacto: str = Field(..., min_length=3, max_length=100)
    telefono: str = Field(..., min_length=9, max_length=15)
    email: EmailStr
    direccion: Optional[str] = None
    tipo_descuento: str = Field(..., pattern='^(porcentaje|monto_fijo)$')
    valor_descuento: float = Field(..., gt=0)
    fecha_inicio: str
    fecha_termino: Optional[str] = None
    observaciones: Optional[str] = None

    @validator('rut_empresa')
    def validate_rut_empresa(cls, v):
        v = v.replace('.', '').replace('-', '')
        if not re.match(r'^\d{7,8}[\dkK]$', v):
            raise ValueError('Formato de RUT inválido')
        return v

    @validator('telefono')
    def validate_telefono(cls, v):
        v_clean = v.replace('+', '').replace(' ', '').replace('-', '')
        if not re.match(r'^(56)?9\d{8}$', v_clean):
            raise ValueError('Formato de teléfono inválido')
        return v

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
    precio: float = Field(..., gt=0)

# --- LIQUIDACIONES ---
class LiquidacionCreate(BaseModel):
    id_empleado: int = Field(..., gt=0)
    periodo_inicio: str
    periodo_fin: str

    @validator('periodo_fin')
    def validate_periodo(cls, v, values):
        if 'periodo_inicio' in values and v < values['periodo_inicio']:
            raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
        return v