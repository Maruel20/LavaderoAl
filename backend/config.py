import os
import secrets
from dotenv import load_dotenv

load_dotenv()

# Configuración de Base de Datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),  # Vacío por defecto en XAMPP
    'database': os.getenv('DB_NAME', 'lavadero_al'),
    'port': int(os.getenv('DB_PORT', '3306'))
}

# Configuración de JWT
# IMPORTANTE: En producción, DEBES cambiar esto por una clave segura
# Puedes generar una con: python -c "import secrets; print(secrets.token_urlsafe(32))"
_default_secret = secrets.token_urlsafe(32) if os.getenv('ENV') == 'development' else None

SECRET_KEY = os.getenv('SECRET_KEY', _default_secret)

if SECRET_KEY is None:
    raise ValueError(
        "ERROR: SECRET_KEY no está configurada.\n"
        "Por favor, configura SECRET_KEY en el archivo .env\n"
        "Puedes generar una con: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60 * 24))  # 24 horas por defecto

# Entorno
ENV = os.getenv('ENV', 'development')  # development, production