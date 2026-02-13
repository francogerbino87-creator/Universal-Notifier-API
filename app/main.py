"""Main FastAPI application entry point"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events"""
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Universal Notifier API - Sistema de notificaciones multi-canal",
    lifespan=lifespan,
)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint"""
    return {
        "message": "Universal Notifier API is running",
        "version": settings.VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy"}
