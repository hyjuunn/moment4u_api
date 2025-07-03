from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from .image import Image

class Story(BaseModel):
    story: str

class StoryCreate(BaseModel):
    story_title: str
    story_id: str
    image_urls: List[str]
    story_text: str