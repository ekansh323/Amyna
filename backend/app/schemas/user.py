"""
User Pydantic schemas.

Schema hierarchy:
  UserBase        — shared fields (name, email)
  ├── UserCreate  — incoming registration request (adds plain password)
  └── UserResponse — outgoing API response (NO password fields)

  UserLogin       — login request body
  UserInDB        — internal representation including hashed_password
                    (never returned to clients)

  Token / TokenData — JWT response and payload schemas
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------

class UserBase(BaseModel):
    """Fields shared across multiple user schemas."""
    name: str
    email: EmailStr


# ---------------------------------------------------------------------------
# Inbound (API → server)
# ---------------------------------------------------------------------------

class UserCreate(UserBase):
    """
    Registration request body.

    ``password`` is the plain-text password supplied by the user.
    It MUST be hashed before being persisted — see security.hash_password().
    """
    password: str


class UserLogin(BaseModel):
    """Login request body (JSON variant; the OAuth2 form variant is in auth.py)."""
    email: EmailStr
    password: str


# ---------------------------------------------------------------------------
# Outbound (server → client)
# ---------------------------------------------------------------------------

class UserResponse(UserBase):
    """
    Public user representation returned by the API.

    ``hashed_password`` is intentionally excluded — passwords are NEVER
    sent back to clients, not even in hashed form.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    # Pydantic v2: allow constructing from SQLAlchemy ORM objects
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Internal (server only — never returned to clients)
# ---------------------------------------------------------------------------

class UserInDB(UserBase):
    """
    Internal schema that includes the hashed password.

    Used by the service layer when loading a full user record from the DB.
    Must NOT be serialised and returned in API responses.
    """
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Token schemas
# ---------------------------------------------------------------------------

class Token(BaseModel):
    """JWT token response returned after successful login."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Decoded JWT payload — used internally by the auth dependency."""
    email: Optional[str] = None

