from src.auth.jwt_handler import verify_access_token
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/signin")


def authenticate(token: str = Depends(oauth2_scheme)) -> int:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Sign in for access"
        )

    decoded_token = verify_access_token(token)
    return decoded_token["user_id"]
