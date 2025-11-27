import { Injectable } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  constructor(private toastr: ToastrService) {}

  success(message: string, title?: string): void {
    this.toastr.success(message, title || 'Success', {
      timeOut: 3000,
      progressBar: true,
      closeButton: true
    });
  }

  error(message: string, title?: string): void {
    this.toastr.error(message, title || 'Error', {
      timeOut: 5000,
      progressBar: true,
      closeButton: true
    });
  }

  warning(message: string, title?: string): void {
    this.toastr.warning(message, title || 'Warning', {
      timeOut: 4000,
      progressBar: true,
      closeButton: true
    });
  }

  info(message: string, title?: string): void {
    this.toastr.info(message, title || 'Info', {
      timeOut: 3000,
      progressBar: true,
      closeButton: true
    });
  }
}
