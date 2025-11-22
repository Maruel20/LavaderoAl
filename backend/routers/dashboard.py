from fastapi import APIRouter, HTTPException
from database import get_db_connection

router = APIRouter()

@router.get("/dashboard/metricas")
def get_metricas_dashboard():
    """Obtener métricas principales del dashboard"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Servicios del día
        cursor.execute("""
            SELECT COUNT(*) as servicios_hoy
            FROM servicios
            WHERE DATE(fecha) = CURDATE()
                AND estado = 'completado'
        """)
        servicios_hoy = cursor.fetchone()['servicios_hoy']

        # Ingresos del día
        cursor.execute("""
            SELECT COALESCE(SUM(monto_total), 0) as ingresos_hoy
            FROM servicios
            WHERE DATE(fecha) = CURDATE()
                AND estado = 'completado'
        """)
        ingresos_hoy = cursor.fetchone()['ingresos_hoy']

        # Clientes activos (patentes únicas del mes)
        cursor.execute("""
            SELECT COUNT(DISTINCT patente) as clientes_activos
            FROM servicios
            WHERE MONTH(fecha) = MONTH(CURDATE())
                AND YEAR(fecha) = YEAR(CURDATE())
                AND estado = 'completado'
        """)
        clientes_activos = cursor.fetchone()['clientes_activos']

        # Insumos con stock bajo
        cursor.execute("""
            SELECT COUNT(*) as insumos_bajos
            FROM inventario
            WHERE stock <= stock_minimo
        """)
        insumos_bajos = cursor.fetchone()['insumos_bajos']

        # Servicios del mes
        cursor.execute("""
            SELECT COUNT(*) as servicios_mes
            FROM servicios
            WHERE MONTH(fecha) = MONTH(CURDATE())
                AND YEAR(fecha) = YEAR(CURDATE())
                AND estado = 'completado'
        """)
        servicios_mes = cursor.fetchone()['servicios_mes']

        # Ingresos del mes
        cursor.execute("""
            SELECT COALESCE(SUM(monto_total), 0) as ingresos_mes
            FROM servicios
            WHERE MONTH(fecha) = MONTH(CURDATE())
                AND YEAR(fecha) = YEAR(CURDATE())
                AND estado = 'completado'
        """)
        ingresos_mes = cursor.fetchone()['ingresos_mes']

        # Empleados activos
        cursor.execute("""
            SELECT COUNT(*) as empleados_activos
            FROM empleados
            WHERE estado = 'activo'
        """)
        empleados_activos = cursor.fetchone()['empleados_activos']

        # Convenios activos
        cursor.execute("""
            SELECT COUNT(*) as convenios_activos
            FROM convenios
            WHERE estado = 'activo'
                AND (fecha_termino IS NULL OR fecha_termino >= CURDATE())
        """)
        convenios_activos = cursor.fetchone()['convenios_activos']

        return {
            "servicios_hoy": servicios_hoy,
            "ingresos_hoy": float(ingresos_hoy),
            "clientes_activos": clientes_activos,
            "insumos_bajos": insumos_bajos,
            "servicios_mes": servicios_mes,
            "ingresos_mes": float(ingresos_mes),
            "empleados_activos": empleados_activos,
            "convenios_activos": convenios_activos
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener métricas: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/dashboard/servicios-recientes")
def get_servicios_recientes(limit: int = 10):
    """Obtener los servicios más recientes"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                s.id,
                s.patente,
                s.tipo_vehiculo,
                s.tipo_servicio,
                s.monto_total,
                s.monto_comision,
                s.fecha,
                s.estado,
                s.es_convenio,
                e.nombre as nombre_empleado,
                c.nombre_empresa
            FROM servicios s
            LEFT JOIN empleados e ON s.id_empleado = e.id
            LEFT JOIN convenios c ON s.id_convenio = c.id
            ORDER BY s.fecha DESC
            LIMIT %s
        """, (limit,))

        servicios = cursor.fetchall()
        return servicios

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener servicios recientes: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/dashboard/alertas-inventario")
def get_alertas_inventario():
    """Obtener alertas de inventario con stock bajo"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                id,
                nombre,
                categoria,
                stock,
                stock_minimo,
                unidad,
                CASE
                    WHEN stock <= stock_minimo THEN 'URGENTE'
                    WHEN stock <= stock_minimo * 1.5 THEN 'ADVERTENCIA'
                    ELSE 'NORMAL'
                END as nivel_alerta
            FROM inventario
            WHERE stock <= stock_minimo * 1.5
            ORDER BY stock ASC
            LIMIT 10
        """)

        alertas = cursor.fetchall()
        return alertas

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener alertas de inventario: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/dashboard/empleados-top")
def get_empleados_top(limit: int = 5):
    """Obtener top empleados del mes por ventas"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                e.id,
                e.nombre,
                e.porcentaje_comision,
                COUNT(s.id) as total_servicios,
                COALESCE(SUM(s.monto_total), 0) as total_vendido,
                COALESCE(SUM(s.monto_comision), 0) as total_comisiones
            FROM empleados e
            LEFT JOIN servicios s ON e.id = s.id_empleado
                AND MONTH(s.fecha) = MONTH(CURDATE())
                AND YEAR(s.fecha) = YEAR(CURDATE())
                AND s.estado = 'completado'
            WHERE e.estado = 'activo'
            GROUP BY e.id, e.nombre, e.porcentaje_comision
            ORDER BY total_vendido DESC
            LIMIT %s
        """, (limit,))

        empleados = cursor.fetchall()
        return empleados

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener top empleados: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/dashboard/grafico-servicios")
def get_grafico_servicios(dias: int = 7):
    """Obtener datos para gráfico de servicios de los últimos N días"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                DATE(fecha) as fecha,
                COUNT(*) as cantidad,
                SUM(monto_total) as ingresos
            FROM servicios
            WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
                AND estado = 'completado'
            GROUP BY DATE(fecha)
            ORDER BY fecha ASC
        """, (dias,))

        datos = cursor.fetchall()
        return datos

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos del gráfico: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/dashboard/servicios-por-tipo")
def get_servicios_por_tipo():
    """Obtener distribución de servicios por tipo del mes actual"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                tipo_servicio,
                COUNT(*) as cantidad,
                SUM(monto_total) as ingresos
            FROM servicios
            WHERE MONTH(fecha) = MONTH(CURDATE())
                AND YEAR(fecha) = YEAR(CURDATE())
                AND estado = 'completado'
            GROUP BY tipo_servicio
            ORDER BY cantidad DESC
        """)

        servicios = cursor.fetchall()
        return servicios

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener servicios por tipo: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/dashboard/liquidaciones-pendientes")
def get_liquidaciones_pendientes():
    """Obtener liquidaciones pendientes de pago"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                l.id,
                l.periodo_inicio,
                l.periodo_fin,
                l.total_comisiones,
                e.nombre as nombre_empleado
            FROM liquidaciones l
            JOIN empleados e ON l.id_empleado = e.id
            WHERE l.estado = 'pendiente'
            ORDER BY l.fecha_creacion DESC
            LIMIT 5
        """)

        liquidaciones = cursor.fetchall()
        return liquidaciones

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener liquidaciones pendientes: {str(e)}")
    finally:
        cursor.close()
        conn.close()
