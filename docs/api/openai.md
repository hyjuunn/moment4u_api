# OpenAI API Documentation

## Base URL
```
/api/v1/openai
```

## Endpoints

### 1. Generate Story
Generate a story from image descriptions using OpenAI GPT.

**Method**: POST  
**Endpoint**: `/generate-story`  
**Tags**: openai

#### Request Body
```json
{
  "imageDescriptions": "A cat sitting on a windowsill watching birds outside. A cat chasing a red laser dot on the floor. A cat sleeping in a sunbeam."
}
```

#### Response
```json
{
  "story": "In a cozy house by the park, there lived a curious orange tabby named Whiskers. One sunny morning, Whiskers perched on his favorite windowsill, his tail twitching with excitement as he watched the sparrows dance through the air. The morning entertainment soon gave way to an afternoon adventure when his human brought out the mysterious red dot. Whiskers pounced and twirled, determined to catch the elusive light. After his energetic pursuit, Whiskers found the perfect spot where golden sunlight streamed through the window. He curled up in the warm beam, purring contentedly as he drifted off to sleep, dreaming of his daily adventures."
}
```

#### Example
```bash
curl -X POST "http://localhost:8000/api/v1/openai/generate-story" \
  -H "Content-Type: application/json" \
  -d '{
    "imageDescriptions": "A cat sitting on a windowsill watching birds outside. A cat chasing a red laser dot on the floor. A cat sleeping in a sunbeam."
  }'
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Image descriptions cannot be empty"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Failed to generate story using OpenAI"
}
```

## Usage Examples

### Python
```python
import requests

# Generate story from image descriptions
story_request = {
    "imageDescriptions": "A sunny beach with palm trees, children playing in the sand..."
}
response = requests.post(
    'http://localhost:8000/api/v1/openai/generate-story',
    json=story_request
)
story = response.json()
```

### JavaScript
```javascript
// Generate story from image descriptions
const storyResponse = await fetch('http://localhost:8000/api/v1/openai/generate-story', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    imageDescriptions: "A sunny beach with palm trees, children playing in the sand..."
  })
});
const story = await storyResponse.json();
```

## Note

The OpenAI integration requires a valid OpenAI API key to be set in the backend's environment variables. Make sure to set the `OPENAI_API_KEY` environment variable before using these endpoints. 