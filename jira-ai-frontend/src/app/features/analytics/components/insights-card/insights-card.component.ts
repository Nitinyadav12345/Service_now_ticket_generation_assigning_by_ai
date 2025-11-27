import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LearningInsight } from '../../../../core/models/analytics.model';

@Component({
  selector: 'app-insights-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './insights-card.component.html',
  styleUrls: ['./insights-card.component.scss']
})
export class InsightsCardComponent {
  @Input() insights: LearningInsight[] = [];
  
  showAll = false;

  get displayedInsights(): LearningInsight[] {
    return this.showAll ? this.insights : this.insights.slice(0, 3);
  }

  getInsightClass(type: string): string {
    switch (type) {
      case 'success': return 'insight-success';
      case 'warning': return 'insight-warning';
      case 'improvement': return 'insight-improvement';
      default: return 'insight-info';
    }
  }

  getImpactBadgeClass(impact: string): string {
    switch (impact) {
      case 'high': return 'impact-high';
      case 'medium': return 'impact-medium';
      default: return 'impact-low';
    }
  }

  toggleShowAll(): void {
    this.showAll = !this.showAll;
  }
}