from fastapi import APIRouter, HTTPException
from database import get_db_connection
from schemas import LoginRequest

router = APIRouter()

@router.post("/api/login")
def login(credentials: LoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # NOTA: En un sistema real, usa hash para passwords (bcrypt)
    query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
    cursor.execute(query, (credentials.username, credentials.password))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if user:
        return {
            "success": True,
            "token": "token_simulado_123", # Aquí iría JWT
            "user": {
                "id": user["id"],
                "username": user["username"],
                "rol": user["rol"]
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")