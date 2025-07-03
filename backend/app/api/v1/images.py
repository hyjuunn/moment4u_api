from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
from ...services.image_service import ImageService
from ...models.image import Image

# Initialize services
image_service = ImageService()

# Create router for images
image_router = APIRouter()

@image_router.get(
    "/",
    summary="Get all images",
    tags=["images"],
    response_model=List[Image]
)
async def get_images():
    """
    Get all stored images across all stories.
    Returns a list of images sorted by creation time (newest first).
    """
    return image_service.get_all_images()

@image_router.get(
    "/story-ids",
    summary="Get all story ids",
    tags=["images"],
    response_model=List[str]
)
async def get_story_ids():
    return image_service.get_all_story_ids()

@image_router.get(
    "/{story_id}",
    summary="Get images for a specific story",
    tags=["images"],
    response_model=List[Image]
)
async def get_story_images(story_id: str):
    """
    Get all images for a specific story.
    Returns a list of images sorted by image number.
    """
    images = image_service.get_story_images(story_id)
    if not images:
        raise HTTPException(status_code=404, detail=f"No images found for story {story_id}")
    return images

@image_router.post(
    "/upload",
    summary="Upload multiple images",
    tags=["images"],
    response_model=dict
)
async def upload_images(files: List[UploadFile] = File(...)):
    """
    Upload multiple images using form-data.
    Send as form-data with key 'files' containing multiple files.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
        
    try:
        story_id, image_paths = await image_service.store_story_images(files)
        return {
            "story_id": story_id,
            "image_paths": image_paths,
            "image_count": len(files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    
@image_router.delete(
    "/{story_id}",
    summary="Delete story images by story id",
    tags=["images"],
    response_model=None
)
async def delete_story_images_by_id(story_id: str):
    return image_service.delete_story_images_by_id(story_id)

@image_router.delete(
    "/",
    summary="Delete all story images",
    tags=["images"],
    response_model=None
)
async def delete_all_story_images():
    return image_service.delete_all_story_images()

