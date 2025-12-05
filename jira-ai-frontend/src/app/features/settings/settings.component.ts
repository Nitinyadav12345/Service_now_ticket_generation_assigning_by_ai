import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

interface ModelOption {
  id: string;
  name: string;
  description: string;
}

interface ProviderConfig {
  display_name: string;
  models: ModelOption[];
  api_base: string | null;
  requires_key: boolean;
}

interface AIModelSettings {
  provider: string;
  model: string;
  api_key?: string;
  api_base?: string;
  temperature: number;
}

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {
  providers: { [key: string]: ProviderConfig } = {};
  providerKeys: string[] = [];
  
  selectedProvider: string = 'openai';
  selectedModel: string = '';
  apiKey: string = '';
  temperature: number = 0.7;
  
  currentSettings: any = null;
  availableModels: ModelOption[] = [];
  
  loading: boolean = false;
  testing: boolean = false;
  saving: boolean = false;
  
  testResult: { status: string; message: string } | null = null;
  saveResult: { status: string; message: string } | null = null;
  
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadAvailableModels();
    this.loadCurrentSettings();
  }

  loadAvailableModels() {
    this.loading = true;
    this.http.get<{ models: { [key: string]: ProviderConfig } }>(`${this.apiUrl}/settings/models`)
      .subscribe({
        next: (response) => {
          this.providers = response.models;
          this.providerKeys = Object.keys(this.providers);
          
          // Set default provider if available
          if (this.providerKeys.length > 0 && !this.selectedProvider) {
            this.selectedProvider = this.providerKeys[0];
            this.onProviderChange();
          }
          
          this.loading = false;
        },
        error: (error) => {
          console.error('Error loading models:', error);
          this.loading = false;
        }
      });
  }

  loadCurrentSettings() {
    this.http.get<any>(`${this.apiUrl}/settings/current`)
      .subscribe({
        next: (response) => {
          this.currentSettings = response;
          
          if (response.ai_model) {
            this.selectedProvider = response.ai_model.provider || 'openai';
            this.selectedModel = response.ai_model.model || '';
            this.temperature = response.ai_model.temperature || 0.7;
            
            // Don't load API key for security
            this.apiKey = '';
            
            this.onProviderChange();
          }
        },
        error: (error) => {
          console.error('Error loading current settings:', error);
        }
      });
  }

  onProviderChange() {
    const provider = this.providers[this.selectedProvider];
    if (provider && provider.models.length > 0) {
      this.availableModels = provider.models;
      
      // Set default model if not already set
      if (!this.selectedModel || !this.availableModels.find(m => m.id === this.selectedModel)) {
        this.selectedModel = this.availableModels[0].id;
      }
    }
  }

  testConnection() {
    if (!this.apiKey && !this.hasApiKey()) {
      this.testResult = {
        status: 'error',
        message: 'Please enter an API key'
      };
      return;
    }

    this.testing = true;
    this.testResult = null;

    const settings: AIModelSettings = {
      provider: this.selectedProvider,
      model: this.selectedModel,
      api_key: this.apiKey || undefined,
      temperature: this.temperature
    };

    const provider = this.providers[this.selectedProvider];
    if (provider?.api_base) {
      settings.api_base = provider.api_base;
    }

    this.http.post<any>(`${this.apiUrl}/settings/test-connection`, settings)
      .subscribe({
        next: (response) => {
          this.testResult = {
            status: response.status,
            message: response.message
          };
          this.testing = false;
        },
        error: (error) => {
          this.testResult = {
            status: 'error',
            message: error.error?.message || 'Connection test failed'
          };
          this.testing = false;
        }
      });
  }

  saveSettings() {
    if (!this.apiKey && !this.hasApiKey()) {
      this.saveResult = {
        status: 'error',
        message: 'Please enter an API key or test connection first'
      };
      return;
    }

    this.saving = true;
    this.saveResult = null;

    const settings: AIModelSettings = {
      provider: this.selectedProvider,
      model: this.selectedModel,
      api_key: this.apiKey || undefined,
      temperature: this.temperature
    };

    const provider = this.providers[this.selectedProvider];
    if (provider?.api_base) {
      settings.api_base = provider.api_base;
    }

    this.http.post<any>(`${this.apiUrl}/settings/update-model`, settings)
      .subscribe({
        next: (response) => {
          this.saveResult = {
            status: 'success',
            message: response.message || 'Settings saved successfully'
          };
          this.saving = false;
          
          // Clear API key field after successful save
          this.apiKey = '';
          
          // Reload current settings
          this.loadCurrentSettings();
        },
        error: (error) => {
          this.saveResult = {
            status: 'error',
            message: error.error?.detail || 'Failed to save settings'
          };
          this.saving = false;
        }
      });
  }

  hasApiKey(): boolean {
    return this.currentSettings?.ai_model?.api_keys_status?.[this.selectedProvider] || false;
  }

  getProviderDisplayName(key: string): string {
    return this.providers[key]?.display_name || key;
  }
}