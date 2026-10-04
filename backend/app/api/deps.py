from typing import Generator, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core import security
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import TokenData

# OAuth2 scheme for Swagger UI and token extraction
# The tokenUrl must match the endpoint we create for login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/login")

# Dependency for database session
SessionDep = Annotated[Session, Depends(get_db)]
# Dependency for extracting token from header
TokenDep = Annotated[str, Depends(oauth2_scheme)]

def get_current_user(db: SessionDep, token: TokenDep) -> User:
    """
    Authentication dependency to get the current authenticated user.
    Validates the JWT token, extracts the subject (email), and retrieves the user from DB.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode JWT token
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        # Extract email (subject) from payload
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
        
    # Get user from database using the email
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
        
    return user

# Dependency to inject current user into route handlers
CurrentUser = Annotated[User, Depends(get_current_user)]
