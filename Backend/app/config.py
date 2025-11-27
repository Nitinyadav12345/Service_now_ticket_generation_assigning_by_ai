from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Application
    app_name: str = "Jira AI Assistant"
    app_version: str = "1.0.0"
    debug: bool = True
    secret_key: str = "change-this-secret-key-in-production"
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/jira_ai_db"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # OpenAI / LLM Configuration (supports OpenAI, DeepSeek, local models, etc.)
    openai_api_key: str = ""
    openai_api_base: str = ""  # Optional: Custom API base URL (e.g., https://api.deepseek.com)
    openai_model: str = "gpt-4-turbo-preview"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_temperature: float = 0.7
    
    # Jira
    jira_url: str = ""
    jira_email: str = ""
    jira_api_token: str = ""
    jira_project_key: str = "PROJ"
    
    # Pinecone
    pinecone_api_key: str = ""
    pinecone_environment: str = ""
    pinecone_index_name: str = "jira-ai-stories"
    
    # CORS
    cors_origins: str = "http://localhost:4200,http://localhost:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    
    # Capacity Calculation
    capacity_sync_interval: int = 900  # 15 minutes
    daily_working_hours: int = 8  # Standard work day
    hours_per_story_point: float = 4.0  # Hours needed per story point
    focus_factor: float = 0.7  # 70% focus factor (accounts for meetings, emails, etc.)
    
    # Assignment
    max_assignment_attempts: int = 3
    assignment_queue_process_interval: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
