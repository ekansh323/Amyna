"""
User ORM model.

Passwords are NEVER stored in plain text.  The ``hashed_password`` column
always holds a bcrypt hash produced by ``app.core.security.hash_password()``.
"""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    # email is the login identifier — must be unique and non-null at DB level
    email = Column(String, unique=True, index=True, nullable=False)
    # bcrypt hash — NEVER the plain-text password
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    projects = relationship("Project", back_populates="owner")

