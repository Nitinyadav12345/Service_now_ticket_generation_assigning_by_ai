import { Injectable } from '@angular/core';
import { Observable, of, delay } from 'rxjs';
import {
  AnalyticsDashboard,
  DashboardStats,
  EstimationAccuracy,
  AssignmentAccuracy,
  LearningInsight,
  Recommendation,
  ActivityItem,
  PerformanceMetrics
} from '../models/analytics.model';
import { TeamMember } from '../models/team-member.model';
import { TeamCapacity } from '../models/capacity.model';
import { Story } from '../models/story.model';

@Injectable({
  providedIn: 'root'
})
export class MockDataService {

  // Dashboard Stats
  getDashboardStats(): Observable<DashboardStats> {
    const stats: DashboardStats = {
      teamCapacity: 250,
      availableCapacity: 70,
      utilizationPercentage: 72,
      storiesCreated: 156,
      storiesCompleted: 142,
      estimationAccuracy: 78,
      assignmentAccuracy: 82,
      averageCycleTime: 4.2,
      sprintVelocity: 45
    };
    return of(stats).pipe(delay(500));
  }

  // Estimation Accuracy
  getEstimationAccuracy(): Observable<EstimationAccuracy> {
    const data: EstimationAccuracy = {
      acceptanceRate: 78,
      averageError: 1.2,
      totalEstimations: 156,
      accurateEstimations: 122,
      overEstimations: 18,
      underEstimations: 16,
      monthlyTrend: [
        { month: 'Jul', year: 2024, acceptanceRate: 65, averageError: 2.1, count: 18 },
        { month: 'Aug', year: 2024, acceptanceRate: 68, averageError: 1.9, count: 22 },
        { month: 'Sep', year: 2024, acceptanceRate: 72, averageError: 1.6, count: 25 },
        { month: 'Oct', year: 2024, acceptanceRate: 75, averageError: 1.4, count: 28 },
        { month: 'Nov', year: 2024, acceptanceRate: 78, averageError: 1.2, count: 32 },
        { month: 'Dec', year: 2024, acceptanceRate: 82, averageError: 1.0, count: 31 }
      ],
      byComplexity: [
        { complexity: 'Low', accuracy: 92, count: 45 },
        { complexity: 'Medium', accuracy: 78, count: 72 },
        { complexity: 'High', accuracy: 65, count: 39 }
      ]
    };
    return of(data).pipe(delay(500));
  }

  // Assignment Accuracy
  getAssignmentAccuracy(): Observable<AssignmentAccuracy> {
    const data: AssignmentAccuracy = {
      acceptanceRate: 82,
      totalAssignments: 156,
      reassignments: 28,
      autoAssigned: 142,
      manualOverrides: 14,
      averageAssignmentScore: 87.5,
      commonReassignmentPatterns: [
        { from: 'john.doe', fromDisplayName: 'John Doe', to: 'jane.smith', toDisplayName: 'Jane Smith', count: 8, reason: 'Frontend expertise needed' },
        { from: 'alice.johnson', fromDisplayName: 'Alice Johnson', to: 'john.doe', toDisplayName: 'John Doe', count: 5, reason: 'Complexity too high for Junior' },
        { from: 'jane.smith', fromDisplayName: 'Jane Smith', to: 'alice.johnson', toDisplayName: 'Alice Johnson', count: 4, reason: 'Growth opportunity' },
        { from: 'bob.wilson', fromDisplayName: 'Bob Wilson', to: 'john.doe', toDisplayName: 'John Doe', count: 3, reason: 'DevOps to Backend transition' }
      ],
      assignmentsByMember: [
        { username: 'john.doe', displayName: 'John Doe', totalAssigned: 45, completed: 42, reassigned: 3, averageCompletionDays: 3.5, successRate: 93 },
        { username: 'jane.smith', displayName: 'Jane Smith', totalAssigned: 38, completed: 35, reassigned: 5, averageCompletionDays: 4.2, successRate: 87 },
        { username: 'alice.johnson', displayName: 'Alice Johnson', totalAssigned: 28, completed: 24, reassigned: 6, averageCompletionDays: 5.8, successRate: 79 },
        { username: 'bob.wilson', displayName: 'Bob Wilson', totalAssigned: 25, completed: 23, reassigned: 4, averageCompletionDays: 3.8, successRate: 84 },
        { username: 'charlie.brown', displayName: 'Charlie Brown', totalAssigned: 20, completed: 18, reassigned: 10, averageCompletionDays: 4.5, successRate: 50 }
      ]
    };
    return of(data).pipe(delay(500));
  }

