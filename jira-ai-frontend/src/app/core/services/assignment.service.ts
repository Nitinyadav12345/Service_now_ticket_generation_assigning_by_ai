import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { 
  AssignmentRequest, 
  AssignmentResponse, 
  AssignmentQueue 
} from '../models/assignment.model';

@Injectable({
  providedIn: 'root'
})
export class AssignmentService {
  private readonly endpoint = '/assignment';

  constructor(private api: ApiService) {}

  assignTicket(request: AssignmentRequest): Observable<AssignmentResponse> {
    return this.api.post<AssignmentResponse>(`${this.endpoint}/assign-ticket`, request);
  }

  getQueue(): Observable<AssignmentQueue> {
    return this.api.get<AssignmentQueue>(`${this.endpoint}/queue`);
  }

  processQueue(): Observable<void> {
    return this.api.post<void>(`${this.endpoint}/process-queue`, {});
  }

  retryAssignment(issueKey: string): Observable<AssignmentResponse> {
    return this.api.post<AssignmentResponse>(`${this.endpoint}/retry/${issueKey}`, {});
  }
}