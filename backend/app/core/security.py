from datetime import datetime, timedelta, timezone
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------
# bcrypt is used because it is intentionally slow (work-factor based), making
# brute-force and rainbow-table attacks computationally expensive.
# "deprecated=auto" automatically re-hashes passwords that use weaker schemes.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """
    Hash a plain-text password using bcrypt.

    The plain password is NEVER stored — only the returned hash reaches the DB.
    """
    return pwd_context.hash(plain_password)


# Alias kept for backward-compatibility with existing call sites (auth.py).
get_password_hash = hash_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a stored bcrypt hash.

    Returns True only if the password matches.  Timing-safe — uses constant-time
    comparison internally to prevent timing-oracle attacks.
    """
    return pwd_context.verify(plain_password, hashed_password)


# ---------------------------------------------------------------------------
# JWT token creation  (verification lives in app/api/deps.py)
# ---------------------------------------------------------------------------

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """
    Generate a signed JWT access token.

    The payload contains:
      - ``sub``: the subject (typically the user's email)
      - ``exp``: UTC expiration timestamp

    The token is signed with JWT_SECRET_KEY using JWT_ALGORITHM (HS256).
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