  // Learning Insights
  getLearningInsights(): Observable<LearningInsight[]> {
    const insights: LearningInsight[] = [
      {
        id: '1',
        type: 'improvement',
        icon: 'fa-chart-line',
        title: 'Estimation Accuracy Improving',
        message: 'Authentication stories are now estimated more accurately. AI has learned from 15 corrections and reduced error by 30%.',
        category: 'estimation',
        impact: 'high',
        createdAt: new Date()
      },
      {
        id: '2',
        type: 'success',
        icon: 'fa-user-check',
        title: 'Assignment Pattern Learned',
        message: 'Frontend tasks are now preferentially assigned to Jane Smith based on 12 successful completions.',
        category: 'assignment',
        impact: 'medium',
        createdAt: new Date(Date.now() - 86400000)
      },
      {
        id: '3',
        type: 'warning',
        icon: 'fa-clock',
        title: 'Testing Tasks Taking Longer',
        message: 'Testing tasks are taking 20% longer than estimated. Consider adjusting estimation factors.',
        category: 'estimation',
        impact: 'medium',
        createdAt: new Date(Date.now() - 172800000)
      },
      {
        id: '4',
        type: 'info',
        icon: 'fa-brain',
        title: 'New Pattern Detected',
        message: 'Stories involving database migrations typically require 2 additional story points.',
        category: 'estimation',
        impact: 'low',
        createdAt: new Date(Date.now() - 259200000)
      },
      {
        id: '5',
        type: 'success',
        icon: 'fa-trophy',
        title: 'Team Velocity Increased',
        message: 'Sprint velocity has increased by 15% over the last 3 sprints due to better task distribution.',
        category: 'performance',
        impact: 'high',
        createdAt: new Date(Date.now() - 345600000)
      }
    ];
    return of(insights).pipe(delay(300));
  }

  // Recommendations
  getRecommendations(): Observable<Recommendation[]> {
    const recommendations: Recommendation[] = [
      {
        id: '1',
        type: 'hiring',
        title: 'Consider Backend Capacity',
        message: 'Backend tasks are frequently queued. Team could benefit from additional backend developer.',
        priority: 'high',
        actionable: true,
        action: 'Review hiring plan'
      },
      {
        id: '2',
        type: 'training',
        title: 'Junior Developer Ready for Growth',
        message: 'Alice Johnson is ready for Medium priority tasks based on recent performance improvements.',
        priority: 'medium',
        actionable: true,
        action: 'Update skill level'
      },
      {
        id: '3',
        type: 'capacity',
        title: 'Adjust Sprint Capacity',
        message: 'Based on historical data, consider setting sprint capacity to 18 pts/person instead of 20.',
        priority: 'medium',
        actionable: true,
        action: 'Update settings'
      },
      {
        id: '4',
        type: 'process',
        title: 'Improve Testing Estimates',
        message: 'Add 1.2x multiplier for testing tasks to improve estimation accuracy.',
        priority: 'low',
        actionable: true,
        action: 'Update AI config'
      }
    ];
    return of(recommendations).pipe(delay(300));
  }

  // Performance Metrics
  getPerformanceMetrics(): Observable<PerformanceMetrics> {
    const metrics: PerformanceMetrics = {
      velocityTrend: [
        { sprint: 'Sprint 18', planned: 42, completed: 38 },
        { sprint: 'Sprint 19', planned: 45, completed: 43 },
        { sprint: 'Sprint 20', planned: 44, completed: 44 },
        { sprint: 'Sprint 21', planned: 46, completed: 42 },
        { sprint: 'Sprint 22', planned: 48, completed: 47 },
        { sprint: 'Sprint 23', planned: 50, completed: 48 }
      ],
      cycleTimeTrend: [
        { week: 'Week 1', averageDays: 5.2 },
        { week: 'Week 2', averageDays: 4.8 },
        { week: 'Week 3', averageDays: 4.5 },
        { week: 'Week 4', averageDays: 4.3 },
        { week: 'Week 5', averageDays: 4.1 },
        { week: 'Week 6', averageDays: 3.9 },
        { week: 'Week 7', averageDays: 4.0 },
        { week: 'Week 8', averageDays: 3.8 }
      ],
      throughputTrend: [
        { week: 'Week 1', count: 8 },
        { week: 'Week 2', count: 10 },
        { week: 'Week 3', count: 9 },
        { week: 'Week 4', count: 12 },
        { week: 'Week 5', count: 11 },
        { week: 'Week 6', count: 14 },
        { week: 'Week 7', count: 13 },
        { week: 'Week 8', count: 15 }
      ]
    };
    return of(metrics).pipe(delay(500));
  }

