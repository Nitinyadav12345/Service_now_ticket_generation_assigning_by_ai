export interface EstimationAccuracy {
  acceptanceRate: number;
  averageError: number;
  totalEstimations: number;
  accurateEstimations: number;
  overEstimations: number;
  underEstimations: number;
  monthlyTrend: MonthlyTrend[];
  byComplexity: ComplexityBreakdown[];
}

export interface MonthlyTrend {
  month: string;
  year: number;
  acceptanceRate: number;
  averageError: number;
  count: number;
}

export interface ComplexityBreakdown {
  complexity: 'Low' | 'Medium' | 'High';
  accuracy: number;
  count: number;
}

export interface AssignmentAccuracy {
  acceptanceRate: number;
  totalAssignments: number;
  reassignments: number;
  autoAssigned: number;
  manualOverrides: number;
  averageAssignmentScore: number;
  commonReassignmentPatterns: ReassignmentPattern[];
  assignmentsByMember: MemberAssignmentStats[];
}

export interface ReassignmentPattern {
  from: string;
  fromDisplayName: string;
  to: string;
  toDisplayName: string;
  count: number;
  reason?: string;
}

export interface MemberAssignmentStats {
  username: string;
  displayName: string;
  totalAssigned: number;
  completed: number;
  reassigned: number;
  averageCompletionDays: number;
  successRate: number;
}

export interface DashboardStats {
  teamCapacity: number;
  availableCapacity: number;
  utilizationPercentage: number;
  storiesCreated: number;
  storiesCompleted: number;
  estimationAccuracy: number;
  assignmentAccuracy: number;
  averageCycleTime: number;
  sprintVelocity: number;
}

export interface LearningInsight {
  id: string;
  type: 'info' | 'warning' | 'success' | 'improvement';
  icon: string;
  title: string;
  message: string;
  category: 'estimation' | 'assignment' | 'capacity' | 'performance';
  impact: 'high' | 'medium' | 'low';
  createdAt: Date;
}

export interface Recommendation {
  id: string;
  type: 'hiring' | 'training' | 'process' | 'capacity';
  title: string;
  message: string;
  priority: 'high' | 'medium' | 'low';
  actionable: boolean;
  action?: string;
}

export interface AnalyticsDashboard {
  stats: DashboardStats;
  estimationAccuracy: EstimationAccuracy;
  assignmentAccuracy: AssignmentAccuracy;
  insights: LearningInsight[];
  recommendations: Recommendation[];
  recentActivity: ActivityItem[];
}

export interface ActivityItem {
  id: string;
  type: 'story_created' | 'story_completed' | 'assignment' | 'estimation_adjusted';
  title: string;
  description: string;
  user?: string;
  issueKey?: string;
  timestamp: Date;
}

export interface PerformanceMetrics {
  velocityTrend: VelocityPoint[];
  cycleTimeTrend: CycleTimePoint[];
  throughputTrend: ThroughputPoint[];
}

export interface VelocityPoint {
  sprint: string;
  planned: number;
  completed: number;
}

export interface CycleTimePoint {
  week: string;
  averageDays: number;
}

export interface ThroughputPoint {
  week: string;
  count: number;
}