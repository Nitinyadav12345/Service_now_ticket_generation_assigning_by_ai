import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json'
    });
  }

  private handleError(error: any) {
    console.error('API Error:', error);
    return throwError(() => error);
  }

  // ============= Generic HTTP Methods =============

  get<T>(url: string): Observable<T> {
    return this.http.get<T>(url, {
      headers: this.getHeaders()
    }).pipe(
      catchError(this.handleError)
    );
  }

  post<T>(url: string, data: any): Observable<T> {
    return this.http.post<T>(url, data, {
      headers: this.getHeaders()
    }).pipe(
      catchError(this.handleError)
    );
  }

  // ============= Story/Ticket Creation =============

  createStory(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/prompt/create-story`, data, {
      headers: this.getHeaders()
    }).pipe(
      catchError(this.handleError)
    );
  }

  getStoryStatus(requestId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/prompt/story-status/${requestId}`).pipe(
      retry(3),
      catchError(this.handleError)
    );
  }

  suggestEstimation(data: { story_title: string; story_description: string }): Observable<any> {
    return this.http.post(`${this.apiUrl}/prompt/suggest-estimation`, data, {
      headers: this.getHeaders()
    }).pipe(
      catchError(this.handleError)
    );
  }

  chat(data: { message: string; session_id?: string; context?: any }): Observable<any> {
    return this.http.post(`${this.apiUrl}/prompt/chat`, data, {
      headers: this.getHeaders()
    }).pipe(
      catchError(this.handleError)
    );
  }

  // ============= Team Capacity =============

  getTeamCapacity(): Observable<any> {
    return this.http.get(`${this.apiUrl}/capacity/team`).pipe(
      catchError(this.handleError)
    );
  }

  getMemberCapacity(username: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/capacity/member/${username}`).pipe(
      catchError(this.handleError)
    );
  }

  getAllMembers(): Observable<any> {
    return this.http.get(`${this.apiUrl}/capacity/members`).pipe(
      catchError(this.handleError)
    );
  }

  markOutOfOffice(data: {
    username: string;
    start_date: string;
    end_date: string;
    reason: string;
    partial_capacity?: number;
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}/capacity/mark-ooo`, data, {
      headers: this.getHeaders()
    }).pipe(
      catchError(this.handleError)
    );
  }

  refreshCapacity(): Observable<any> {
    return this.http.post(`${this.apiUrl}/capacity/refresh`, {}, {
      headers: this.getHeaders()
    }).pipe(
      catchError(this.handleError)
    );
  }

  syncFromJira(): Observable<any> {
    return this.http.post(`${this.apiUrl}/capacity/sync-from-jira`, {}, {
      headers: this.getHeaders()
    }).pipe(
      catchError(this.handleError)
    );
  }

  updateMember(username: string, data: {
    skills?: string[];
    max_story_points?: number;
    seniority_level?: string;
    display_name?: string;
    email?: string;
    designation?: string;
  }): Observable<any> {
    return this.http.put(`${this.apiUrl}/capacity/member/${username}`, {
      username,
      ...data
    }, {
      headers: this.getHeaders()
    }).pipe(
      catchError(this.handleError)
    );
  }

  // ============= Assignment =============

  assignTicket(data: {
    issue_key: string;
    priority: string;
    estimated_points: number;
    required_skills: string[];
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}/assignment/assign-ticket`, data, {
      headers: this.getHeaders()
    }).pipe(
      catchError(this.handleError)
    );
  }

  getAssignmentQueue(): Observable<any> {
    return this.http.get(`${this.apiUrl}/assignment/queue`).pipe(
      catchError(this.handleError)
    );
  }

  processQueue(): Observable<any> {
    return this.http.post(`${this.apiUrl}/assignment/process-queue`, {}, {
      headers: this.getHeaders()
    }).pipe(
      catchError(this.handleError)
    );
  }

  // ============= Analytics =============

  getDashboardStats(): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/dashboard-stats`).pipe(
      catchError(this.handleError)
    );
  }

  getEstimationAccuracy(): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/estimation-accuracy`).pipe(
      catchError(this.handleError)
    );
  }

  getAssignmentAccuracy(): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/assignment-accuracy`).pipe(
      catchError(this.handleError)
    );
  }

  // ============= Health Check =============

  healthCheck(): Observable<any> {
    return this.http.get(`${this.apiUrl.replace('/api', '')}/api/health`).pipe(
      catchError(this.handleError)
    );
  }
}
