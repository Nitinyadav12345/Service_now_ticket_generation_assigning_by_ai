import { createAction, props } from '@ngrx/store';
import { TeamCapacity, CapacityOverview } from '../../core/models/capacity.model';
import { TeamMember } from '../../core/models/team-member.model';

// Load Team Capacity
export const loadTeamCapacity = createAction('[Capacity] Load Team Capacity');

export const loadTeamCapacitySuccess = createAction(
  '[Capacity] Load Team Capacity Success',
  props<{ capacity: TeamCapacity }>()
);

export const loadTeamCapacityFailure = createAction(
  '[Capacity] Load Team Capacity Failure',
  props<{ error: string }>()
);

// Load All Members
export const loadMembers = createAction('[Capacity] Load Members');

export const loadMembersSuccess = createAction(
  '[Capacity] Load Members Success',
  props<{ members: TeamMember[] }>()
);

export const loadMembersFailure = createAction(
  '[Capacity] Load Members Failure',
  props<{ error: string }>()
);

// Refresh Capacity
export const refreshCapacity = createAction('[Capacity] Refresh Capacity');

export const refreshCapacitySuccess = createAction('[Capacity] Refresh Capacity Success');