import { createFeatureSelector, createSelector } from '@ngrx/store';
import { StoryState } from './story.reducer';

export const selectStoryState = createFeatureSelector<StoryState>('story');

export const selectRecentStories = createSelector(
  selectStoryState,
  (state) => state.recentStories
);

export const selectCurrentStory = createSelector(
  selectStoryState,
  (state) => state.currentStory
);

export const selectIsCreating = createSelector(
  selectStoryState,
  (state) => state.isCreating
);

export const selectStoryError = createSelector(
  selectStoryState,
  (state) => state.error
);

export const selectIsLoading = createSelector(
  selectStoryState,
  (state) => state.isLoading
);