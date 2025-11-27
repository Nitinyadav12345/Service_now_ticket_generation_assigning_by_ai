from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import get_db
from app import models, schemas
from app.services.jira_service import JiraService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/team", response_model=schemas.TeamCapacityOverview)
async def get_team_capacity(db: Session = Depends(get_db)):
    """Get team capacity overview"""
    try:
        members = db.query(models.TeamMember).all()
        
        total_capacity = sum(m.max_story_points for m in members)
        used_capacity = sum(m.current_story_points for m in members)
        available_capacity = total_capacity - used_capacity
        utilization = (used_capacity / total_capacity * 100) if total_capacity > 0 else 0
        
        members_by_status = {
            "available": [m.username for m in members if m.availability_status == "available"],
            "busy": [m.username for m in members if m.availability_status == "busy"],
            "overloaded": [m.username for m in members if m.availability_status == "overloaded"],
            "ooo": [m.username for m in members if m.is_out_of_office]
        }
        
        return schemas.TeamCapacityOverview(
            total_team_capacity=total_capacity,
            total_used_capacity=used_capacity,
            available_capacity=available_capacity,
            utilization_percentage=utilization,
            team_size=len(members),
            available_members=len(members_by_status["available"]),
            members_by_status=members_by_status
        )
    except Exception as e:
        logger.error(f"Error getting team capacity: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/member/{username}", response_model=schemas.TeamMember)
async def get_member_capacity(username: str, db: Session = Depends(get_db)):
    """Get individual member capacity"""
    member = db.query(models.TeamMember).filter(
        models.TeamMember.username == username
    ).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")
    
    return member


@router.post("/mark-ooo")
async def mark_out_of_office(
    request: schemas.MarkOOORequest,
    db: Session = Depends(get_db)
):
    """Mark team member as out of office"""
    try:
        member = db.query(models.TeamMember).filter(
            models.TeamMember.username == request.username
        ).first()
        
        if not member:
            raise HTTPException(status_code=404, detail="Team member not found")
        
        from datetime import datetime
        
        # Update member status
        member.is_out_of_office = True
        member.ooo_start_date = datetime.fromisoformat(request.start_date)
        member.ooo_end_date = datetime.fromisoformat(request.end_date)
        member.ooo_reason = request.reason
        member.partial_capacity_percentage = request.partial_capacity or 0.0
        member.availability_status = "ooo"
        
        # Create OOO record
        ooo_record = models.TeamMemberOOO(
            username=request.username,
            start_date=member.ooo_start_date,
            end_date=member.ooo_end_date,
            reason=request.reason,
            is_partial=request.partial_capacity > 0,
            partial_capacity_percentage=request.partial_capacity or 0.0
        )
        db.add(ooo_record)
        db.commit()
        
        return {"status": "success", "message": f"{request.username} marked as OOO"}
        
    except Exception as e:
        logger.error(f"Error marking OOO: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/refresh")
async def refresh_capacity(db: Session = Depends(get_db)):
    """Refresh capacity from Jira"""
    try:
        jira_service = JiraService()
        members = db.query(models.TeamMember).all()
        
        for member in members:
            workload = jira_service.get_user_workload(member.username)
            member.current_story_points = workload["story_points"]
            member.current_ticket_count = workload["ticket_count"]
            
            # Update availability status
            utilization = (member.current_story_points / member.max_story_points) * 100
            if utilization >= 100:
                member.availability_status = "overloaded"
            elif utilization >= 75:
                member.availability_status = "busy"
            else:
                member.availability_status = "available"
        
        db.commit()
        
        return {"status": "success", "message": "Capacity refreshed from Jira"}
        
    except Exception as e:
        logger.error(f"Error refreshing capacity: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/members", response_model=List[schemas.TeamMember])
async def get_all_members(db: Session = Depends(get_db)):
    """Get all team members"""
    members = db.query(models.TeamMember).all()
    return members


