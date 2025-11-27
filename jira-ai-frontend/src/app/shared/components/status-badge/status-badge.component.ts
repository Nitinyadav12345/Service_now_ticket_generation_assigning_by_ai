import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-status-badge',
  standalone: true,
  imports: [CommonModule],
  template: `
    <span class="status-badge" [ngClass]="statusClass">
      <span class="status-dot"></span>
      <span>{{ displayLabel }}</span>
    </span>
  `,
  styles: [`
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 500;
    }

    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }

    .status-available {
      background-color: #E3FCEF;
      color: #006644;
    }
    .status-available .status-dot {
      background-color: #36B37E;
    }

    .status-busy {
      background-color: #FFF7D6;
      color: #FF8B00;
    }
    .status-busy .status-dot {
      background-color: #FFAB00;
    }

    .status-overloaded {
      background-color: #FFEBE6;
      color: #BF2600;
    }
    .status-overloaded .status-dot {
      background-color: #FF5630;
    }

    .status-ooo {
      background-color: #F4F5F7;
      color: #5E6C84;
    }
    .status-ooo .status-dot {
      background-color: #97A0AF;
    }

    .status-pending {
      background-color: #EAE6FF;
      color: #403294;
    }
    .status-pending .status-dot {
      background-color: #6554C0;
    }

    .status-processing {
      background-color: #DEEBFF;
      color: #0747A6;
    }
    .status-processing .status-dot {
      background-color: #0052CC;
      animation: pulse 1.5s infinite;
    }

    .status-completed {
      background-color: #E3FCEF;
      color: #006644;
    }
    .status-completed .status-dot {
      background-color: #36B37E;
    }

    .status-failed {
      background-color: #FFEBE6;
      color: #BF2600;
    }
    .status-failed .status-dot {
      background-color: #FF5630;
    }

    @keyframes pulse {
      0%, 100% {
        opacity: 1;
      }
      50% {
        opacity: 0.5;
      }
    }
  `]
})
export class StatusBadgeComponent {
  @Input() status: string = 'available';
  @Input() label?: string;

  get statusClass(): string {
    return `status-${this.status.toLowerCase()}`;
  }

  get displayLabel(): string {
    if (this.label) return this.label;
    
    const labels: { [key: string]: string } = {
      'available': 'Available',
      'busy': 'Busy',
      'overloaded': 'Overloaded',
      'ooo': 'Out of Office',
      'pending': 'Pending',
      'processing': 'Processing',
      'completed': 'Completed',
      'failed': 'Failed'
    };
    return labels[this.status.toLowerCase()] || this.status;
  }
}