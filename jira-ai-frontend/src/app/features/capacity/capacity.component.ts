import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subject, takeUntil } from 'rxjs';
import { CapacityService } from '../../core/services/capacity.service';
import { AssignmentService } from '../../core/services/assignment.service';
import { NotificationService } from '../../core/services/notification.service';
import { TeamMember, AvailabilityStatus } from '../../core/models/team-member.model';
import { TeamCapacity } from '../../core/models/capacity.model';
import { AssignmentQueue } from '../../core/models/assignment.model';
import { StatusBadgeComponent } from '../../shared/components/status-badge/status-badge.component';
import { CapacityBarComponent } from '../../shared/components/capacity-bar/capacity-bar.component';
import { SkillTagComponent } from '../../shared/components/skill-tag/skill-tag.component';
import { EmptyStateComponent } from '../../shared/components/empty-state/empty-state.component';
import { ConfirmationDialogComponent } from '../../shared/components/confirmation-dialog/confirmation-dialog.component';
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';

@Component({
  selector: 'app-capacity',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    StatusBadgeComponent,
    CapacityBarComponent,
    SkillTagComponent,
    EmptyStateComponent,
    ConfirmationDialogComponent,
    LoadingSpinnerComponent
  ],
  templateUrl: './capacity.component.html',
  styleUrls: ['./capacity.component.scss']
})
export class CapacityComponent implements OnInit, OnDestroy {
  teamCapacity: TeamCapacity | null = null;
  members: TeamMember[] = [];
  assignmentQueue: AssignmentQueue | null = null;
  
  isLoading = false;
  isRefreshing = false;
  selectedMember: TeamMember | null = null;
  showOOOModal = false;
  showMemberDetail = false;
  
  filterStatus: string = 'all';
  searchQuery: string = '';

  // OOO Form
  oooForm = {
    startDate: '',
    endDate: '',
    reason: '',
    partialCapacity: 0
  };

  private destroy$ = new Subject<void>();

  constructor(
    private capacityService: CapacityService,
    private assignmentService: AssignmentService,
    private notificationService: NotificationService
  ) {}

  ngOnInit(): void {
    this.loadData();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadData(): void {
    this.isLoading = true;
    
    // Load team capacity
    this.capacityService.getTeamCapacity()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (capacity) => {
          this.teamCapacity = capacity;
        },
        error: (err) => console.error('Error loading capacity:', err)
      });

