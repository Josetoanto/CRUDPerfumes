from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# ==============================
# Password Utilities
# ==============================

def hash_password(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.
    """
    if not password or not password.strip():
        raise ValueError("Password cannot be empty.")

    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.
    """
    if not password or not hashed_password:
        return False

    return pwd_context.verify(password, hashed_password)


# ==============================
# JWT Utilities
# ==============================

def create_access_token(
    subject: str,
    additional_claims: Dict[str, Any] | None = None,
    expires_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
) -> str:
    """
    Creates a signed JWT access token.
    """

    if not subject:
        raise ValueError("Token subject (sub) is required.")

    if not settings.SECRET_KEY:
        raise RuntimeError("SECRET_KEY is not configured.")

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes)

    payload: Dict[str, Any] = {
        "sub": subject,
        "exp": int(expire.timestamp()),   # ✅ timestamp limpio
        "iat": int(now.timestamp()),      # ✅ timestamp limpio
    }

    if additional_claims:
        payload.update(additional_claims)

    try:
        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
    except JWTError as e:
        raise RuntimeError(f"JWT encoding failed: {str(e)}") from e