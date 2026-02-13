"""Notification schemas for request/response validation"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.models.notification import (
    NotificationChannel,
    NotificationPriority,
    NotificationStatus,
)


class NotificationCreate(BaseModel):
    """Schema for creating a new notification"""
    
    channel: NotificationChannel = Field(..., description="Notification channel")
    recipient: str = Field(..., min_length=1, description="Recipient identifier")
    subject: Optional[str] = Field(None, max_length=200, description="Subject/title")
    message: str = Field(..., min_length=1, description="Message content")
    priority: NotificationPriority = Field(default=NotificationPriority.NORMAL)
    metadata: Optional[dict] = Field(default_factory=dict)
    scheduled_at: Optional[datetime] = Field(None, description="Schedule for later")
    max_retries: int = Field(default=3, ge=0, le=10)
    
    @field_validator("recipient")
    @classmethod
    def validate_recipient(cls, v: str) -> str:
        """Validate recipient format"""
        if not v or not v.strip():
            raise ValueError("Recipient cannot be empty")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "channel": "email",
                "recipient": "user@example.com",
                "subject": "Welcome!",
                "message": "Welcome to our platform",
                "priority": "normal",
                "metadata": {"user_id": "123"}
            }
        }


class NotificationUpdate(BaseModel):
    """Schema for updating a notification"""
    
    status: Optional[NotificationStatus] = None
    subject: Optional[str] = Field(None, max_length=200)
    message: Optional[str] = None
    priority: Optional[NotificationPriority] = None
    scheduled_at: Optional[datetime] = None
    metadata: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "sent",
                "priority": "high"
            }
        }


class NotificationResponse(BaseModel):
    """Schema for notification response"""
    
    id: str = Field(..., description="Notification ID")
    channel: NotificationChannel
    recipient: str
    subject: Optional[str] = None
    message: str
    priority: NotificationPriority
    status: NotificationStatus
    metadata: dict
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    retry_count: int
    max_retries: int
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "channel": "email",
                "recipient": "user@example.com",
                "subject": "Welcome!",
                "message": "Welcome to our platform",
                "priority": "normal",
                "status": "pending",
                "metadata": {},
                "created_at": "2026-02-13T10:00:00Z",
                "updated_at": "2026-02-13T10:00:00Z",
                "retry_count": 0,
                "max_retries": 3
            }
        }


class NotificationListResponse(BaseModel):
    """Schema for paginated notification list"""
    
    total: int = Field(..., description="Total number of notifications")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    notifications: list[NotificationResponse] = Field(..., description="List of notifications")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total": 100,
                "page": 1,
                "page_size": 10,
                "notifications": []
            }
        }
