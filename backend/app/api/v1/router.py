from fastapi import APIRouter

# Create main v1 router
router = APIRouter(prefix="/api/v1")

# Import routes after router creation to avoid circular imports
from .stories import story_router
from .images import image_router
from .openai import openai_router
from .paligemma import paligemma_router
from .blip import blip_router

# Include all routers
router.include_router(story_router, prefix="/stories", tags=["stories"])
router.include_router(image_router, prefix="/images", tags=["images"])
router.include_router(openai_router, prefix="/openai", tags=["openai"]) 
router.include_router(paligemma_router, prefix="/paligemma", tags=["paligemma"])
router.include_router(blip_router, prefix="/blip", tags=["blip"])