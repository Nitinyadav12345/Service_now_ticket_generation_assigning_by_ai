import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivityItem } from '../../../../core/models/analytics.model';
import { TimeAgoPipe } from '../../../../shared/pipes/time-ago.pipe';

@Component({
  selector: 'app-activity-feed',
  standalone: true,
  imports: [CommonModule, TimeAgoPipe],
  templateUrl: './activity-feed.component.html',
  styleUrls: ['./activity-feed.component.scss']
})
export class ActivityFeedComponent {
  @Input() activities: ActivityItem[] = [];

  getActivityIcon(type: string): string {
    switch (type) {
      case 'story_created': return 'fa-plus-circle';
      case 'story_completed': return 'fa-check-circle';
      case 'assignment': return 'fa-user-check';
      case 'estimation_adjusted': return 'fa-edit';
      default: return 'fa-info-circle';
    }
  }

  getActivityClass(type: string): string {
    switch (type) {
      case 'story_created': return 'activity-created';
      case 'story_completed': return 'activity-completed';
      case 'assignment': return 'activity-assignment';
      case 'estimation_adjusted': return 'activity-adjusted';
      default: return 'activity-info';
    }
  }
}