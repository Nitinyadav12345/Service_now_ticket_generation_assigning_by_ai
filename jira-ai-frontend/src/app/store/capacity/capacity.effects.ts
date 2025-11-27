import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of } from 'rxjs';
import { map, mergeMap, catchError, tap, switchMap } from 'rxjs/operators';
import { CapacityService } from '../../core/services/capacity.service';
import { NotificationService } from '../../core/services/notification.service';
import * as CapacityActions from './capacity.actions';

@Injectable()
export class CapacityEffects {
  constructor(
    private actions$: Actions,
    private capacityService: CapacityService,
    private notificationService: NotificationService
  ) {}

  loadTeamCapacity$ = createEffect(() =>
    this.actions$.pipe(
      ofType(CapacityActions.loadTeamCapacity),
      mergeMap(() =>
        this.capacityService.getTeamCapacity().pipe(
          map((capacity) => CapacityActions.loadTeamCapacitySuccess({ capacity })),
          catchError((error) =>
            of(CapacityActions.loadTeamCapacityFailure({ error: error.message }))
          )
        )
      )
    )
  );

  loadMembers$ = createEffect(() =>
    this.actions$.pipe(
      ofType(CapacityActions.loadMembers),
      mergeMap(() =>
        this.capacityService.getAllMembers().pipe(
          map((members) => CapacityActions.loadMembersSuccess({ members })),
          catchError((error) =>
            of(CapacityActions.loadMembersFailure({ error: error.message }))
          )
        )
      )
    )
  );

  refreshCapacity$ = createEffect(() =>
    this.actions$.pipe(
      ofType(CapacityActions.refreshCapacity),
      switchMap(() =>
        this.capacityService.refreshCapacity().pipe(
          tap(() => this.notificationService.success('Capacity refreshed')),
          map(() => CapacityActions.refreshCapacitySuccess()),
          catchError((error) => {
            this.notificationService.error('Failed to refresh capacity');
            return of(CapacityActions.loadTeamCapacityFailure({ error: error.message }));
          })
        )
      )
    )
  );

  refreshCapacitySuccess$ = createEffect(() =>
    this.actions$.pipe(
      ofType(CapacityActions.refreshCapacitySuccess),
      map(() => CapacityActions.loadTeamCapacity())
    )
  );
}