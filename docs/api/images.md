# Images API Documentation (v2)

## Base URL
```
/api/v2/images
```

## Endpoints

### 1. Upload Images
Upload multiple images using Cloudinary service.

**Method**: POST  
**Endpoint**: `/upload`  
**Tags**: images-v2

#### Request
- Content-Type: multipart/form-data
- Body: Array of image files

#### Response
```json
{
  "story_id": "123e4567-e89b-12d3-a456-426614174000",
  "image_urls": [
    "https://cloudinary.com/v1/stories/123e4567/image1.jpg",
    "https://cloudinary.com/v1/stories/123e4567/image2.jpg"
  ],
  "image_count": 2
}
```

#### Example
```bash
curl -X POST "http://localhost:8000/api/v2/images/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg"
```

### 2. Get Story Images
Retrieve all images for a specific story.

**Method**: GET  
**Endpoint**: `/{story_id}`  
**Tags**: images-v2

#### Parameters
- `story_id` (path parameter, required): The unique identifier of the story

#### Response
```json
[
  {
    "url": "https://cloudinary.com/v1/stories/123e4567/image1.jpg",
    "story_id": "123e4567-e89b-12d3-a456-426614174000",
    "image_number": 1,
    "created_at": "2024-03-21T10:30:00Z"
  },
  {
    "url": "https://cloudinary.com/v1/stories/123e4567/image2.jpg",
    "story_id": "123e4567-e89b-12d3-a456-426614174000",
    "image_number": 2,
    "created_at": "2024-03-21T10:30:00Z"
  }
]
```

#### Example
```bash
curl "http://localhost:8000/api/v2/images/123e4567-e89b-12d3-a456-426614174000"
```

### 3. Get All Images
Retrieve all images across all stories.

**Method**: GET  
**Endpoint**: `/`  
**Tags**: images-v2

#### Response
```json
[
  {
    "url": "https://cloudinary.com/v1/stories/123e4567/image1.jpg",
    "story_id": "123e4567-e89b-12d3-a456-426614174000",
    "image_number": 1,
    "created_at": "2024-03-21T10:30:00Z"
  },
  {
    "url": "https://cloudinary.com/v1/stories/987fcdeb/image1.jpg",
    "story_id": "987fcdeb-a654-12d3-a456-426614174000",
    "image_number": 1,
    "created_at": "2024-03-21T11:30:00Z"
  }
]
```

#### Example
```bash
curl "http://localhost:8000/api/v2/images"
```

### 4. Get Story IDs
Retrieve all story IDs that have images.

**Method**: GET  
**Endpoint**: `/story-ids`  
**Tags**: images-v2

#### Response
```json
[
  "123e4567-e89b-12d3-a456-426614174000",
  "987fcdeb-a654-12d3-a456-426614174000"
]
```

#### Example
```bash
curl "http://localhost:8000/api/v2/images/story-ids"
```

### 5. Delete Story Images
Delete all images for a specific story from Cloudinary.

**Method**: DELETE  
**Endpoint**: `/{story_id}`  
**Tags**: images-v2

#### Parameters
- `story_id` (path parameter, required): The unique identifier of the story

#### Response
```json
{
  "message": "Successfully deleted all images for story 123e4567-e89b-12d3-a456-426614174000"
}
```

#### Example
```bash
curl -X DELETE "http://localhost:8000/api/v2/images/123e4567-e89b-12d3-a456-426614174000"
```

### 6. Delete All Images
Delete all images from Cloudinary.

**Method**: DELETE  
**Endpoint**: `/`  
**Tags**: images-v2

#### Response
```json
{
  "message": "Successfully deleted all images"
}
```

#### Example
```bash
curl -X DELETE "http://localhost:8000/api/v2/images"
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "No files provided"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Failed to upload image to Cloudinary"
}
``` 