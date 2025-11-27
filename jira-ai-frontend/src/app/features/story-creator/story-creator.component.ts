import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Subject, takeUntil, interval, switchMap, takeWhile } from 'rxjs';
import { StoryService } from '../../core/services/story.service';
import { NotificationService } from '../../core/services/notification.service';
import { 
  StoryRequest, 
  StoryResponse, 
  Priority, 
  IssueType 
} from '../../core/models/story.model';
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';
import { PriorityBadgeComponent } from '../../shared/components/priority-badge/priority-badge.component';
import { StatusBadgeComponent } from '../../shared/components/status-badge/status-badge.component';
import { SkillTagComponent } from '../../shared/components/skill-tag/skill-tag.component';

@Component({
  selector: 'app-story-creator',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    LoadingSpinnerComponent,
    PriorityBadgeComponent,
    StatusBadgeComponent,
    SkillTagComponent
  ],
  templateUrl: './story-creator.component.html',
  styleUrls: ['./story-creator.component.scss']
})
export class StoryCreatorComponent implements OnInit, OnDestroy {
  storyForm!: FormGroup;
  isSubmitting = false;
  showResult = false;
  createdStory: StoryResponse | null = null;
  
  priorities: Priority[] = ['Highest', 'High', 'Medium', 'Low', 'Lowest'];
  issueTypes: IssueType[] = ['Story', 'Task', 'Bug'];
  
  examplePrompts = [
    'Create user authentication with email, password, and Google OAuth',
    'Build a dashboard showing real-time analytics with charts',
    'Implement file upload feature with drag and drop support',
    'Create REST API endpoints for user management',
    'Design and implement a notification system with email alerts'
  ];

  private destroy$ = new Subject<void>();

  constructor(
    private fb: FormBuilder,
    private storyService: StoryService,
    private notificationService: NotificationService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.initForm();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private initForm(): void {
    this.storyForm = this.fb.group({
      prompt: ['', [Validators.required, Validators.minLength(10)]],
      issueType: ['Story'],
      priority: ['Medium'],
      projectKey: [''],
      epicKey: [''],
      labels: [''],
      autoEstimate: [true],
      autoBreakdown: [true],
      autoAssign: [true]
    });
  }

  useExample(example: string): void {
    this.storyForm.patchValue({ prompt: example });
  }

  async onSubmit(): Promise<void> {
    if (this.storyForm.invalid) {
      this.notificationService.error('Please enter a valid prompt (at least 10 characters)');
      return;
    }

    this.isSubmitting = true;
    
    const formValue = this.storyForm.value;
    const request: StoryRequest = {
      prompt: formValue.prompt,
      issueType: formValue.issueType,
      priority: formValue.priority,
      projectKey: formValue.projectKey || undefined,
      epicKey: formValue.epicKey || undefined,
      labels: formValue.labels ? formValue.labels.split(',').map((l: string) => l.trim()) : undefined,
      autoEstimate: formValue.autoEstimate,
      autoBreakdown: formValue.autoBreakdown,
      autoAssign: formValue.autoAssign
    };

    this.storyService.createStory(request)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          this.createdStory = response;
          
          if (response.status === 'processing') {
            this.pollStoryStatus(response.requestId);
          } else if (response.status === 'completed') {
            this.isSubmitting = false;
            this.showResult = true;
            this.notificationService.success('Story created successfully!');
          } else if (response.status === 'failed') {
            this.isSubmitting = false;
            this.showResult = true;
            this.notificationService.error(response.errorMessage || 'Failed to create story');
          }
        },
        error: (error) => {
          this.isSubmitting = false;
          this.notificationService.error('Failed to create story. Please try again.');
          console.error('Story creation error:', error);
        }
      });
  }

  private pollStoryStatus(requestId: string): void {
    interval(2000)
      .pipe(
        takeUntil(this.destroy$),
        switchMap(() => this.storyService.getStoryStatus(requestId)),
        takeWhile((response) => response.status === 'processing', true)
      )
      .subscribe({
        next: (response) => {
          this.createdStory = response;
          
          if (response.status === 'completed') {
            this.isSubmitting = false;
            this.showResult = true;
            this.notificationService.success('Story created successfully!');
          } else if (response.status === 'failed') {
            this.isSubmitting = false;
            this.showResult = true;
            this.notificationService.error(response.errorMessage || 'Failed to create story');
          }
        },
        error: (error) => {
          this.isSubmitting = false;
          console.error('Polling error:', error);
        }
      });
  }

  createAnother(): void {
    this.showResult = false;
    this.createdStory = null;
    this.storyForm.reset({
      issueType: 'Story',
      priority: 'Medium',
      autoEstimate: true,
      autoBreakdown: true,
      autoAssign: true
    });
  }

  viewInJira(): void {
    if (this.createdStory?.jiraUrl) {
      window.open(this.createdStory.jiraUrl, '_blank');
    }
  }

  get promptControl() {
    return this.storyForm.get('prompt');
  }
}