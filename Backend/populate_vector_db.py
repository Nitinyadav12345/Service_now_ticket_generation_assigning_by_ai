"""
Script to populate vector database with historical Jira stories
Run this to enable RAG for better estimation
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.vector_service import VectorService
from app.services.jira_service import JiraService
from app.config import settings

def populate_vector_db():
    """Populate vector DB with completed Jira stories"""
    try:
        print("Initializing services...")
        vector_service = VectorService()
        jira_service = JiraService()
        
        if not jira_service.jira:
            print("❌ Jira client not initialized. Check your credentials in .env")
            return
        
        # Get completed stories from last 6 months
        jql = f'project = "{settings.jira_project_key}" AND status = Done AND resolved >= -180d'
        print(f"\nFetching stories with JQL: {jql}")
        
        issues = jira_service.jira.search_issues(jql, maxResults=200)
        print(f"Found {len(issues)} completed stories")
        
        added_count = 0
        skipped_count = 0
        
        for issue in issues:
            try:
                # Get story points
                story_points = (
                    getattr(issue.fields, 'customfield_10016', None) or
                    getattr(issue.fields, 'customfield_10002', None) or
                    5  # Default
                )
                
                # Get completion time
                completion_time = None
                if hasattr(issue.fields, 'created') and hasattr(issue.fields, 'resolutiondate'):
                    from datetime import datetime
                    created = datetime.fromisoformat(issue.fields.created.replace('Z', '+00:00'))
                    resolved = datetime.fromisoformat(issue.fields.resolutiondate.replace('Z', '+00:00'))
                    completion_time = (resolved - created).days
                
                # Add to vector DB
                vector_service.add_story(
                    issue_key=issue.key,
                    title=issue.fields.summary,
                    description=issue.fields.description or issue.fields.summary,
                    estimated_points=int(story_points) if story_points else 5,
                    actual_points=int(story_points) if story_points else 5,
                    completion_time_days=completion_time
                )
                
                added_count += 1
                print(f"✅ Added {issue.key}: {issue.fields.summary[:50]}... ({story_points} pts)")
                
            except Exception as e:
                print(f"⚠️  Skipped {issue.key}: {e}")
                skipped_count += 1
                continue
        
        # Get collection stats
        stats = vector_service.get_collection_stats()
        
        print(f"\n{'='*60}")
        print(f"✅ Vector DB Population Complete!")
        print(f"{'='*60}")
        print(f"Added: {added_count} stories")
        print(f"Skipped: {skipped_count} stories")
        print(f"Total in DB: {stats.get('count', 0)} stories")
        print(f"\nRAG is now enabled for better estimation!")
        
    except Exception as e:
        print(f"❌ Error populating vector DB: {e}")
        raise


if __name__ == "__main__":
    print("="*60)
    print("Jira AI Assistant - Vector DB Population")
    print("="*60)
    populate_vector_db()
