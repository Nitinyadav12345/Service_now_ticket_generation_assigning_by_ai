from sqlalchemy.orm import Session
from typing import List, Dict, Optional
import logging
from datetime import datetime

from app import models

logger = logging.getLogger(__name__)

class AssignmentService:
    """Service for ticket assignment logic"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def assign_ticket(
        self,
        issue_key: str,
        priority: str,
        estimated_points: int,
        required_skills: List[str]
    ) -> Optional[Dict]:
        """
        Assign ticket to best-fit team member
        
        Scoring formula:
        - Bandwidth × 40%
        - Skills × 30%
        - Priority Fit × 20%
        - Performance × 10%
        """
        try:
            # Get eligible candidates
            candidates = self._get_eligible_candidates(estimated_points)
            
            if not candidates:
                # Add to queue
                self._add_to_queue(issue_key, priority, estimated_points, required_skills)
                return None
            
            # Score each candidate
            scored_candidates = []
            for candidate in candidates:
                score = self._calculate_assignment_score(
                    candidate,
                    priority,
                    estimated_points,
                    required_skills
                )
                scored_candidates.append({
                    "member": candidate,
                    "score": score["total_score"],
                    "breakdown": score
                })
            
            # Sort by score (highest first)
            scored_candidates.sort(key=lambda x: x["score"], reverse=True)
            best_candidate = scored_candidates[0]
            
            # Validate assignment won't overload
            if not self._validate_capacity(best_candidate["member"], estimated_points):
                self._add_to_queue(issue_key, priority, estimated_points, required_skills)
                return None
            
            # Create assignment record
            assignment = models.AssignmentHistory(
                issue_key=issue_key,
                assignee=best_candidate["member"].username,
                assignment_score=best_candidate["score"],
                assignment_reason=self._generate_reasoning(best_candidate),
                bandwidth_score=best_candidate["breakdown"]["bandwidth_score"],
                skills_score=best_candidate["breakdown"]["skills_score"],
                priority_score=best_candidate["breakdown"]["priority_score"],
                performance_score=best_candidate["breakdown"]["performance_score"]
            )
            self.db.add(assignment)
            
            # Update member capacity
            member = best_candidate["member"]
            member.current_story_points += estimated_points
            member.current_ticket_count += 1
            member.availability_status = self._calculate_availability_status(member)
            
            self.db.commit()
            
            logger.info(f"Assigned {issue_key} to {member.username} (score: {best_candidate['score']:.2f})")
            
            return {
                "assigned_to": member.username,
                "display_name": member.display_name,
                "assignment_score": best_candidate["score"],
                "reasoning": assignment.assignment_reason,
                "alternatives": [
                    {
                        "username": c["member"].username,
                        "score": c["score"]
                    }
                    for c in scored_candidates[1:4]  # Top 3 alternatives
                ]
            }
            
        except Exception as e:
            logger.error(f"Error assigning ticket: {e}")
            return None
    
    def _get_eligible_candidates(self, estimated_points: int) -> List[models.TeamMember]:
        """Get team members eligible for assignment"""
        return self.db.query(models.TeamMember).filter(
            models.TeamMember.is_out_of_office == False,
            models.TeamMember.current_story_points + estimated_points <= models.TeamMember.max_story_points
        ).all()
    
    def _calculate_assignment_score(
        self,
        member: models.TeamMember,
        priority: str,
        estimated_points: int,
        required_skills: List[str]
    ) -> Dict:
        """Calculate assignment score for a team member"""
        
        # 1. Bandwidth Score (40%)
        available_capacity = member.max_story_points - member.current_story_points
        bandwidth_score = (available_capacity / member.max_story_points) * 100
        
        # 2. Skills Score (30%)
        member_skills = set(member.skills or [])
        required_skills_set = set(required_skills)
        if required_skills_set:
            matching_skills = len(member_skills & required_skills_set)
            skills_score = (matching_skills / len(required_skills_set)) * 100
        else:
            skills_score = 50  # Neutral if no skills specified
        
        # 3. Priority Fit Score (20%)
        priority_map = {
            "Highest": {"Senior": 100, "Lead": 100, "Mid": 70, "Junior": 40},
            "High": {"Senior": 100, "Lead": 100, "Mid": 90, "Junior": 60},
            "Medium": {"Senior": 90, "Lead": 90, "Mid": 100, "Junior": 80},
            "Low": {"Senior": 70, "Lead": 70, "Mid": 90, "Junior": 100}
        }
        priority_score = priority_map.get(priority, {}).get(member.seniority_level, 50)
        
        # 4. Performance Score (10%)
        performance_score = (member.performance_score / 10) * 100
        
        # Calculate weighted total
        total_score = (
            bandwidth_score * 0.40 +
            skills_score * 0.30 +
            priority_score * 0.20 +
            performance_score * 0.10
        )
        
        return {
            "total_score": total_score,
            "bandwidth_score": bandwidth_score,
            "skills_score": skills_score,
            "priority_score": priority_score,
            "performance_score": performance_score
        }
    
    def _validate_capacity(self, member: models.TeamMember, estimated_points: int) -> bool:
        """Validate assignment won't overload member"""
        new_total = member.current_story_points + estimated_points
        return new_total <= member.max_story_points
    
    def _calculate_availability_status(self, member: models.TeamMember) -> str:
        """Calculate member's availability status"""
        utilization = (member.current_story_points / member.max_story_points) * 100
        
        if utilization >= 100:
            return "overloaded"
        elif utilization >= 75:
            return "busy"
        else:
            return "available"
    
    def _generate_reasoning(self, candidate: Dict) -> str:
        """Generate human-readable assignment reasoning"""
        member = candidate["member"]
        breakdown = candidate["breakdown"]
        
        reasons = []
        
        if breakdown["bandwidth_score"] > 70:
            reasons.append(f"Good available capacity ({member.max_story_points - member.current_story_points}/{member.max_story_points} pts)")
        
        if breakdown["skills_score"] > 70:
            reasons.append("Strong skills match")
        
        if breakdown["priority_score"] > 80:
            reasons.append(f"Appropriate seniority for priority")
        
        if breakdown["performance_score"] > 75:
            reasons.append(f"Strong historical performance ({member.performance_score}/10)")
        
        return " • ".join(reasons) if reasons else "Best available match"
    
    def _add_to_queue(
        self,
        issue_key: str,
        priority: str,
        estimated_points: int,
        required_skills: List[str]
    ):
        """Add ticket to assignment queue"""
        queue_item = models.AssignmentQueue(
            issue_key=issue_key,
            priority=priority,
            estimated_points=estimated_points,
            required_skills=required_skills,
            reason="No available team members with sufficient capacity"
        )
        self.db.add(queue_item)
        self.db.commit()
        logger.info(f"Added {issue_key} to assignment queue")
