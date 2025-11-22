from fastapi import APIRouter
from database import get_db_connection
from schemas import EmpleadoCreate

router = APIRouter()

@router.get("/api/empleados")
def get_empleados():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM empleados WHERE estado = 'activo'")
    empleados = cursor.fetchall()
    cursor.close()
    conn.close()
    return empleados

@router.post("/api/empleados")
def create_empleado(empleado: EmpleadoCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO empleados (nombre, rut, telefono, email, porcentaje_comision)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (empleado.nombre, empleado.rut, empleado.telefono, empleado.email, empleado.porcentaje_comision)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Empleado creado correctamente"}