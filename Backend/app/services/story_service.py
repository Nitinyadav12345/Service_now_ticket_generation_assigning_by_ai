from sqlalchemy.orm import Session
from uuid import UUID
import logging
from datetime import datetime

from app import models, schemas
from app.services.ai_service import AIService
from app.services.jira_service import JiraService
from app.services.assignment_service import AssignmentService

logger = logging.getLogger(__name__)

class StoryService:
    """Service for story/ticket creation and management"""
    
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()
        self.jira_service = JiraService()
        self.assignment_service = AssignmentService(db)
    
    def create_story_request(self, request: schemas.StoryCreateRequest) -> models.StoryRequest:
        """Create initial story request record"""
        story_request = models.StoryRequest(
            user_prompt=request.prompt,
            issue_type=request.issue_type,
            priority=request.priority,
            project_key=request.project_key,
            epic_key=request.epic_key,
            labels=request.labels,
            status="pending"
        )
        self.db.add(story_request)
        self.db.commit()
        self.db.refresh(story_request)
        return story_request
    
    async def process_story_creation(
        self,
        request_id: UUID,
        request: schemas.StoryCreateRequest
    ):
        """Process story creation (runs in background)"""
        try:
            # Get story request
            story_request = self.db.query(models.StoryRequest).filter(
                models.StoryRequest.request_id == request_id
            ).first()
            
            if not story_request:
                logger.error(f"Story request {request_id} not found")
                return
            
            # Update status
            story_request.status = "processing"
            self.db.commit()
            
            # Step 1: Generate story details using AI
            logger.info(f"Generating story for request {request_id}")
            generated_story = await self.ai_service.generate_story(request.prompt)
            
            story_request.generated_title = generated_story["title"]
            story_request.generated_description = generated_story["description"]
            story_request.acceptance_criteria = generated_story["acceptance_criteria"]
            story_request.technical_requirements = generated_story.get("technical_requirements")
            story_request.required_skills = generated_story.get("required_skills", [])
            self.db.commit()
            
            # Step 2: Estimate story points (if enabled)
            if request.auto_estimate:
                logger.info(f"Estimating story points for request {request_id}")
                estimation = await self.ai_service.estimate_story_points(
                    generated_story["title"],
                    generated_story["description"]
                )
                story_request.estimated_points = estimation["points"]
                self.db.commit()
            
            # Step 3: Create ticket in Jira
            logger.info(f"Creating Jira ticket for request {request_id}")
            jira_issue = self.jira_service.create_issue(
                project_key=request.project_key or "PROJ",
                issue_type=request.issue_type,
                summary=story_request.generated_title,
                description=story_request.generated_description,
                priority=request.priority,
                story_points=story_request.estimated_points,
                labels=request.labels,
                epic_key=request.epic_key
            )
            
            story_request.jira_issue_key = jira_issue.key
            self.db.commit()
            
            # Step 4: Break down into subtasks (if enabled and points > 5)
            subtasks = []
            if request.auto_breakdown and story_request.estimated_points and story_request.estimated_points > 5:
                logger.info(f"Breaking down story {jira_issue.key} into subtasks")
                subtasks = await self.ai_service.breakdown_story(
                    generated_story["title"],
                    generated_story["description"],
                    story_request.estimated_points
                )
                
                # Create subtasks in Jira
                for subtask in subtasks:
                    self.jira_service.create_subtask(
                        parent_key=jira_issue.key,
                        summary=subtask["title"],
                        description=subtask.get("description", ""),
                        story_points=subtask.get("points")
                    )
            
            # Step 5: Assign to team member (if enabled)
            if request.auto_assign:
                logger.info(f"Assigning ticket {jira_issue.key}")
                assignment = await self.assignment_service.assign_ticket(
                    issue_key=jira_issue.key,
                    priority=request.priority,
                    estimated_points=story_request.estimated_points or 5,
                    required_skills=story_request.required_skills or []
                )
                
                if assignment:
                    story_request.assigned_to = assignment["assigned_to"]
                    # Update assignee in Jira
                    self.jira_service.assign_issue(jira_issue.key, assignment["assigned_to"])
                    self.db.commit()
            
            # Mark as completed
            story_request.status = "completed"
            story_request.updated_at = datetime.utcnow()
            self.db.commit()
            
            logger.info(f"Successfully created story {jira_issue.key} for request {request_id}")
            
        except Exception as e:
            logger.error(f"Error processing story creation for {request_id}: {e}")
            story_request.status = "failed"
            story_request.error_message = str(e)
            self.db.commit()
