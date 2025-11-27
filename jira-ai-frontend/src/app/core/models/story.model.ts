export interface Story {
  id?: string;
  requestId: string;
  userPrompt: string;
  generatedTitle: string;
  generatedDescription: string;
  acceptanceCriteria: string[];
  estimatedPoints: number;
  jiraIssueKey?: string;
  jiraUrl?: string;
  status: StoryStatus;
  priority: Priority;
  issueType: IssueType;
  assignee?: TeamMemberSummary;
  subtasks?: Subtask[];
  createdAt: Date;
  updatedAt?: Date;
}

export interface StoryRequest {
  prompt: string;
  issueType?: IssueType;
  priority?: Priority;
  projectKey?: string;
  epicKey?: string;
  labels?: string[];
  autoBreakdown?: boolean;
  autoEstimate?: boolean;
  autoAssign?: boolean;
}

export interface StoryResponse {
  requestId: string;
  status: StoryStatus;
  generatedStory?: GeneratedStory;
  jiraIssueKey?: string;
  jiraUrl?: string;
  createdAt: string;
  errorMessage?: string;
}

export interface GeneratedStory {
  title: string;
  description: string;
  acceptanceCriteria: string[];
  estimatedPoints: number;
  technicalRequirements?: string[];
  requiredSkills?: string[];
}

export interface Subtask {
  id: string;
  title: string;
  description: string;
  category: SubtaskCategory;
  estimatedPoints: number;
  jiraIssueKey?: string;
  assignee?: TeamMemberSummary;
  status: string;
}

export interface TeamMemberSummary {
  username: string;
  displayName: string;
  avatarUrl?: string;
}

export type StoryStatus = 'pending' | 'processing' | 'completed' | 'failed';
export type Priority = 'Highest' | 'High' | 'Medium' | 'Low' | 'Lowest';
export type IssueType = 'Story' | 'Task' | 'Bug' | 'Epic';
export type SubtaskCategory = 'Frontend' | 'Backend' | 'Testing' | 'DevOps' | 'Documentation' | 'Design';

export interface EstimationSuggestion {
  estimatedPoints: number;
  reasoning: string;
  confidence: number;
  similarStories: SimilarStory[];
}

export interface SimilarStory {
  issueKey: string;
  title: string;
  points: number;
  similarity: number;
}