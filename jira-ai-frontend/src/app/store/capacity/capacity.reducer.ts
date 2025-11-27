import { createReducer, on } from '@ngrx/store';
import * as CapacityActions from './capacity.actions';
import { TeamCapacity } from '../../core/models/capacity.model';
import { TeamMember } from '../../core/models/team-member.model';

export interface CapacityState {
  teamCapacity: TeamCapacity | null;
  members: TeamMember[];
  isLoading: boolean;
  error: string | null;
}

export const initialState: CapacityState = {
  teamCapacity: null,
  members: [],
  isLoading: false,
  error: null
};

export const capacityReducer = createReducer(
  initialState,
  
  // Load Team Capacity
  on(CapacityActions.loadTeamCapacity, (state) => ({
    ...state,
    isLoading: true
  })),
  on(CapacityActions.loadTeamCapacitySuccess, (state, { capacity }) => ({
    ...state,
    teamCapacity: capacity,
    isLoading: false
  })),
  on(CapacityActions.loadTeamCapacityFailure, (state, { error }) => ({
    ...state,
    isLoading: false,
    error
  })),
  
  // Load Members
  on(CapacityActions.loadMembers, (state) => ({
    ...state,
    isLoading: true
  })),
  on(CapacityActions.loadMembersSuccess, (state, { members }) => ({
    ...state,
    members,
    isLoading: false
  })),
  on(CapacityActions.loadMembersFailure, (state, { error }) => ({
    ...state,
    isLoading: false,
    error
  }))
);