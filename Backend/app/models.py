from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

class StoryRequest(Base):
    """Story/Ticket creation requests"""
    __tablename__ = "story_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, index=True)
    user_prompt = Column(Text, nullable=False)
    generated_title = Column(String(500))
    generated_description = Column(Text)
    acceptance_criteria = Column(JSON)  # List of strings
    technical_requirements = Column(Text)
    required_skills = Column(JSON)  # List of strings
    estimated_points = Column(Integer)
    jira_issue_key = Column(String(50), unique=True, index=True)
    issue_type = Column(String(50), default="Story")  # Story, Task, Bug
    priority = Column(String(50), default="Medium")
    project_key = Column(String(50))
    epic_key = Column(String(50))
    labels = Column(JSON)  # List of strings
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    error_message = Column(Text)
    assigned_to = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    feedback_estimations = relationship("FeedbackEstimation", back_populates="story_request")
    assignment_history = relationship("AssignmentHistory", back_populates="story_request")


class TeamMember(Base):
    """Team member capacity and information"""
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(255))
    designation = Column(String(255))  # Job title/role from Jira
    skills = Column(JSON)  # List of skills
    max_story_points = Column(Integer, default=20)
    manual_capacity_override = Column(Boolean, default=False)  # True if capacity manually set
    current_story_points = Column(Integer, default=0)
    current_ticket_count = Column(Integer, default=0)
    availability_status = Column(String(50), default="available")  # available, busy, overloaded, ooo
    seniority_level = Column(String(50), default="Mid")  # Junior, Mid, Senior, Lead
    performance_score = Column(Float, default=7.5)
    average_completion_days = Column(Float, default=5.0)
    quality_score = Column(Float, default=7.5)
    preferred_work = Column(JSON)  # List of preferred work types
    is_out_of_office = Column(Boolean, default=False)
    ooo_start_date = Column(DateTime)
    ooo_end_date = Column(DateTime)
    ooo_reason = Column(String(255))
    partial_capacity_percentage = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ooo_records = relationship("TeamMemberOOO", back_populates="team_member")
    assignment_history = relationship("AssignmentHistory", back_populates="team_member")


class FeedbackEstimation(Base):
    """Feedback on AI estimations for learning"""
    __tablename__ = "feedback_estimations"
    
    id = Column(Integer, primary_key=True, index=True)
    issue_key = Column(String(50), ForeignKey("story_requests.jira_issue_key"), nullable=False, index=True)
    ai_estimated_points = Column(Integer)
    human_estimated_points = Column(Integer)
    actual_points = Column(Integer)
    estimation_error = Column(Float)  # Difference between AI and human
    was_accepted = Column(Boolean, default=True)  # Was AI estimation accepted?
    feedback_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    story_request = relationship("StoryRequest", back_populates="feedback_estimations")


class AssignmentHistory(Base):
    """History of ticket assignments"""
    __tablename__ = "assignment_history"
    
    id = Column(Integer, primary_key=True, index=True)
    issue_key = Column(String(50), ForeignKey("story_requests.jira_issue_key"), nullable=False, index=True)
    assignee = Column(String(100), ForeignKey("team_members.username"), nullable=False, index=True)
    assignment_score = Column(Float)  # Score used for assignment decision
    assignment_reason = Column(Text)  # Explanation of why assigned
    bandwidth_score = Column(Float)
    skills_score = Column(Float)
    priority_score = Column(Float)
    performance_score = Column(Float)
    was_reassigned = Column(Boolean, default=False)
    reassignment_reason = Column(Text)
    completion_time_days = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    story_request = relationship("StoryRequest", back_populates="assignment_history")
    team_member = relationship("TeamMember", back_populates="assignment_history")


class TeamMemberOOO(Base):
    """Out of office records"""
    __tablename__ = "team_member_ooo"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), ForeignKey("team_members.username"), nullable=False, index=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    reason = Column(String(255))
    is_partial = Column(Boolean, default=False)
    partial_capacity_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    team_member = relationship("TeamMember", back_populates="ooo_records")


class AssignmentQueue(Base):
    """Queue for tickets that couldn't be assigned"""
    __tablename__ = "assignment_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    issue_key = Column(String(50), unique=True, nullable=False, index=True)
    priority = Column(String(50), nullable=False)
    estimated_points = Column(Integer)
    required_skills = Column(JSON)  # List of required skills
    status = Column(String(50), default="queued")  # queued, processing, assigned, failed
    assignment_attempts = Column(Integer, default=0)
    reason = Column(Text)  # Why it couldn't be assigned
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_attempt_at = Column(DateTime)


class VectorEmbedding(Base):
    """Store embeddings for RAG"""
    __tablename__ = "vector_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    issue_key = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(500))
    description = Column(Text)
    embedding_id = Column(String(255))  # ID in Pinecone/ChromaDB
    estimated_points = Column(Integer)
    actual_points = Column(Integer)
    completion_time_days = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
