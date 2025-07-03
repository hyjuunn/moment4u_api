from fastapi import APIRouter, HTTPException
from typing import List
from ...services.image_analysis_service import ImageAnalysisService
from ...models.story import Story
from ...models.image import Image

# Initialize the PaligemmaService
image_analysis_service = ImageAnalysisService()

# Create router for Paligemma endpoints
paligemma_router = APIRouter()

@paligemma_router.post(
    "/analyze-images/{story_id}",
    summary="Analyze a list of images using Paligemma model",
    tags=["paligemma"],
    response_model=str
)
async def analyze_images_by_story_id(story_id: str):
    return image_analysis_service.analyze_images_by_story_id(story_id)