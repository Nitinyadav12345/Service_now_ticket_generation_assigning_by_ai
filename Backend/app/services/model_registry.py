"""
Model Registry Module
----------------------
Centralizes configuration and runtime helpers for supported AI models.
New models can be added by registering an initializer along with
handlers for different AI operations.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Callable
import logging
from app.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Registry helpers
# ---------------------------------------------------------------------------

MODEL_REGISTRY: Dict[str, Dict[str, Any]] = {}


def register_model(key: str, config: Dict[str, Any]) -> None:
    """Register or overwrite an AI model configuration."""
    MODEL_REGISTRY[key] = config


def list_available_models() -> List[Dict[str, Any]]:
    """Return all enabled models with metadata for UI consumption."""
    models: List[Dict[str, Any]] = []
    for key, config in MODEL_REGISTRY.items():
        if not config.get("enabled", True):
            continue
        models.append({
            "key": key,
            "display_name": config.get("display_name", key.title()),
            "description": config.get("description", ""),
            "tags": config.get("tags", []),
            "supports_json_mode": config.get("supports_json_mode", False),
        })
    return models


def get_model_display_name(key: str) -> str:
    """Map a model key to its human-readable name."""
    config = MODEL_REGISTRY.get(key)
    return config.get("display_name", key.title()) if config else key.title()


def initialize_model_client(model_key: str) -> Optional[Dict[str, Any]]:
    """Create a model client using its registered initializer."""
    config = MODEL_REGISTRY.get(model_key)
    if not config:
        logger.error(f"Attempted to initialize unknown AI model: {model_key}")
        return None
    
    initializer = config.get("initializer")
    if not initializer:
        logger.error(f"Model '{model_key}' is missing an initializer")
        return None
    
    try:
        instance = initializer()
        if not instance:
            return None
        
        instance.setdefault("key", model_key)
        instance.setdefault("display_name", config.get("display_name", model_key.title()))
        instance.setdefault("supports_json_mode", config.get("supports_json_mode", False))
        return instance
    except Exception as e:
        logger.error(f"Error initializing model '{model_key}': {e}", exc_info=True)
        return None


def get_completion_handler(model_key: str) -> Optional[Callable]:
    """Get the completion handler for a specific model."""
    definition = MODEL_REGISTRY.get(model_key)
    if not definition:
        logger.error(f"No registry definition for model '{model_key}'")
        return None
    
    handler = definition.get("completion_handler")
    if not handler:
        logger.error(f"Model '{model_key}' does not implement completion handler")
        return None
    
    return handler


# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------

def _require_package(import_path: str, package_name: str = None) -> Optional[Any]:
    """Safely import an optional package."""
    package_name = package_name or import_path
    try:
        if "." in import_path:
            parts = import_path.split(".")
            module = __import__(import_path, fromlist=[parts[-1]])
        else:
            module = __import__(import_path)
        return module
    except ImportError:
        logger.warning(f"Package '{package_name}' not installed. Install with: pip install {package_name}")
        return None


def _strip_markdown_fences(text: str) -> str:
    """Remove common markdown code fences from model output."""
    if not text:
        return text
    
    for fence in ("```sql", "```json", "```", "~~~sql", "~~~"):
        text = text.replace(fence, "")
    
    return text.strip().rstrip(";")


# ---------------------------------------------------------------------------
# Model: OpenAI
# ---------------------------------------------------------------------------

def _initialize_openai() -> Optional[Dict[str, Any]]:
    """Initialize OpenAI client."""
    api_key = settings.openai_api_key
    if not api_key:
        logger.warning("OpenAI API key not found")
        return None
    
    openai_module = _require_package("openai")
    if not openai_module:
        return None
    
    client = openai_module.OpenAI(api_key=api_key)
    
    return {
        "key": "openai",
        "display_name": "OpenAI",
        "client": client,
        "model_name": settings.openai_model or "gpt-4-turbo-preview",
        "temperature": settings.openai_temperature or 0.7,
        "supports_json_mode": True,
    }


def _openai_completion(model_instance: Dict[str, Any], messages: List[Dict], **kwargs) -> str:
    """Execute OpenAI chat completion."""
    client = model_instance.get("client")
    if not client:
        raise ValueError("OpenAI client not initialized")
    
    params = {
        "model": model_instance.get("model_name"),
        "messages": messages,
        "temperature": kwargs.get("temperature", model_instance.get("temperature", 0.7)),
        "max_tokens": kwargs.get("max_tokens", 1000),
    }
    
    # Add JSON mode if requested and supported
    if kwargs.get("json_mode") and model_instance.get("supports_json_mode"):
        params["response_format"] = {"type": "json_object"}
    
    response = client.chat.completions.create(**params)
    content = response.choices[0].message.content if response.choices else ""
    
    return content


# ---------------------------------------------------------------------------
# Model: DeepSeek
# ---------------------------------------------------------------------------

def _initialize_deepseek() -> Optional[Dict[str, Any]]:
    """Initialize DeepSeek client (OpenAI-compatible)."""
    api_key = os.getenv("DEEPSEEK_API_KEY") or settings.openai_api_key
    if not api_key:
        logger.warning("DeepSeek API key not found")
        return None
    
    openai_module = _require_package("openai")
    if not openai_module:
        return None
    
    base_url = os.getenv("DEEPSEEK_API_BASE_URL", "https://api.deepseek.com/v1")
    model_name = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat")
    
    client = openai_module.OpenAI(api_key=api_key, base_url=base_url)
    
    return {
        "key": "deepseek",
        "display_name": "DeepSeek",
        "client": client,
        "model_name": model_name,
        "temperature": float(os.getenv("DEEPSEEK_TEMPERATURE", "0.7")),
        "supports_json_mode": False,  # DeepSeek doesn't support JSON mode
    }


# ---------------------------------------------------------------------------
# Model: Gemini
# ---------------------------------------------------------------------------

def _initialize_gemini() -> Optional[Dict[str, Any]]:
    """Initialize Google Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.warning("Gemini API key not found")
        return None
    
    genai_module = _require_package("google.generativeai", "google-generativeai")
    if not genai_module:
        return None
    
    genai_module.configure(api_key=api_key)
    model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.0-flash-exp")
    
    try:
        client = genai_module.GenerativeModel(model_name)
    except Exception as e:
        logger.error(f"Error initializing Gemini client: {e}", exc_info=True)
        return None
    
    return {
        "key": "gemini",
        "display_name": "Gemini",
        "client": client,
        "model_name": model_name,
        "supports_json_mode": True,  # Gemini supports JSON mode
    }


