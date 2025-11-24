from fastapi import APIRouter, HTTPException, Depends
from database import get_db_connection
from dependencies import get_current_user, require_role
from typing import Dict
from schemas import ConvenioCreate, ConvenioUpdate, VehiculoConvenioCreate

router = APIRouter()

@router.get("/api/convenios")
def get_convenios(current_user: Dict = Depends(get_current_user)):
    """Obtener todos los convenios"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                c.*,
                COUNT(DISTINCT v.id) as total_vehiculos
            FROM convenios c
            LEFT JOIN vehiculos_convenio v ON c.id = v.id_convenio AND v.estado = 'activo'
            GROUP BY c.id
            ORDER BY c.fecha_creacion DESC
        """)

        convenios = cursor.fetchall()
        return convenios

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener convenios: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/api/convenios/{id_convenio}")
def get_convenio_detalle(id_convenio: int):
    """Obtener detalle de un convenio específico"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Obtener datos del convenio
        cursor.execute("SELECT * FROM convenios WHERE id = %s", (id_convenio,))
        convenio = cursor.fetchone()

        if not convenio:
            raise HTTPException(status_code=404, detail="Convenio no encontrado")

        # Obtener vehículos asociados
        cursor.execute("""
            SELECT * FROM vehiculos_convenio
            WHERE id_convenio = %s
            ORDER BY fecha_registro DESC
        """, (id_convenio,))

        vehiculos = cursor.fetchall()
        convenio['vehiculos'] = vehiculos

        return convenio

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener detalle de convenio: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/api/convenios")
def create_convenio(convenio: ConvenioCreate, current_user: Dict = Depends(require_role("admin"))):
    """Crear un nuevo convenio"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            INSERT INTO convenios
            (nombre_empresa, rut_empresa, contacto, telefono, email, direccion,
             tipo_descuento, valor_descuento, fecha_inicio, fecha_termino, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            convenio.nombre_empresa,
            convenio.rut_empresa,
            convenio.contacto,
            convenio.telefono,
            convenio.email,
            convenio.direccion,
            convenio.tipo_descuento,
            convenio.valor_descuento,
            convenio.fecha_inicio,
            convenio.fecha_termino,
            convenio.observaciones
        ))

        conn.commit()
        id_convenio = cursor.lastrowid

        return {"mensaje": "Convenio creado exitosamente", "id": id_convenio}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear convenio: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.put("/api/convenios/{id_convenio}")
def update_convenio(id_convenio: int, convenio: ConvenioUpdate, current_user: Dict = Depends(get_current_user)):
    """Actualizar un convenio existente"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Construir query dinámicamente
        updates = []
        values = []

        if convenio.nombre_empresa is not None:
            updates.append("nombre_empresa = %s")
            values.append(convenio.nombre_empresa)
        if convenio.contacto is not None:
            updates.append("contacto = %s")
            values.append(convenio.contacto)
        if convenio.telefono is not None:
            updates.append("telefono = %s")
            values.append(convenio.telefono)
        if convenio.email is not None:
            updates.append("email = %s")
            values.append(convenio.email)
        if convenio.direccion is not None:
            updates.append("direccion = %s")
            values.append(convenio.direccion)
        if convenio.tipo_descuento is not None:
            updates.append("tipo_descuento = %s")
            values.append(convenio.tipo_descuento)
        if convenio.valor_descuento is not None:
            updates.append("valor_descuento = %s")
            values.append(convenio.valor_descuento)
        if convenio.fecha_inicio is not None:
            updates.append("fecha_inicio = %s")
            values.append(convenio.fecha_inicio)
        if convenio.fecha_termino is not None:
            updates.append("fecha_termino = %s")
            values.append(convenio.fecha_termino)
        if convenio.estado is not None:
            updates.append("estado = %s")
            values.append(convenio.estado)
        if convenio.observaciones is not None:
            updates.append("observaciones = %s")
            values.append(convenio.observaciones)

        if not updates:
            raise HTTPException(status_code=400, detail="No se proporcionaron campos para actualizar")

        values.append(id_convenio)
        query = f"UPDATE convenios SET {', '.join(updates)} WHERE id = %s"

        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Convenio no encontrado")

        return {"mensaje": "Convenio actualizado exitosamente"}

    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar convenio: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/api/convenios/{id_convenio}/vehiculos")
def add_vehiculo_convenio(id_convenio: int, vehiculo: VehiculoConvenioCreate):
    """Agregar un vehículo a un convenio"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verificar que el convenio existe
        cursor.execute("SELECT id FROM convenios WHERE id = %s", (id_convenio,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Convenio no encontrado")

        # Verificar que la patente no esté ya registrada en este convenio
        cursor.execute("""
            SELECT id FROM vehiculos_convenio
            WHERE id_convenio = %s AND patente = %s AND estado = 'activo'
        """, (id_convenio, vehiculo.patente))

        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Este vehículo ya está registrado en el convenio")

        # Insertar vehículo
        query = """
            INSERT INTO vehiculos_convenio
            (id_convenio, patente, tipo_vehiculo, modelo, color)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            id_convenio,
            vehiculo.patente,
            vehiculo.tipo_vehiculo,
            vehiculo.modelo,
            vehiculo.color
        ))

        conn.commit()
        id_vehiculo = cursor.lastrowid

        return {"mensaje": "Vehículo agregado al convenio exitosamente", "id": id_vehiculo}

    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al agregar vehículo: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/api/convenios/{id_convenio}/vehiculos")
def get_vehiculos_convenio(id_convenio: int):
    """Obtener todos los vehículos de un convenio"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM vehiculos_convenio
            WHERE id_convenio = %s
            ORDER BY fecha_registro DESC
        """, (id_convenio,))

        vehiculos = cursor.fetchall()
        return vehiculos

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener vehículos del convenio: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/api/convenios/vehiculos/{id_vehiculo}")
def remove_vehiculo_convenio(id_vehiculo: int):
    """Desactivar un vehículo de un convenio"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE vehiculos_convenio
            SET estado = 'inactivo'
            WHERE id = %s
        """, (id_vehiculo,))

        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        return {"mensaje": "Vehículo desactivado del convenio"}

    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al desactivar vehículo: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/api/convenios/patente/{patente}")
def verificar_convenio_patente(patente: str):
    """Verificar si una patente tiene convenio activo"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                c.id as id_convenio,
                c.nombre_empresa,
                c.tipo_descuento,
                c.valor_descuento,
                v.tipo_vehiculo
            FROM vehiculos_convenio v
            JOIN convenios c ON v.id_convenio = c.id
            WHERE v.patente = %s
                AND v.estado = 'activo'
                AND c.estado = 'activo'
                AND (c.fecha_termino IS NULL OR c.fecha_termino >= CURDATE())
        """, (patente,))

        convenio = cursor.fetchone()

        if convenio:
            return {
                "tiene_convenio": True,
                "convenio": convenio
            }
        else:
            return {"tiene_convenio": False}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al verificar convenio: {str(e)}")
    finally:
        cursor.close()
        conn.close()
