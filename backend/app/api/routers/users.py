from fastapi import APIRouter
from app.api.deps import CurrentUser
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: CurrentUser):
    """
    Get current authenticated user.
    """
    return current_user
