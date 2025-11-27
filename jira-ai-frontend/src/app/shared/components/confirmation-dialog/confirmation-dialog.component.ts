import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-confirmation-dialog',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="dialog-overlay" *ngIf="isOpen" (click)="onCancel()">
      <div class="dialog" (click)="$event.stopPropagation()">
        <div class="dialog-header">
          <div class="dialog-icon" [ngClass]="type">
            <i [class]="iconClass"></i>
          </div>
          <h3>{{ title }}</h3>
        </div>
        <div class="dialog-body">
          <p>{{ message }}</p>
        </div>
        <div class="dialog-footer">
          <button class="btn btn-secondary" (click)="onCancel()">
            {{ cancelText }}
          </button>
          <button class="btn" [ngClass]="confirmButtonClass" (click)="onConfirm()">
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .dialog-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10000;
      animation: fadeIn 0.2s ease;
    }

    .dialog {
      background: white;
      border-radius: 8px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
      max-width: 400px;
      width: 90%;
      animation: slideIn 0.2s ease;
    }

    .dialog-header {
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 20px;
      border-bottom: 1px solid #DFE1E6;
    }

    .dialog-icon {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
    }

    .dialog-icon.warning {
      background-color: #FFF7D6;
      color: #FF8B00;
    }

    .dialog-icon.danger {
      background-color: #FFEBE6;
      color: #DE350B;
    }

    .dialog-icon.info {
      background-color: #DEEBFF;
      color: #0052CC;
    }

    .dialog-icon.success {
      background-color: #E3FCEF;
      color: #006644;
    }

    h3 {
      font-size: 18px;
      font-weight: 600;
      color: #172B4D;
      margin: 0;
    }

    .dialog-body {
      padding: 20px;
    }

    .dialog-body p {
      margin: 0;
      color: #5E6C84;
      line-height: 1.6;
    }

    .dialog-footer {
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      padding: 16px 20px;
      background-color: #FAFBFC;
      border-top: 1px solid #DFE1E6;
      border-radius: 0 0 8px 8px;
    }

    .btn {
      padding: 8px 16px;
      border-radius: 4px;
      font-weight: 500;
      cursor: pointer;
      border: none;
      transition: all 0.2s;
    }

    .btn-secondary {
      background-color: #F4F5F7;
      color: #172B4D;
    }

    .btn-secondary:hover {
      background-color: #DFE1E6;
    }

    .btn-primary {
      background-color: #0052CC;
      color: white;
    }

    .btn-primary:hover {
      background-color: #0747A6;
    }

    .btn-danger {
      background-color: #DE350B;
      color: white;
    }

    .btn-danger:hover {
      background-color: #BF2600;
    }

    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }

    @keyframes slideIn {
      from {
        opacity: 0;
        transform: translateY(-20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
  `]
})
export class ConfirmationDialogComponent {
  @Input() isOpen: boolean = false;
  @Input() title: string = 'Confirm Action';
  @Input() message: string = 'Are you sure you want to proceed?';
  @Input() confirmText: string = 'Confirm';
  @Input() cancelText: string = 'Cancel';
  @Input() type: 'warning' | 'danger' | 'info' | 'success' = 'warning';
  
  @Output() confirm = new EventEmitter<void>();
  @Output() cancel = new EventEmitter<void>();

  get iconClass(): string {
    const icons = {
      warning: 'fas fa-exclamation-triangle',
      danger: 'fas fa-trash-alt',
      info: 'fas fa-info-circle',
      success: 'fas fa-check-circle'
    };
    return icons[this.type];
  }

  get confirmButtonClass(): string {
    return this.type === 'danger' ? 'btn-danger' : 'btn-primary';
  }

  onConfirm(): void {
    this.confirm.emit();
  }

  onCancel(): void {
    this.cancel.emit();
  }
}