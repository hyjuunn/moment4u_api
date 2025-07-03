# GoogleML Project

AI-powered story generation and image creation project using OpenAI and other models.

## Project Structure

```
GoogleML/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   │   └── v1/         # API version 1
│   │   ├── core/           # Core configurations
│   │   ├── db/             # Database connections
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── images/             # Generated images storage
│   ├── requirements.txt    # Python dependencies
│   └── run.sh             # Backend startup script
│
├── frontend/               # React Frontend
│   ├── public/            # Static files
│   ├── src/               # Source code
│   ├── package.json       # Node dependencies
│   └── tsconfig.json      # TypeScript configuration
│
└── ml/                    # Machine Learning
    ├── data/              # Dataset storage
    ├── inference/         # Model inference
    └── training/          # Model training
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB
- OpenAI API Key

## Setup Instructions

### Backend Setup

1. Create and activate virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file in backend directory:
```env
MONGODB_URL=mongodb://localhost:27017
OPENAI_API_KEY=your_api_key_here
```

4. Run the backend:
```bash
./run.sh  # On Windows: run.sh
# Or alternatively:
uvicorn app.main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Create `.env` file in frontend directory:
```env
REACT_APP_API_URL=http://localhost:8000
```

3. Run the frontend:
```bash
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## API Documentation

The API documentation is available at `/docs` endpoint when the backend server is running. It provides detailed information about all available endpoints and their usage.

## Features

- Story Generation using OpenAI GPT models
- Image Generation for stories
- Story and Image Management
- Interactive User Interface

