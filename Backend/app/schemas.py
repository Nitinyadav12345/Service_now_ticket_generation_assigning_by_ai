from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID

# ============= Story/Ticket Creation =============

class StoryCreateRequest(BaseModel):
    """Request to create a story/ticket"""
    prompt: str = Field(..., min_length=10, max_length=2000, description="Natural language description")
    project_key: str = Field(..., min_length=1, max_length=50, description="Jira project key (required)")
    issue_type: str = Field(default="Story", description="Story, Task, or Bug")
    priority: str = Field(default="Medium", description="Highest, High, Medium, or Low")
    sprint_id: Optional[int] = Field(None, description="Sprint ID to add ticket to (if not provided, uses active sprint)")
    labels: Optional[List[str]] = Field(None, description="Labels to add to ticket")
    auto_breakdown: bool = Field(default=True, description="Auto-break into subtasks if > 5 points")
    auto_estimate: bool = Field(default=True, description="Auto-estimate story points")
    auto_assign: bool = Field(default=True, description="Auto-assign to team member")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Create a user login feature with OAuth support for Google and GitHub",
                "project_key": "PROJ",
                "issue_type": "Story",
                "priority": "High",
                "auto_estimate": True,
                "auto_breakdown": True,
                "auto_assign": True
            }
        }


class GeneratedStory(BaseModel):
    """Generated story details"""
    title: str
    description: str
    acceptance_criteria: List[str]
    technical_requirements: Optional[str] = None
    required_skills: List[str]
    estimated_points: Optional[int] = None
    estimation_reasoning: Optional[str] = None
    confidence_score: Optional[float] = None


class StoryCreateResponse(BaseModel):
    """Response after creating a story"""
    request_id: UUID
    status: str  # pending, processing, completed, failed
    generated_story: Optional[GeneratedStory] = None
    jira_issue_key: Optional[str] = None
    jira_url: Optional[str] = None
    assigned_to: Optional[str] = None
    assignment_reasoning: Optional[str] = None
    subtasks: Optional[List[str]] = None
    error_message: Optional[str] = None
    created_at: datetime


class StoryStatusResponse(BaseModel):
    """Status of story creation request"""
    request_id: UUID
    status: str
    generated_story: Optional[GeneratedStory] = None
    jira_issue_key: Optional[str] = None
    error_message: Optional[str] = None


# ============= Team Capacity =============

class TeamMemberBase(BaseModel):
    """Base team member info"""
    username: str
    email: str  # Changed from EmailStr to avoid email-validator dependency
    display_name: Optional[str] = None
    designation: Optional[str] = None
    skills: List[str] = []
    max_story_points: int = 20
    seniority_level: str = "Mid"


class TeamMemberCreate(TeamMemberBase):
    """Create team member"""
    pass


class TeamMember(TeamMemberBase):
    """Team member with capacity info"""
    id: int
    current_story_points: int
    current_ticket_count: int
    availability_status: str
    manual_capacity_override: bool = False
    performance_score: float
    average_completion_days: float
    quality_score: float
    is_out_of_office: bool
    ooo_end_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TeamCapacityOverview(BaseModel):
    """Team capacity overview"""
    total_team_capacity: int
    total_used_capacity: int
    available_capacity: int
    utilization_percentage: float
    team_size: int
    available_members: int
    members_by_status: Dict[str, List[str]]


class MarkOOORequest(BaseModel):
    """Mark team member as out of office"""
    username: str
    start_date: str  # ISO format
    end_date: str
    reason: str
    partial_capacity: Optional[float] = 0.0


class UpdateSkillsRequest(BaseModel):
    """Update team member skills"""
    username: str
    skills: List[str]


class UpdateMemberRequest(BaseModel):
    """Update team member details"""
    username: str
    skills: Optional[List[str]] = None
    max_story_points: Optional[int] = None
    reset_capacity_to_auto: Optional[bool] = None  # Reset to auto-calculated capacity
    seniority_level: Optional[str] = None
    display_name: Optional[str] = None
    email: Optional[str] = None
    designation: Optional[str] = None


# ============= Assignment =============

class AssignmentRequest(BaseModel):
    """Request to assign a ticket"""
    issue_key: str = Field(..., min_length=1, description="Jira issue key (e.g., PROJ-123)")
    priority: str = Field(..., description="Highest, High, Medium, or Low")
    estimated_points: int = Field(..., gt=0, le=21, description="Story points (1-21)")
    required_skills: List[str] = Field(default=[], description="Required technical skills")


class AssignmentCandidate(BaseModel):
    """Assignment candidate with score"""
    username: str
    display_name: str
    score: float
    bandwidth_score: float
    skills_score: float
    priority_score: float
    performance_score: float


class AssignmentResponse(BaseModel):
    """Assignment result"""
    assigned_to: str
    display_name: str
    assignment_score: float
    reasoning: str
    alternatives: List[AssignmentCandidate]


class AssignmentQueueItem(BaseModel):
    """Item in assignment queue"""
    issue_key: str
    priority: str
    estimated_points: int
    attempts: int
    reason: str
    created_at: datetime
    waiting_time: str


class AssignmentQueueResponse(BaseModel):
    """Assignment queue"""
    queued_count: int
    items: List[AssignmentQueueItem]


# ============= Analytics =============

class DashboardStats(BaseModel):
    """Dashboard statistics"""
    total_stories_created: int
    estimation_accuracy: float
    assignment_accuracy: float
    average_completion_time: float
    team_utilization: float


class EstimationAccuracy(BaseModel):
    """Estimation accuracy metrics"""
    acceptance_rate: float
    average_error: float
    total_estimations: int
    monthly_trend: List[Dict[str, Any]]


class AssignmentAccuracy(BaseModel):
    """Assignment accuracy metrics"""
    acceptance_rate: float
    total_assignments: int
    reassignments: int
    common_reassignment_patterns: List[Dict[str, Any]]


class LearningInsight(BaseModel):
    """AI learning insight"""
    category: str
    insight: str
    impact: str
    confidence: float


class Recommendation(BaseModel):
    """System recommendation"""
    title: str
    description: str
    priority: str
    action: Optional[str] = None


# ============= Estimation =============

class EstimationSuggestionRequest(BaseModel):
    """Request estimation suggestion"""
    story_title: str
    story_description: str


class SimilarStory(BaseModel):
    """Similar story for RAG"""
    issue_key: str
    title: str
    similarity_score: float
    estimated_points: int
    actual_points: Optional[int] = None


class EstimationSuggestionResponse(BaseModel):
    """Estimation suggestion"""
    estimated_points: int
    reasoning: str
    confidence: float
    similar_stories: List[SimilarStory]


# ============= Chat =============

class ChatMessage(BaseModel):
    """Chat message"""
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict] = None


class ChatAction(BaseModel):
    """Chat action"""
    type: str
    data: Dict


class ChatResponse(BaseModel):
    """Chat response"""
    response: str
    suggestions: List[str]
    actions: List[ChatAction]
    session_id: str


# ============= Webhooks =============

class JiraWebhookPayload(BaseModel):
    """Jira webhook payload"""
    webhookEvent: str
    issue: Dict
    changelog: Optional[Dict] = None
    user: Optional[Dict] = None


class WebhookResponse(BaseModel):
    """Webhook processing response"""
    status: str  # received, processed, ignored
    message: Optional[str] = None
