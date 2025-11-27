import { ActionReducerMap, MetaReducer } from '@ngrx/store';
import { environment } from '../../environments/environment';
import { storyReducer, StoryState } from './story/story.reducer';
import { capacityReducer, CapacityState } from './capacity/capacity.reducer';
import { uiReducer, UiState } from './ui/ui.reducer';

export interface AppState {
  story: StoryState;
  capacity: CapacityState;
  ui: UiState;
}

export const reducers: ActionReducerMap<AppState> = {
  story: storyReducer,
  capacity: capacityReducer,
  ui: uiReducer
};

export const metaReducers: MetaReducer<AppState>[] = !environment.production ? [] : [];