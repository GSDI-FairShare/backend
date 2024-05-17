import time
from datetime import datetime, timezone
from fastapi import HTTPException, status
from jose import jwt, JWTError

SECRET_KEY = "your_secret_key"  # Cambia esto por tu clave secreta


def create_access_token(user_id: int):
    payload = {"user_id": user_id, "expires": time.time() + 3600}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def verify_access_token(token: str):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        expire = data.get("expires")
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied",
            )
        if datetime.now(timezone.utc) > datetime.fromtimestamp(expire, timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expired!",
            )
        return data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )
