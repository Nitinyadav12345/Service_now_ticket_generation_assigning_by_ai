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
  private useMockData = true; // Set to false when backend is ready

  constructor(
    private api: ApiService,
    private mockData: MockDataService
  ) {}

  getDashboardStats(): Observable<DashboardStats> {
    if (this.useMockData) {
      return this.mockData.getDashboardStats();
    }
    return this.api.get<DashboardStats>(`${this.endpoint}/dashboard-stats`);
  }

  getEstimationAccuracy(): Observable<EstimationAccuracy> {
    if (this.useMockData) {
      return this.mockData.getEstimationAccuracy();
    }
    return this.api.get<EstimationAccuracy>(`${this.endpoint}/estimation-accuracy`);
  }

  getAssignmentAccuracy(): Observable<AssignmentAccuracy> {
    if (this.useMockData) {
      return this.mockData.getAssignmentAccuracy();
    }
    return this.api.get<AssignmentAccuracy>(`${this.endpoint}/assignment-accuracy`);
  }

  getLearningInsights(): Observable<LearningInsight[]> {
    if (this.useMockData) {
      return this.mockData.getLearningInsights();
    }
    return this.api.get<LearningInsight[]>(`${this.endpoint}/insights`);
  }

  getRecommendations(): Observable<Recommendation[]> {
    if (this.useMockData) {
      return this.mockData.getRecommendations();
    }
    return this.api.get<Recommendation[]>(`${this.endpoint}/recommendations`);
  }

  getPerformanceMetrics(): Observable<PerformanceMetrics> {
    if (this.useMockData) {
      return this.mockData.getPerformanceMetrics();
    }
    return this.api.get<PerformanceMetrics>(`${this.endpoint}/performance`);
  }

  getRecentActivity(): Observable<ActivityItem[]> {
    if (this.useMockData) {
      return this.mockData.getRecentActivity();
    }
    return this.api.get<ActivityItem[]>(`${this.endpoint}/activity`);
  }
}