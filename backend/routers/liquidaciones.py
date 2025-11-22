from fastapi import APIRouter, HTTPException
from database import get_db_connection
from schemas import LiquidacionCreate
from datetime import datetime

router = APIRouter()

@router.get("/api/liquidaciones")
def get_liquidaciones():
    """Obtener todas las liquidaciones"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                l.*,
                e.nombre as nombre_empleado,
                e.rut
            FROM liquidaciones l
            JOIN empleados e ON l.id_empleado = e.id
            ORDER BY l.fecha_creacion DESC
        """)

        liquidaciones = cursor.fetchall()
        return liquidaciones

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener liquidaciones: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/api/liquidaciones/{id_liquidacion}")
def get_liquidacion_detalle(id_liquidacion: int):
    """Obtener detalle de una liquidación específica"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Obtener datos de la liquidación
        cursor.execute("""
            SELECT
                l.*,
                e.nombre as nombre_empleado,
                e.rut,
                e.email,
                e.telefono
            FROM liquidaciones l
            JOIN empleados e ON l.id_empleado = e.id
            WHERE l.id = %s
        """, (id_liquidacion,))

        liquidacion = cursor.fetchone()

        if not liquidacion:
            raise HTTPException(status_code=404, detail="Liquidación no encontrada")

        # Obtener detalle de servicios
        cursor.execute("""
            SELECT
                s.id,
                s.patente,
                s.tipo_vehiculo,
                s.tipo_servicio,
                s.fecha,
                s.monto_total,
                s.monto_comision
            FROM servicios s
            WHERE s.id_empleado = %s
                AND s.fecha BETWEEN %s AND %s
                AND s.estado = 'completado'
            ORDER BY s.fecha DESC
        """, (liquidacion['id_empleado'], liquidacion['periodo_inicio'], liquidacion['periodo_fin']))

        servicios = cursor.fetchall()
        liquidacion['servicios'] = servicios

        return liquidacion

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener detalle de liquidación: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/api/liquidaciones/calcular")
def calcular_liquidacion(liquidacion: LiquidacionCreate):
    """Calcular y crear una nueva liquidación"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Verificar que el empleado existe
        cursor.execute("SELECT id, nombre FROM empleados WHERE id = %s", (liquidacion.id_empleado,))
        empleado = cursor.fetchone()

        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        # Verificar que no exista una liquidación para el mismo período
        cursor.execute("""
            SELECT id FROM liquidaciones
            WHERE id_empleado = %s
                AND (
                    (periodo_inicio <= %s AND periodo_fin >= %s)
                    OR (periodo_inicio <= %s AND periodo_fin >= %s)
                )
        """, (
            liquidacion.id_empleado,
            liquidacion.periodo_inicio, liquidacion.periodo_inicio,
            liquidacion.periodo_fin, liquidacion.periodo_fin
        ))

        if cursor.fetchone():
            raise HTTPException(
                status_code=400,
                detail="Ya existe una liquidación para este empleado en el período especificado"
            )

        # Calcular totales de servicios en el período
        cursor.execute("""
            SELECT
                COUNT(*) as total_servicios,
                COALESCE(SUM(monto_total), 0) as monto_total_servicios,
                COALESCE(SUM(monto_comision), 0) as total_comisiones
            FROM servicios
            WHERE id_empleado = %s
                AND fecha BETWEEN %s AND %s
                AND estado = 'completado'
        """, (liquidacion.id_empleado, liquidacion.periodo_inicio, liquidacion.periodo_fin))

        totales = cursor.fetchone()

        # Crear la liquidación
        cursor.execute("""
            INSERT INTO liquidaciones
            (id_empleado, periodo_inicio, periodo_fin, total_servicios,
             monto_total_servicios, total_comisiones, estado)
            VALUES (%s, %s, %s, %s, %s, %s, 'pendiente')
        """, (
            liquidacion.id_empleado,
            liquidacion.periodo_inicio,
            liquidacion.periodo_fin,
            totales['total_servicios'],
            totales['monto_total_servicios'],
            totales['total_comisiones']
        ))

        id_liquidacion = cursor.lastrowid

        # Insertar detalle de servicios
        cursor.execute("""
            INSERT INTO detalle_liquidaciones
            (id_liquidacion, id_servicio, monto_servicio, monto_comision)
            SELECT %s, id, monto_total, monto_comision
            FROM servicios
            WHERE id_empleado = %s
                AND fecha BETWEEN %s AND %s
                AND estado = 'completado'
        """, (id_liquidacion, liquidacion.id_empleado, liquidacion.periodo_inicio, liquidacion.periodo_fin))

        conn.commit()

        return {
            "mensaje": "Liquidación calculada exitosamente",
            "id": id_liquidacion,
            "total_servicios": totales['total_servicios'],
            "monto_total_servicios": float(totales['monto_total_servicios']),
            "total_comisiones": float(totales['total_comisiones'])
        }

    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al calcular liquidación: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.put("/api/liquidaciones/{id_liquidacion}/pagar")
def marcar_liquidacion_pagada(id_liquidacion: int):
    """Marcar una liquidación como pagada"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE liquidaciones
            SET estado = 'pagada', fecha_pago = CURDATE()
            WHERE id = %s AND estado = 'pendiente'
        """, (id_liquidacion,))

        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Liquidación no encontrada o ya está pagada"
            )

        return {"mensaje": "Liquidación marcada como pagada"}

    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al marcar liquidación como pagada: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/api/liquidaciones/empleado/{id_empleado}")
def get_liquidaciones_empleado(id_empleado: int):
    """Obtener liquidaciones de un empleado específico"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                l.*,
                e.nombre as nombre_empleado,
                e.rut
            FROM liquidaciones l
            JOIN empleados e ON l.id_empleado = e.id
            WHERE l.id_empleado = %s
            ORDER BY l.fecha_creacion DESC
        """, (id_empleado,))

        liquidaciones = cursor.fetchall()
        return liquidaciones

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener liquidaciones del empleado: {str(e)}")
    finally:
        cursor.close()
        conn.close()
