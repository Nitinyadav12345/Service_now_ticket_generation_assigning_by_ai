import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { ApiService } from './api.service';
import { Story } from '../models/story.model';

export interface StoryRequest {
  prompt: string;
  issueType: string;
  priority: string;
  projectKey?: string;
  epicKey?: string;
  labels?: string[];
  autoEstimate: boolean;
  autoBreakdown: boolean;
  autoAssign: boolean;
}

export interface StoryResponse {
  requestId: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  generatedStory?: {
    title: string;
    description: string;
    acceptanceCriteria: string[];
    technicalRequirements?: string;
    requiredSkills: string[];
    estimatedPoints?: number;
  };
  jiraIssueKey?: string;
  jiraUrl?: string;
  assignedTo?: string;
  assignmentReasoning?: string;
  subtasks?: string[];
  errorMessage?: string;
  createdAt: string;
}

@Injectable({
  providedIn: 'root'
})
export class StoryService {
  constructor(private apiService: ApiService) {}

  createStory(request: StoryRequest): Observable<StoryResponse> {
    return this.apiService.createStory({
      prompt: request.prompt,
      issue_type: request.issueType,
      priority: request.priority,
      project_key: request.projectKey,
      epic_key: request.epicKey,
      labels: request.labels,
      auto_estimate: request.autoEstimate,
      auto_breakdown: request.autoBreakdown,
      auto_assign: request.autoAssign
    }).pipe(
      map(response => this.mapToStoryResponse(response))
    );
  }

  getStoryStatus(requestId: string): Observable<StoryResponse> {
    return this.apiService.getStoryStatus(requestId).pipe(
      map(response => this.mapToStoryResponse(response))
    );
  }

  getRecentStories(): Observable<Story[]> {
    // This would typically call a backend endpoint
    // For now, return empty array as placeholder
    return new Observable(observer => {
      observer.next([]);
      observer.complete();
    });
  }

  private mapToStoryResponse(response: any): StoryResponse {
    return {
      requestId: response.request_id,
      status: response.status,
      generatedStory: response.generated_story ? {
        title: response.generated_story.title,
        description: response.generated_story.description,
        acceptanceCriteria: response.generated_story.acceptance_criteria || [],
        technicalRequirements: response.generated_story.technical_requirements,
        requiredSkills: response.generated_story.required_skills || [],
        estimatedPoints: response.generated_story.estimated_points
      } : undefined,
      jiraIssueKey: response.jira_issue_key,
      jiraUrl: response.jira_url,
      assignedTo: response.assigned_to,
      assignmentReasoning: response.assignment_reasoning,
      subtasks: response.subtasks,
      errorMessage: response.error_message,
      createdAt: response.created_at
    };
  }
}
