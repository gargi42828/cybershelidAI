
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database.connection import Base, engine
from backend.app.database import models
from backend.app.routers.auth import router as auth_router
from backend.app.routers.scan import router as scan_router


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="CyberShield AI",
    description="AI-Powered Cybersecurity Threat Detection Platform",
    version="1.0.0"
)


# ================================
# CORS CONFIGURATION
# ================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================================
# ROUTES
# ================================

# Register authentication routes
app.include_router(auth_router)

# Register security scan routes
app.include_router(scan_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to CyberShield AI",
        "status": "Backend is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