  // Recent Activity
  getRecentActivity(): Observable<ActivityItem[]> {
    const activities: ActivityItem[] = [
      {
        id: '1',
        type: 'story_created',
        title: 'Story Created',
        description: 'User authentication with OAuth created and assigned to John Doe',
        user: 'AI Assistant',
        issueKey: 'PROJ-156',
        timestamp: new Date(Date.now() - 1800000)
      },
      {
        id: '2',
        type: 'story_completed',
        title: 'Story Completed',
        description: 'Export CSV feature completed by Jane Smith',
        user: 'jane.smith',
        issueKey: 'PROJ-152',
        timestamp: new Date(Date.now() - 7200000)
      },
      {
        id: '3',
        type: 'estimation_adjusted',
        title: 'Estimation Adjusted',
        description: 'Story points changed from 5 to 8 for PROJ-154',
        user: 'john.doe',
        issueKey: 'PROJ-154',
        timestamp: new Date(Date.now() - 14400000)
      },
      {
        id: '4',
        type: 'assignment',
        title: 'Task Reassigned',
        description: 'API integration task reassigned from Alice to Bob',
        user: 'System',
        issueKey: 'PROJ-148',
        timestamp: new Date(Date.now() - 28800000)
      },
      {
        id: '5',
        type: 'story_created',
        title: 'Story Created',
        description: 'Dashboard redesign created with 5 subtasks',
        user: 'AI Assistant',
        issueKey: 'PROJ-155',
        timestamp: new Date(Date.now() - 43200000)
      }
    ];
    return of(activities).pipe(delay(300));
  }

  // Team Members
  getTeamMembers(): Observable<TeamMember[]> {
    const members: TeamMember[] = [
      {
        id: '1',
        username: 'john.doe',
        displayName: 'John Doe',
        email: 'john.doe@company.com',
        avatarUrl: '',
        skills: ['Python', 'FastAPI', 'PostgreSQL', 'AWS', 'Docker'],
        maxStoryPoints: 20,
        currentStoryPoints: 15,
        currentTicketCount: 5,
        availabilityStatus: 'busy',
        seniorityLevel: 'Senior',
        preferredWork: ['Backend', 'API'],
        performanceScore: 8.5,
        averageCompletionDays: 3.5,
        qualityScore: 9.0,
        isOutOfOffice: false
      },
      {
        id: '2',
        username: 'jane.smith',
        displayName: 'Jane Smith',
        email: 'jane.smith@company.com',
        avatarUrl: '',
        skills: ['React', 'TypeScript', 'Tailwind CSS', 'Next.js'],
        maxStoryPoints: 20,
        currentStoryPoints: 18,
        currentTicketCount: 4,
        availabilityStatus: 'busy',
        seniorityLevel: 'Mid',
        preferredWork: ['Frontend', 'UI/UX'],
        performanceScore: 7.8,
        averageCompletionDays: 4.2,
        qualityScore: 8.5,
        isOutOfOffice: false
      },
      {
        id: '3',
        username: 'alice.johnson',
        displayName: 'Alice Johnson',
        email: 'alice.johnson@company.com',
        avatarUrl: '',
        skills: ['Python', 'React', 'PostgreSQL', 'Node.js'],
        maxStoryPoints: 15,
        currentStoryPoints: 5,
        currentTicketCount: 2,
        availabilityStatus: 'available',
        seniorityLevel: 'Junior',
        preferredWork: ['Full-Stack'],
        performanceScore: 7.2,
        averageCompletionDays: 5.8,
        qualityScore: 7.5,
        isOutOfOffice: false
      },
      {
        id: '4',
        username: 'bob.wilson',
        displayName: 'Bob Wilson',
        email: 'bob.wilson@company.com',
        avatarUrl: '',
        skills: ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Terraform'],
        maxStoryPoints: 20,
        currentStoryPoints: 0,
        currentTicketCount: 0,
        availabilityStatus: 'ooo',
        seniorityLevel: 'Senior',
        preferredWork: ['DevOps', 'Infrastructure'],
        performanceScore: 8.8,
        averageCompletionDays: 3.8,
        qualityScore: 9.2,
        isOutOfOffice: true,
        oooEndDate: new Date('2024-12-20')
      },
      {
        id: '5',
        username: 'charlie.brown',
        displayName: 'Charlie Brown',
        email: 'charlie.brown@company.com',
        avatarUrl: '',
        skills: ['React', 'Vue.js', 'CSS', 'JavaScript'],
        maxStoryPoints: 18,
        currentStoryPoints: 16,
        currentTicketCount: 6,
        availabilityStatus: 'overloaded',
        seniorityLevel: 'Mid',
        preferredWork: ['Frontend'],
        performanceScore: 7.0,
        averageCompletionDays: 4.5,
        qualityScore: 7.8,
        isOutOfOffice: false
      }
    ];
    return of(members).pipe(delay(500));
  }

