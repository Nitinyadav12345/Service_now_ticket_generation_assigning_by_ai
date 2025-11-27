from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging

from app.database import get_db
from app import models, schemas

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/dashboard-stats", response_model=schemas.DashboardStats)
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    try:
        # Total stories created
        total_stories = db.query(models.StoryRequest).filter(
            models.StoryRequest.status == "completed"
        ).count()
        
        # Estimation accuracy
        feedback = db.query(models.FeedbackEstimation).filter(
            models.FeedbackEstimation.was_accepted == True
        ).count()
        total_feedback = db.query(models.FeedbackEstimation).count()
        estimation_accuracy = (feedback / total_feedback * 100) if total_feedback > 0 else 0
        
        # Assignment accuracy
        assignments = db.query(models.AssignmentHistory).filter(
            models.AssignmentHistory.was_reassigned == False
        ).count()
        total_assignments = db.query(models.AssignmentHistory).count()
        assignment_accuracy = (assignments / total_assignments * 100) if total_assignments > 0 else 0
        
        # Average completion time
        avg_completion = db.query(
            func.avg(models.AssignmentHistory.completion_time_days)
        ).scalar() or 0
        
        # Team utilization
        members = db.query(models.TeamMember).all()
        total_capacity = sum(m.max_story_points for m in members)
        used_capacity = sum(m.current_story_points for m in members)
        utilization = (used_capacity / total_capacity * 100) if total_capacity > 0 else 0
        
        return schemas.DashboardStats(
            total_stories_created=total_stories,
            estimation_accuracy=round(estimation_accuracy, 1),
            assignment_accuracy=round(assignment_accuracy, 1),
            average_completion_time=round(avg_completion, 1),
            team_utilization=round(utilization, 1)
        )
        
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estimation-accuracy", response_model=schemas.EstimationAccuracy)
async def get_estimation_accuracy(db: Session = Depends(get_db)):
    """Get estimation accuracy metrics"""
    try:
        # Acceptance rate
        accepted = db.query(models.FeedbackEstimation).filter(
            models.FeedbackEstimation.was_accepted == True
        ).count()
        total = db.query(models.FeedbackEstimation).count()
        acceptance_rate = (accepted / total * 100) if total > 0 else 0
        
        # Average error
        avg_error = db.query(
            func.avg(func.abs(models.FeedbackEstimation.estimation_error))
        ).scalar() or 0
        
        # Monthly trend (simplified)
        monthly_trend = []
        
        return schemas.EstimationAccuracy(
            acceptance_rate=round(acceptance_rate, 1),
            average_error=round(avg_error, 1),
            total_estimations=total,
            monthly_trend=monthly_trend
        )
        
    except Exception as e:
        logger.error(f"Error getting estimation accuracy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assignment-accuracy", response_model=schemas.AssignmentAccuracy)
async def get_assignment_accuracy(db: Session = Depends(get_db)):
    """Get assignment accuracy metrics"""
    try:
        # Acceptance rate
        not_reassigned = db.query(models.AssignmentHistory).filter(
            models.AssignmentHistory.was_reassigned == False
        ).count()
        total = db.query(models.AssignmentHistory).count()
        acceptance_rate = (not_reassigned / total * 100) if total > 0 else 0
        
        # Reassignments
        reassignments = total - not_reassigned
        
        # Common patterns (simplified)
        patterns = []
        
        return schemas.AssignmentAccuracy(
            acceptance_rate=round(acceptance_rate, 1),
            total_assignments=total,
            reassignments=reassignments,
            common_reassignment_patterns=patterns
        )
        
    except Exception as e:
        logger.error(f"Error getting assignment accuracy: {e}")
        raise HTTPException(status_code=500, detail=str(e))
