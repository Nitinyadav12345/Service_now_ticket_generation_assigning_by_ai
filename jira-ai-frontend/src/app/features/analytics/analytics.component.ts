import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subject, takeUntil, forkJoin } from 'rxjs';

import { AnalyticsService } from '../../core/services/analytics.service';

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.scss']
})
export class AnalyticsComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  // Data
  stats: any = null;
  estimationAccuracy: any = null;
  assignmentAccuracy: any = null;
  insights: any[] = [];
  recommendations: any[] = [];
  performanceMetrics: any = null;
  recentActivity: any[] = [];
  filteredActivity: any[] = [];

  // UI State
  isLoading = true;
  isRefreshingActivity = false;
  selectedTimeRange = '30days';
  activeTab = 'overview';
  activityFilter = 'all';

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
          // Map API response to component data
          this.stats = data.stats;
          this.estimationAccuracy = data.estimation;
          this.assignmentAccuracy = data.assignment;
          this.insights = data.insights?.insights || data.insights || [];
          this.recommendations = data.recommendations?.recommendations || data.recommendations || [];
          this.performanceMetrics = data.performance;
          this.recentActivity = data.activity?.activities || data.activity || [];
          this.applyActivityFilter();
          this.isLoading = false;
          
          console.log('Analytics data loaded successfully');
          console.log('Recent activity count:', this.recentActivity.length);
        },
        error: (error) => {
          console.error('Error loading analytics data:', error);
          this.isLoading = false;
        }
      });
  }

  refreshActivity(): void {
    this.isRefreshingActivity = true;
    this.analyticsService.getRecentActivity()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (data) => {
          this.recentActivity = data?.activities || data || [];
          this.applyActivityFilter();
          this.isRefreshingActivity = false;
          console.log('Activity refreshed:', this.recentActivity.length, 'items');
        },
        error: (error) => {
          console.error('Error refreshing activity:', error);
          this.isRefreshingActivity = false;
        }
      });
  }

  filterActivity(filter: string): void {
    this.activityFilter = filter;
    this.applyActivityFilter();
  }

  applyActivityFilter(): void {
    if (this.activityFilter === 'all') {
      this.filteredActivity = this.recentActivity;
    } else if (this.activityFilter === 'assignments') {
      this.filteredActivity = this.recentActivity.filter(a => 
        a.type?.includes('assign') || a.type?.includes('reassign')
      );
    } else if (this.activityFilter === 'stories') {
      this.filteredActivity = this.recentActivity.filter(a => 
        a.type?.includes('story') || a.type?.includes('created')
      );
    } else if (this.activityFilter === 'changes') {
      this.filteredActivity = this.recentActivity.filter(a => 
        a.type?.includes('changed') || a.type?.includes('updated') || a.type?.includes('status')
      );
    }
  }

  getActivityTypeLabel(type: string): string {
    const labels: { [key: string]: string } = {
      'story_created': 'Story',
      'story_completed': 'Completed',
      'ticket_assigned': 'Assigned',
      'ticket_reassigned': 'Reassigned',
      'assignee_changed': 'Reassigned',
      'status_changed': 'Status',
      'priority_changed': 'Priority',
      'story_points_changed': 'Points',
      'ticket_updated': 'Updated'
    };
    return labels[type] || type;
  }

  formatActivityTime(timestamp: string): string {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
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