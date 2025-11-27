import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-capacity-bar',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="capacity-bar-container">
      <div class="capacity-bar">
        <div 
          class="capacity-fill" 
          [style.width.%]="percentage"
          [ngClass]="capacityClass">
        </div>
      </div>
      <div class="capacity-text" *ngIf="showText">
        <span class="current">{{ current }}</span>
        <span class="separator">/</span>
        <span class="max">{{ max }} pts</span>
        <span class="percentage">({{ percentage | number:'1.0-0' }}%)</span>
      </div>
    </div>
  `,
  styles: [`
    .capacity-bar-container {
      width: 100%;
    }

    .capacity-bar {
      height: 8px;
      background-color: #EBECF0;
      border-radius: 4px;
      overflow: hidden;
    }

    .capacity-fill {
      height: 100%;
      border-radius: 4px;
      transition: width 0.3s ease;
    }

    .capacity-low {
      background-color: #36B37E;
    }

    .capacity-medium {
      background-color: #FFAB00;
    }

    .capacity-high {
      background-color: #FF5630;
    }

    .capacity-text {
      display: flex;
      align-items: center;
      gap: 4px;
      margin-top: 4px;
      font-size: 12px;
      color: #5E6C84;
    }

    .current {
      font-weight: 600;
      color: #172B4D;
    }

    .percentage {
      color: #97A0AF;
    }
  `]
})
export class CapacityBarComponent {
  @Input() current: number = 0;
  @Input() max: number = 20;
  @Input() showText: boolean = true;

  get percentage(): number {
    if (this.max === 0) return 0;
    return Math.min((this.current / this.max) * 100, 100);
  }

  get capacityClass(): string {
    if (this.percentage < 60) return 'capacity-low';
    if (this.percentage < 85) return 'capacity-medium';
    return 'capacity-high';
  }
}