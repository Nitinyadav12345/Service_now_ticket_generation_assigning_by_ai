from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
import os
from typing import Optional, Dict, List
from app.services.model_registry import list_available_models, initialize_model_client

logger = logging.getLogger(__name__)

router = APIRouter()


class AIModelSettings(BaseModel):
    """AI Model configuration"""
    provider: str  # openai, deepseek, gemini, grok
    model: str
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    temperature: float = 0.7


class SystemSettings(BaseModel):
    """System settings"""
    ai_model: AIModelSettings
    auto_estimate: bool = True
    auto_breakdown: bool = True
    auto_assign: bool = True


# Model configurations with their environment variable mappings
MODEL_CONFIGS = {
    "openai": {
        "display_name": "OpenAI",
        "models": [
            {"id": "gpt-4-turbo-preview", "name": "GPT-4 Turbo", "description": "Most capable, best for complex tasks"},
            {"id": "gpt-4", "name": "GPT-4", "description": "Powerful and accurate"},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "Fast and cost-effective"}
        ],
        "api_base": None,
        "env_key": "OPENAI_API_KEY",
        "env_base": "OPENAI_API_BASE",
        "env_model": "OPENAI_MODEL",
        "requires_key": True
    },
    "deepseek": {
        "display_name": "DeepSeek",
        "models": [
            {"id": "deepseek-chat", "name": "DeepSeek Chat", "description": "Fast and efficient"},
            {"id": "deepseek-coder", "name": "DeepSeek Coder", "description": "Optimized for code"}
        ],
        "api_base": "https://api.deepseek.com/v1",
        "env_key": "DEEPSEEK_API_KEY",
        "env_base": "DEEPSEEK_API_BASE_URL",
        "env_model": "DEEPSEEK_MODEL_NAME",
        "requires_key": True
    },
    "gemini": {
        "display_name": "Gemini",
        "models": [
            {"id": "gemini-2.0-flash-exp", "name": "Gemini 2.0 Flash", "description": "Latest experimental model"},
            {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "description": "Advanced reasoning"},
            {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash", "description": "Fast and efficient"}
        ],
        "api_base": None,
        "env_key": "GEMINI_API_KEY",
        "env_base": None,
        "env_model": "GEMINI_MODEL_NAME",
        "requires_key": True
    },
    "grok": {
        "display_name": "Grok",
        "models": [
            {"id": "grok-beta", "name": "Grok Beta", "description": "xAI's conversational model"},
            {"id": "grok-vision-beta", "name": "Grok Vision Beta", "description": "Multimodal capabilities"}
        ],
        "api_base": "https://api.x.ai/v1",
        "env_key": "GROK_API_KEY",
        "env_base": "GROK_API_BASE_URL",
        "env_model": "GROK_MODEL_NAME",
        "requires_key": True
    }
}


@router.get("/models")
async def get_available_models():
    """Get list of available AI models from registry"""
    try:
        # Get models from registry
        registry_models = list_available_models()
        
        # Enhance with configuration details
        enhanced_models = {}
        for model in registry_models:
            key = model["key"]
            if key in MODEL_CONFIGS:
                enhanced_models[key] = {
                    **MODEL_CONFIGS[key],
                    "registry_info": model
                }
        
        return {"models": enhanced_models}
    except Exception as e:
        logger.error(f"Error getting available models: {e}")
        return {"models": MODEL_CONFIGS}


@router.get("/current")
async def get_current_settings():
    """Get current system settings"""
    from app.config import settings
    
    # Detect current provider
    provider = "openai"
    if os.getenv("DEEPSEEK_API_KEY"):
        provider = "deepseek"
    elif os.getenv("GEMINI_API_KEY"):
        provider = "gemini"
    elif os.getenv("GROK_API_KEY"):
        provider = "grok"
    elif settings.openai_api_base:
        if "deepseek" in settings.openai_api_base.lower():
            provider = "deepseek"
        elif "x.ai" in settings.openai_api_base.lower():
            provider = "grok"
    
    # Get API keys status for all providers
    api_keys_status = {
        "openai": bool(settings.openai_api_key),
        "deepseek": bool(os.getenv("DEEPSEEK_API_KEY")),
        "gemini": bool(os.getenv("GEMINI_API_KEY")),
        "grok": bool(os.getenv("GROK_API_KEY"))
    }
    
    return {
        "ai_model": {
            "provider": provider,
            "model": settings.openai_model,
            "api_base": settings.openai_api_base if hasattr(settings, 'openai_api_base') else None,
            "temperature": settings.openai_temperature if hasattr(settings, 'openai_temperature') else 0.7,
            "has_api_key": api_keys_status.get(provider, False),
            "api_keys_status": api_keys_status
        },
        "auto_estimate": True,
        "auto_breakdown": True,
        "auto_assign": True
    }


