import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full'
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./features/dashboard/dashboard.component')
      .then(m => m.DashboardComponent),
    title: 'Dashboard - Jira AI Assistant'
  },
  {
    path: 'create-story',
    loadComponent: () => import('./features/story-creator/story-creator.component')
      .then(m => m.StoryCreatorComponent),
    title: 'Create Ticket - Jira AI Assistant'
  },
  {
    path: 'capacity',
    loadComponent: () => import('./features/capacity/capacity.component')
      .then(m => m.CapacityComponent),
    title: 'Team Capacity - Jira AI Assistant'
  },
  {
    path: 'analytics',
    loadComponent: () => import('./features/analytics/analytics.component')
      .then(m => m.AnalyticsComponent),
    title: 'Analytics - Jira AI Assistant'
  },
  {
    path: 'settings',
    loadComponent: () => import('./features/settings/settings.component')
      .then(m => m.SettingsComponent),
    title: 'Settings - Jira AI Assistant'
  },
  {
    path: 'story/:id',
    loadComponent: () => import('./features/story-detail/story-detail.component')
      .then(m => m.StoryDetailComponent),
    title: 'Story Details - Jira AI Assistant'
  },
  {
    path: '**',
    loadComponent: () => import('./shared/components/not-found/not-found.component')
      .then(m => m.NotFoundComponent),
    title: 'Page Not Found'
  }
];