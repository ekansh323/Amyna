from fastapi import APIRouter
from app.api.routers import auth, users

router = APIRouter()

router.include_router(auth.router)
router.include_router(users.router)

@router.get("/")
def read_root():
    return {"message": "Aegis Backend API is running"}

@router.get("/health")
def health_check():
    return {"status": "healthy"}
