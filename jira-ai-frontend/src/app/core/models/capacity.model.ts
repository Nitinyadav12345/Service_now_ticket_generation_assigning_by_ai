import { TeamMember, AvailabilityStatus } from './team-member.model';

export interface TeamCapacity {
  totalTeamCapacity: number;
  totalUsedCapacity: number;
  availableCapacity: number;
  utilizationPercentage: number;
  teamSize: number;
  availableMembers: number;
  membersByStatus: MembersByStatus;
}

export interface MembersByStatus {
  available: string[];
  busy: string[];
  overloaded: string[];
  ooo: string[];
}

export interface CapacityOverview {
  teamCapacity: TeamCapacity;
  members: TeamMember[];
}

export interface OOORequest {
  username: string;
  startDate: string;
  endDate: string;
  reason: string;
  partialCapacity?: number;
}

export interface OOOResponse {
  status: string;
  message: string;
}