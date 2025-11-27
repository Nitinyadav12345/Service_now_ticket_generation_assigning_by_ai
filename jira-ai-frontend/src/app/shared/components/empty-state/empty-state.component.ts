import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-empty-state',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="empty-state">
      <div class="empty-icon">
        <i [class]="icon"></i>
      </div>
      <h3>{{ title }}</h3>
      <p>{{ description }}</p>
      <button *ngIf="actionLabel" class="btn btn-primary" (click)="onAction()">
        <i *ngIf="actionIcon" [class]="actionIcon"></i>
        {{ actionLabel }}
      </button>
    </div>
  `,
  styles: [`
    .empty-state {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 48px 24px;
      text-align: center;
    }

    .empty-icon {
      width: 80px;
      height: 80px;
      background-color: #F4F5F7;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 20px;
    }

    .empty-icon i {
      font-size: 32px;
      color: #97A0AF;
    }

    h3 {
      font-size: 18px;
      font-weight: 600;
      color: #172B4D;
      margin: 0 0 8px;
    }

    p {
      font-size: 14px;
      color: #5E6C84;
      margin: 0 0 24px;
      max-width: 300px;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 20px;
      background-color: #0052CC;
      color: white;
      border: none;
      border-radius: 6px;
      font-weight: 500;
      cursor: pointer;
      transition: background-color 0.2s;
    }

    .btn:hover {
      background-color: #0747A6;
    }
  `]
})
export class EmptyStateComponent {
  @Input() icon: string = 'fas fa-inbox';
  @Input() title: string = 'No data';
  @Input() description: string = 'There is no data to display.';
  @Input() actionLabel?: string;
  @Input() actionIcon?: string;
  @Output() action = new EventEmitter<void>();

  onAction(): void {
    this.action.emit();
  }
}