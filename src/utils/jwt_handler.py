"""
Utilidad para manejar tokens JWT
"""
import jwt
from fastapi import HTTPException, Header
from typing import Optional

# Cambia esta clave por la misma que usa tu microservicio de auth
SECRET_KEY = "123456789"  # Debe ser la misma que en tu microservicio de auth
ALGORITHM = "HS256"


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


def get_current_user_id(authorization: Optional[str] = Header(None)) -> int:
    if not authorization:
        raise HTTPException(status_code=401, detail="No se proporcionó token de autenticación")
    
    # Verificar que el header tenga el formato correcto "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Formato de token inválido. Use: Bearer <token>")
    
    token = parts[1]
    payload = decode_token(token)
    
    # Extraer el ID del usuario del payload
    # Ajusta el nombre del campo según cómo lo guardas en tu microservicio de auth
    user_id = payload.get("user_id") or payload.get("id_usuario") or payload.get("id")
    user_id = int(user_id)
    print("Payload del token:", payload)

    if not user_id:
        raise HTTPException(status_code=401, detail="Token no contiene ID de usuario")
    
    return user_id