from openai import OpenAI, OpenAIError, AsyncOpenAI
import time
import asyncio
from typing import Dict
import os
from loguru import logger
from ..core.config import OPENAI_API_KEY

class OpenAIService:

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.async_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.prompts_dir = os.path.join(os.path.dirname(__file__), "prompts")

    def _load_prompt(self, prompt_name: str) -> str:
        """
        load prompt from prompts folder
        """
        try:
            prompt_path = os.path.join(self.prompts_dir, prompt_name)
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            raise ValueError(f"Failed to load prompt {prompt_name}: {e}")
        
    def generate_prompt_for_story(self, image_descriptions: str) -> Dict[str, str]:
        """
        Generate prompts for story generation
        """
        SYSTEM_PROMPT = self._load_prompt("story.txt").strip()
        USER_PROMPT = f"""
        Please generate a story based on the following image descriptions:
        {image_descriptions}
        """.strip()
        
        return {
            "system": SYSTEM_PROMPT,
            "user": USER_PROMPT
        }
    
    def generate_prompt_for_story_title(self, story_content: str) -> Dict[str, str]:
        """
        Generate prompts for story title generation
        """
        SYSTEM_PROMPT = self._load_prompt("story_title.txt").strip()
        USER_PROMPT = f"""
        Please generate a title for the following story:
        {story_content}
        """.strip()
        
        return {
            "system": SYSTEM_PROMPT,
            "user": USER_PROMPT
        }
    
    def generate_story(
            self,
            prompts: Dict[str, str],
            retry_count: int = 0,
            max_retries: int = 3,
            base_delay: int = 1,
    ) -> str: 
        """
        LLM output generation with retry logic
        """
        while retry_count < max_retries: 
            try: 
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": prompts["system"]},
                        {"role": "user", "content": prompts["user"]},
                    ],
                    temperature=0.5,
                    max_tokens=3000
                )
                if not response.choices:
                    error_msg = "API response empty"
                    logger.error(error_msg)
                    raise ValueError(error_msg)
                
                return response.choices[0].message.content
            
            except OpenAIError as e:
                wait_time = base_delay * (2 ** retry_count)
                if "rate_limit" in str(e).lower():
                    logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds before retrying...")
                else:
                    logger.warning(f"OpenAI API error: {e}")
                    
                time.sleep(wait_time)
                retry_count += 1

            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise e
            
        error_msg = "Failed to generate story after max retries"
        logger.error(error_msg)
        raise ValueError(error_msg)
