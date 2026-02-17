from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.modules.users.model import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings


def register_user(db: Session, data):
    # Verificar si ya existe el usuario
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "USER_EXISTS", "message": "El correo ya está registrado"}
        )

    try:
        user = User(
            name=data.name,
            email=data.email,
            password=hash_password(data.password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "DB_CONSTRAINT", "message": "Error de integridad en la base de datos"}
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_code": "SERVER_ERROR", "message": "Error interno del servidor"}
        )


def login_user(db: Session, data):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "USER_NOT_FOUND", "message": "Usuario no encontrado"}
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error_code": "INVALID_CREDENTIALS", "message": "Credenciales inválidas"}
        )

    try:
        token = create_access_token(
    subject=str(user.id),
    expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
)

        return token
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_code": "TOKEN_ERROR", "message": "Error al generar el token"}
        )
