# Paligemma API Documentation

## Base URL
```
/api/v1/paligemma
```

## Endpoints

### 1. Analyze Images
Analyze a list of images using Paligemma model for a specific story.

**Method**: POST  
**Endpoint**: `/analyze-images/{story_id}`  
**Tags**: paligemma

#### Parameters
- `story_id` (path parameter, required): The unique identifier of the story whose images need to be analyzed

#### Response
```json
{
  "analysis": "A series of images depicting a playful cat throughout the day. The first image shows a ginger cat observing birds from a window perch, displaying typical feline hunting behavior. In the second image, the same cat is engaged in play, chasing a red laser pointer dot across a hardwood floor. The final image captures the cat in a peaceful moment of rest, curled up in a patch of sunlight streaming through the window."
}
```

#### Example
```bash
curl -X POST "http://localhost:8000/api/v1/paligemma/analyze-images/123e4567-e89b-12d3-a456-426614174000"
```

## Error Responses

### 404 Not Found
```json
{
  "detail": "Story not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Failed to analyze images using Paligemma model"
}
``` 