def _gemini_completion(model_instance: Dict[str, Any], messages: List[Dict], **kwargs) -> str:
    """Execute Gemini completion."""
    client = model_instance.get("client")
    if not client:
        raise ValueError("Gemini client not initialized")
    
    # Convert messages to Gemini format
    system_prompt = ""
    user_prompt = ""
    
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")
        
        if role == "system":
            system_prompt += content + "\n\n"
        elif role == "user":
            user_prompt += content + "\n"
        elif role == "assistant":
            user_prompt += f"Assistant: {content}\n"
    
    full_prompt = f"{system_prompt}{user_prompt}".strip()
    
    # Add JSON instruction if needed
    if kwargs.get("json_mode"):
        full_prompt += "\n\nRespond with valid JSON only."
    
    response = client.generate_content(full_prompt)
    return getattr(response, "text", "")


# ---------------------------------------------------------------------------
# Model: Grok (xAI)
# ---------------------------------------------------------------------------

def _initialize_grok() -> Optional[Dict[str, Any]]:
    """Initialize Grok client (OpenAI-compatible)."""
    api_key = os.getenv("GROK_API_KEY")
    if not api_key:
        logger.warning("Grok API key not found")
        return None
    
    openai_module = _require_package("openai")
    if not openai_module:
        return None
    
    base_url = os.getenv("GROK_API_BASE_URL", "https://api.x.ai/v1")
    model_name = os.getenv("GROK_MODEL_NAME", "grok-beta")
    
    client = openai_module.OpenAI(api_key=api_key, base_url=base_url)
    
    return {
        "key": "grok",
        "display_name": "Grok",
        "client": client,
        "model_name": model_name,
        "temperature": float(os.getenv("GROK_TEMPERATURE", "0.7")),
        "supports_json_mode": True,
    }


# ---------------------------------------------------------------------------
# Register models
# ---------------------------------------------------------------------------

register_model("openai", {
    "display_name": "OpenAI",
    "description": "OpenAI GPT models (GPT-4, GPT-3.5, etc.)",
    "initializer": _initialize_openai,
    "completion_handler": _openai_completion,
    "tags": ["chat", "completion", "json-mode"],
    "supports_json_mode": True,
})

register_model("deepseek", {
    "display_name": "DeepSeek",
    "description": "DeepSeek chat model via OpenAI-compatible API",
    "initializer": _initialize_deepseek,
    "completion_handler": _openai_completion,  # Uses same handler as OpenAI
    "tags": ["chat", "completion", "openai-compatible"],
    "supports_json_mode": False,
})

register_model("gemini", {
    "display_name": "Gemini",
    "description": "Google Gemini generative AI model",
    "initializer": _initialize_gemini,
    "completion_handler": _gemini_completion,
    "tags": ["chat", "completion", "google"],
    "supports_json_mode": True,
})

register_model("grok", {
    "display_name": "Grok",
    "description": "xAI Grok model via OpenAI-compatible API",
    "initializer": _initialize_grok,
    "completion_handler": _openai_completion,  # Uses same handler as OpenAI
    "tags": ["chat", "completion", "openai-compatible"],
    "supports_json_mode": True,
})
