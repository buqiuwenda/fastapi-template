from fastapi import APIRouter
from app.utils import res
router = APIRouter(prefix="/api/v1", tags=["health"])

@router.get("/health")
def health():
    return res(msg="ok")