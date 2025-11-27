import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  
  // For now, always allow access (no authentication required for prototype)
  // In production, check for valid token
  const isAuthenticated = true; // Replace with actual auth check
  
  if (!isAuthenticated) {
    router.navigate(['/login']);
    return false;
  }
  
  return true;
};