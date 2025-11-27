import { createFeatureSelector, createSelector } from '@ngrx/store';
import { UiState } from './ui.reducer';

export const selectUiState = createFeatureSelector<UiState>('ui');

export const selectIsLoading = createSelector(
  selectUiState,
  (state) => state.isLoading
);

export const selectSidebarCollapsed = createSelector(
  selectUiState,
  (state) => state.sidebarCollapsed
);

export const selectNotification = createSelector(
  selectUiState,
  (state) => state.notification
);

export const selectNotificationMessage = createSelector(
  selectNotification,
  (notification) => notification?.message
);

export const selectNotificationType = createSelector(
  selectNotification,
  (notification) => notification?.notificationType
);