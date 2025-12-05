import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

interface DashboardStats {
  team_capacity: number;
  available_points: number;
  utilization: number;
  estimation_accuracy: number;
}

interface RecentTicket {
  id: string;
  jira_key: string;
  title: string;
  description: string;
  issue_type: string;
  priority: string;
  story_points: number;
  assigned_to: string;
  created_at: string;
  status: string;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  stats: DashboardStats = {
    team_capacity: 0,
    available_points: 0,
    utilization: 0,
    estimation_accuracy: 0
  };
  
  recentTickets: RecentTicket[] = [];
  loading = true;
  error: string | null = null;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    this.loading = true;
    this.error = null;

    // Load stats
    this.http.get<DashboardStats>(`${environment.apiUrl}/analytics/dashboard-stats`)
      .subscribe({
        next: (data) => {
          this.stats = data;
        },
        error: (err) => {
          console.error('Error loading stats:', err);
          this.error = 'Failed to load dashboard stats';
        }
      });

    // Load recent tickets
    this.http.get<{tickets: RecentTicket[], total: number}>(`${environment.apiUrl}/analytics/recent-tickets?limit=5`)
      .subscribe({
        next: (data) => {
          this.recentTickets = data.tickets;
          this.loading = false;
        },
        error: (err) => {
          console.error('Error loading recent tickets:', err);
          this.loading = false;
        }
      });
  }

  getJiraUrl(jiraKey: string): string {
    // Construct Jira URL - you may need to adjust this based on your Jira instance
    return `https://your-domain.atlassian.net/browse/${jiraKey}`;
  }

  getPriorityClass(priority: string): string {
    const priorityMap: {[key: string]: string} = {
      'Highest': 'priority-highest',
      'High': 'priority-high',
      'Medium': 'priority-medium',
      'Low': 'priority-low',
      'Lowest': 'priority-lowest'
    };
    return priorityMap[priority] || 'priority-medium';
  }

  getIssueTypeIcon(issueType: string): string {
    const iconMap: {[key: string]: string} = {
      'Story': 'fa-book',
      'Task': 'fa-tasks',
      'Bug': 'fa-bug',
      'Epic': 'fa-bolt'
    };
    return iconMap[issueType] || 'fa-ticket-alt';
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 60) {
      return `${diffMins} min${diffMins !== 1 ? 's' : ''} ago`;
    } else if (diffHours < 24) {
      return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
    } else if (diffDays < 7) {
      return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
    } else {
      return date.toLocaleDateString();
    }
  }
}