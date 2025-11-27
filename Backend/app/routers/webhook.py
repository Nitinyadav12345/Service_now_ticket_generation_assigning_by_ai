from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app import models, schemas

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/jira", response_model=schemas.WebhookResponse)
async def jira_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Handle Jira webhooks for learning from human changes
    
    Events handled:
    - issue_updated: Capture estimation changes, reassignments
    - issue_created: Track manually created issues
    """
    try:
        payload = await request.json()
        webhook_event = payload.get("webhookEvent")
        
        logger.info(f"Received Jira webhook: {webhook_event}")
        
        if webhook_event == "jira:issue_updated":
            return await handle_issue_updated(payload, db)
        elif webhook_event == "jira:issue_created":
            return await handle_issue_created(payload, db)
        else:
            return schemas.WebhookResponse(
                status="ignored",
                message=f"Event {webhook_event} not handled"
            )
            
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def handle_issue_updated(payload: dict, db: Session) -> schemas.WebhookResponse:
    """Handle issue update events"""
    try:
        issue = payload.get("issue", {})
        issue_key = issue.get("key")
        changelog = payload.get("changelog", {})
        
        if not changelog:
            return schemas.WebhookResponse(status="ignored", message="No changes")
        
        # Check for estimation changes
        for item in changelog.get("items", []):
            field = item.get("field")
            
            # Story points changed
            if field == "Story Points":
                from_value = item.get("fromString")
                to_value = item.get("toString")
                
                # Find story request
                story_request = db.query(models.StoryRequest).filter(
                    models.StoryRequest.jira_issue_key == issue_key
                ).first()
                
                if story_request:
                    # Create feedback record
                    feedback = models.FeedbackEstimation(
                        issue_key=issue_key,
                        ai_estimated_points=story_request.estimated_points,
                        human_estimated_points=int(to_value) if to_value else None,
                        estimation_error=abs(story_request.estimated_points - int(to_value)) if to_value else 0,
                        was_accepted=False
                    )
                    db.add(feedback)
                    logger.info(f"Captured estimation change for {issue_key}: {from_value} -> {to_value}")
            
            # Assignee changed
            elif field == "assignee":
                from_user = item.get("from")
                to_user = item.get("to")
                
                # Find assignment record
                assignment = db.query(models.AssignmentHistory).filter(
                    models.AssignmentHistory.issue_key == issue_key
                ).first()
                
                if assignment and from_user != to_user:
                    assignment.was_reassigned = True
                    assignment.reassignment_reason = f"Manually reassigned from {from_user} to {to_user}"
                    logger.info(f"Captured reassignment for {issue_key}: {from_user} -> {to_user}")
        
        db.commit()
        
        return schemas.WebhookResponse(
            status="processed",
            message=f"Processed changes for {issue_key}"
        )
        
    except Exception as e:
        logger.error(f"Error handling issue update: {e}")
        return schemas.WebhookResponse(status="error", message=str(e))


async def handle_issue_created(payload: dict, db: Session) -> schemas.WebhookResponse:
    """Handle issue creation events"""
    # Can be used to track manually created issues for learning
    return schemas.WebhookResponse(
        status="received",
        message="Issue creation logged"
    )
