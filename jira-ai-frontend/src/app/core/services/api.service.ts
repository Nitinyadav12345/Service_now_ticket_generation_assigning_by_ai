import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  get<T>(endpoint: string, params?: any, skipLoading = false): Observable<T> {
    const options = this.buildOptions(params, skipLoading);
    return this.http.get<T>(`${this.baseUrl}${endpoint}`, options);
  }

  post<T>(endpoint: string, body: any, skipLoading = false): Observable<T> {
    const options = this.buildOptions(null, skipLoading);
    return this.http.post<T>(`${this.baseUrl}${endpoint}`, body, options);
  }

  put<T>(endpoint: string, body: any, skipLoading = false): Observable<T> {
    const options = this.buildOptions(null, skipLoading);
    return this.http.put<T>(`${this.baseUrl}${endpoint}`, body, options);
  }

  patch<T>(endpoint: string, body: any, skipLoading = false): Observable<T> {
    const options = this.buildOptions(null, skipLoading);
    return this.http.patch<T>(`${this.baseUrl}${endpoint}`, body, options);
  }

  delete<T>(endpoint: string, skipLoading = false): Observable<T> {
    const options = this.buildOptions(null, skipLoading);
    return this.http.delete<T>(`${this.baseUrl}${endpoint}`, options);
  }

  private buildOptions(params?: any, skipLoading = false): { params?: HttpParams; headers?: HttpHeaders } {
    let httpParams = new HttpParams();
    let headers = new HttpHeaders();

    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== null && params[key] !== undefined) {
          httpParams = httpParams.set(key, params[key].toString());
        }
      });
    }

    if (skipLoading) {
      headers = headers.set('X-Skip-Loading', 'true');
    }

    return { params: httpParams, headers };
  }
}