from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    if credentials.username != settings.SUPERADMIN_USERNAME or credentials.password != settings.SUPERADMIN_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    token = create_access_token(subject=settings.SUPERADMIN_USERNAME)
    return {"access_token": token, "token_type": "bearer"}
