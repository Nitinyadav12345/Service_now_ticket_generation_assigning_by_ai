import { createReducer, on } from '@ngrx/store';
import * as StoryActions from './story.actions';
import { Story, StoryResponse } from '../../core/models/story.model';

export interface StoryState {
  recentStories: Story[];
  currentStory: StoryResponse | null;
  isCreating: boolean;
  isLoading: boolean;
  error: string | null;
}

export const initialState: StoryState = {
  recentStories: [],
  currentStory: null,
  isCreating: false,
  isLoading: false,
  error: null
};

export const storyReducer = createReducer(
  initialState,
  
  // Create Story
  on(StoryActions.createStory, (state) => ({
    ...state,
    isCreating: true,
    error: null
  })),
  on(StoryActions.createStorySuccess, (state, { response }) => ({
    ...state,
    currentStory: response,
    isCreating: false
  })),
  on(StoryActions.createStoryFailure, (state, { error }) => ({
    ...state,
    isCreating: false,
    error
  })),
  
  // Load Recent Stories
  on(StoryActions.loadRecentStories, (state) => ({
    ...state,
    isLoading: true
  })),
  on(StoryActions.loadRecentStoriesSuccess, (state, { stories }) => ({
    ...state,
    recentStories: stories,
    isLoading: false
  })),
  on(StoryActions.loadRecentStoriesFailure, (state, { error }) => ({
    ...state,
    isLoading: false,
    error
  })),
  
  // Clear Current Story
  on(StoryActions.clearCurrentStory, (state) => ({
    ...state,
    currentStory: null,
    error: null
  })),
  
  // Update Story Status
  on(StoryActions.updateStoryStatusSuccess, (state, { response }) => ({
    ...state,
    currentStory: response
  }))
);