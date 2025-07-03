from typing import List, Optional
from ..models.story_db import StoryDB
from ..db.mongodb import get_database
from datetime import datetime, timezone
from loguru import logger

class StoryService:
    def __init__(self):
        db = get_database()
        self.collection = db.stories

    async def post_story(self, story_id: str, story_title: str, image_urls: List[str], story_text: str) -> StoryDB:
        """
        Create a new story in the database
        """
        try:
            now = datetime.now(timezone.utc)
            
            story = StoryDB(
                story_id=story_id,
                story_title=story_title,
                image_urls=image_urls,
                story_text=story_text,
                created_at=now,
                updated_at=now
            )
            
            await self.collection.insert_one(story.model_dump(by_alias=True))
            logger.info(f"Created story with ID: {story_id}")
            
            return story
            
        except Exception as e:
            logger.error(f"Error creating story in database: {str(e)}")
            raise e

    async def get_story(self, story_id: str) -> Optional[StoryDB]:
        """
        Get a story by its ID
        """
        try:
            story_dict = await self.collection.find_one({"_id": story_id})
            if story_dict:
                return StoryDB(**story_dict)
            return None
        except Exception as e:
            logger.error(f"Error getting story {story_id}: {str(e)}")
            raise e

    async def get_all_stories(self) -> List[StoryDB]:
        """
        Get all stories, sorted by creation date (newest first)
        """
        try:
            cursor = self.collection.find().sort("created_at", -1)
            stories = []
            async for story_dict in cursor:
                stories.append(StoryDB(**story_dict))
            return stories
        except Exception as e:
            logger.error(f"Error getting all stories: {str(e)}")
            raise e

    async def update_story(self, story_id: str, story_text: str) -> Optional[StoryDB]:
        """
        Update a story's text
        """
        try:
            update_data = {
                "$set": {
                    "story_text": story_text,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
            result = await self.collection.update_one(
                {"_id": story_id},
                update_data
            )
            if result.modified_count:
                return await self.get_story(story_id)
            return None
        except Exception as e:
            logger.error(f"Error updating story {story_id}: {str(e)}")
            raise e
        
    async def update_story_title(self, story_id: str, story_title: str) -> Optional[StoryDB]:
        """
        Update a story's title
        """
        try:
            update_data = {
                "$set": {
                    "story_title": story_title,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
            result = await self.collection.update_one(
                {"_id": story_id},
                update_data
            )
            if result.modified_count:
                return await self.get_story(story_id)
            return None
        except Exception as e:
            logger.error(f"Error updating story title {story_id}: {str(e)}")
            raise e

    async def delete_story(self, story_id: str) -> bool:
        """
        Delete a story by its ID
        """
        try:
            result = await self.collection.delete_one({"_id": story_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting story {story_id}: {str(e)}")
            raise e
        
    async def delete_all_stories(self) -> bool:
        """
        Delete all stories
        """
        try:
            result = await self.collection.delete_many({})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting all stories: {str(e)}")
            raise e
            