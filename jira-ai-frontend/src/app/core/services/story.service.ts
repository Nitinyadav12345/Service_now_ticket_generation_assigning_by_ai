import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { 
  Story, 
  StoryRequest, 
  StoryResponse, 
  EstimationSuggestion 
} from '../models/story.model';

@Injectable({
  providedIn: 'root'
})
export class StoryService {
  private readonly endpoint = '/prompt';

  constructor(private api: ApiService) {}

  createStory(request: StoryRequest): Observable<StoryResponse> {
    return this.api.post<StoryResponse>(`${this.endpoint}/create-story`, request);
  }

  getStoryStatus(requestId: string): Observable<StoryResponse> {
    return this.api.get<StoryResponse>(`${this.endpoint}/story-status/${requestId}`);
  }

  getEstimationSuggestion(title: string, description: string): Observable<EstimationSuggestion> {
    return this.api.post<EstimationSuggestion>(`${this.endpoint}/suggest-estimation`, {
      story_title: title,
      story_description: description
    });
  }

  getRecentStories(limit = 10): Observable<Story[]> {
    return this.api.get<Story[]>(`${this.endpoint}/recent`, { limit });
  }

  getStoryById(id: string): Observable<Story> {
    return this.api.get<Story>(`${this.endpoint}/story/${id}`);
  }

  chat(message: string, sessionId?: string): Observable<any> {
    return this.api.post(`${this.endpoint}/chat`, {
      message,
      session_id: sessionId
    });
  }
}