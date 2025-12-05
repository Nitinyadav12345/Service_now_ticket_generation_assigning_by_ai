from typing import Dict, List, Optional
import logging
import json
import re
from app.config import settings
from app.services.model_registry import (
    initialize_model_client,
    get_completion_handler,
    list_available_models,
)

# CrewAI is optional - only import if available
try:
    from app.agents.crew_manager import JiraAICrew
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    JiraAICrew = None

# VectorService is optional - only import if available
try:
    from app.services.vector_service import VectorService
    VECTOR_SERVICE_AVAILABLE = True
except ImportError:
    VECTOR_SERVICE_AVAILABLE = False
    VectorService = None

logger = logging.getLogger(__name__)

class AIService:
    """Service for AI/LLM operations with multi-model support via registry"""
    
    def __init__(self, model_key: str = None):
        """
        Initialize AI service with specified model.
        
        Args:
            model_key: Model identifier (openai, deepseek, gemini, grok)
                      If None, attempts to auto-detect from settings
        """
        self.vector_service = VectorService() if VECTOR_SERVICE_AVAILABLE else None
        
        # Auto-detect model if not specified
        if not model_key:
            model_key = self._detect_model_from_settings()
        
        self.model_key = model_key
        self.model_instance = initialize_model_client(model_key)
        
        if not self.model_instance:
            logger.error(f"Failed to initialize model: {model_key}")
            raise ValueError(f"Could not initialize AI model: {model_key}")
        
        self.completion_handler = get_completion_handler(model_key)
        if not self.completion_handler:
            raise ValueError(f"No completion handler for model: {model_key}")
        
        logger.info(f"Initialized AI service with model: {self.model_instance.get('display_name')}")
        
        # Initialize CrewAI with model configuration
        if CREWAI_AVAILABLE and JiraAICrew:
            try:
                import os
                # Get API key and base URL from environment based on provider
                api_key = None
                base_url = None
                
                if model_key == "deepseek":
                    api_key = os.getenv("DEEPSEEK_API_KEY")
                    base_url = os.getenv("DEEPSEEK_API_BASE_URL", "https://api.deepseek.com/v1")
                elif model_key == "openai":
                    api_key = settings.openai_api_key
                    base_url = settings.openai_api_base
                elif model_key == "gemini":
                    api_key = os.getenv("GEMINI_API_KEY")
                    base_url = None
                elif model_key == "grok":
                    api_key = os.getenv("GROK_API_KEY")
                    base_url = os.getenv("GROK_API_BASE_URL", "https://api.x.ai/v1")
                
                if not api_key:
                    logger.warning(f"No API key found for {model_key}, CrewAI disabled")
                    self.crew_manager = None
                else:
                    # Pass model config to CrewAI
                    model_config = {
                        "api_key": api_key,
                        "base_url": base_url,
                        "model_name": self.model_instance.get("model_name"),
                        "temperature": self.model_instance.get("temperature", 0.7),
                        "provider": model_key
                    }
                    self.crew_manager = JiraAICrew(model_config)
                    logger.info(f"CrewAI initialized successfully with {model_key}")
            except Exception as e:
                logger.warning(f"Failed to initialize CrewAI: {e}")
                self.crew_manager = None
        else:
            self.crew_manager = None
            if not CREWAI_AVAILABLE:
                logger.info("CrewAI not available - using direct model calls")
    
    def _detect_model_from_settings(self) -> str:
        """Auto-detect which model to use based on settings."""
        import os
        
        # Priority order: Check environment variables for API keys
        # 1. Check for DeepSeek
        if os.getenv("DEEPSEEK_API_KEY"):
            logger.info("Auto-detected DeepSeek from DEEPSEEK_API_KEY")
            return "deepseek"
        
        # 2. Check for Grok
        if os.getenv("GROK_API_KEY"):
            logger.info("Auto-detected Grok from GROK_API_KEY")
            return "grok"
        
        # 3. Check for Gemini
        if os.getenv("GEMINI_API_KEY"):
            logger.info("Auto-detected Gemini from GEMINI_API_KEY")
            return "gemini"
        
        # 4. Check for OpenAI
        if settings.openai_api_key:
            logger.info("Auto-detected OpenAI from OPENAI_API_KEY")
            return "openai"
        
        # 5. Check API base URL as fallback
        if settings.openai_api_base:
            if 'deepseek' in settings.openai_api_base.lower():
                logger.info("Auto-detected DeepSeek from API base URL")
                return "deepseek"
            if 'x.ai' in settings.openai_api_base.lower():
                logger.info("Auto-detected Grok from API base URL")
                return "grok"
        
        # Default to OpenAI (will fail if no key, but that's expected)
        logger.warning("No AI model API key found, defaulting to OpenAI")
        return "openai"
    
    @staticmethod
    def list_models() -> List[Dict]:
        """List all available AI models."""
        return list_available_models()
    
    def _call_model(self, messages: List[Dict], **kwargs) -> str:
        """
        Call the AI model with messages.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional parameters (temperature, max_tokens, json_mode, etc.)
        
        Returns:
            Model response as string
        """
        try:
            return self.completion_handler(self.model_instance, messages, **kwargs)
        except Exception as e:
            logger.error(f"Error calling model: {e}", exc_info=True)
            raise
    
    def _extract_json_from_response(self, content: str) -> Dict:
        """Extract JSON from response, handling both pure JSON and markdown-wrapped JSON"""
        try:
            # Try direct JSON parse first
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            # Try to find JSON object in text
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            raise ValueError("Could not extract JSON from response")
    
    async def generate_story(self, prompt: str) -> Dict:
        """
        Generate story details from natural language prompt using CrewAI or direct model call
        
        Returns:
            {
                "title": "As a user, I want...",
                "description": "Detailed description...",
                "acceptance_criteria": ["criterion 1", "criterion 2", ...],
                "technical_requirements": "Technical notes...",
                "required_skills": ["Python", "React", ...]
            }
        """
        try:
            # Try CrewAI first if available
            if self.crew_manager and CREWAI_AVAILABLE:
                try:
                    logger.info("Using CrewAI for story generation")
                    result = await self.crew_manager.generate_story(prompt)
                    logger.info(f"CrewAI generated story: {result.get('title', 'N/A')}")
                    return result
                except Exception as e:
                    logger.warning(f"CrewAI failed, falling back to direct model call: {e}")
            
            # Use model registry for structured output
            system_prompt = """You are a Jira story creation expert. Generate well-structured user stories.

Format the response as JSON with these fields:
- title: User story format "As a [user], I want [feature] so that [benefit]"
- description: Detailed description with context, problem, and solution
- acceptance_criteria: Array of 3-7 testable criteria
- technical_requirements: Technical implementation notes
- required_skills: Array of required technical skills

Be specific, clear, and actionable."""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create a user story for: {prompt}"}
            ]
            
            # Call model with JSON mode if supported
            response_text = self._call_model(
                messages,
                temperature=0.7,
                json_mode=self.model_instance.get("supports_json_mode", False)
            )
            
            # Extract JSON from response (handles both pure JSON and markdown-wrapped)
            result = self._extract_json_from_response(response_text)
            logger.info(f"Generated story: {result.get('title', 'N/A')}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating story: {e}")
            # Fallback response
            return {
                "title": f"Story: {prompt[:100]}",
                "description": prompt,
                "acceptance_criteria": ["Implement the feature", "Test the feature", "Document the feature"],
                "technical_requirements": "To be determined",
                "required_skills": ["Development"]
            }
    
    async def estimate_story_points(self, title: str, description: str) -> Dict:
        """
        Estimate story points using AI with RAG (similar stories)
        
        Returns:
            {
                "points": 5,
                "reasoning": "Explanation...",
                "confidence": 0.85
            }
        """
        try:
            # Find similar stories using RAG if available
            similar_stories = []
            if self.vector_service:
                try:
                    similar_stories = self.vector_service.find_similar_stories(title, description, top_k=3)
                except Exception:
                    pass
            
            # Use CrewAI if available
            if self.crew_manager:
                try:
                    crew = self.crew_manager.create_estimation_crew(title, description, similar_stories)
                    result_text = await self.crew_manager.run_crew(crew)
                except Exception:
                    pass
            
            # Use model registry for estimation
            context = ""
            if similar_stories:
                context = "\n\nSimilar stories for reference:\n"
                for story in similar_stories:
                    context += f"- {story.get('title', 'N/A')}: {story.get('estimated_points', 'N/A')} points (similarity: {story.get('similarity_score', 0)})\n"
            
            system_prompt = f"""You are a story point estimation expert. Estimate using Fibonacci scale: 1, 2, 3, 5, 8, 13, 21.

Consider:
- Complexity
- Uncertainty
- Effort required
{context}

Respond in JSON format:
- points: Integer (Fibonacci number)
- reasoning: Brief explanation
- confidence: Float 0-1"""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Title: {title}\n\nDescription: {description}"}
            ]
            
            response_text = self._call_model(
                messages,
                temperature=0.5,
                json_mode=self.model_instance.get("supports_json_mode", False)
            )
            
            result = self._extract_json_from_response(response_text)
            logger.info(f"Estimated {result.get('points', 'N/A')} points for: {title} (with RAG)")
            return result
            
        except Exception as e:
            logger.error(f"Error estimating story points: {e}")
            return {
                "points": 5,
                "reasoning": "Default estimation",
                "confidence": 0.5
            }
    
    async def breakdown_story(self, title: str, description: str, points: int) -> List[Dict]:
        """
        Break down large story into subtasks
        
        Returns:
            [
                {
                    "title": "Subtask title",
                    "description": "Subtask description",
                    "category": "Frontend|Backend|Testing|...",
                    "points": 2
                },
                ...
            ]
        """
        try:
            system_prompt = f"""You are a task breakdown expert. Break this {points}-point story into 4-8 subtasks.

Categories: Frontend, Backend, Testing, Documentation, DevOps

Each subtask should be 1-3 points. Respond in JSON format with a "subtasks" array:
{{
  "subtasks": [
    {{
      "title": "Brief subtask title",
      "description": "What needs to be done",
      "category": "Frontend|Backend|Testing|Documentation|DevOps",
      "points": 1-3
    }}
  ]
}}"""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Title: {title}\n\nDescription: {description}"}
            ]
            
            response_text = self._call_model(
                messages,
                temperature=0.7,
                json_mode=self.model_instance.get("supports_json_mode", False)
            )
            
            result = self._extract_json_from_response(response_text)
            subtasks = result.get("subtasks", [])
            
            if not subtasks:
                logger.warning(f"No subtasks in response. Full response: {result}")
                # If response is directly an array, use it
                if isinstance(result, list):
                    subtasks = result
            
            logger.info(f"Created {len(subtasks)} subtasks for: {title}")
            return subtasks
            
        except Exception as e:
            logger.error(f"Error breaking down story: {e}", exc_info=True)
            return []
    
    async def process_chat_message(
        self,
        message: str,
        session_id: str = None,
        context: Dict = None
    ) -> Dict:
        """
        Process conversational message for story creation
        
        Returns:
            {
                "response": "AI response",
                "suggestions": ["suggestion 1", ...],
                "actions": [{"type": "create_story", "data": {...}}],
                "session_id": "session-id"
            }
        """
        try:
            messages = [
                {"role": "system", "content": "You are a helpful Jira assistant. Help users create stories."},
                {"role": "user", "content": message}
            ]
            
            response_text = self._call_model(messages, temperature=0.7)
            
            return {
                "response": response_text,
                "suggestions": [],
                "actions": [],
                "session_id": session_id or "new-session"
            }
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return {
                "response": "I'm having trouble processing that. Could you rephrase?",
                "suggestions": [],
                "actions": [],
                "session_id": session_id or "new-session"
            }
    
    async def suggest_estimation(self, title: str, description: str) -> Dict:
        """Get estimation suggestion with similar stories"""
        # This would use RAG with vector database in production
        estimation = await self.estimate_story_points(title, description)
        
        return {
            "estimated_points": estimation["points"],
            "reasoning": estimation["reasoning"],
            "confidence": estimation["confidence"],
            "similar_stories": []  # Would query vector DB here
        }
