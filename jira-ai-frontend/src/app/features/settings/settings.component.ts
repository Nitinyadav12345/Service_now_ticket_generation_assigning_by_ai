import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="settings">
      <h1>Settings</h1>
      <p>Settings component - Coming in Part 6</p>
    </div>
  `,
  styles: [`
    .settings {
      padding: 24px;
      background: white;
      border-radius: 8px;
    }
  `]
})
export class SettingsComponent {}