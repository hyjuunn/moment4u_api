from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timezone

class StoryDB(BaseModel):
    story_id: str = Field(alias="_id")  # MongoDB의 _id를 story_id로 접근
    story_title: str
    image_urls: List[str]
    story_text: str
    created_at: datetime
    updated_at: datetime

    class Config:
        # _id 필드를 story_id로 alias 사용할 수 있게 함
        populate_by_name = True
        # MongoDB에서 가져올 때 _id를 story_id로 변환
        allow_population_by_field_name = True 