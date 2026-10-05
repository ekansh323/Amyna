"""
M3.1 — Authentication Foundation Verification Script
=====================================================
Run from the backend/ directory with the venv activated:

    python verify_m3_1.py

This script verifies the auth foundation WITHOUT hitting any HTTP endpoints.
It checks:
  1. Config loads JWT settings from environment / defaults
  2. User model imports cleanly
  3. User Pydantic schemas validate correctly
  4. hash_password() produces a non-plaintext hash
  5. verify_password() returns True for correct password
  6. verify_password() returns False for wrong password
  7. The hash is never equal to the plain password
"""
import sys


def section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def ok(msg: str) -> None:
    print(f"  OK  {msg}")


def fail(msg: str) -> None:
    print(f"  FAIL  {msg}")
    sys.exit(1)


# ---------------------------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------------------------
section("1. Configuration (JWT settings)")
try:
    from app.core.config import settings

    assert settings.JWT_SECRET_KEY, "JWT_SECRET_KEY is empty"
    assert settings.JWT_ALGORITHM == "HS256", f"Unexpected algorithm: {settings.JWT_ALGORITHM}"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0, "Token expiry must be positive"
    ok(f"JWT_SECRET_KEY loaded  (len={len(settings.JWT_SECRET_KEY)})")
    ok(f"JWT_ALGORITHM          = {settings.JWT_ALGORITHM}")
    ok(f"ACCESS_TOKEN_EXPIRE_MINUTES = {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
except Exception as exc:
    fail(f"Config failed: {exc}")

# ---------------------------------------------------------------------------
# 2. User model import
# ---------------------------------------------------------------------------
section("2. User SQLAlchemy model")
try:
    from app.models.user import User  # noqa: F401

    # Verify the expected columns exist on the model
    mapper = User.__mapper__
    column_names = {c.key for c in mapper.columns}
    required = {"id", "name", "email", "hashed_password", "created_at", "updated_at"}
    missing = required - column_names
    if missing:
        fail(f"User model missing columns: {missing}")
    ok(f"User model columns: {sorted(column_names)}")

    # Confirm hashed_password is non-nullable at DB level
    hp_col = mapper.columns["hashed_password"]
    assert not hp_col.nullable, "hashed_password must be non-nullable"
    ok("hashed_password column is non-nullable")

    email_col = mapper.columns["email"]
    assert email_col.unique, "email column must be unique"
    assert not email_col.nullable, "email must be non-nullable"
    ok("email column is unique and non-nullable")
except Exception as exc:
    fail(f"User model check failed: {exc}")

# ---------------------------------------------------------------------------
# 3. Pydantic schemas
# ---------------------------------------------------------------------------
section("3. Pydantic schemas")
try:
    from app.schemas.user import (
        Token,
        TokenData,
        UserCreate,
        UserInDB,
        UserLogin,
        UserResponse,
    )

    # UserCreate should accept name + email + password
    uc = UserCreate(name="Test User", email="test@example.com", password="s3cr3t!")
    assert uc.name == "Test User"
    assert uc.email == "test@example.com"
    assert uc.password == "s3cr3t!"
    ok("UserCreate validated correctly")

    # UserCreate must NOT expose a hashed_password field
    assert not hasattr(uc, "hashed_password"), "UserCreate must not have hashed_password"
    ok("UserCreate does not contain hashed_password field")

    # UserResponse must NOT expose password fields
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc)
    ur = UserResponse(
        id=1,
        name="Test User",
        email="test@example.com",
        created_at=now,
        updated_at=now,
    )
    response_dict = ur.model_dump()
    assert "hashed_password" not in response_dict, "UserResponse must NOT contain hashed_password"
    assert "password" not in response_dict, "UserResponse must NOT contain plain password"
    ok("UserResponse does not leak any password field")

    ok("All schemas import and validate successfully")
except Exception as exc:
    fail(f"Schema check failed: {exc}")

# ---------------------------------------------------------------------------
# 4. Password hashing
# ---------------------------------------------------------------------------
section("4. Password hashing (hash_password / verify_password)")
try:
    from app.core.security import hash_password, verify_password, get_password_hash

    plain = "SuperSecretPassword123!"
    hashed = hash_password(plain)

    # Hash must not equal the plain password
    assert hashed != plain, "CRITICAL: hash equals plain password — no hashing occurred!"
    ok(f"hash_password() produced a hash  (len={len(hashed)})")

    # Hash must look like a bcrypt hash
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$"), (
        f"Hash does not look like a bcrypt hash: {hashed[:10]}"
    )
    ok("Hash starts with bcrypt prefix ($2b$ or $2a$)")

    # Correct password must verify
    assert verify_password(plain, hashed), "verify_password returned False for correct password!"
    ok("verify_password() returns True for the correct password")

    # Wrong password must NOT verify
    assert not verify_password("WrongPassword!", hashed), (
        "CRITICAL: verify_password returned True for the WRONG password!"
    )
    ok("verify_password() returns False for an incorrect password")

    # Hashing the same password twice must produce different hashes (salt)
    hashed2 = hash_password(plain)
    assert hashed != hashed2, "Two hashes of the same password are identical — missing salt!"
    ok("Two hashes of the same password differ (unique salt confirmed)")

    # get_password_hash is an alias — must work identically
    hashed3 = get_password_hash(plain)
    assert verify_password(plain, hashed3), "get_password_hash alias does not produce a valid hash"
    ok("get_password_hash() alias works correctly")

except Exception as exc:
    fail(f"Password hashing check failed: {exc}")

# ---------------------------------------------------------------------------
# 5. Summary
# ---------------------------------------------------------------------------
section("RESULT — All M3.1 checks passed")
print("""
  What this confirms:
    * JWT config loads from environment / defaults
    * User model has all required columns with correct DB-level constraints
    * Pydantic schemas validate and never expose passwords in API responses
    * hash_password() produces bcrypt hashes (never stores plaintext)
    * verify_password() correct for right/wrong passwords
    * Each hash uses a unique salt (two hashes of same password differ)
""")