  // Team Capacity
  getTeamCapacity(): Observable<TeamCapacity> {
    const capacity: TeamCapacity = {
      totalTeamCapacity: 93,
      totalUsedCapacity: 54,
      availableCapacity: 39,
      utilizationPercentage: 58,
      teamSize: 5,
      availableMembers: 3,
      membersByStatus: {
        available: ['alice.johnson'],
        busy: ['john.doe', 'jane.smith'],
        overloaded: ['charlie.brown'],
        ooo: ['bob.wilson']
      }
    };
    return of(capacity).pipe(delay(300));
  }

  // Recent Stories
  getRecentStories(): Observable<Story[]> {
    const stories: Story[] = [
      {
        requestId: '1',
        userPrompt: 'Create user authentication with email and password',
        generatedTitle: 'As a user, I want to authenticate with email and password',
        generatedDescription: 'Implement secure user authentication system with email/password login.',
        acceptanceCriteria: ['User can register', 'User can login', 'Password is hashed'],
        estimatedPoints: 8,
        jiraIssueKey: 'PROJ-156',
        jiraUrl: 'https://jira.example.com/browse/PROJ-156',
        status: 'completed',
        priority: 'High',
        issueType: 'Story',
        assignee: { username: 'john.doe', displayName: 'John Doe' },
        createdAt: new Date(Date.now() - 3600000)
      },
      {
        requestId: '2',
        userPrompt: 'Add CSV export functionality',
        generatedTitle: 'As a user, I want to export data as CSV',
        generatedDescription: 'Allow users to export their data in CSV format.',
        acceptanceCriteria: ['Export button visible', 'CSV downloads correctly', 'All fields included'],
        estimatedPoints: 5,
        jiraIssueKey: 'PROJ-155',
        jiraUrl: 'https://jira.example.com/browse/PROJ-155',
        status: 'processing',
        priority: 'Medium',
        issueType: 'Story',
        assignee: { username: 'jane.smith', displayName: 'Jane Smith' },
        createdAt: new Date(Date.now() - 18000000)
      },
      {
        requestId: '3',
        userPrompt: 'Create dashboard with analytics charts',
        generatedTitle: 'As a manager, I want to view analytics dashboard',
        generatedDescription: 'Build analytics dashboard with key metrics and charts.',
        acceptanceCriteria: ['Charts render correctly', 'Data is accurate', 'Responsive design'],
        estimatedPoints: 13,
        jiraIssueKey: 'PROJ-154',
        jiraUrl: 'https://jira.example.com/browse/PROJ-154',
        status: 'completed',
        priority: 'High',
        issueType: 'Story',
        assignee: { username: 'jane.smith', displayName: 'Jane Smith' },
        createdAt: new Date(Date.now() - 86400000)
      }
    ];
    return of(stories).pipe(delay(500));
  }
}