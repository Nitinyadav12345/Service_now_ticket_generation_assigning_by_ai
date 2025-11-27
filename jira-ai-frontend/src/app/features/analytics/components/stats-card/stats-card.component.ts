import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-stats-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './stats-card.component.html',
  styleUrls: ['./stats-card.component.scss']
})
export class StatsCardComponent {
  @Input() title = '';
  @Input() value: number = 0;
  @Input() suffix = '';
  @Input() prefix = '';
  @Input() icon = 'fa-chart-bar';
  @Input() color: 'blue' | 'green' | 'yellow' | 'purple' | 'red' = 'blue';
  @Input() trend?: { value: number; direction: 'up' | 'down' };

  get formattedValue(): string {
    if (typeof this.value === 'number') {
      return this.value % 1 === 0 ? this.value.toString() : this.value.toFixed(1);
    }
    return this.value;
  }

  get trendClass(): string {
    if (!this.trend) return '';
    return this.trend.direction === 'up' ? 'trend-up' : 'trend-down';
  }

  get trendIcon(): string {
    if (!this.trend) return '';
    return this.trend.direction === 'up' ? 'fa-arrow-up' : 'fa-arrow-down';
  }

  get isPositiveTrend(): boolean {
    if (!this.trend) return true;
    // For cycle time, down is good. For accuracy, up is good.
    if (this.title.toLowerCase().includes('time')) {
      return this.trend.direction === 'down';
    }
    return this.trend.direction === 'up';
  }
}