@router.put("/member/{username}")
async def update_member(
    username: str,
    request: schemas.UpdateMemberRequest,
    db: Session = Depends(get_db)
):
    """Update team member details (skills, capacity, seniority, etc.)"""
    try:
        member = db.query(models.TeamMember).filter(
            models.TeamMember.username == username
        ).first()
        
        if not member:
            raise HTTPException(status_code=404, detail="Team member not found")
        
        # Update fields if provided
        if request.skills is not None:
            member.skills = request.skills
        
        if request.max_story_points is not None:
            member.max_story_points = request.max_story_points
            # Recalculate availability status
            utilization = (member.current_story_points / member.max_story_points) * 100
            if utilization >= 100:
                member.availability_status = "overloaded"
            elif utilization >= 75:
                member.availability_status = "busy"
            else:
                member.availability_status = "available"
        
        if request.seniority_level is not None:
            member.seniority_level = request.seniority_level
        
        if request.display_name is not None:
            member.display_name = request.display_name
        
        if request.designation is not None:
            member.designation = request.designation
        
        if request.email is not None:
            member.email = request.email
        
        db.commit()
        db.refresh(member)
        
        return {
            "status": "success",
            "message": f"Updated {member.display_name}",
            "member": {
                "username": member.username,
                "display_name": member.display_name,
                "email": member.email,
                "designation": member.designation,
                "skills": member.skills,
                "max_story_points": member.max_story_points,
                "seniority_level": member.seniority_level
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating member: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync-from-jira")
async def sync_team_from_jira(db: Session = Depends(get_db)):
    """Sync team members from Jira project with real-time capacity calculation"""
    try:
        jira_service = JiraService()
        
        # Get active sprint information
        sprint_info = jira_service.get_active_sprint()
        logger.info(f"Active sprint: {sprint_info}")
        
        # Get all users from the Jira project
        jira_users = jira_service.get_project_users()
        
        synced_members = []
        
        for jira_user in jira_users:
            username = jira_user.get('accountId') or jira_user.get('name')
            # Generate unique email if not provided
            email = jira_user.get('emailAddress')
            if not email:
                email = f"{username}@jira.local"
            display_name = jira_user.get('displayName', username)
            designation = jira_user.get('jobTitle')
            
            # Check if member already exists
            member = db.query(models.TeamMember).filter(
                models.TeamMember.username == username
            ).first()
            
            if not member:
                # Create new member
                member = models.TeamMember(
                    username=username,
                    email=email,
                    display_name=display_name,
                    designation=designation,
                    skills=[],  # Can be updated manually later
                    max_story_points=20,  # Will be updated below
                    current_story_points=0,
                    current_ticket_count=0,
                    availability_status="available",
                    seniority_level="Mid",  # Default
                    performance_score=0.80,
                    average_completion_days=5.0,
                    quality_score=0.80,
                    is_out_of_office=False
                )
                db.add(member)
                synced_members.append(username)
            else:
                # Update existing member's email and designation if available
                if member.email.endswith('@jira.local') and email and not email.endswith('@jira.local'):
                    member.email = email
                if designation:
                    member.designation = designation
            
            # Calculate capacity based on sprint and current workload
            try:
                capacity_data = jira_service.calculate_user_capacity(username, sprint_info)
                
                member.max_story_points = capacity_data["max_story_points"]
                member.current_story_points = capacity_data["current_story_points"]
                member.current_ticket_count = capacity_data["current_ticket_count"]
                member.availability_status = capacity_data["status"]
                
                logger.info(
                    f"User {display_name}: {capacity_data['current_story_points']}/{capacity_data['max_story_points']} "
                    f"points ({capacity_data['utilization_percentage']}% utilized) - {capacity_data['status']}"
                )
            except Exception as e:
                logger.warning(f"Could not calculate capacity for {username}: {e}")
        
        db.commit()
        
        sprint_message = ""
        if sprint_info:
            sprint_message = f" (Sprint: {sprint_info['name']}, {sprint_info['remainingDays']} days remaining)"
        
        return {
            "status": "success",
            "message": f"Synced {len(jira_users)} team members from Jira{sprint_message}",
            "synced_count": len(jira_users),
            "new_members": synced_members,
            "new_members_count": len(synced_members),
            "sprint_info": sprint_info
        }
        
    except Exception as e:
        logger.error(f"Error syncing from Jira: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to sync from Jira: {str(e)}")
