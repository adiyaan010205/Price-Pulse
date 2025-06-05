from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .db.database import engine, Base
from .routes.tracker import router as tracker_router
from .services.scheduler import price_scheduler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting up...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Start the price scheduler
    price_scheduler.start()
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    price_scheduler.stop()

app = FastAPI(
    title="Price Tracker API",
    description="A comprehensive price tracking application",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tracker_router)

@app.get("/")
def read_root():
    return {"message": "Price Tracker API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
