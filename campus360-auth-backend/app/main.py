"""
CAMPUS360 Authentication Module
Main FastAPI application with Prisma ORM integration
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import admin, admin_users, auth, health, qr_access
from app.utils.auth_utils import prisma


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application
    Handles Prisma client connection on startup and disconnection on shutdown
    """
    # Startup: Connect to database
    await prisma.connect()
    print("✅ Connected to database")
    
    yield
    
    # Shutdown: Disconnect from database
    await prisma.disconnect()
    print("✅ Disconnected from database")


# Initialize FastAPI application
app = FastAPI(
    title="CAMPUS360 - Authentication Module",
    description="Intelligent authentication system with QR-based access control",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(qr_access.router)
app.include_router(admin.router)
app.include_router(admin_users.router)  # Admin user management


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "CAMPUS360 Authentication Module",
        "status": "running",
        "version": "1.0.0"
    }
