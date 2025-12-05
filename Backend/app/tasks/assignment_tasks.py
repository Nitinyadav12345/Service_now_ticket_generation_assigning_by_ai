"""
Celery tasks for assignment management
"""
from celery import shared_task
from sqlalchemy.orm import Session
import logging

from app.database import SessionLocal
from app.services.assignment_service import AssignmentService
from app.services.jira_service import JiraService
from app import models

logger = logging.getLogger(__name__)


@shared_task(name='app.tasks.assignment_tasks.process_assignment_queue')
def process_assignment_queue():
    """
    Process queued assignments
    Runs every hour via Celery Beat
    """
    db = SessionLocal()
    try:
        logger.info("Starting assignment queue processing")
        
        assignment_service = AssignmentService(db)
        jira_service = JiraService()
        
        # Get queued items
        queue_items = db.query(models.AssignmentQueue).filter(
            models.AssignmentQueue.status == "queued"
        ).all()
        
        processed = 0
        assigned = 0
        failed = 0
        
        for item in queue_items:
            try:
                processed += 1
                
                # Try to assign
                result = assignment_service.assign_ticket(
                    issue_key=item.issue_key,
                    priority=item.priority,
                    estimated_points=item.estimated_points,
                    required_skills=item.required_skills or []
                )
                
                if result:
                    # Assignment successful
                    item.status = "assigned"
                    assigned += 1
                    
                    # Update in Jira
                    try:
                        jira_service.assign_issue(item.issue_key, result["assigned_to"])
                    except Exception as e:
                        logger.error(f"Failed to update Jira for {item.issue_key}: {e}")
                    
                    logger.info(f"Assigned {item.issue_key} to {result['assigned_to']}")
                else:
                    # Still can't assign
                    item.assignment_attempts += 1
                    failed += 1
                    
                    # Give up after max attempts
                    if item.assignment_attempts >= 10:
                        item.status = "failed"
                        item.reason = "Max assignment attempts reached"
                        logger.warning(f"Giving up on {item.issue_key} after 10 attempts")
                
                from datetime import datetime
                item.last_attempt_at = datetime.utcnow()
                
            except Exception as e:
                logger.error(f"Error processing queue item {item.issue_key}: {e}")
                item.assignment_attempts += 1
                failed += 1
                continue
        
        db.commit()
        
        logger.info(
            f"Queue processing completed: {processed} processed, "
            f"{assigned} assigned, {failed} still queued"
        )
        
        return {
            "status": "success",
            "processed": processed,
            "assigned": assigned,
            "failed": failed
        }
        
    except Exception as e:
        logger.error(f"Error in queue processing task: {e}")
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
