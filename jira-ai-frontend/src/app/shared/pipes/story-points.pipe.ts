import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'storyPoints',
  standalone: true
})
export class StoryPointsPipe implements PipeTransform {
  transform(value: number | null): string {
    if (value === null || value === undefined) return '-';
    
    if (value === 1) return '1 pt';
    
    return `${value} pts`;
  }
}