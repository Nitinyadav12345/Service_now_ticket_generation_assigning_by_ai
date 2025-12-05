"""
Celery tasks for capacity management
"""
from celery import shared_task
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from app.database import SessionLocal
from app.services.jira_service import JiraService
from app import models

logger = logging.getLogger(__name__)


@shared_task(name='app.tasks.capacity_tasks.sync_team_capacity')
def sync_team_capacity():
    """
    Sync team capacity from Jira
    Runs every 15 minutes via Celery Beat
    """
    db = SessionLocal()
    try:
        logger.info("Starting automatic capacity sync from Jira")
        
        jira_service = JiraService()
        sprint_info = jira_service.get_active_sprint()
        
        members = db.query(models.TeamMember).all()
        synced_count = 0
        
        for member in members:
            try:
                # Get current workload
                sprint_id = sprint_info.get("id") if sprint_info else None
                workload = jira_service.get_user_workload(member.username, sprint_id)
                
                # Update workload
                member.current_story_points = workload["story_points"]
                member.current_ticket_count = workload["ticket_count"]
                
                # Recalculate status
                if member.max_story_points > 0:
                    utilization = (member.current_story_points / member.max_story_points) * 100
                    if utilization >= 100:
                        member.availability_status = "overloaded"
                    elif utilization >= 75:
                        member.availability_status = "busy"
                    else:
                        member.availability_status = "available"
                
                synced_count += 1
                
            except Exception as e:
                logger.error(f"Error syncing capacity for {member.username}: {e}")
                continue
        
        db.commit()
        logger.info(f"Capacity sync completed: {synced_count} members updated")
        
        return {
            "status": "success",
            "synced_count": synced_count,
            "sprint": sprint_info.get("name") if sprint_info else None
        }
        
    except Exception as e:
        logger.error(f"Error in capacity sync task: {e}")
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


@shared_task(name='app.tasks.capacity_tasks.cleanup_old_data')
def cleanup_old_data():
    """
    Cleanup old data (older than 6 months)
    Runs weekly on Sunday at 3 AM
    """
    db = SessionLocal()
    try:
        logger.info("Starting data cleanup")
        
        cutoff_date = datetime.utcnow() - timedelta(days=180)  # 6 months
        
        # Cleanup old story requests
        deleted_stories = db.query(models.StoryRequest).filter(
            models.StoryRequest.created_at < cutoff_date,
            models.StoryRequest.status.in_(["completed", "failed"])
        ).delete()
        
        # Cleanup old assignment history
        deleted_assignments = db.query(models.AssignmentHistory).filter(
            models.AssignmentHistory.created_at < cutoff_date
        ).delete()
        
        # Cleanup old OOO records
        deleted_ooo = db.query(models.TeamMemberOOO).filter(
            models.TeamMemberOOO.end_date < cutoff_date
        ).delete()
        
        db.commit()
        
        logger.info(
            f"Cleanup completed: {deleted_stories} stories, "
            f"{deleted_assignments} assignments, {deleted_ooo} OOO records"
        )
        
        return {
            "status": "success",
            "deleted_stories": deleted_stories,
            "deleted_assignments": deleted_assignments,
            "deleted_ooo": deleted_ooo
        }
        
    except Exception as e:
        logger.error(f"Error in cleanup task: {e}")
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
