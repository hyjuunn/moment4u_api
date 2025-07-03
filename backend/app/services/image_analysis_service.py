from pathlib import Path
from typing import List
from uuid import uuid4
from datetime import datetime
from ..models.image import Image
from loguru import logger

class ImageAnalysisService:
    #todo: 이미지 분석 모델 추가 필요
    def __init__(self):
        """
        Initialize the ImageAnalysisService
        """
        pass
    
    def analyze_image(self, image: Image) -> str:
        """
        Analyze an image and return a description using Paligemma model
        """
        pass
    
    def analyze_images_by_story_id(self, story_id: str) -> str:
        """
        Analyze images by story id and return a list of descriptions using Paligemma model
        아직 구현 안해서 그냥 예시 텍스트 반환으로 할게
        """
        output_analysis = "1. 강아지, 들판, 하늘, 파란색, 빛 2. 사람, 카메라, 사진 3. 카페, 커피, 노트북 4. 책상, 따듯함, 방, 집"
        return output_analysis