from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from PIL import Image
import requests
from io import BytesIO
import logging

class ImageAnalyzer:
    def __init__(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        
        # 로깅 설정
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _process_image(self, image):
        """이미지 전처리 함수"""
        try:
            # RGB 모드로 변환
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # 적절한 크기로 조정
            max_size = 1000
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            return image
        except Exception as e:
            self.logger.error(f"Image processing error: {str(e)}")
            raise

    async def analyze_image(self, image_url: str):
        try:
            # 이미지 다운로드
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            
            # 이미지 전처리
            processed_image = self._process_image(image)
            
            # 여러 프롬프트 준비
            prompts = [
                ""
            ]
            
            # 각 프롬프트로 시도
            for prompt in prompts:
                try:
                    # 입력 처리
                    if prompt:
                        inputs = self.processor(processed_image, prompt, return_tensors="pt")
                    else:
                        inputs = self.processor(processed_image, return_tensors="pt")
                    
                    # 생성 파라미터 설정
                    out = self.model.generate(
                        **inputs,
                        max_length=100,
                        num_beams=5,
                        min_length=10,
                        length_penalty=1.0,
                        no_repeat_ngram_size=3,
                        temperature=0.7,
                        do_sample=True
                    )
                    
                    description = self.processor.decode(out[0], skip_special_tokens=True)
                    
                    # 결과 검증
                    if description and len(description.strip()) > 10:
                        return {
                            "description": description,
                            "success": True,
                            "prompt_used": prompt if prompt else "no prompt"
                        }
                    
                except Exception as e:
                    self.logger.warning(f"Generation failed with prompt '{prompt}': {str(e)}")
                    continue
            
            # 모든 프롬프트가 실패한 경우
            return {
                "description": "Failed to generate description",
                "success": False,
                "error": "No valid description generated with any prompt"
            }
            
        except Exception as e:
            self.logger.error(f"Image analysis failed: {str(e)}")
            return {
                "description": "Error analyzing image",
                "success": False,
                "error": str(e)
            }