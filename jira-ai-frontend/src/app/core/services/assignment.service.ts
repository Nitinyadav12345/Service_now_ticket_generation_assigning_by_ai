import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { ApiService } from './api.service';

export interface AssignmentQueue {
  queuedCount: number;
  items: AssignmentQueueItem[];
}

export interface AssignmentQueueItem {
  issueKey: string;
  priority: string;
  estimatedPoints: number;
  requiredSkills: string[];
  attempts: number;
  reason: string;
  createdAt: string;
  waitingTime: string;
}

@Injectable({
  providedIn: 'root'
})
export class AssignmentService {
  constructor(private apiService: ApiService) {}

  assignTicket(data: {
    issueKey: string;
    priority: string;
    estimatedPoints: number;
    requiredSkills: string[];
  }): Observable<any> {
    return this.apiService.assignTicket({
      issue_key: data.issueKey,
      priority: data.priority,
      estimated_points: data.estimatedPoints,
      required_skills: data.requiredSkills
    });
  }

  getQueue(): Observable<AssignmentQueue> {
    return this.apiService.getAssignmentQueue().pipe(
      map(response => ({
        queuedCount: response.queued_count,
        items: response.items.map((item: any) => ({
          issueKey: item.issue_key,
          priority: item.priority,
          estimatedPoints: item.estimated_points,
          requiredSkills: item.required_skills || [],
          attempts: item.attempts,
          reason: item.reason,
          createdAt: item.created_at,
          waitingTime: item.waiting_time
        }))
      }))
    );
  }

  processQueue(): Observable<any> {
    return this.apiService.processQueue();
  }
}
