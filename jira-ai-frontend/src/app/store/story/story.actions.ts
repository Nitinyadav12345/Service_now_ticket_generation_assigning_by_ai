import { createAction, props } from '@ngrx/store';
import { Story, StoryRequest, StoryResponse } from '../../core/models/story.model';

// Create Story
export const createStory = createAction(
  '[Story] Create Story',
  props<{ request: StoryRequest }>()
);

export const createStorySuccess = createAction(
  '[Story] Create Story Success',
  props<{ response: StoryResponse }>()
);

export const createStoryFailure = createAction(
  '[Story] Create Story Failure',
  props<{ error: string }>()
);

// Load Recent Stories
export const loadRecentStories = createAction('[Story] Load Recent Stories');

export const loadRecentStoriesSuccess = createAction(
  '[Story] Load Recent Stories Success',
  props<{ stories: Story[] }>()
);

export const loadRecentStoriesFailure = createAction(
  '[Story] Load Recent Stories Failure',
  props<{ error: string }>()
);

// Clear Current Story
export const clearCurrentStory = createAction('[Story] Clear Current Story');

// Update Story Status
export const updateStoryStatus = createAction(
  '[Story] Update Story Status',
  props<{ requestId: string }>()
);

export const updateStoryStatusSuccess = createAction(
  '[Story] Update Story Status Success',
  props<{ response: StoryResponse }>()
);