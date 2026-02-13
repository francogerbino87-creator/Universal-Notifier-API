"""Main FastAPI application entry point"""

from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Universal Notifier API - Sistema de notificaciones multi-canal",
)


@app.get("/")
async def root() -> dict[str, str]:
    """Health check endpoint"""
    return {"message": "Universal Notifier API is running", "version": settings.VERSION}


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy"}
