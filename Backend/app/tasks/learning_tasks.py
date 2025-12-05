"""
Celery tasks for AI learning and improvement
"""
from celery import shared_task
from sqlalchemy.orm import Session
import logging

from app.database import SessionLocal
from app import models

logger = logging.getLogger(__name__)


@shared_task(name='app.tasks.learning_tasks.update_learning_models')
def update_learning_models():
    """
    Update AI learning models based on feedback
    Runs daily at 2 AM via Celery Beat
    """
    db = SessionLocal()
    try:
        logger.info("Starting learning model update")
        
        # Calculate estimation accuracy
        feedback_records = db.query(models.FeedbackEstimation).all()
        
        if feedback_records:
            total_error = sum(abs(f.estimation_error or 0) for f in feedback_records)
            avg_error = total_error / len(feedback_records)
            acceptance_rate = sum(1 for f in feedback_records if f.was_accepted) / len(feedback_records)
            
            logger.info(
                f"Estimation metrics: {len(feedback_records)} records, "
                f"avg error: {avg_error:.2f}, acceptance rate: {acceptance_rate:.2%}"
            )
        
        # Calculate assignment accuracy
        assignment_records = db.query(models.AssignmentHistory).all()
        
        if assignment_records:
            reassignment_rate = sum(1 for a in assignment_records if a.was_reassigned) / len(assignment_records)
            avg_completion = sum(a.completion_time_days or 0 for a in assignment_records if a.completion_time_days) / len([a for a in assignment_records if a.completion_time_days])
            
            logger.info(
                f"Assignment metrics: {len(assignment_records)} records, "
                f"reassignment rate: {reassignment_rate:.2%}, "
                f"avg completion: {avg_completion:.1f} days"
            )
        
        # TODO: Update vector DB with completed stories
        # TODO: Adjust AI prompts based on patterns
        # TODO: Update scoring weights
        
        return {
            "status": "success",
            "feedback_count": len(feedback_records) if feedback_records else 0,
            "assignment_count": len(assignment_records) if assignment_records else 0
        }
        
    except Exception as e:
        logger.error(f"Error in learning update task: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
