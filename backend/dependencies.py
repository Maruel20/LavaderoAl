"""
Dependencias de seguridad y autenticación
"""
from fastapi import Depends, HTTPException, Header
from typing import Optional, Dict
from auth_utils import decode_token


def verify_token(authorization: Optional[str] = Header(None)) -> Dict:
    """
    Middleware para verificar el token JWT en todas las peticiones.

    Args:
        authorization: Header de autorización con formato "Bearer <token>"

    Returns:
        Dict con la información del usuario (id, username, rol)

    Raises:
        HTTPException: Si el token es inválido, expirado o no proporcionado
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token de autenticación no proporcionado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Extraer el token del header "Bearer <token>"
        parts = authorization.split()

        if len(parts) != 2:
            raise HTTPException(
                status_code=401,
                detail="Formato de autorización inválido. Use: Bearer <token>",
                headers={"WWW-Authenticate": "Bearer"},
            )

        scheme, token = parts

        if scheme.lower() != 'bearer':
            raise HTTPException(
                status_code=401,
                detail="Esquema de autenticación inválido. Use: Bearer",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Decodificar y verificar el token
        payload = decode_token(token)

        if payload is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Error al verificar token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_role(*allowed_roles: str):
    """
    Decorador para requerir roles específicos.

    Uso:
        @router.get("/admin/usuarios", dependencies=[Depends(require_role("admin"))])
        def get_usuarios():
            ...

    Args:
        *allowed_roles: Lista de roles permitidos (ej: "admin", "empleado")

    Returns:
        Función de dependencia que valida el rol
    """
    def role_checker(current_user: Dict = Depends(verify_token)) -> Dict:
        user_role = current_user.get("rol")

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Acceso denegado. Se requiere uno de estos roles: {', '.join(allowed_roles)}"
            )

        return current_user

    return role_checker


def get_current_user(authorization: Optional[str] = Header(None)) -> Dict:
    """
    Obtiene el usuario actual autenticado.
    Alias de verify_token para uso más semántico.
    """
    return verify_token(authorization)
