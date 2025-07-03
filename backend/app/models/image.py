from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Image(BaseModel):
    story_id: str
    image_path: str
    image_number: int
    created_at: datetime = datetime.now()
    description: Optional[str] = None 