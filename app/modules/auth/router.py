from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Dict

from app.core.dependencies import get_db
from app.modules.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)
from app.modules.auth.service import register_user, login_user


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


# ==========================================
# Error Helper
# ==========================================

def http_error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={
            "error_code": code,
            "message": message,
        },
    )


# ==========================================
# Register
# ==========================================

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
) -> Dict:
    try:
        user = register_user(db, data)
        db.commit()
        return user

    except IntegrityError:
        db.rollback()
        raise http_error(
            status.HTTP_400_BAD_REQUEST,
            "USER_ALREADY_EXISTS",
            "El usuario ya está registrado.",
        )


# ==========================================
# Login
# ==========================================

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    token = login_user(db, data)

    if not token:
        raise http_error(
            status.HTTP_401_UNAUTHORIZED,
            "INVALID_CREDENTIALS",
            "Credenciales inválidas.",
        )

    return TokenResponse(access_token=token)
