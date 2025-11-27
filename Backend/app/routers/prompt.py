from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from uuid import UUID
import logging

from app.database import get_db
from app import models, schemas
from app.services.story_service import StoryService
from app.services.ai_service import AIService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/create-story", response_model=schemas.StoryCreateResponse)
async def create_story(
    request: schemas.StoryCreateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create a Jira story/ticket from natural language prompt
    
    This endpoint:
    1. Generates story details using AI
    2. Estimates story points (if auto_estimate=True)
    3. Breaks down into subtasks (if auto_breakdown=True and points > 5)
    4. Assigns to team member (if auto_assign=True)
    5. Creates ticket in Jira
    """
    try:
        story_service = StoryService(db)
        
        # Create story request record
        story_request = story_service.create_story_request(request)
        
        # Process in background
        background_tasks.add_task(
            story_service.process_story_creation,
            story_request.request_id,
            request
        )
        
        return schemas.StoryCreateResponse(
            request_id=story_request.request_id,
            status="processing",
            created_at=story_request.created_at
        )
        
    except Exception as e:
        logger.error(f"Error creating story: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/story-status/{request_id}", response_model=schemas.StoryStatusResponse)
async def get_story_status(
    request_id: UUID,
    db: Session = Depends(get_db)
):
    """Get status of story creation request"""
    story_request = db.query(models.StoryRequest).filter(
        models.StoryRequest.request_id == request_id
    ).first()
    
    if not story_request:
        raise HTTPException(status_code=404, detail="Story request not found")
    
    generated_story = None
    if story_request.status == "completed":
        generated_story = schemas.GeneratedStory(
            title=story_request.generated_title,
            description=story_request.generated_description,
            acceptance_criteria=story_request.acceptance_criteria or [],
            technical_requirements=story_request.technical_requirements,
            required_skills=story_request.required_skills or [],
            estimated_points=story_request.estimated_points
        )
    
    return schemas.StoryStatusResponse(
        request_id=story_request.request_id,
        status=story_request.status,
        generated_story=generated_story,
        jira_issue_key=story_request.jira_issue_key,
        error_message=story_request.error_message
    )


@router.post("/chat", response_model=schemas.ChatResponse)
async def chat(
    message: schemas.ChatMessage,
    db: Session = Depends(get_db)
):
    """
    Conversational interface for story creation
    
    Users can chat with AI to create stories interactively
    """
    try:
        ai_service = AIService()
        response = await ai_service.process_chat_message(
            message.message,
            message.session_id,
            message.context
        )
        return response
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suggest-estimation", response_model=schemas.EstimationSuggestionResponse)
async def suggest_estimation(
    request: schemas.EstimationSuggestionRequest,
    db: Session = Depends(get_db)
):
    """
    Get estimation suggestion for existing story
    
    Uses RAG to find similar stories and suggest story points
    """
    try:
        ai_service = AIService()
        suggestion = await ai_service.suggest_estimation(
            request.story_title,
            request.story_description
        )
        return suggestion
    except Exception as e:
        logger.error(f"Error suggesting estimation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
