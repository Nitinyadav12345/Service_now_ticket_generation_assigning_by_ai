import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-not-found',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="not-found-container">
      <div class="not-found-content">
        <h1>404</h1>
        <h2>Page Not Found</h2>
        <p>The page you're looking for doesn't exist or has been moved.</p>
        <a routerLink="/dashboard" class="btn btn-primary">
          <i class="fas fa-home"></i>
          Go to Dashboard
        </a>
      </div>
    </div>
  `,
  styles: [`
    .not-found-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: calc(100vh - 64px);
      text-align: center;
      padding: 24px;
    }

    .not-found-content {
      max-width: 400px;
    }

    h1 {
      font-size: 120px;
      font-weight: 700;
      color: #0052CC;
      margin: 0;
      line-height: 1;
    }

    h2 {
      font-size: 24px;
      color: #172B4D;
      margin: 16px 0;
    }

    p {
      color: #5E6C84;
      margin-bottom: 24px;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }
  `]
})
export class NotFoundComponent {}