import requests
from PIL import Image
from io import BytesIO
import logging
from clarifai.client.model import Model
from ...core.config import CLARIFAI_PAT

class ImageAnalyzer:
    def __init__(self):
        # Clarifai general image recognition model
        self.model_url = "https://clarifai.com/clarifai/main/models/general-image-recognition"
        
        # 로깅 설정
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def analyze_image(self, image_url: str) -> dict:
        """이미지 URL을 받아 Clarifai API를 통해 분석"""
        try:
            self.logger.info(f"🔄 Analyzing image with Clarifai: {image_url}")
            
            # Clarifai 모델 호출
            model = Model(url=self.model_url, pat=CLARIFAI_PAT)
            prediction = model.predict_by_url(url=image_url, input_type="image")
            
            # 결과 파싱
            if (prediction and 
                hasattr(prediction, 'outputs') and 
                prediction.outputs and 
                hasattr(prediction.outputs[0], 'data') and
                hasattr(prediction.outputs[0].data, 'concepts')):
                
                # 상위 10개 컨셉을 콤마로 구분
                concepts = prediction.outputs[0].data.concepts[:10]
                description = ", ".join(c.name for c in concepts)
                
                self.logger.info(f"✅ Generated description: {description}")
                return {
                    "description": description,
                    "success": True,
                    "source": "Clarifai General Recognition"
                }
            else:
                self.logger.warning("⚠️ No valid concepts in Clarifai response")
                return {
                    "description": "Failed to generate description",
                    "success": False,
                    "error": "Invalid response from Clarifai"
                }

        except Exception as e:
            self.logger.error(f"❌ Image analysis failed: {str(e)}")
            return {
                "description": "Error analyzing image",
                "success": False,
                "error": str(e)
            }