@router.post("/update-model")
async def update_ai_model(model_settings: AIModelSettings):
    """Update AI model settings"""
    try:
        from app.config import settings
        
        provider = model_settings.provider
        config = MODEL_CONFIGS.get(provider)
        
        if not config:
            raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")
        
        # Update provider-specific environment variables
        if model_settings.api_key:
            env_key = config.get("env_key")
            if env_key:
                os.environ[env_key] = model_settings.api_key
                logger.info(f"Updated {env_key}")
                
                # Also update OPENAI_API_KEY for backward compatibility
                if provider == "openai":
                    settings.openai_api_key = model_settings.api_key
        
        # Update API base if provided
        if model_settings.api_base:
            env_base = config.get("env_base")
            if env_base:
                os.environ[env_base] = model_settings.api_base
                logger.info(f"Updated {env_base}")
        elif config.get("api_base"):
            # Use default API base
            env_base = config.get("env_base")
            if env_base:
                os.environ[env_base] = config["api_base"]
        
        # Update model name
        env_model = config.get("env_model")
        if env_model:
            os.environ[env_model] = model_settings.model
            logger.info(f"Updated {env_model}")
        
        # Update main settings for backward compatibility
        if provider == "openai":
            settings.openai_model = model_settings.model
            if model_settings.api_base:
                settings.openai_api_base = model_settings.api_base
        
        # Update temperature
        if hasattr(settings, 'openai_temperature'):
            settings.openai_temperature = model_settings.temperature
        
        logger.info(f"Updated AI model to {provider}: {model_settings.model}")
        
        return {
            "status": "success",
            "message": f"AI model updated to {config['display_name']} - {model_settings.model}",
            "settings": {
                "provider": provider,
                "model": model_settings.model,
                "api_base": model_settings.api_base or config.get("api_base"),
                "temperature": model_settings.temperature
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating AI model: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test-connection")
async def test_ai_connection(model_settings: AIModelSettings):
    """Test AI model connection using model registry"""
    try:
        provider = model_settings.provider
        config = MODEL_CONFIGS.get(provider)
        
        if not config:
            return {
                "status": "error",
                "message": f"Unknown provider: {provider}"
            }
        
        # Temporarily set environment variables for testing
        original_env = {}
        
        try:
            # Save original values
            env_key = config.get("env_key")
            env_base = config.get("env_base")
            env_model = config.get("env_model")
            
            if env_key:
                original_env[env_key] = os.environ.get(env_key)
                if model_settings.api_key:
                    os.environ[env_key] = model_settings.api_key
            
            if env_base and model_settings.api_base:
                original_env[env_base] = os.environ.get(env_base)
                os.environ[env_base] = model_settings.api_base
            elif env_base and config.get("api_base"):
                original_env[env_base] = os.environ.get(env_base)
                os.environ[env_base] = config["api_base"]
            
            if env_model:
                original_env[env_model] = os.environ.get(env_model)
                os.environ[env_model] = model_settings.model
            
            # Try to initialize the model
            model_instance = initialize_model_client(provider)
            
            if not model_instance:
                return {
                    "status": "error",
                    "message": f"Failed to initialize {config['display_name']} client. Check API key and configuration."
                }
            
            # Test with a simple completion
            from app.services.model_registry import get_completion_handler
            handler = get_completion_handler(provider)
            
            if not handler:
                return {
                    "status": "error",
                    "message": f"No completion handler for {provider}"
                }
            
            messages = [{"role": "user", "content": "Say 'Hello' in one word"}]
            response = handler(model_instance, messages, max_tokens=10, temperature=0.5)
            
            return {
                "status": "success",
                "message": f"Connection to {config['display_name']} successful!",
                "response": response[:100] if response else "No response",
                "model": model_settings.model
            }
            
        finally:
            # Restore original environment variables
            for key, value in original_env.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
        
    except Exception as e:
        logger.error(f"Error testing AI connection: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Connection failed: {str(e)}"
        }
