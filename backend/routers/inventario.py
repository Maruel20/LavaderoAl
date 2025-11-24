from fastapi import APIRouter, HTTPException, Depends
from database import get_db_connection
from dependencies import get_current_user, require_role
from typing import Dict
from schemas import InsumoCreate, InsumoUpdate, MovimientoInventario

router = APIRouter()

@router.get("/api/inventario")
def get_inventario(current_user: Dict = Depends(get_current_user)):
    """Obtener todos los insumos del inventario"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                i.*,
                CASE
                    WHEN i.stock > i.stock_minimo * 2 THEN 'optimo'
                    WHEN i.stock > i.stock_minimo THEN 'bajo'
                    ELSE 'critico'
                END as estado_stock
            FROM inventario i
            ORDER BY i.nombre
        """)

        inventario = cursor.fetchall()
        return inventario

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener inventario: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/api/inventario")
def create_insumo(insumo: InsumoCreate, current_user: Dict = Depends(get_current_user)):
    """Crear un nuevo insumo en el inventario"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            INSERT INTO inventario
            (nombre, categoria, stock, stock_minimo, precio_unitario, unidad)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            insumo.nombre,
            insumo.categoria,
            insumo.stock,
            insumo.stock_minimo,
            insumo.precio_unitario,
            insumo.unidad
        ))

        conn.commit()

        # Registrar el movimiento inicial
        id_insumo = cursor.lastrowid
        cursor.execute("""
            INSERT INTO movimientos_inventario
            (id_insumo, tipo_movimiento, cantidad, motivo, usuario)
            VALUES (%s, 'entrada', %s, 'Stock inicial', 'sistema')
        """, (id_insumo, insumo.stock))

        conn.commit()

        return {"mensaje": "Insumo creado exitosamente", "id": id_insumo}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear insumo: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.put("/api/inventario/{id_insumo}")
def update_insumo(id_insumo: int, insumo: InsumoUpdate, current_user: Dict = Depends(get_current_user)):
    """Actualizar un insumo existente"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Construir query dinámicamente solo con campos proporcionados
        updates = []
        values = []

        if insumo.nombre is not None:
            updates.append("nombre = %s")
            values.append(insumo.nombre)
        if insumo.categoria is not None:
            updates.append("categoria = %s")
            values.append(insumo.categoria)
        if insumo.stock is not None:
            updates.append("stock = %s")
            values.append(insumo.stock)
        if insumo.stock_minimo is not None:
            updates.append("stock_minimo = %s")
            values.append(insumo.stock_minimo)
        if insumo.precio_unitario is not None:
            updates.append("precio_unitario = %s")
            values.append(insumo.precio_unitario)
        if insumo.unidad is not None:
            updates.append("unidad = %s")
            values.append(insumo.unidad)

        if not updates:
            raise HTTPException(status_code=400, detail="No se proporcionaron campos para actualizar")

        values.append(id_insumo)
        query = f"UPDATE inventario SET {', '.join(updates)} WHERE id = %s"

        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Insumo no encontrado")

        return {"mensaje": "Insumo actualizado exitosamente"}

    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar insumo: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/api/inventario/movimiento")
def registrar_movimiento(movimiento: MovimientoInventario):
    """Registrar un movimiento de inventario (entrada/salida/ajuste)"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verificar que el insumo existe
        cursor.execute("SELECT stock FROM inventario WHERE id = %s", (movimiento.id_insumo,))
        resultado = cursor.fetchone()

        if not resultado:
            raise HTTPException(status_code=404, detail="Insumo no encontrado")

        stock_actual = resultado[0]

        # Calcular nuevo stock
        if movimiento.tipo_movimiento == 'entrada':
            nuevo_stock = stock_actual + movimiento.cantidad
        elif movimiento.tipo_movimiento == 'salida':
            nuevo_stock = stock_actual - movimiento.cantidad
            if nuevo_stock < 0:
                raise HTTPException(status_code=400, detail="Stock insuficiente")
        elif movimiento.tipo_movimiento == 'ajuste':
            nuevo_stock = movimiento.cantidad
        else:
            raise HTTPException(status_code=400, detail="Tipo de movimiento inválido")

        # Actualizar stock
        cursor.execute(
            "UPDATE inventario SET stock = %s WHERE id = %s",
            (nuevo_stock, movimiento.id_insumo)
        )

        # Registrar movimiento
        cursor.execute("""
            INSERT INTO movimientos_inventario
            (id_insumo, tipo_movimiento, cantidad, motivo, usuario)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            movimiento.id_insumo,
            movimiento.tipo_movimiento,
            movimiento.cantidad,
            movimiento.motivo,
            movimiento.usuario
        ))

        conn.commit()

        return {
            "mensaje": "Movimiento registrado exitosamente",
            "stock_anterior": stock_actual,
            "stock_nuevo": nuevo_stock
        }

    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al registrar movimiento: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/api/inventario/movimientos/{id_insumo}")
def get_movimientos_insumo(id_insumo: int):
    """Obtener historial de movimientos de un insumo"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM movimientos_inventario
            WHERE id_insumo = %s
            ORDER BY fecha DESC
            LIMIT 50
        """, (id_insumo,))

        movimientos = cursor.fetchall()
        return movimientos

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener movimientos: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/api/inventario/alertas")
def get_alertas_inventario(current_user: Dict = Depends(get_current_user)):
    """Obtener insumos con stock bajo o crítico"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                i.*,
                CASE
                    WHEN i.stock <= i.stock_minimo THEN 'URGENTE'
                    WHEN i.stock <= i.stock_minimo * 1.5 THEN 'ADVERTENCIA'
                    ELSE 'NORMAL'
                END as nivel_alerta
            FROM inventario i
            WHERE i.stock <= i.stock_minimo * 1.5
            ORDER BY i.stock ASC
        """)

        alertas = cursor.fetchall()
        return alertas

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener alertas: {str(e)}")
    finally:
        cursor.close()
        conn.close()
