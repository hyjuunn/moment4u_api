from fastapi import APIRouter
from .images import image_router

v2_router = APIRouter(prefix="/v2")

v2_router.include_router(image_router, prefix="/images", tags=["images-v2"]) 