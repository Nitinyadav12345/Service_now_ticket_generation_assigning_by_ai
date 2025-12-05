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
            epic_key=None,  # Removed epic_key, using sprint_id instead
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
                project_key=request.project_key,
                issue_type=request.issue_type,
                summary=story_request.generated_title,
                description=story_request.generated_description,
                priority=request.priority,
                story_points=story_request.estimated_points,
                labels=request.labels,
                epic_key=None  # Removed epic support, using sprint_id instead
            )
            
            story_request.jira_issue_key = jira_issue.key
            self.db.commit()
            
            # Step 4: Break down into subtasks (if enabled and points > 5)
            subtasks = []
            created_subtask_keys = []
            if request.auto_breakdown and story_request.estimated_points and story_request.estimated_points > 5:
                logger.info(f"Breaking down story {jira_issue.key} into subtasks (estimated points: {story_request.estimated_points})")
                try:
                    subtasks = await self.ai_service.breakdown_story(
                        generated_story["title"],
                        generated_story["description"],
                        story_request.estimated_points
                    )
                    
                    logger.info(f"AI generated {len(subtasks)} subtasks")
                    
                    # Create subtasks in Jira
                    for idx, subtask in enumerate(subtasks, 1):
                        try:
                            logger.info(f"Creating subtask {idx}/{len(subtasks)}: {subtask.get('title', 'N/A')}")
                            subtask_issue = self.jira_service.create_subtask(
                                parent_key=jira_issue.key,
                                summary=subtask["title"],
                                description=subtask.get("description", ""),
                                story_points=subtask.get("points")
                            )
                            if subtask_issue:
                                created_subtask_keys.append({
                                    "key": subtask_issue.key,
                                    "points": subtask.get("points", 1),
                                    "category": subtask.get("category", "General")
                                })
                        except Exception as e:
                            logger.error(f"Failed to create subtask {idx}: {e}")
                            # Continue with other subtasks
                    
                    logger.info(f"Successfully created {len(created_subtask_keys)} subtasks for {jira_issue.key}")
                except Exception as e:
                    logger.error(f"Error during story breakdown: {e}", exc_info=True)
                    # Continue with assignment even if breakdown fails
            else:
                if not request.auto_breakdown:
                    logger.info(f"Auto-breakdown disabled for {jira_issue.key}")
                elif not story_request.estimated_points:
                    logger.info(f"No story points estimated for {jira_issue.key}, skipping breakdown")
                elif story_request.estimated_points <= 5:
                    logger.info(f"Story points ({story_request.estimated_points}) <= 5 for {jira_issue.key}, skipping breakdown")
            
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
                    assignee_username = assignment["assigned_to"]
                    assignee_display = assignment.get("display_name", assignee_username)
                    
                    logger.info(f"Assignment service selected: {assignee_display} ({assignee_username})")
                    story_request.assigned_to = assignee_username
                    
                    # Update assignee in Jira using account ID
                    try:
                        self.jira_service.assign_issue(jira_issue.key, assignee_username)
                        logger.info(f"Successfully assigned {jira_issue.key} to {assignee_display}")
                        
                        # Add to sprint (uses provided sprint_id or active sprint if not provided)
                        sprint_added = self.jira_service.add_issue_to_sprint(
                            jira_issue.key, 
                            sprint_id=request.sprint_id
                        )
                        if sprint_added:
                            sprint_msg = f"sprint {request.sprint_id}" if request.sprint_id else "active sprint"
                            logger.info(f"Added {jira_issue.key} to {sprint_msg}")
                        else:
                            logger.warning(f"Could not add {jira_issue.key} to sprint (no active sprint or API error)")
                    except Exception as e:
                        logger.error(f"Failed to assign in Jira: {e}")
                        # Continue even if assignment fails
                    
                    self.db.commit()
                else:
                    logger.warning(f"No suitable assignee found for {jira_issue.key}, added to queue")
                
                # Step 5b: Assign subtasks (if any were created)
                if created_subtask_keys and request.auto_assign:
                    logger.info(f"Assigning {len(created_subtask_keys)} subtasks for {jira_issue.key}")
                    for subtask_info in created_subtask_keys:
                        try:
                            subtask_key = subtask_info["key"]
                            subtask_points = subtask_info["points"]
                            
                            # Assign subtask
                            subtask_assignment = await self.assignment_service.assign_ticket(
                                issue_key=subtask_key,
                                priority=request.priority,
                                estimated_points=subtask_points,
                                required_skills=story_request.required_skills or []
                            )
                            
                            if subtask_assignment:
                                subtask_assignee = subtask_assignment["assigned_to"]
                                self.jira_service.assign_issue(subtask_key, subtask_assignee)
                                logger.info(f"Assigned subtask {subtask_key} to {subtask_assignee}")
                                
                                # Add subtask to sprint (same sprint as parent)
                                self.jira_service.add_issue_to_sprint(subtask_key, sprint_id=request.sprint_id)
                            else:
                                logger.warning(f"No assignee found for subtask {subtask_key}")
                        except Exception as e:
                            logger.error(f"Failed to assign subtask {subtask_key}: {e}")
                            # Continue with other subtasks
            
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
