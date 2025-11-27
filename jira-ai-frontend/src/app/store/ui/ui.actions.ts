import { createAction, props } from '@ngrx/store';

export const setLoading = createAction(
  '[UI] Set Loading',
  props<{ isLoading: boolean }>()
);

export const toggleSidebar = createAction('[UI] Toggle Sidebar');

export const setSidebarCollapsed = createAction(
  '[UI] Set Sidebar Collapsed',
  props<{ collapsed: boolean }>()
);

// Changed 'type' to 'notificationType' to avoid NgRx reserved property conflict
export const showNotification = createAction(
  '[UI] Show Notification',
  props<{ message: string; notificationType: 'success' | 'error' | 'warning' | 'info' }>()
);

export const clearNotification = createAction('[UI] Clear Notification');