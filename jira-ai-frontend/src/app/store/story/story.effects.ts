import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of } from 'rxjs';
import { map, mergeMap, catchError, tap } from 'rxjs/operators';
import { StoryService } from '../../core/services/story.service';
import { NotificationService } from '../../core/services/notification.service';
import * as StoryActions from './story.actions';

@Injectable()
export class StoryEffects {
  constructor(
    private actions$: Actions,
    private storyService: StoryService,
    private notificationService: NotificationService
  ) {}

  createStory$ = createEffect(() =>
    this.actions$.pipe(
      ofType(StoryActions.createStory),
      mergeMap(({ request }) =>
        this.storyService.createStory(request).pipe(
          map((response) => StoryActions.createStorySuccess({ response })),
          catchError((error) =>
            of(StoryActions.createStoryFailure({ error: error.message }))
          )
        )
      )
    )
  );

  createStorySuccess$ = createEffect(
    () =>
      this.actions$.pipe(
        ofType(StoryActions.createStorySuccess),
        tap(({ response }) => {
          if (response.jiraIssueKey) {
            this.notificationService.success(
              `Story ${response.jiraIssueKey} created successfully!`
            );
          }
        })
      ),
    { dispatch: false }
  );

  createStoryFailure$ = createEffect(
    () =>
      this.actions$.pipe(
        ofType(StoryActions.createStoryFailure),
        tap(({ error }) => {
          this.notificationService.error(error);
        })
      ),
    { dispatch: false }
  );

  loadRecentStories$ = createEffect(() =>
    this.actions$.pipe(
      ofType(StoryActions.loadRecentStories),
      mergeMap(() =>
        this.storyService.getRecentStories().pipe(
          map((stories) => StoryActions.loadRecentStoriesSuccess({ stories })),
          catchError((error) =>
            of(StoryActions.loadRecentStoriesFailure({ error: error.message }))
          )
        )
      )
    )
  );
}