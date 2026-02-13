"""Notification model for MongoDB"""

from datetime import datetime
from enum import Enum
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class NotificationStatus(str, Enum):
    """Notification status enumeration"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    CANCELLED = "cancelled"


class NotificationChannel(str, Enum):
    """Notification channel enumeration"""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    WEBHOOK = "webhook"
    SLACK = "slack"
    TELEGRAM = "telegram"


class NotificationPriority(str, Enum):
    """Notification priority enumeration"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic validation"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class NotificationModel(BaseModel):
    """Base notification model for MongoDB document"""
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    channel: NotificationChannel
    recipient: str = Field(..., description="Recipient identifier (email, phone, user_id, etc.)")
    subject: Optional[str] = Field(None, description="Notification subject/title")
    message: str = Field(..., description="Notification message content")
    priority: NotificationPriority = Field(default=NotificationPriority.NORMAL)
    status: NotificationStatus = Field(default=NotificationStatus.PENDING)
    
    # Metadata
    metadata: Optional[dict] = Field(default_factory=dict, description="Additional metadata")
    scheduled_at: Optional[datetime] = Field(None, description="Schedule notification for future delivery")
    sent_at: Optional[datetime] = Field(None, description="Timestamp when notification was sent")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Retry logic
    retry_count: int = Field(default=0, description="Number of retry attempts")
    max_retries: int = Field(default=3, description="Maximum number of retries")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "channel": "email",
                "recipient": "user@example.com",
                "subject": "Welcome!",
                "message": "Welcome to Universal Notifier API",
                "priority": "normal",
                "metadata": {"campaign_id": "123", "user_id": "456"}
            }
        }
