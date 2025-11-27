import openai
from typing import Dict, List
import logging
import json
from app.config import settings
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

# Configure OpenAI-compatible client (supports OpenAI, DeepSeek, etc.)
openai.api_key = settings.openai_api_key

# Support for custom API base URL (for DeepSeek, local models, etc.)
if hasattr(settings, 'openai_api_base') and settings.openai_api_base:
    openai.base_url = settings.openai_api_base
    logger.info(f"Using custom API base: {settings.openai_api_base}")

class AIService:
    """Service for AI/LLM operations with CrewAI"""
    
    def __init__(self):
        self.model = settings.openai_model
        self.embedding_model = settings.openai_embedding_model
        self.crew_manager = JiraAICrew() if CREWAI_AVAILABLE else None
        self.vector_service = VectorService() if VECTOR_SERVICE_AVAILABLE else None
    
    def _is_deepseek_model(self) -> bool:
        """Check if using DeepSeek model"""
        return 'deepseek' in self.model.lower()
    
    def _extract_json_from_response(self, content: str) -> Dict:
        """Extract JSON from response, handling both pure JSON and markdown-wrapped JSON"""
        try:
            # Try direct JSON parse first
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            import re
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
        Generate story details from natural language prompt using CrewAI
        
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
            # Use CrewAI if available, otherwise use direct OpenAI call
            if self.crew_manager:
                try:
                    crew = self.crew_manager.create_story_generation_crew(prompt)
                    result_text = await self.crew_manager.run_crew(crew)
                except Exception as e:
                    logger.warning(f"CrewAI failed, using direct OpenAI: {e}")
            
            # Use direct OpenAI call for structured output
            system_prompt = """You are a Jira story creation expert. Generate well-structured user stories.

Format the response as JSON with these fields:
- title: User story format "As a [user], I want [feature] so that [benefit]"
- description: Detailed description with context, problem, and solution
- acceptance_criteria: Array of 3-7 testable criteria
- technical_requirements: Technical implementation notes
- required_skills: Array of required technical skills

Be specific, clear, and actionable."""

            # Check if model supports response_format (OpenAI does, some others don't)
            completion_params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Create a user story for: {prompt}"}
                ],
                "temperature": 0.7
            }
            
            # Only add response_format for models that support it
            if not self._is_deepseek_model():
                completion_params["response_format"] = {"type": "json_object"}
            
            response = openai.chat.completions.create(**completion_params)
            
            # Extract JSON from response (handles both pure JSON and markdown-wrapped)
            result = self._extract_json_from_response(response.choices[0].message.content)
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
            
            # Fallback to direct OpenAI call for structured output
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

            completion_params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Title: {title}\n\nDescription: {description}"}
                ],
                "temperature": 0.5
            }
            
            if not self._is_deepseek_model():
                completion_params["response_format"] = {"type": "json_object"}
            
            response = openai.chat.completions.create(**completion_params)
            
            result = self._extract_json_from_response(response.choices[0].message.content)
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

Each subtask should be 1-3 points. Respond in JSON format as an array of objects:
- title: Brief subtask title
- description: What needs to be done
- category: One of the categories above
- points: 1, 2, or 3"""

            completion_params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Title: {title}\n\nDescription: {description}"}
                ],
                "temperature": 0.7
            }
            
            if not self._is_deepseek_model():
                completion_params["response_format"] = {"type": "json_object"}
            
            response = openai.chat.completions.create(**completion_params)
            
            result = self._extract_json_from_response(response.choices[0].message.content)
            subtasks = result.get("subtasks", [])
            logger.info(f"Created {len(subtasks)} subtasks for: {title}")
            return subtasks
            
        except Exception as e:
            logger.error(f"Error breaking down story: {e}")
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
        # Simplified implementation - can be enhanced with conversation history
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful Jira assistant. Help users create stories."},
                    {"role": "user", "content": message}
                ],
                temperature=0.7
            )
            
            return {
                "response": response.choices[0].message.content,
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
