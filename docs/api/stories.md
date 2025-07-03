# Stories API Documentation

## Base URL
```
/api/v1/stories
```

## Endpoints

### 1. Create Story
Create a new story with images and text.

**Method**: POST  
**Endpoint**: `/`  
**Tags**: stories

#### Request Body
```json
{
  "story_id": "string",
  "image_urls": [
    "https://cloudinary.com/example1.jpg",
    "https://cloudinary.com/example2.jpg"
  ],
  "story_text": "Once upon a time..."
}
```

#### Response
```json
{
  "story_id": "123e4567-e89b-12d3-a456-426614174000",
  "image_urls": [
    "https://cloudinary.com/example1.jpg",
    "https://cloudinary.com/example2.jpg"
  ],
  "story_text": "Once upon a time...",
  "created_at": "2024-03-21T10:30:00Z",
  "updated_at": "2024-03-21T10:30:00Z"
}
```

#### Example
```bash
curl -X POST "http://localhost:8000/api/v1/stories" \
  -H "Content-Type: application/json" \
  -d '{
    "story_id": "123e4567-e89b-12d3-a456-426614174000",
    "image_urls": [
      "https://cloudinary.com/example1.jpg",
      "https://cloudinary.com/example2.jpg"
    ],
    "story_text": "Once upon a time..."
  }'
```

### 2. Get Story by ID
Retrieve a specific story by its ID.

**Method**: GET  
**Endpoint**: `/{story_id}`  
**Tags**: stories

#### Parameters
- `story_id` (path parameter, required): The unique identifier of the story

#### Response
```json
{
  "story_id": "123e4567-e89b-12d3-a456-426614174000",
  "image_urls": [
    "https://cloudinary.com/example1.jpg",
    "https://cloudinary.com/example2.jpg"
  ],
  "story_text": "Once upon a time...",
  "created_at": "2024-03-21T10:30:00Z",
  "updated_at": "2024-03-21T10:30:00Z"
}
```

#### Example
```bash
curl "http://localhost:8000/api/v1/stories/123e4567-e89b-12d3-a456-426614174000"
```

### 3. Get All Stories
Retrieve all stories.

**Method**: GET  
**Endpoint**: `/`  
**Tags**: stories

#### Response
```json
[
  {
    "story_id": "123e4567-e89b-12d3-a456-426614174000",
    "image_urls": [
      "https://cloudinary.com/example1.jpg",
      "https://cloudinary.com/example2.jpg"
    ],
    "story_text": "Once upon a time...",
    "created_at": "2024-03-21T10:30:00Z",
    "updated_at": "2024-03-21T10:30:00Z"
  },
  {
    "story_id": "987fcdeb-a654-12d3-a456-426614174000",
    "image_urls": [
      "https://cloudinary.com/example3.jpg"
    ],
    "story_text": "In a galaxy far far away...",
    "created_at": "2024-03-21T11:30:00Z",
    "updated_at": "2024-03-21T11:30:00Z"
  }
]
```

#### Example
```bash
curl "http://localhost:8000/api/v1/stories"
```

### 4. Delete Story
Delete a specific story by its ID.

**Method**: DELETE  
**Endpoint**: `/{story_id}`  
**Tags**: stories

#### Parameters
- `story_id` (path parameter, required): The unique identifier of the story

#### Response
```json
{
  "message": "Story deleted successfully"
}
```

#### Example
```bash
curl -X DELETE "http://localhost:8000/api/v1/stories/123e4567-e89b-12d3-a456-426614174000"
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
  "detail": "Internal server error message"
}
``` 