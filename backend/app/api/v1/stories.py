from fastapi import APIRouter, HTTPException
from typing import List
from ...models.story import Story, StoryCreate
from ...models.story_db import StoryDB
from ...services.story_service import StoryService
from pydantic import BaseModel

story_router = APIRouter()
story_service = StoryService()

@story_router.post(
    "/",
    summary="Create a new story",
    tags=["stories"],
    response_model=StoryCreate
)
async def create_story(story_data: StoryCreate):
    try:
        story = await story_service.post_story(
            story_title=story_data.story_title,
            story_id=story_data.story_id,
            image_urls=story_data.image_urls,
            story_text=story_data.story_text
        )
        return story
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@story_router.put(
    "/{story_id}",
    summary="Update a story",
    tags=["stories"]
)
async def update_story(story_id: str, story_text: str):
    story = await story_service.update_story(story_id, story_text)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@story_router.put(
    "/{story_id}/title",
    summary="Update a story's title",
    tags=["stories"]
)
async def update_story_title(story_id: str, story_title: str):
    story = await story_service.update_story_title(story_id, story_title)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@story_router.get(
    "/{story_id}",
    summary="Get a story by ID",
    tags=["stories"]
)
async def get_story(story_id: str):
    story = await story_service.get_story(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@story_router.get(
    "/",
    summary="Get all stories",
    tags=["stories"]
)
async def get_all_stories():
    try:
        stories = await story_service.get_all_stories()
        return stories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@story_router.delete(
    "/{story_id}",
    summary="Delete a story by ID",
    tags=["stories"]
)
async def delete_story(story_id: str):
    try:
        success = await story_service.delete_story(story_id)
        if not success:
            raise HTTPException(status_code=404, detail="Story not found")
        return {"message": "Story deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@story_router.delete(
    "/",
    summary="Delete all stories",
    tags=["stories"]
)
async def delete_all_stories():
    try:
        success = await story_service.delete_all_stories()
        return {"message": "All stories deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

