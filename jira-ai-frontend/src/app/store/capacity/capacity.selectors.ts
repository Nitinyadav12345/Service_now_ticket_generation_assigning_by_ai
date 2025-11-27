import { createFeatureSelector, createSelector } from '@ngrx/store';
import { CapacityState } from './capacity.reducer';

export const selectCapacityState = createFeatureSelector<CapacityState>('capacity');

export const selectTeamCapacity = createSelector(
  selectCapacityState,
  (state) => state.teamCapacity
);

export const selectMembers = createSelector(
  selectCapacityState,
  (state) => state.members
);

export const selectCapacityLoading = createSelector(
  selectCapacityState,
  (state) => state.isLoading
);

export const selectCapacityError = createSelector(
  selectCapacityState,
  (state) => state.error
);

export const selectAvailableMembers = createSelector(
  selectMembers,
  (members) => members.filter(m => m.availabilityStatus === 'available')
);

export const selectUtilizationPercentage = createSelector(
  selectTeamCapacity,
  (capacity) => capacity?.utilizationPercentage ?? 0
);