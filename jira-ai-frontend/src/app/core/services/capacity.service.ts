import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { 
  TeamCapacity, 
  CapacityOverview,
  OOORequest,
  OOOResponse 
} from '../models/capacity.model';
import { TeamMember, TeamMemberCapacity } from '../models/team-member.model';

@Injectable({
  providedIn: 'root'
})
export class CapacityService {
  private readonly endpoint = '/capacity';

  constructor(private api: ApiService) {}

  getTeamCapacity(): Observable<TeamCapacity> {
    return this.api.get<TeamCapacity>(`${this.endpoint}/team`);
  }

  getCapacityOverview(): Observable<CapacityOverview> {
    return this.api.get<CapacityOverview>(`${this.endpoint}/overview`);
  }

  getMemberCapacity(username: string): Observable<TeamMemberCapacity> {
    return this.api.get<TeamMemberCapacity>(`${this.endpoint}/member/${username}`);
  }

  getAllMembers(): Observable<TeamMember[]> {
    return this.api.get<TeamMember[]>(`${this.endpoint}/members`);
  }

  markOutOfOffice(request: OOORequest): Observable<OOOResponse> {
    return this.api.post<OOOResponse>(`${this.endpoint}/mark-ooo`, request);
  }

  cancelOOO(username: string): Observable<OOOResponse> {
    return this.api.delete<OOOResponse>(`${this.endpoint}/ooo/${username}`);
  }

  refreshCapacity(): Observable<void> {
    return this.api.post<void>(`${this.endpoint}/refresh`, {});
  }
}