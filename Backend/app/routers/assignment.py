from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app import models, schemas
from app.services.assignment_service import AssignmentService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/assign-ticket", response_model=schemas.AssignmentResponse)
async def assign_ticket(
    request: schemas.AssignmentRequest,
    db: Session = Depends(get_db)
):
    """Manually trigger ticket assignment"""
    try:
        assignment_service = AssignmentService(db)
        result = await assignment_service.assign_ticket(
            issue_key=request.issue_key,
            priority=request.priority,
            estimated_points=request.estimated_points,
            required_skills=request.required_skills
        )
        
        if not result:
            raise HTTPException(
                status_code=400,
                detail="Could not assign ticket - no available team members"
            )
        
        return result
        
    except Exception as e:
        logger.error(f"Error assigning ticket: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/queue", response_model=schemas.AssignmentQueueResponse)
async def get_assignment_queue(db: Session = Depends(get_db)):
    """Get current assignment queue"""
    try:
        queue_items = db.query(models.AssignmentQueue).filter(
            models.AssignmentQueue.status == "queued"
        ).order_by(models.AssignmentQueue.created_at).all()
        
        from datetime import datetime
        
        items = []
        for item in queue_items:
            # Calculate waiting time
            waiting_seconds = (datetime.utcnow() - item.created_at).total_seconds()
            if waiting_seconds < 3600:
                waiting_time = f"{int(waiting_seconds / 60)} minutes"
            else:
                waiting_time = f"{int(waiting_seconds / 3600)} hours"
            
            items.append(schemas.AssignmentQueueItem(
                issue_key=item.issue_key,
                priority=item.priority,
                estimated_points=item.estimated_points,
                attempts=item.assignment_attempts,
                reason=item.reason,
                created_at=item.created_at,
                waiting_time=waiting_time
            ))
        
        return schemas.AssignmentQueueResponse(
            queued_count=len(items),
            items=items
        )
        
    except Exception as e:
        logger.error(f"Error getting assignment queue: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process-queue")
async def process_assignment_queue(db: Session = Depends(get_db)):
    """Process queued assignments"""
    try:
        assignment_service = AssignmentService(db)
        
        queue_items = db.query(models.AssignmentQueue).filter(
            models.AssignmentQueue.status == "queued"
        ).all()
        
        processed = 0
        failed = 0
        
        for item in queue_items:
            result = await assignment_service.assign_ticket(
                issue_key=item.issue_key,
                priority=item.priority,
                estimated_points=item.estimated_points,
                required_skills=item.required_skills or []
            )
            
            if result:
                item.status = "assigned"
                processed += 1
            else:
                item.assignment_attempts += 1
                failed += 1
            
            from datetime import datetime
            item.last_attempt_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "status": "success",
            "processed": processed,
            "failed": failed,
            "message": f"Processed {processed} assignments, {failed} still queued"
        }
        
    except Exception as e:
        logger.error(f"Error processing queue: {e}")
        raise HTTPException(status_code=500, detail=str(e))
