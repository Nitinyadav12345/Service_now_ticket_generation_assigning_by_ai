export type Priority = 'Highest' | 'High' | 'Medium' | 'Low' | 'Lowest';
export type IssueType = 'Story' | 'Task' | 'Bug';
export type StoryStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface Story {
  id?: string;
  key?: string;
  requestId?: string;
  title?: string;
  userPrompt?: string;
  generatedTitle?: string;
  description?: string;
  generatedDescription?: string;
  acceptanceCriteria?: string[];
  status: StoryStatus;
  priority: Priority;
  issueType: IssueType;
  assignee?: string;
  estimatedPoints?: number;
  jiraIssueKey?: string;
  jiraUrl?: string;
  createdAt: string;
  updatedAt?: string;
}

export interface StoryRequest {
  prompt: string;
  projectKey: string;  // Required
  issueType: IssueType;
  priority: Priority;
  sprintId?: number;  // Optional - if not provided, uses active sprint
  labels?: string[];
  autoEstimate: boolean;
  autoBreakdown: boolean;
  autoAssign: boolean;
}

export interface GeneratedStory {
  title: string;
  description: string;
  acceptanceCriteria: string[];
  technicalRequirements?: string;
  requiredSkills: string[];
  estimatedPoints?: number;
}

export interface StoryResponse {
  requestId: string;
  status: StoryStatus;
  generatedStory?: GeneratedStory;
  jiraIssueKey?: string;
  jiraUrl?: string;
  assignedTo?: string;
  assignmentReasoning?: string;
  subtasks?: string[];
  errorMessage?: string;
  createdAt: string;
}
