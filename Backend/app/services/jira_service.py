from jira import JIRA
from typing import Optional, List, Dict
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class JiraService:
    """Service for Jira API operations"""
    
    def __init__(self):
        try:
            # Initialize Jira client with API v3 (Cloud)
            self.jira = JIRA(
                server=settings.jira_url,
                basic_auth=(settings.jira_email, settings.jira_api_token),
                options={'rest_api_version': '3'}  # Force API v3
            )
            self.project_key = settings.jira_project_key
            logger.info("Jira client initialized successfully with API v3")
        except Exception as e:
            logger.error(f"Failed to initialize Jira client: {e}")
            self.jira = None
            self.project_key = settings.jira_project_key
    
    @staticmethod
    def convert_to_adf(text: str) -> Dict:
        """
        Convert plain text to Atlassian Document Format (ADF).
        
        Args:
            text: Plain text description
            
        Returns:
            ADF formatted document
        """
        if not text:
            return {
                "version": 1,
                "type": "doc",
                "content": []
            }
        
        # Split text into paragraphs
        paragraphs = text.split('\n\n')
        content = []
        
        for para in paragraphs:
            if not para.strip():
                continue
            
            # Check if it's a list item
            lines = para.split('\n')
            if any(line.strip().startswith(('-', '*', '•')) for line in lines):
                # Create bullet list
                list_items = []
                for line in lines:
                    line = line.strip()
                    if line.startswith(('-', '*', '•')):
                        # Remove bullet and trim
                        item_text = line[1:].strip()
                        list_items.append({
                            "type": "listItem",
                            "content": [{
                                "type": "paragraph",
                                "content": [{
                                    "type": "text",
                                    "text": item_text
                                }]
                            }]
                        })
                
                if list_items:
                    content.append({
                        "type": "bulletList",
                        "content": list_items
                    })
            else:
                # Regular paragraph
                content.append({
                    "type": "paragraph",
                    "content": [{
                        "type": "text",
                        "text": para.strip()
                    }]
                })
        
        return {
            "version": 1,
            "type": "doc",
            "content": content
        }
    
    def create_issue(
        self,
        project_key: str,
        issue_type: str,
        summary: str,
        description: str,
        priority: str = "Medium",
        story_points: Optional[int] = None,
        labels: Optional[List[str]] = None,
        epic_key: Optional[str] = None
    ):
        """Create a Jira issue"""
        if not self.jira:
            raise Exception("Jira client not initialized")
        
        try:
            # Convert description to Atlassian Document Format (ADF) for API v3
            description_adf = self.convert_to_adf(description)
            
            issue_dict = {
                'project': {'key': project_key},
                'summary': summary,
                'description': description_adf,  # Use ADF format
                'issuetype': {'name': issue_type},
                'priority': {'name': priority}
            }
            
            # Add story points if provided (custom field)
            if story_points:
                # Note: Field ID may vary by Jira instance
                issue_dict['customfield_10016'] = story_points
            
            # Add labels
            if labels:
                issue_dict['labels'] = labels
            
            # Link to epic
            if epic_key:
                issue_dict['customfield_10014'] = epic_key
            
            issue = self.jira.create_issue(fields=issue_dict)
            logger.info(f"Created Jira issue: {issue.key}")
            return issue
            
        except Exception as e:
            logger.error(f"Error creating Jira issue: {e}")
            raise
    
    def get_subtask_issue_type(self, project_key: str) -> str:
        """Get the correct subtask issue type name for the project"""
        if not self.jira:
            raise Exception("Jira client not initialized")
        
        try:
            # Get project metadata
            project = self.jira.project(project_key)
            issue_types = self.jira.issue_types()
            
            # Look for subtask issue type (case-insensitive)
            for issue_type in issue_types:
                if issue_type.subtask:
                    logger.info(f"Found subtask issue type: {issue_type.name}")
                    return issue_type.name
            
            # Fallback to common names
            for name in ['Subtask', 'Sub-task', 'Sub task']:
                for issue_type in issue_types:
                    if issue_type.name.lower() == name.lower():
                        return issue_type.name
            
            # Default fallback
            logger.warning("Could not find subtask issue type, using 'Subtask'")
            return "Subtask"
            
        except Exception as e:
            logger.warning(f"Error getting subtask issue type: {e}, using default")
            return "Subtask"
    
    def create_subtask(
        self,
        parent_key: str,
        summary: str,
        description: str = "",
        story_points: Optional[int] = None
    ):
        """Create a subtask"""
        if not self.jira:
            raise Exception("Jira client not initialized")
        
        try:
            parent_issue = self.jira.issue(parent_key)
            
            # Get correct subtask issue type name
            subtask_type = self.get_subtask_issue_type(parent_issue.fields.project.key)
            
            # Convert description to ADF format
            description_adf = self.convert_to_adf(description)
            
            subtask_dict = {
                'project': {'key': parent_issue.fields.project.key},
                'summary': summary,
                'description': description_adf,  # Use ADF format
                'issuetype': {'name': subtask_type},  # Use detected type
                'parent': {'key': parent_key}
            }
            
            if story_points:
                subtask_dict['customfield_10016'] = story_points
            
            subtask = self.jira.create_issue(fields=subtask_dict)
            logger.info(f"Created subtask: {subtask.key} for {parent_key}")
            return subtask
            
        except Exception as e:
            logger.error(f"Error creating subtask: {e}")
            raise
    
    def assign_issue(self, issue_key: str, assignee: str):
        """Assign issue to user using account ID"""
        if not self.jira:
            raise Exception("Jira client not initialized")
        
        try:
            issue = self.jira.issue(issue_key)
            
            # Log before assignment
            logger.info(f"Attempting to assign {issue_key} to {assignee}")
            
            # Jira Cloud uses account IDs for assignment
            # The assignee parameter should be the account ID (e.g., "712020:xxx")
            self.jira.assign_issue(issue, assignee)
            
            # Verify assignment
            issue = self.jira.issue(issue_key)
            actual_assignee = issue.fields.assignee
            if actual_assignee:
                logger.info(f"Successfully assigned {issue_key} to {actual_assignee.displayName} ({actual_assignee.accountId})")
            else:
                logger.warning(f"Assignment completed but issue {issue_key} has no assignee")
                
        except Exception as e:
            logger.error(f"Error assigning issue {issue_key} to {assignee}: {e}")
            # Don't raise - assignment failure shouldn't fail the whole story creation
            logger.warning(f"Continuing without assignment for {issue_key}")
    
    def get_user_workload(self, username: str, sprint_id: Optional[int] = None) -> Dict:
        """Get user's current workload from Jira (active sprint only, excluding Done)"""
        if not self.jira:
            return {"story_points": 0, "ticket_count": 0}
        
        try:
            # For Jira Cloud, username is actually accountId
            # JQL format: assignee = accountId (no quotes for accountId)
            # For Jira Server, use quoted username
            
            # Detect if it's an accountId (starts with numbers like "712020:")
            is_account_id = username and ':' in username and username.split(':')[0].isdigit()
            
            if is_account_id:
                assignee_clause = f'assignee = {username}'
            else:
                assignee_clause = f'assignee = "{username}"'
            
            # Build JQL query for active sprint issues only
            if sprint_id:
                # Query issues in specific sprint, excluding Done/Closed
                jql = (
                    f'{assignee_clause} '
                    f'AND project = "{self.project_key}" '
                    f'AND sprint = {sprint_id} '
                    f'AND status NOT IN (Done, Closed, Resolved, Cancelled)'
                )
            else:
                # Fallback: Query open issues in current sprint
                jql = (
                    f'{assignee_clause} '
                    f'AND project = "{self.project_key}" '
                    f'AND sprint in openSprints() '
                    f'AND status NOT IN (Done, Closed, Resolved, Cancelled)'
                )
            
            logger.debug(f"Workload JQL for {username}: {jql}")
            
            # Use JQL API directly (new endpoint required by Atlassian)
            import requests
            from requests.auth import HTTPBasicAuth
            
            url = f"{settings.jira_url}/rest/api/3/search/jql"
            auth = HTTPBasicAuth(settings.jira_email, settings.jira_api_token)
            headers = {"Accept": "application/json"}
            params = {
                "jql": jql,
                "maxResults": 100,
                "fields": "customfield_10016,customfield_10002,customfield_10026"  # Story points fields
            }
            
            response = requests.get(url, headers=headers, params=params, auth=auth)
            response.raise_for_status()
            data = response.json()
            issues = data.get("issues", [])
            
            total_points = 0
            for issue in issues:
                # Get story points from fields (try multiple common field IDs)
                fields = issue.get("fields", {})
                points = (
                    fields.get('customfield_10016') or
                    fields.get('customfield_10002') or
                    fields.get('customfield_10026')
                )
                if points:
                    total_points += float(points)
            
            logger.info(
                f"Workload for {username}: {len(issues)} tickets, "
                f"{total_points} story points (active sprint only)"
            )
            
            return {
                "story_points": int(total_points),
                "ticket_count": len(issues)
            }
        except Exception as e:
            logger.error(f"Error getting user workload: {e}")
            return {"story_points": 0, "ticket_count": 0}
    
    def get_all_users(self) -> List[Dict]:
        """Get all Jira users"""
        if not self.jira:
            return []
        
        try:
            users = self.jira.search_users('', maxResults=100)
            return [
                {
                    "username": user.name,
                    "display_name": user.displayName,
                    "email": user.emailAddress
                }
                for user in users
                if user.active
            ]
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            return []
    
    def get_project_users(self) -> List[Dict]:
        """Get all users who have access to the project"""
        if not self.jira:
            return []
        
        try:
            # Get users who can be assigned issues in this project
            assignable_users = self.jira.search_assignable_users_for_projects(
                username='',  # Empty to get all users
                projectKeys=self.project_key,
                maxResults=100
            )
            
            users = []
            for user in assignable_users:
                account_id = user.accountId if hasattr(user, 'accountId') else user.name
                
                # Try to get full user details including email and job title
                email = None
                job_title = None
                
                try:
                    # Method 1: Try to get from assignable user object
                    email = getattr(user, 'emailAddress', None)
                    
                    # Method 2: Fetch full user details
                    user_details = self.jira.user(account_id)
                    
                    # Try to get email from full details
                    if not email:
                        email = getattr(user_details, 'emailAddress', None)
                    
                    # Try to get job title
                    job_title = getattr(user_details, 'jobTitle', None)
                    
                    # Log if email is missing
                    if not email:
                        logger.warning(
                            f"Email not available for user {user.displayName} ({account_id}). "
                            f"This may be due to Jira privacy settings or API permissions."
                        )
                    
                except Exception as e:
                    logger.debug(f"Could not fetch full details for user {account_id}: {e}")
                
                user_data = {
                    "accountId": account_id,
                    "name": user.name if hasattr(user, 'name') else account_id,
                    "displayName": user.displayName,
                    "emailAddress": email,
                    "jobTitle": job_title,
                    "active": getattr(user, 'active', True)
                }
                
                # Only include active users
                if user_data.get("active", True):
                    users.append(user_data)
            
            logger.info(f"Found {len(users)} assignable users in project {self.project_key}")
            return users
            
        except Exception as e:
            logger.error(f"Error getting project users: {e}")
            # Return empty list if we can't get users from Jira
            return []
    
    def update_issue(self, issue_key: str, fields: Dict):
        """Update issue fields"""
        if not self.jira:
            raise Exception("Jira client not initialized")
        
        try:
            issue = self.jira.issue(issue_key)
            issue.update(fields=fields)
            logger.info(f"Updated issue {issue_key}")
        except Exception as e:
            logger.error(f"Error updating issue: {e}")
            raise
    
    def get_active_sprint(self) -> Optional[Dict]:
        """Get the active sprint for the project"""
        if not self.jira:
            return None
        
        try:
            # Get the board for the project
            boards = self.jira.boards(projectKeyOrID=self.project_key)
            if not boards:
                logger.warning(f"No boards found for project {self.project_key}")
                return None
            
            board = boards[0]  # Use first board
            
            # Get active sprints
            sprints = self.jira.sprints(board.id, state='active')
            if not sprints:
                logger.info("No active sprint found")
                return None
            
            sprint = sprints[0]  # Use first active sprint
            
            from datetime import datetime
            
            # Parse sprint dates
            start_date = None
            end_date = None
            
            if hasattr(sprint, 'startDate') and sprint.startDate:
                start_date = datetime.fromisoformat(sprint.startDate.replace('Z', '+00:00'))
            if hasattr(sprint, 'endDate') and sprint.endDate:
                end_date = datetime.fromisoformat(sprint.endDate.replace('Z', '+00:00'))
            
            # Calculate remaining days
            remaining_days = 0
            total_days = 0
            if start_date and end_date:
                now = datetime.now(start_date.tzinfo)
                total_days = (end_date - start_date).days
                remaining_days = max(0, (end_date - now).days)
            
            return {
                "id": sprint.id,
                "name": sprint.name,
                "state": sprint.state,
                "startDate": start_date.isoformat() if start_date else None,
                "endDate": end_date.isoformat() if end_date else None,
                "totalDays": total_days,
                "remainingDays": remaining_days
            }
            
        except Exception as e:
            logger.error(f"Error getting active sprint: {e}")
            return None
    
    def add_issue_to_sprint(self, issue_key: str, sprint_id: Optional[int] = None) -> bool:
        """
        Add an issue to a sprint (defaults to active sprint if sprint_id not provided)
        
        Args:
            issue_key: Jira issue key (e.g., SCRUM-123)
            sprint_id: Sprint ID (if None, uses active sprint)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.jira:
            logger.warning("Jira client not initialized")
            return False
        
        try:
            # Get active sprint if not provided
            if not sprint_id:
                active_sprint = self.get_active_sprint()
                if not active_sprint:
                    logger.warning(f"No active sprint found, cannot add {issue_key} to sprint")
                    return False
                sprint_id = active_sprint["id"]
            
            # Add issue to sprint using Jira API
            # The Jira library doesn't have a direct method, so we use the REST API
            url = f"{self.jira._options['server']}/rest/agile/1.0/sprint/{sprint_id}/issue"
            headers = {"Content-Type": "application/json"}
            data = {"issues": [issue_key]}
            
            response = self.jira._session.post(url, json=data, headers=headers)
            
            if response.status_code in [200, 204]:
                logger.info(f"Successfully added {issue_key} to sprint {sprint_id}")
                return True
            else:
                logger.error(f"Failed to add {issue_key} to sprint: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error adding {issue_key} to sprint: {e}")
            return False
    
    def get_user_velocity(self, username: str, sprint_count: int = 3) -> float:
        """Calculate user's average velocity from completed sprints"""
        if not self.jira:
            return 2.0  # Default 2 points per day
        
        try:
            # Get completed issues from recent sprints
            jql = f'assignee = "{username}" AND project = "{self.project_key}" AND status = Done AND resolved >= -60d'
            issues = self.jira.search_issues(jql, maxResults=100)
            
            total_points = 0
            issue_count = 0
            
            for issue in issues:
                points = getattr(issue.fields, 'customfield_10016', None)
                if points:
                    total_points += points
                    issue_count += 1
            
            if issue_count > 0:
                # Calculate average points per issue
                avg_points_per_issue = total_points / issue_count
                # Estimate velocity (assuming ~60 days = 3 sprints of 2 weeks each)
                velocity = total_points / 60  # Points per day
                return max(1.0, velocity)  # Minimum 1 point per day
            
            return 2.0  # Default if no history
            
        except Exception as e:
            logger.warning(f"Could not calculate velocity for {username}: {e}")
            return 2.0
    
    def calculate_user_capacity(
        self, 
        username: str, 
        sprint_info: Optional[Dict] = None,
        seniority_level: str = "Mid"
    ) -> Dict:
        """
        Calculate user's capacity using proper sprint capacity formula:
        Sprint Capacity = (Working Days × Daily Working Hours − Leave Hours) × Focus Factor × Seniority Multiplier
        
        Seniority multipliers account for different productivity and responsibilities:
        - Junior: 60% (learning, needs guidance)
        - Mid: 100% (baseline)
        - Senior: 120% (more efficient)
        - Lead: 80% (more meetings, mentoring)
        - Principal: 70% (architecture, strategy, mentoring)
        """
        if not self.jira:
            return {
                "max_story_points": 20,
                "current_story_points": 0,
                "available_capacity": 20,
                "utilization_percentage": 0,
                "status": "available"
            }
        
        try:
            # Get current workload from active sprint only
            sprint_id = sprint_info.get("id") if sprint_info else None
            workload = self.get_user_workload(username, sprint_id)
            current_points = workload["story_points"]
            ticket_count = workload["ticket_count"]
            
            # Calculate max capacity based on sprint duration
            if sprint_info and sprint_info.get("totalDays"):
                total_days = sprint_info["totalDays"]
                
                # Get capacity calculation parameters from settings
                DAILY_WORKING_HOURS = settings.daily_working_hours
                HOURS_PER_STORY_POINT = settings.hours_per_story_point
                FOCUS_FACTOR = settings.focus_factor
                
                # Get seniority multiplier
                seniority_multipliers = {
                    "Junior": settings.capacity_multiplier_junior,
                    "Mid": settings.capacity_multiplier_mid,
                    "Senior": settings.capacity_multiplier_senior,
                    "Lead": settings.capacity_multiplier_lead,
                    "Principal": settings.capacity_multiplier_principal
                }
                seniority_multiplier = seniority_multipliers.get(seniority_level, 1.0)
                
                # Calculate working days (exclude weekends)
                working_days = (total_days / 7) * 5
                
                # Get leave hours (check if user has OOO during sprint)
                leave_hours = 0  # TODO: Can be enhanced to check OOO records
                
                # Sprint Capacity Formula:
                # (Working Days × Daily Working Hours − Leave Hours) × Focus Factor × Seniority Multiplier
                base_hours = (working_days * DAILY_WORKING_HOURS - leave_hours) * FOCUS_FACTOR
                total_available_hours = base_hours * seniority_multiplier
                
                # Convert hours to story points
                max_capacity = round(total_available_hours / HOURS_PER_STORY_POINT)
                
                # Ensure minimum capacity
                max_capacity = max(5, max_capacity)
                
                logger.info(
                    f"Capacity calculation for {username} ({seniority_level}): "
                    f"{total_days} total days, {working_days:.1f} working days, "
                    f"{base_hours:.1f} base hours × {seniority_multiplier} multiplier = "
                    f"{total_available_hours:.1f} available hours, "
                    f"= {max_capacity} story points"
                )
            else:
                # Default 2-week sprint capacity
                # 10 working days × 8 hours × 0.7 focus factor / 4 hours per point = 14 points
                max_capacity = 14
            
            # Calculate utilization
            utilization = (current_points / max_capacity * 100) if max_capacity > 0 else 0
            available_capacity = max(0, max_capacity - current_points)
            
            # Determine status
            if utilization >= 100:
                status = "overloaded"
            elif utilization >= 75:
                status = "busy"
            else:
                status = "available"
            
            return {
                "max_story_points": max_capacity,
                "current_story_points": current_points,
                "current_ticket_count": ticket_count,
                "available_capacity": available_capacity,
                "utilization_percentage": round(utilization, 2),
                "status": status
            }
            
        except Exception as e:
            logger.error(f"Error calculating user capacity: {e}")
            return {
                "max_story_points": 14,
                "current_story_points": 0,
                "available_capacity": 14,
                "utilization_percentage": 0,
                "status": "available"
            }
