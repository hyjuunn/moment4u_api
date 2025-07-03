from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from ...services.cloudinary_service import CloudinaryService
from ...models.image import Image
from uuid import uuid4
from datetime import datetime

cloudinary_service = CloudinaryService()

image_router = APIRouter()

@image_router.post(
    "/upload",
    summary="Upload multiple images using Cloudinary",
    tags=["images-v2"],
    response_model=dict
)
async def upload_images(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    try:
        story_id = str(uuid4())
        saved_urls = []
        
        for idx, file in enumerate(files, 1):
            if not file.filename:
                raise HTTPException(status_code=400, detail=f"Image {idx} has no filename")
            
            # Upload to Cloudinary
            image_url = await cloudinary_service.upload_image(file, story_id, idx)
            saved_urls.append(image_url)
        
        return {
            "story_id": story_id,
            "image_urls": saved_urls,
            "image_count": len(files)
        }
    except Exception as e:
        await cloudinary_service.delete_story_images(story_id)
        raise HTTPException(status_code=500, detail=str(e))

@image_router.delete(
    "/{story_id}",
    summary="Delete story images by story id from Cloudinary",
    tags=["images-v2"]
)
async def delete_story_images(story_id: str):
    try:
        await cloudinary_service.delete_story_images(story_id)
        return {"message": f"Successfully deleted all images for story {story_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@image_router.delete(
    "/",
    summary="Delete all images from Cloudinary",
    tags=["images-v2"]
)
async def delete_all_images():
    try:
        await cloudinary_service.delete_all_images()
        return {"message": "Successfully deleted all images"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    
@image_router.get(
    "/story-ids",
    summary="Get all story ids",
    tags=["images-v2"],
    response_model=List[str]
)
async def get_story_ids():
    return await cloudinary_service.get_all_story_ids()

@image_router.get(
    "/{story_id}",
    summary="Get all images for a specific story",
    tags=["images-v2"],
    response_model=List[Image]
)
async def get_story_images(story_id: str):
    return await cloudinary_service.get_story_images(story_id)

@image_router.get(
    "/",
    summary="Get all images",
    tags=["images-v2"],
    response_model=List[Image]
)
async def get_images():
    return await cloudinary_service.get_all_images()