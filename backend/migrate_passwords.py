"""
Script para migrar contraseñas de texto plano a bcrypt hash.
IMPORTANTE: Ejecutar solo UNA VEZ después de implementar la autenticación segura.

Uso:
    python migrate_passwords.py
"""

import mysql.connector
from auth_utils import get_password_hash
from config import DB_CONFIG

def migrate_passwords():
    """Migra todas las contraseñas de texto plano a bcrypt hash"""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Obtener todos los usuarios
        cursor.execute("SELECT id, username, password FROM usuarios")
        usuarios = cursor.fetchall()

        print(f"Encontrados {len(usuarios)} usuarios para migrar")

        for usuario in usuarios:
            # Si la contraseña no está hasheada (no empieza con $2b$)
            if not usuario['password'].startswith('$2b$'):
                # Hashear la contraseña
                hashed_password = get_password_hash(usuario['password'])

                # Actualizar en la base de datos
                update_query = "UPDATE usuarios SET password = %s WHERE id = %s"
                cursor.execute(update_query, (hashed_password, usuario['id']))

                print(f"✓ Migrado usuario: {usuario['username']}")
            else:
                print(f"○ Usuario ya migrado: {usuario['username']}")

        conn.commit()
        print("\n✓ Migración completada exitosamente")

    except Exception as e:
        print(f"\n✗ Error durante la migración: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("MIGRACIÓN DE CONTRASEÑAS A BCRYPT")
    print("=" * 60)
    print("\nADVERTENCIA: Este script modificará todas las contraseñas")
    print("en la base de datos. Asegúrate de tener un respaldo.\n")

    respuesta = input("¿Deseas continuar? (s/n): ")

    if respuesta.lower() == 's':
        migrate_passwords()
    else:
        print("Migración cancelada")
