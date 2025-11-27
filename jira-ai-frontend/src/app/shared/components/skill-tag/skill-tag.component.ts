import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-skill-tag',
  standalone: true,
  imports: [CommonModule],
  template: `
    <span class="skill-tag" [ngClass]="{'removable': removable, 'selected': selected}">
      <i *ngIf="icon" [class]="icon"></i>
      {{ skill }}
      <button *ngIf="removable" class="remove-btn" (click)="onRemove()">
        <i class="fas fa-times"></i>
      </button>
    </span>
  `,
  styles: [`
    .skill-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      background-color: #F4F5F7;
      border: 1px solid #DFE1E6;
      border-radius: 4px;
      font-size: 12px;
      color: #172B4D;
      transition: all 0.2s;
    }

    .skill-tag:hover {
      background-color: #EBECF0;
    }

    .skill-tag.selected {
      background-color: #DEEBFF;
      border-color: #4C9AFF;
      color: #0052CC;
    }

    .skill-tag.removable {
      padding-right: 6px;
    }

    .remove-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 16px;
      height: 16px;
      padding: 0;
      border: none;
      background: none;
      color: #97A0AF;
      cursor: pointer;
      border-radius: 50%;
      transition: all 0.2s;
    }

    .remove-btn:hover {
      background-color: #DFE1E6;
      color: #172B4D;
    }

    i {
      font-size: 10px;
    }
  `]
})
export class SkillTagComponent {
  @Input() skill: string = '';
  @Input() icon?: string;
  @Input() removable: boolean = false;
  @Input() selected: boolean = false;
  @Output() remove = new EventEmitter<string>();

  onRemove(): void {
    this.remove.emit(this.skill);
  }
}