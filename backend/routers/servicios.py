from fastapi import APIRouter, HTTPException
from database import get_db_connection
from schemas import ServicioCreate

router = APIRouter()

@router.get("/api/servicios")
def get_servicios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Hacemos JOIN para traer el nombre del empleado
    query = """
        SELECT s.*, e.nombre as nombre_empleado 
        FROM servicios s
        LEFT JOIN empleados e ON s.id_empleado = e.id
        ORDER BY s.fecha DESC
    """
    cursor.execute(query)
    servicios = cursor.fetchall()
    conn.close()
    return servicios

@router.post("/api/servicios")
def create_servicio(data: ServicioCreate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # 1. Obtener porcentaje del empleado
    cursor.execute("SELECT porcentaje_comision FROM empleados WHERE id = %s", (data.id_empleado,))
    empleado = cursor.fetchone()
    
    if not empleado:
        conn.close()
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
        
    # 2. Calcular comisión
    porcentaje = empleado['porcentaje_comision']
    monto_comision = int(data.monto_total * (porcentaje / 100))
    
    # 3. Insertar servicio
    query = """
        INSERT INTO servicios (patente, tipo_vehiculo, tipo_servicio, monto_total, monto_comision, id_empleado, fecha)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """
    values = (data.patente, data.tipo_vehiculo, data.tipo_servicio, data.monto_total, monto_comision, data.id_empleado)
    
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    
    return {"success": True, "message": "Servicio registrado"}