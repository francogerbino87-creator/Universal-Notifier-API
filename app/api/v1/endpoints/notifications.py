"""Notifications CRUD endpoints"""

from datetime import datetime
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.models.notification import NotificationStatus
from app.schemas.notification import (
    NotificationCreate,
    NotificationListResponse,
    NotificationResponse,
    NotificationUpdate,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


def notification_helper(notification: dict) -> dict:
    """Transform MongoDB document to API response format"""
    return {
        "id": str(notification["_id"]),
        "channel": notification["channel"],
        "recipient": notification["recipient"],
        "subject": notification.get("subject"),
        "message": notification["message"],
        "priority": notification["priority"],
        "status": notification["status"],
        "metadata": notification.get("metadata", {}),
        "scheduled_at": notification.get("scheduled_at"),
        "sent_at": notification.get("sent_at"),
        "created_at": notification["created_at"],
        "updated_at": notification["updated_at"],
        "retry_count": notification.get("retry_count", 0),
        "max_retries": notification.get("max_retries", 3),
        "error_message": notification.get("error_message"),
    }


@router.post(
    "/",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new notification",
)
async def create_notification(notification: NotificationCreate) -> NotificationResponse:
    """
    Create a new notification.
    
    - **channel**: Notification channel (email, sms, push, etc.)
    - **recipient**: Recipient identifier
    - **message**: Message content
    - **priority**: Notification priority (low, normal, high, urgent)
    """
    db: AsyncIOMotorDatabase = get_database()
    
    notification_dict = notification.model_dump(exclude_unset=True)
    notification_dict["status"] = NotificationStatus.PENDING
    notification_dict["created_at"] = datetime.utcnow()
    notification_dict["updated_at"] = datetime.utcnow()
    notification_dict["retry_count"] = 0
    
    result = await db.notifications.insert_one(notification_dict)
    
    new_notification = await db.notifications.find_one({"_id": result.inserted_id})
    if not new_notification:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create notification"
        )
    
    return NotificationResponse(**notification_helper(new_notification))


@router.get(
    "/",
    response_model=NotificationListResponse,
    summary="List all notifications",
)
async def list_notifications(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    status: Optional[NotificationStatus] = Query(None, description="Filter by status"),
    channel: Optional[str] = Query(None, description="Filter by channel"),
) -> NotificationListResponse:
    """
    List notifications with pagination and optional filters.
    
    - **page**: Page number (starts at 1)
    - **page_size**: Number of items per page (max 100)
    - **status**: Filter by notification status
    - **channel**: Filter by notification channel
    """
    db: AsyncIOMotorDatabase = get_database()
    
    # Build filter query
    filter_query: dict = {}
    if status:
        filter_query["status"] = status
    if channel:
        filter_query["channel"] = channel
    
    # Get total count
    total = await db.notifications.count_documents(filter_query)
    
    # Calculate pagination
    skip = (page - 1) * page_size
    
    # Fetch notifications
    cursor = db.notifications.find(filter_query).sort("created_at", -1).skip(skip).limit(page_size)
    notifications = await cursor.to_list(length=page_size)
    
    return NotificationListResponse(
        total=total,
        page=page,
        page_size=page_size,
        notifications=[NotificationResponse(**notification_helper(n)) for n in notifications],
    )


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
    summary="Get notification by ID",
)
async def get_notification(notification_id: str) -> NotificationResponse:
    """
    Get a specific notification by ID.
    
    - **notification_id**: MongoDB ObjectId of the notification
    """
    db: AsyncIOMotorDatabase = get_database()
    
    if not ObjectId.is_valid(notification_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid notification ID format"
        )
    
    notification = await db.notifications.find_one({"_id": ObjectId(notification_id)})
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification with ID {notification_id} not found"
        )
    
    return NotificationResponse(**notification_helper(notification))


@router.patch(
    "/{notification_id}",
    response_model=NotificationResponse,
    summary="Update notification",
)
async def update_notification(
    notification_id: str,
    notification_update: NotificationUpdate,
) -> NotificationResponse:
    """
    Update a notification.
    
    - **notification_id**: MongoDB ObjectId of the notification
    - Only provided fields will be updated
    """
    db: AsyncIOMotorDatabase = get_database()
    
    if not ObjectId.is_valid(notification_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid notification ID format"
        )
    
    # Get update data (only set fields)
    update_data = notification_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.notifications.update_one(
        {"_id": ObjectId(notification_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification with ID {notification_id} not found"
        )
    
    updated_notification = await db.notifications.find_one({"_id": ObjectId(notification_id)})
    
    return NotificationResponse(**notification_helper(updated_notification))


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete notification",
)
async def delete_notification(notification_id: str) -> None:
    """
    Delete a notification.
    
    - **notification_id**: MongoDB ObjectId of the notification
    """
    db: AsyncIOMotorDatabase = get_database()
    
    if not ObjectId.is_valid(notification_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid notification ID format"
        )
    
    result = await db.notifications.delete_one({"_id": ObjectId(notification_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification with ID {notification_id} not found"
        )
