import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { ApiService } from './api.service';
import { TeamMember } from '../models/team-member.model';

export interface TeamCapacity {
  totalTeamCapacity: number;
  totalUsedCapacity: number;
  availableCapacity: number;
  utilizationPercentage: number;
  teamSize: number;
  availableMembers: number;
  membersByStatus: {
    available: string[];
    busy: string[];
    overloaded: string[];
    ooo: string[];
  };
}

@Injectable({
  providedIn: 'root'
})
export class CapacityService {
  constructor(private apiService: ApiService) {}

  getTeamCapacity(): Observable<TeamCapacity> {
    return this.apiService.getTeamCapacity().pipe(
      map(response => ({
        totalTeamCapacity: response.total_team_capacity,
        totalUsedCapacity: response.total_used_capacity,
        availableCapacity: response.available_capacity,
        utilizationPercentage: response.utilization_percentage,
        teamSize: response.team_size,
        availableMembers: response.available_members,
        membersByStatus: response.members_by_status
      }))
    );
  }

  getAllMembers(): Observable<TeamMember[]> {
    return this.apiService.getAllMembers().pipe(
      map(members => members.map((m: any) => this.mapToTeamMember(m)))
    );
  }

  getMemberCapacity(username: string): Observable<TeamMember> {
    return this.apiService.getMemberCapacity(username).pipe(
      map(m => this.mapToTeamMember(m))
    );
  }

  markOutOfOffice(data: {
    username: string;
    startDate: string;
    endDate: string;
    reason: string;
    partialCapacity?: number;
  }): Observable<any> {
    return this.apiService.markOutOfOffice({
      username: data.username,
      start_date: data.startDate,
      end_date: data.endDate,
      reason: data.reason,
      partial_capacity: data.partialCapacity
    });
  }

  refreshCapacity(): Observable<any> {
    return this.apiService.refreshCapacity();
  }

  syncFromJira(): Observable<any> {
    return this.apiService.syncFromJira();
  }

  updateMember(username: string, data: {
    skills?: string[];
    maxStoryPoints?: number;
    seniorityLevel?: string;
    displayName?: string;
    email?: string;
    designation?: string;
  }): Observable<any> {
    return this.apiService.updateMember(username, {
      skills: data.skills,
      max_story_points: data.maxStoryPoints,
      seniority_level: data.seniorityLevel,
      display_name: data.displayName,
      email: data.email,
      designation: data.designation
    });
  }

  private mapToTeamMember(m: any): TeamMember {
    return {
      id: m.id,
      username: m.username,
      email: m.email,
      displayName: m.display_name || m.username,
      designation: m.designation,
      skills: m.skills || [],
      maxStoryPoints: m.max_story_points,
      currentStoryPoints: m.current_story_points,
      currentTicketCount: m.current_ticket_count,
      availabilityStatus: m.availability_status as 'available' | 'busy' | 'overloaded' | 'ooo',
      seniorityLevel: m.seniority_level as 'Junior' | 'Mid' | 'Senior' | 'Lead' | 'Principal',
      performanceScore: m.performance_score,
      averageCompletionDays: m.average_completion_days,
      qualityScore: m.quality_score,
      isOutOfOffice: m.is_out_of_office,
      oooEndDate: m.ooo_end_date
    };
  }
}
