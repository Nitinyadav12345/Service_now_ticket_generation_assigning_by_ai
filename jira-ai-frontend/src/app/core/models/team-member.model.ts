export interface TeamMember {
  id: string;
  username: string;
  displayName: string;
  email: string;
  avatarUrl?: string;
  skills: string[];
  maxStoryPoints: number;
  currentStoryPoints: number;
  currentTicketCount: number;
  availabilityStatus: AvailabilityStatus;
  seniorityLevel: SeniorityLevel;
  preferredWork?: string[];
  performanceScore?: number;
  averageCompletionDays?: number;
  qualityScore?: number;
  isOutOfOffice: boolean;
  oooEndDate?: Date;
}

export interface TeamMemberOOO {
  id: string;
  username: string;
  startDate: Date;
  endDate: Date;
  reason: string;
  isPartial: boolean;
  partialCapacity?: number;
}

export type AvailabilityStatus = 'available' | 'busy' | 'overloaded' | 'ooo';
export type SeniorityLevel = 'Junior' | 'Mid' | 'Senior' | 'Lead' | 'Principal';

export interface TeamMemberCapacity {
  username: string;
  displayName: string;
  currentStoryPoints: number;
  maxStoryPoints: number;
  availableStoryPoints: number;
  currentTicketCount: number;
  availabilityPercentage: number;
  availabilityStatus: AvailabilityStatus;
  isOutOfOffice: boolean;
  skills: string[];
  preferredWork?: string[];
}