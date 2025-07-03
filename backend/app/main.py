from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .api.v1.router import router
from .api.v2.router import v2_router
from .db.mongodb import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB
    await db.connect_to_mongo()
    yield
    # Shutdown: Close MongoDB connection
    db.close_mongo_connection()

app = FastAPI(
    title="Moment4U API",
    description="API for generating stories from images using PaLI-Gemma and OpenAI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes
app.include_router(router) 
app.include_router(v2_router)