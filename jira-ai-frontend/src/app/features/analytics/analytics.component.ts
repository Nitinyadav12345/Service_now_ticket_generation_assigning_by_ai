import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subject, takeUntil, forkJoin } from 'rxjs';
import { BaseChartDirective } from 'ng2-charts';

import { AnalyticsService } from '../../core/services/analytics.service';
import {
  DashboardStats,
  EstimationAccuracy,
  AssignmentAccuracy,
  LearningInsight,
  Recommendation,
  PerformanceMetrics,
  ActivityItem
} from '../../core/models/analytics.model';

import { StatsCardComponent } from './components/stats-card/stats-card.component';
import { EstimationChartComponent } from './components/estimation-chart/estimation-chart.component';
import { AssignmentChartComponent } from './components/assignment-chart/assignment-chart.component';
import { InsightsCardComponent } from './components/insights-card/insights-card.component';
import { RecommendationsCardComponent } from './components/recommendations-card/recommendations-card.component';
import { ActivityFeedComponent } from './components/activity-feed/activity-feed.component';
import { PerformanceChartsComponent } from './components/performance-charts/performance-charts.component';
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    BaseChartDirective,
    StatsCardComponent,
    EstimationChartComponent,
    AssignmentChartComponent,
    InsightsCardComponent,
    RecommendationsCardComponent,
    ActivityFeedComponent,
    PerformanceChartsComponent,
    LoadingSpinnerComponent
  ],
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.scss']
})
export class AnalyticsComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  // Data
  stats: DashboardStats | null = null;
  estimationAccuracy: EstimationAccuracy | null = null;
  assignmentAccuracy: AssignmentAccuracy | null = null;
  insights: LearningInsight[] = [];
  recommendations: Recommendation[] = [];
  performanceMetrics: PerformanceMetrics | null = null;
  recentActivity: ActivityItem[] = [];

  // UI State
  isLoading = true;
  selectedTimeRange = '30days';
  activeTab = 'overview';

  timeRangeOptions = [
    { value: '7days', label: 'Last 7 Days' },
    { value: '30days', label: 'Last 30 Days' },
    { value: '90days', label: 'Last 90 Days' },
    { value: 'all', label: 'All Time' }
  ];

  tabs = [
    { id: 'overview', label: 'Overview', icon: 'fa-chart-pie' },
    { id: 'estimation', label: 'Estimation', icon: 'fa-calculator' },
    { id: 'assignment', label: 'Assignment', icon: 'fa-user-check' },
    { id: 'performance', label: 'Performance', icon: 'fa-tachometer-alt' }
  ];

  constructor(private analyticsService: AnalyticsService) {}

  ngOnInit(): void {
    this.loadAllData();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadAllData(): void {
    this.isLoading = true;

    forkJoin({
      stats: this.analyticsService.getDashboardStats(),
      estimation: this.analyticsService.getEstimationAccuracy(),
      assignment: this.analyticsService.getAssignmentAccuracy(),
      insights: this.analyticsService.getLearningInsights(),
      recommendations: this.analyticsService.getRecommendations(),
      performance: this.analyticsService.getPerformanceMetrics(),
      activity: this.analyticsService.getRecentActivity()
    })
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (data) => {
          this.stats = data.stats;
          this.estimationAccuracy = data.estimation;
          this.assignmentAccuracy = data.assignment;
          this.insights = data.insights;
          this.recommendations = data.recommendations;
          this.performanceMetrics = data.performance;
          this.recentActivity = data.activity;
          this.isLoading = false;
        },
        error: (error) => {
          console.error('Error loading analytics data:', error);
          this.isLoading = false;
        }
      });
  }

  onTimeRangeChange(range: string): void {
    this.selectedTimeRange = range;
    this.loadAllData();
  }

  setActiveTab(tabId: string): void {
    this.activeTab = tabId;
  }

  refreshData(): void {
    this.loadAllData();
  }
}