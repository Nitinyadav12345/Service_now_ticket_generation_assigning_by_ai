import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-story-detail',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="story-detail">
      <h1>Story Detail</h1>
      <p>Story detail component - Coming soon</p>
    </div>
  `,
  styles: [`
    .story-detail {
      padding: 24px;
      background: white;
      border-radius: 8px;
    }
  `]
})
export class StoryDetailComponent {}