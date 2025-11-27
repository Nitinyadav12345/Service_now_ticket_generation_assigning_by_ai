import { createReducer, on } from '@ngrx/store';
import * as UiActions from './ui.actions';

export interface UiState {
  isLoading: boolean;
  sidebarCollapsed: boolean;
  notification: {
    message: string;
    notificationType: 'success' | 'error' | 'warning' | 'info';
  } | null;
}

export const initialState: UiState = {
  isLoading: false,
  sidebarCollapsed: false,
  notification: null
};

export const uiReducer = createReducer(
  initialState,
  on(UiActions.setLoading, (state, { isLoading }) => ({
    ...state,
    isLoading
  })),
  on(UiActions.toggleSidebar, (state) => ({
    ...state,
    sidebarCollapsed: !state.sidebarCollapsed
  })),
  on(UiActions.setSidebarCollapsed, (state, { collapsed }) => ({
    ...state,
    sidebarCollapsed: collapsed
  })),
  on(UiActions.showNotification, (state, { message, notificationType }) => ({
    ...state,
    notification: { message, notificationType }
  })),
  on(UiActions.clearNotification, (state) => ({
    ...state,
    notification: null
  }))
);