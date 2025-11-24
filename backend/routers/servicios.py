from fastapi import APIRouter, HTTPException, Depends
from database import get_db_connection
from dependencies import get_current_user, require_role
from typing import Dict
from schemas import ServicioCreate
import mysql.connector

router = APIRouter()

@router.get("/api/servicios")
def get_servicios(current_user: Dict = Depends(get_current_user)):
    """Obtener todos los servicios con información del empleado"""
    conn = None
    cursor = None
    try:
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
        return servicios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener servicios: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.post("/api/servicios")
def create_servicio(data: ServicioCreate, current_user: Dict = Depends(get_current_user)):
    """Crear un nuevo servicio y calcular comisión"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 1. Obtener porcentaje del empleado
        cursor.execute(
            "SELECT porcentaje_comision FROM empleados WHERE id = %s AND estado = 'activo'",
            (data.id_empleado,)
        )
        empleado = cursor.fetchone()

        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado o inactivo")

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

        servicio_id = cursor.lastrowid
        return {
            "success": True,
            "message": "Servicio registrado",
            "id": servicio_id,
            "monto_comision": monto_comision
        }

    except HTTPException:
        raise
    except mysql.connector.Error as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear servicio: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()