    // Load team members
    this.capacityService.getAllMembers()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (members) => {
          this.members = members;
          this.isLoading = false;
        },
        error: (err) => {
          console.error('Error loading members:', err);
          this.isLoading = false;
          // Use mock data for demo
          this.loadMockData();
        }
      });

    // Load assignment queue
    this.assignmentService.getQueue()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (queue) => {
          this.assignmentQueue = queue;
        },
        error: (err) => console.error('Error loading queue:', err)
      });
  }

  loadMockData(): void {
    this.teamCapacity = {
      totalTeamCapacity: 100,
      totalUsedCapacity: 72,
      availableCapacity: 28,
      utilizationPercentage: 72,
      teamSize: 5,
      availableMembers: 3,
      membersByStatus: {
        available: ['alice.johnson'],
        busy: ['john.doe', 'jane.smith'],
        overloaded: ['mike.wilson'],
        ooo: ['bob.brown']
      }
    };

    this.members = [
      {
        id: '1',
        username: 'john.doe',
        displayName: 'John Doe',
        email: 'john@example.com',
        skills: ['Python', 'FastAPI', 'PostgreSQL', 'AWS'],
        maxStoryPoints: 20,
        currentStoryPoints: 15,
        currentTicketCount: 5,
        availabilityStatus: 'busy',
        seniorityLevel: 'Senior',
        performanceScore: 8.5,
        averageCompletionDays: 3.5,
        qualityScore: 8.5,
        isOutOfOffice: false
      },
      {
        id: '2',
        username: 'jane.smith',
        displayName: 'Jane Smith',
        email: 'jane@example.com',
        skills: ['React', 'TypeScript', 'Tailwind CSS', 'Node.js'],
        maxStoryPoints: 20,
        currentStoryPoints: 18,
        currentTicketCount: 4,
        availabilityStatus: 'busy',
        seniorityLevel: 'Mid',
        performanceScore: 7.8,
        averageCompletionDays: 4.2,
        qualityScore: 7.8,
        isOutOfOffice: false
      },
      {
        id: '3',
        username: 'bob.brown',
        displayName: 'Bob Brown',
        email: 'bob@example.com',
        skills: ['AWS', 'Docker', 'Kubernetes', 'CI/CD'],
        maxStoryPoints: 20,
        currentStoryPoints: 0,
        currentTicketCount: 0,
        availabilityStatus: 'ooo',
        seniorityLevel: 'Senior',
        performanceScore: 9.0,
        averageCompletionDays: 2.8,
        qualityScore: 9.0,
        isOutOfOffice: true,
        oooEndDate: new Date('2024-12-20')
      },
      {
        id: '4',
        username: 'alice.johnson',
        displayName: 'Alice Johnson',
        email: 'alice@example.com',
        skills: ['Python', 'React', 'PostgreSQL'],
        maxStoryPoints: 15,
        currentStoryPoints: 5,
        currentTicketCount: 2,
        availabilityStatus: 'available',
        seniorityLevel: 'Junior',
        performanceScore: 7.2,
        averageCompletionDays: 5.8,
        qualityScore: 7.2,
        isOutOfOffice: false
      },
      {
        id: '5',
        username: 'mike.wilson',
        displayName: 'Mike Wilson',
        email: 'mike@example.com',
        skills: ['Java', 'Spring Boot', 'MySQL', 'Redis'],
        maxStoryPoints: 20,
        currentStoryPoints: 22,
        currentTicketCount: 7,
        availabilityStatus: 'overloaded',
        seniorityLevel: 'Senior',
        performanceScore: 8.0,
        averageCompletionDays: 3.0,
        qualityScore: 8.0,
        isOutOfOffice: false
      }
    ];

    this.assignmentQueue = {
      queuedCount: 2,
      items: [
        {
          issueKey: 'PROJ-125',
          priority: 'High',
          estimatedPoints: 8,
          requiredSkills: ['Python', 'AWS'],
          attempts: 2,
          reason: 'All candidates would be overloaded',
          createdAt: new Date(),
          waitingTime: '2 hours'
        },
        {
          issueKey: 'PROJ-126',
          priority: 'Medium',
          estimatedPoints: 5,
          requiredSkills: ['React', 'GraphQL'],
          attempts: 1,
          reason: 'No team members with required skills available',
          createdAt: new Date(),
          waitingTime: '5 hours'
        }
      ]
    };
  }

  refreshCapacity(): void {
    this.isRefreshing = true;
    this.capacityService.refreshCapacity()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => {
          this.loadData();
          this.notificationService.success('Capacity refreshed successfully');
          this.isRefreshing = false;
        },
        error: () => {
          this.notificationService.error('Failed to refresh capacity');
          this.isRefreshing = false;
        }
      });
  }

  get filteredMembers(): TeamMember[] {
    let filtered = this.members;

    if (this.filterStatus !== 'all') {
      filtered = filtered.filter(m => m.availabilityStatus === this.filterStatus);
    }

    if (this.searchQuery) {
      const query = this.searchQuery.toLowerCase();
      filtered = filtered.filter(m => 
        m.displayName.toLowerCase().includes(query) ||
        m.username.toLowerCase().includes(query) ||
        m.skills.some(s => s.toLowerCase().includes(query))
      );
    }

    return filtered;
  }

  getStatusCount(status: AvailabilityStatus): number {
    return this.members.filter(m => m.availabilityStatus === status).length;
  }

  openMemberDetail(member: TeamMember): void {
    this.selectedMember = member;
    this.showMemberDetail = true;
  }

  closeMemberDetail(): void {
    this.showMemberDetail = false;
    this.selectedMember = null;
  }

  openOOOModal(member: TeamMember): void {
    this.selectedMember = member;
    this.oooForm = {
      startDate: new Date().toISOString().split('T')[0],
      endDate: '',
      reason: '',
      partialCapacity: 0
    };
    this.showOOOModal = true;
  }

  closeOOOModal(): void {
    this.showOOOModal = false;
    this.selectedMember = null;
  }

  submitOOO(): void {
    if (!this.selectedMember) return;

    this.capacityService.markOutOfOffice({
      username: this.selectedMember.username,
      startDate: this.oooForm.startDate,
      endDate: this.oooForm.endDate,
      reason: this.oooForm.reason,
      partialCapacity: this.oooForm.partialCapacity
    }).pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => {
          this.notificationService.success('Out of office marked successfully');
          this.closeOOOModal();
          this.loadData();
        },
        error: () => {
          this.notificationService.error('Failed to mark out of office');
        }
      });
  }

  processQueue(): void {
    this.assignmentService.processQueue()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => {
          this.notificationService.success('Queue processing started');
          this.loadData();
        },
        error: () => {
          this.notificationService.error('Failed to process queue');
        }
      });
  }
}