import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-priority-badge',
  standalone: true,
  imports: [CommonModule],
  template: `
    <span class="priority-badge" [ngClass]="priorityClass">
      <i [class]="iconClass"></i>
      <span *ngIf="showLabel">{{ priority }}</span>
    </span>
  `,
  styles: [`
    .priority-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 500;
    }

    .priority-highest {
      background-color: #FFEBE6;
      color: #BF2600;
    }

    .priority-high {
      background-color: #FFEBE6;
      color: #DE350B;
    }

    .priority-medium {
      background-color: #FFF7D6;
      color: #FF8B00;
    }

    .priority-low {
      background-color: #E3FCEF;
      color: #006644;
    }

    .priority-lowest {
      background-color: #E3FCEF;
      color: #36B37E;
    }

    i {
      font-size: 10px;
    }
  `]
})
export class PriorityBadgeComponent {
  @Input() priority: string = 'Medium';
  @Input() showLabel: boolean = true;

  get priorityClass(): string {
    return `priority-${this.priority.toLowerCase()}`;
  }

  get iconClass(): string {
    const icons: { [key: string]: string } = {
      'highest': 'fas fa-angle-double-up',
      'high': 'fas fa-angle-up',
      'medium': 'fas fa-equals',
      'low': 'fas fa-angle-down',
      'lowest': 'fas fa-angle-double-down'
    };
    return icons[this.priority.toLowerCase()] || 'fas fa-equals';
  }
}