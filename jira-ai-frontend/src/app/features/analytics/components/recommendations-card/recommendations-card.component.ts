import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Recommendation } from '../../../../core/models/analytics.model';

@Component({
  selector: 'app-recommendations-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './recommendations-card.component.html',
  styleUrls: ['./recommendations-card.component.scss']
})
export class RecommendationsCardComponent {
  @Input() recommendations: Recommendation[] = [];
  @Output() actionClicked = new EventEmitter<Recommendation>();

  getTypeIcon(type: string): string {
    switch (type) {
      case 'hiring': return 'fa-user-plus';
      case 'training': return 'fa-graduation-cap';
      case 'process': return 'fa-cogs';
      case 'capacity': return 'fa-chart-pie';
      default: return 'fa-lightbulb';
    }
  }

  getPriorityClass(priority: string): string {
    switch (priority) {
      case 'high': return 'priority-high';
      case 'medium': return 'priority-medium';
      default: return 'priority-low';
    }
  }

  onActionClick(recommendation: Recommendation): void {
    this.actionClicked.emit(recommendation);
  }
}