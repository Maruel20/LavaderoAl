from fastapi import APIRouter, HTTPException
from database import get_db_connection
from schemas import EmpleadoCreate
import mysql.connector

router = APIRouter()

@router.get("/api/empleados")
def get_empleados():
    """Obtener todos los empleados activos"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM empleados WHERE estado = 'activo'")
        empleados = cursor.fetchall()
        return empleados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener empleados: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.post("/api/empleados")
def create_empleado(empleado: EmpleadoCreate):
    """Crear un nuevo empleado"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Verificar si el RUT ya existe
        cursor.execute("SELECT id FROM empleados WHERE rut = %s", (empleado.rut,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Ya existe un empleado con este RUT")

        # Insertar empleado
        query = """
            INSERT INTO empleados (nombre, rut, telefono, email, porcentaje_comision)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (empleado.nombre, empleado.rut, empleado.telefono, empleado.email, empleado.porcentaje_comision)
        cursor.execute(query, values)
        conn.commit()

        empleado_id = cursor.lastrowid
        return {
            "message": "Empleado creado correctamente",
            "id": empleado_id
        }

    except HTTPException:
        raise
    except mysql.connector.IntegrityError as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=400, detail=f"Error de integridad: {str(e)}")
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear empleado: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()