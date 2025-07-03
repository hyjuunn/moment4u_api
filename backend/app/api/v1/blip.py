from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
from ...models.blip.blip import ImageAnalyzer

blip_router = APIRouter()

@blip_router.post(
    "/analyze",
    summary="Analyze an image",
    tags=["blip"]
)
async def analyze_image(image_url: str):
    description = await ImageAnalyzer().analyze_image(image_url)
    return description