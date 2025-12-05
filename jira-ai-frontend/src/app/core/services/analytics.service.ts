import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { MockDataService } from './mock-data.service';
import { environment } from '../../../environments/environment';
import {
  EstimationAccuracy,
  AssignmentAccuracy,
  DashboardStats,
  AnalyticsDashboard,
  LearningInsight,
  Recommendation,
  PerformanceMetrics,
  ActivityItem
} from '../models/analytics.model';

@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
  private readonly endpoint = '/analytics';
  private useMockData = !environment.production; // Use mock data in dev if backend not available

  constructor(
    private api: ApiService,
    private mockData: MockDataService
  ) {}

  setUseMockData(useMock: boolean): void {
    this.useMockData = useMock;
  }

  getDashboardStats(): Observable<DashboardStats> {
    return this.api.get<DashboardStats>(`${this.endpoint}/dashboard-stats`);
  }

  getEstimationAccuracy(): Observable<EstimationAccuracy> {
    return this.api.get<EstimationAccuracy>(`${this.endpoint}/estimation-accuracy`);
  }

  getAssignmentAccuracy(): Observable<AssignmentAccuracy> {
    return this.api.get<AssignmentAccuracy>(`${this.endpoint}/assignment-accuracy`);
  }

  getLearningInsights(): Observable<any> {
    return this.api.get<any>(`${this.endpoint}/learning-insights`);
  }

  getRecommendations(): Observable<any> {
    return this.api.get<any>(`${this.endpoint}/recommendations`);
  }

  getPerformanceMetrics(): Observable<PerformanceMetrics> {
    return this.api.get<PerformanceMetrics>(`${this.endpoint}/performance-metrics`);
  }

  getRecentActivity(): Observable<any> {
    return this.api.get<any>(`${this.endpoint}/recent-activity`);
  }
}