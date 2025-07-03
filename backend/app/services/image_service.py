import shutil
from pathlib import Path
from typing import List
from fastapi import UploadFile
from uuid import uuid4
from datetime import datetime
from ..models.image import Image
from loguru import logger

class ImageService:
    
    def __init__(self):
        try:
            # Get the absolute path of the current file
            current_file = Path(__file__)
            # Navigate to backend folder (../../..)
            backend_dir = current_file.parent.parent.parent
            # Set base directory for storing images
            self.base_dir = backend_dir / "images" / "stories"
            # Ensure the base directory exists
            self.base_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Image storage directory initialized at: {self.base_dir}")
        except Exception as e:
            logger.error(f"Error initializing image storage: {str(e)}")
            raise
    
    async def store_story_images(self, images: List[UploadFile]) -> tuple[str, List[str]]:
        """
        Store multiple images for a story in a unique directory
        """
        try:    
            # Generate unique story ID
            story_id = str(uuid4())
            story_dir = self.base_dir / story_id
            
            logger.info(f"Creating directory for story {story_id} at {story_dir}")
            
            # Create directory for this story's images
            story_dir.mkdir(parents=True, exist_ok=True)
            
            saved_paths = []
            
            # Save each image
            for idx, image in enumerate(images, 1):
                try:
                    if not image.filename:
                        raise ValueError(f"Image {idx} has no filename")
                        
                    # Get file extension from original filename
                    ext = Path(image.filename).suffix.lower()
                    if ext not in ['.jpg', '.jpeg', '.png']:
                        raise ValueError(f"Unsupported image format for image {idx}: {ext}")
                    
                    # Create standardized filename: 1.jpg, 2.jpg, etc.
                    filename = f"{idx}.jpg"
                    file_path = story_dir / filename
                    
                    logger.debug(f"Saving image {idx} to {file_path}")
                    
                    # Save the file
                    try:
                        with file_path.open("wb") as buffer:
                            shutil.copyfileobj(image.file, buffer)
                        # Store relative path from backend directory
                        rel_path = str(file_path.relative_to(self.base_dir.parent.parent))
                        saved_paths.append(rel_path)
                        logger.debug(f"Successfully saved image {idx} at {rel_path}")
                    finally:
                        # Make sure to close the uploaded file
                        image.file.close()
                except Exception as e:
                    logger.error(f"Error processing image {idx}: {str(e)}")
                    # Clean up any saved files if there's an error
                    if story_dir.exists():
                        shutil.rmtree(story_dir)
                    raise
            
            return story_id, saved_paths
            
        except Exception as e:
            logger.error(f"Error in store_story_images: {str(e)}")
            # Clean up any created directory if there's an error
            if 'story_dir' in locals() and story_dir.exists():
                shutil.rmtree(story_dir)
            raise
    
    def get_image_path(self, story_id: str, image_number: int) -> str:
        """
        Get the path to a specific image in a story
        """
        if not 1 <= image_number <= 4:
            raise ValueError("Image number must be between 1 and 4")
            
        image_path = self.base_dir / story_id / f"{image_number}.jpg"
        if not image_path.exists():
            raise FileNotFoundError(f"Image {image_number} not found for story {story_id}")
            
        return str(image_path.relative_to(Path("backend")))

    def get_all_images(self) -> List[Image]:
        """
        Get all stored images across all stories.
        Returns a list of Image objects sorted by creation time (newest first).
        """
        images = []
        
        # Check if base directory exists
        if not self.base_dir.exists():
            return images
            
        # Iterate through all story directories
        for story_dir in self.base_dir.iterdir():
            if story_dir.is_dir():
                story_id = story_dir.name
                
                # Get all jpg files in the story directory
                for image_file in story_dir.glob("*.jpg"):
                    # Extract image number from filename (e.g., "1.jpg" -> 1)
                    image_number = int(image_file.stem)
                    
                    # Create Image object with relative path from backend root
                    rel_path = str(image_file.relative_to(self.base_dir.parent.parent))
                    image = Image(
                        story_id=story_id,
                        image_path=rel_path,
                        image_number=image_number,
                        created_at=datetime.fromtimestamp(image_file.stat().st_ctime)
                    )
                    images.append(image)
        
        # Sort by creation time, newest first
        return sorted(images, key=lambda x: x.created_at, reverse=True)

    def get_story_images(self, story_id: str) -> List[Image]:
        """
        Get all images for a specific story.
        Returns a list of Image objects sorted by image number.
        """
        images = []
        story_dir = self.base_dir / story_id
        
        if not story_dir.exists():
            return images
            
        # Get all jpg files in the story directory
        for image_file in story_dir.glob("*.jpg"):
            image_number = int(image_file.stem)
            # Create Image object with relative path from backend root
            rel_path = str(image_file.relative_to(self.base_dir.parent.parent))
            image = Image(
                story_id=story_id,
                image_path=rel_path,
                image_number=image_number,
                created_at=datetime.fromtimestamp(image_file.stat().st_ctime)
            )
            images.append(image)
        
        # Sort by image number
        return sorted(images, key=lambda x: x.image_number)
    
    def get_all_story_ids(self) -> List[str]:
        """
        get all story ids
        """
        story_ids = []
        logger.info(f"Looking for stories in directory: {self.base_dir}")
        
        # Check if directory exists
        if not self.base_dir.exists():
            logger.warning(f"Directory does not exist: {self.base_dir}")
            return story_ids
            
        if not self.base_dir.is_dir():
            logger.warning(f"Path exists but is not a directory: {self.base_dir}")
            return story_ids
            
        # List all items in directory
        try:
            for story_dir in self.base_dir.iterdir():
                if story_dir.is_dir():
                    story_ids.append(story_dir.name)
                    logger.debug(f"Found story directory: {story_dir.name}")
                else:
                    logger.debug(f"Skipping non-directory item: {story_dir}")
                    
            logger.info(f"Total stories found: {len(story_ids)}")
            return story_ids
        except Exception as e:
            logger.error(f"Error reading directory {self.base_dir}: {str(e)}")
            return story_ids
        
    def delete_story_images_by_id(self, story_id: str) -> None:
        """
        delete story images by story id
        """
        logger.info(f"Deleting story images by story id: {story_id}")
        story_dir = self.base_dir / story_id
        try:
            if story_dir.exists():
                shutil.rmtree(story_dir)
            logger.info(f"Story images deleted by story id: {story_id}")
        except Exception as e:
            logger.error(f"Error deleting story images by story id: {story_id}: {str(e)}")
            raise e
        
    def delete_all_story_images(self) -> None:
        """
        delete all story images
        """
        logger.info(f"Deleting all story images")
        try:
            if self.base_dir.exists():
                shutil.rmtree(self.base_dir)
            logger.info(f"All story images deleted")
        except Exception as e:
            logger.error(f"Error deleting all story images: {str(e)}")
            raise e