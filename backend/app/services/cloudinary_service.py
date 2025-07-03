import cloudinary
import cloudinary.uploader
import cloudinary.api
from fastapi import UploadFile
from typing import List
from loguru import logger
from ..core.config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
from datetime import datetime
from ..models.image import Image

class CloudinaryService:
    def __init__(self):
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET
        )
        logger.info("Cloudinary service initialized")

    async def upload_image(self, file: UploadFile, story_id: str, image_number: int) -> str:
        """
        Upload an image to Cloudinary
        Returns: Cloudinary URL of the uploaded image
        """
        try:
            # Create the upload path similar to current structure
            public_id = f"stories/{story_id}/{image_number}"
            
            # Upload the file to cloudinary
            result = cloudinary.uploader.upload(
                file.file,
                public_id=public_id,
                folder="googleml",  # Base folder for all uploads
                resource_type="image"
            )
            
            logger.info(f"Successfully uploaded image to Cloudinary: {result['secure_url']}")
            return result['secure_url']
            
        except Exception as e:
            logger.error(f"Error uploading to Cloudinary: {str(e)}")
            raise

    async def delete_story_images(self, story_id: str):
        """
        Delete all images for a specific story
        """
        try:
            # Delete all resources with the story_id prefix
            prefix = f"googleml/stories/{story_id}"
            result = cloudinary.api.delete_resources_by_prefix(prefix)
            logger.info(f"Successfully deleted images for story {story_id}")
            return result
        except Exception as e:
            logger.error(f"Error deleting images from Cloudinary: {str(e)}")
            raise

    async def delete_all_images(self):
        """
        Delete all images in the googleml/stories folder
        """
        try:
            prefix = "googleml/stories"
            result = cloudinary.api.delete_resources_by_prefix(prefix)
            logger.info("Successfully deleted all images")
            return result
        except Exception as e:
            logger.error(f"Error deleting all images from Cloudinary: {str(e)}")
            raise 

    async def get_story_images(self, story_id: str) -> List[Image]:
        """
        Get all images for a specific story.
        """
        try:
            prefix = f"googleml/stories/{story_id}"
            result = cloudinary.api.resources(
                type="upload",
                prefix=prefix,
                max_results=500
            )
            images = []
            for resource in result.get('resources', []):
                # Extract image_number from public_id
                # Format: googleml/stories/{story_id}/{image_number}
                parts = resource['public_id'].split('/')
                image_number = int(parts[-1])
                
                image = Image(
                    story_id=story_id,
                    image_path=resource['secure_url'],
                    image_number=image_number,
                    created_at=datetime.strptime(resource['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                )
                images.append(image)
            
            # Sort by creation time, newest first
            return sorted(images, key=lambda x: x.created_at, reverse=True)
        except Exception as e:
            logger.error(f"Error getting images from Cloudinary: {str(e)}")
            raise

    async def get_all_images(self) -> List[Image]:
        """
        Get all images from Cloudinary
        Returns a list of Image objects
        """
        try:
            # Get all resources in the googleml/stories folder
            result = cloudinary.api.resources(
                type="upload",
                prefix="googleml/stories",
                max_results=500
            )
            
            images = []
            for resource in result.get('resources', []):
                # Extract story_id and image_number from public_id
                # Format: googleml/stories/{story_id}/{image_number}
                parts = resource['public_id'].split('/')
                story_id = parts[-2]
                image_number = int(parts[-1])
                
                # Create Image object
                image = Image(
                    story_id=story_id,
                    image_path=resource['secure_url'],  # Use secure HTTPS URL
                    image_number=image_number,
                    created_at=datetime.strptime(resource['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                )
                images.append(image)
            
            # Sort by creation time, newest first
            return sorted(images, key=lambda x: x.created_at, reverse=True)
            
        except Exception as e:
            logger.error(f"Error getting images from Cloudinary: {str(e)}")
            raise

    async def get_all_story_ids(self) -> List[str]:
        """
        get all story ids
        """
        # 중복 방지 set 으로 처리함
        story_ids_set = set()
        story_ids = []
        logger.info(f"Looking for stories in Cloudinary")

        try:
            result = cloudinary.api.resources(
                type="upload",
                prefix="googleml/stories",
                max_results=500
            )

            for resource in result.get('resources', []):
                story_ids_set.add(resource['public_id'].split('/')[-2])

            story_ids = list(story_ids_set)

            return story_ids
            
        except Exception as e:
            logger.error(f"Error getting story ids from Cloudinary: {str(e)}")
            return story_ids


        

