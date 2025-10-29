from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, status, HTTPException

from app.core.config import ADMIN_NAME, ADMIN_PASSWORD

security = HTTPBasic()


async def admin_auth(credential: HTTPBasicCredentials = Depends(security)):
    if credential.username != ADMIN_NAME or credential.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"}
        )
    return credential.username
