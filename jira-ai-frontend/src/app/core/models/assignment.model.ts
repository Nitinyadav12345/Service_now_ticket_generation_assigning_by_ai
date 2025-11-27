export interface AssignmentRequest {
  issueKey: string;
  priority: string;
  estimatedPoints: number;
  requiredSkills: string[];
}

export interface AssignmentResponse {
  assignedTo: string;
  displayName: string;
  assignmentScore: number;
  reasoning: string;
  alternatives: AssignmentAlternative[];
}

export interface AssignmentAlternative {
  username: string;
  displayName: string;
  score: number;
}

export interface AssignmentQueue {
  queuedCount: number;
  items: QueuedItem[];
}

export interface QueuedItem {
  issueKey: string;
  priority: string;
  estimatedPoints: number;
  requiredSkills: string[];
  attempts: number;
  reason: string;
  createdAt: string | Date;
  waitingTime: string;
}

export interface AssignmentHistory {
  id: string;
  issueKey: string;
  assignee: string;
  assignmentScore: number;
  assignmentReason: string;
  wasReassigned: boolean;
  completionTimeDays?: number;
  createdAt: Date;
}