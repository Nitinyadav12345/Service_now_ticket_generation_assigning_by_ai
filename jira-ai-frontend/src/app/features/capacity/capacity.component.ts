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
  isSyncing = false;
  selectedMember: TeamMember | null = null;
  showOOOModal = false;
  showMemberDetail = false;
  showEditModal = false;
  
  filterStatus: string = 'all';
  searchQuery: string = '';

  // OOO Form
  oooForm = {
    startDate: '',
    endDate: '',
    reason: '',
    partialCapacity: 0
  };

  // Edit Form
  editForm = {
    displayName: '',
    email: '',
    designation: '',
    skills: [] as string[],
    maxStoryPoints: 20,
    seniorityLevel: 'Mid'
  };

  newSkill = '';

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
        error: (err) => {
          console.error('Error loading capacity:', err);
          this.notificationService.error('Failed to load team capacity');
        }
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
          this.notificationService.error('Failed to load team members. Please check backend connection.');
        }
      });

    // Load assignment queue
    this.assignmentService.getQueue()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (queue) => {
          this.assignmentQueue = queue;
        },
        error: (err) => {
          console.error('Error loading queue:', err);
        }
      });
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

  syncFromJira(): void {
    this.isSyncing = true;
    this.capacityService.syncFromJira()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          this.loadData();
          this.notificationService.success(
            `Synced ${response.synced_count} team members from Jira successfully`
          );
          this.isSyncing = false;
        },
        error: (err) => {
          console.error('Sync error:', err);
          this.notificationService.error('Failed to sync from Jira. Check your Jira credentials.');
          this.isSyncing = false;
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

  openEditModal(member: TeamMember): void {
    this.selectedMember = member;
    this.editForm = {
      displayName: member.displayName,
      email: member.email,
      designation: member.designation || '',
      skills: [...member.skills],
      maxStoryPoints: member.maxStoryPoints,
      seniorityLevel: member.seniorityLevel
    };
    this.newSkill = '';
    this.showEditModal = true;
  }

  closeEditModal(): void {
    this.showEditModal = false;
    this.selectedMember = null;
    this.newSkill = '';
  }

  addSkill(): void {
    if (this.newSkill.trim() && !this.editForm.skills.includes(this.newSkill.trim())) {
      this.editForm.skills.push(this.newSkill.trim());
      this.newSkill = '';
    }
  }

  removeSkill(skill: string): void {
    this.editForm.skills = this.editForm.skills.filter(s => s !== skill);
  }

  submitEdit(): void {
    if (!this.selectedMember) return;

    this.capacityService.updateMember(this.selectedMember.username, {
      displayName: this.editForm.displayName,
      email: this.editForm.email,
      designation: this.editForm.designation,
      skills: this.editForm.skills,
      maxStoryPoints: this.editForm.maxStoryPoints,
      seniorityLevel: this.editForm.seniorityLevel
    }).pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => {
          this.notificationService.success('Team member updated successfully');
          this.closeEditModal();
          this.loadData();
        },
        error: () => {
          this.notificationService.error('Failed to update team member');
        }
      });
  }
}