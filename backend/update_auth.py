"""
Script para agregar autenticación a todos los routers
Ejecutar: python update_auth.py
"""
import os
import re


def update_router_file(filepath, router_name):
    """Actualiza un archivo de router para agregar autenticación"""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Si ya tiene la dependencia, saltar
    if 'from dependencies import' in content:
        print(f"✓ {router_name} ya tiene autenticación")
        return False

    # 1. Actualizar imports
    old_import = "from fastapi import APIRouter, HTTPException"
    new_import = "from fastapi import APIRouter, HTTPException, Depends"
    content = content.replace(old_import, new_import)

    # 2. Agregar import de dependencies
    if 'from database import get_db_connection' in content:
        content = content.replace(
            'from database import get_db_connection',
            'from database import get_db_connection\nfrom dependencies import get_current_user, require_role\nfrom typing import Dict'
        )

    # 3. Actualizar funciones GET (todos pueden ver)
    # Patrón: def function_name():
    # Reemplazar por: def function_name(current_user: Dict = Depends(get_current_user)):

    get_patterns = [
        (r'def (get_\w+)\(\):', r'def \1(current_user: Dict = Depends(get_current_user)):'),
    ]

    for pattern, replacement in get_patterns:
        content = re.sub(pattern, replacement, content)

    # 4. Actualizar funciones POST/PUT/DELETE (solo admin puede crear/modificar)
    # Excepto para create_servicio que puede ser usado por empleados

    admin_patterns = [
        (r'def (create_empleado)\((\w+: \w+)\):', r'def \1(\2, current_user: Dict = Depends(require_role("admin", "empleado"))):'),
        (r'def (create_insumo)\((\w+: \w+)\):', r'def \1(\2, current_user: Dict = Depends(get_current_user)):'),
        (r'def (update_\w+)\(([^)]+)\):', r'def \1(\2, current_user: Dict = Depends(get_current_user)):'),
        (r'def (create_convenio)\((\w+: \w+)\):', r'def \1(\2, current_user: Dict = Depends(require_role("admin"))):'),
        (r'def (create_servicio)\((\w+: \w+)\):', r'def \1(\2, current_user: Dict = Depends(get_current_user)):'),
    ]

    for pattern, replacement in admin_patterns:
        content = re.sub(pattern, replacement, content)

    # Escribir archivo actualizado
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Actualizado: {router_name}")
    return True


def main():
    """Función principal"""
    routers_dir = 'routers'

    if not os.path.exists(routers_dir):
        print("Error: Directorio 'routers' no encontrado")
        print("Ejecuta este script desde el directorio backend/")
        return

    routers_to_update = [
        'servicios.py',
        'empleados.py',
        'inventario.py',
        'liquidaciones.py',
        'convenios.py',
        'tarifas.py',
        'reportes.py',
        'dashboard.py'
    ]

    updated_count = 0

    print("=" * 50)
    print("Actualizando routers con autenticación...")
    print("=" * 50)

    for router_file in routers_to_update:
        filepath = os.path.join(routers_dir, router_file)

        if os.path.exists(filepath):
            if update_router_file(filepath, router_file):
                updated_count += 1
        else:
            print(f"✗ No encontrado: {router_file}")

    print("=" * 50)
    print(f"✓ Proceso completado: {updated_count} archivos actualizados")
    print("=" * 50)
    print("\nNOTA IMPORTANTE:")
    print("- Los endpoints GET requieren autenticación (cualquier usuario)")
    print("- Los endpoints de creación de empleados y convenios requieren rol admin")
    print("- El endpoint de crear servicios requiere autenticación (empleado o admin)")
    print("- Los endpoints de inventario requieren autenticación")
    print("\nRevisa manualmente los archivos para ajustes finos si es necesario.")


if __name__ == "__main__":
    main()
