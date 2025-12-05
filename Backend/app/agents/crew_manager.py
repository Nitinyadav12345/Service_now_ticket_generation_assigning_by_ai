"""
CrewAI Agent Orchestration for Jira AI Assistant
-------------------------------------------------
Multi-agent system for story generation, estimation, breakdown, and assignment.
Supports multiple AI providers through the model registry.
"""
from typing import Dict, List, Optional, Any
import logging
import os

logger = logging.getLogger(__name__)

# Check if CrewAI is available
try:
    from crewai import Agent, Task, Crew, Process
    from crewai.llm import LLM
    CREWAI_AVAILABLE = True
except ImportError:
    logger.warning("CrewAI not installed. Agent orchestration will be disabled.")
    CREWAI_AVAILABLE = False
    Agent = Task = Crew = Process = LLM = None


class JiraAICrew:
    """
    CrewAI orchestration for Jira ticket management.
    
    Agents:
    - Story Generator: Creates user stories from natural language
    - Estimator: Estimates story points using historical data
    - Breakdown: Breaks large stories into subtasks
    - Assignment: Assigns tickets to team members
    """
    
    def __init__(self, model_config: Optional[Dict[str, Any]] = None):
        """
        Initialize CrewAI manager with model configuration.
        
        Args:
            model_config: Optional model configuration from model registry
                         If None, will auto-detect from environment
        """
        if not CREWAI_AVAILABLE:
            raise ImportError("CrewAI is not installed. Install with: pip install crewai langchain-openai")
        
        self.model_config = model_config or self._get_default_model_config()
        self.llm = self._initialize_llm()
        
        logger.info(f"Initialized CrewAI with model: {self.model_config.get('model_name', 'unknown')}")
    
    def _get_default_model_config(self) -> Dict[str, Any]:
        """Get default model configuration from environment."""
        # Priority: DeepSeek > Grok > Gemini > OpenAI
        if os.getenv("DEEPSEEK_API_KEY"):
            return {
                "api_key": os.getenv("DEEPSEEK_API_KEY"),
                "base_url": os.getenv("DEEPSEEK_API_BASE_URL", "https://api.deepseek.com/v1"),
                "model_name": os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat"),
                "temperature": float(os.getenv("DEEPSEEK_TEMPERATURE", "0.7")),
                "provider": "deepseek"
            }
        elif os.getenv("GROK_API_KEY"):
            return {
                "api_key": os.getenv("GROK_API_KEY"),
                "base_url": os.getenv("GROK_API_BASE_URL", "https://api.x.ai/v1"),
                "model_name": os.getenv("GROK_MODEL_NAME", "grok-beta"),
                "temperature": float(os.getenv("GROK_TEMPERATURE", "0.7")),
                "provider": "grok"
            }
        elif os.getenv("OPENAI_API_KEY"):
            return {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "base_url": os.getenv("OPENAI_API_BASE", None),
                "model_name": os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
                "temperature": float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
                "provider": "openai"
            }
        else:
            raise ValueError("No AI model API key found. Set DEEPSEEK_API_KEY, GROK_API_KEY, or OPENAI_API_KEY")
    
    def _initialize_llm(self) -> Any:
        """Initialize LLM for CrewAI agents using CrewAI's native LLM class with LiteLLM."""
        import os
        
        provider = self.model_config.get("provider", "openai")
        model_name = self.model_config["model_name"]
        api_key = self.model_config["api_key"]
        temperature = self.model_config.get("temperature", 0.7)
        
        # Set environment variables for LiteLLM
        if provider == "gemini":
            logger.info(f"Initializing Gemini LLM with model: {model_name}")
            os.environ["GEMINI_API_KEY"] = api_key
            return LLM(
                model=f"gemini/{model_name}",
                temperature=temperature
            )
        elif provider == "deepseek":
            logger.info(f"Initializing DeepSeek LLM with model: {model_name}")
            base_url = self.model_config.get("base_url", "https://api.deepseek.com/v1")
            # Set environment variables for LiteLLM to use
            os.environ["DEEPSEEK_API_KEY"] = api_key
            os.environ["DEEPSEEK_API_BASE"] = base_url
            # LiteLLM format for custom OpenAI-compatible endpoints
            return LLM(
                model=f"deepseek/{model_name}",
                temperature=temperature,
                api_key=api_key,
                base_url=base_url
            )
        elif provider == "grok":
            logger.info(f"Initializing Grok LLM with model: {model_name}")
            base_url = self.model_config.get("base_url", "https://api.x.ai/v1")
            os.environ["XAI_API_KEY"] = api_key
            return LLM(
                model=f"xai/{model_name}",
                temperature=temperature,
                api_key=api_key,
                base_url=base_url
            )
        else:  # openai
            logger.info(f"Initializing OpenAI LLM with model: {model_name}")
            os.environ["OPENAI_API_KEY"] = api_key
            return LLM(
                model=model_name,
                temperature=temperature
            )
    
    # =========================================================================
    # AGENTS
    # =========================================================================
    
    def _create_story_generator_agent(self) -> Agent:
        """Create agent for generating user stories."""
        return Agent(
            role="User Story Generator",
            goal="Create well-structured user stories from natural language descriptions",
            backstory="""You are an expert product owner with 10+ years of experience 
            writing user stories. You excel at translating vague requirements into 
            clear, actionable user stories with proper acceptance criteria.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def _create_estimator_agent(self) -> Agent:
        """Create agent for story point estimation."""
        return Agent(
            role="Story Point Estimator",
            goal="Accurately estimate story points using Fibonacci scale (1,2,3,5,8,13,21)",
            backstory="""You are a seasoned scrum master with deep expertise in 
            story point estimation. You consider complexity, uncertainty, and effort 
            when estimating. You learn from historical data to improve accuracy.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def _create_breakdown_agent(self) -> Agent:
        """Create agent for breaking down stories into subtasks."""
        return Agent(
            role="Story Breakdown Specialist",
            goal="Break large stories into manageable subtasks across different categories",
            backstory="""You are a technical lead who excels at decomposing complex 
            features into smaller, actionable tasks. You organize work by categories 
            (Frontend, Backend, Testing, Documentation, DevOps) and ensure each 
            subtask is independently deliverable.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def _create_assignment_agent(self) -> Agent:
        """Create agent for intelligent ticket assignment."""
        return Agent(
            role="Intelligent Assignment Manager",
            goal="Assign tickets to the most suitable team member based on skills, capacity, and performance",
            backstory="""You are an AI-powered resource manager who optimizes team 
            productivity. You consider technical skills, current workload, past 
            performance, and team dynamics when making assignments.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    # =========================================================================
    # CREWS (Agent Workflows)
    # =========================================================================
    
    def create_story_generation_crew(self, prompt: str) -> Crew:
        """
        Create crew for generating a user story from natural language.
        
        Args:
            prompt: Natural language description of the feature
            
        Returns:
            Crew configured for story generation
        """
        agent = self._create_story_generator_agent()
        
        task = Task(
            description=f"""Generate a complete user story from this description:
            
            {prompt}
            
            Create a JSON response with:
            - title: User story in format "As a [user], I want [feature] so that [benefit]"
            - description: Detailed description with context, problem, and solution
            - acceptance_criteria: Array of 3-7 specific, testable criteria
            - technical_requirements: Technical implementation notes
            - required_skills: Array of required technical skills (e.g., Python, React, AWS)
            
            Be specific, clear, and actionable.""",
            agent=agent,
            expected_output="JSON object with title, description, acceptance_criteria, technical_requirements, and required_skills"
        )
        
        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
    
    def create_estimation_crew(
        self, 
        title: str, 
        description: str, 
        similar_stories: Optional[List[Dict]] = None
    ) -> Crew:
        """
        Create crew for estimating story points.
        
        Args:
            title: Story title
            description: Story description
            similar_stories: Optional list of similar stories for context
            
        Returns:
            Crew configured for estimation
        """
        agent = self._create_estimator_agent()
        
        context = ""
        if similar_stories:
            context = "\n\nSimilar stories for reference:\n"
            for story in similar_stories:
                context += f"- {story.get('title', 'N/A')}: {story.get('estimated_points', 'N/A')} points\n"
        
        task = Task(
            description=f"""Estimate story points for this story using Fibonacci scale (1,2,3,5,8,13,21):
            
            Title: {title}
            Description: {description}
            {context}
            
            Consider:
            - Complexity: How complex is the implementation?
            - Uncertainty: How much is unknown?
            - Effort: How much work is required?
            
            Respond in JSON format:
            - points: Integer (Fibonacci number)
            - reasoning: Brief explanation of the estimate
            - confidence: Float between 0 and 1""",
            agent=agent,
            expected_output="JSON object with points, reasoning, and confidence"
        )
        
        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
    
    def create_breakdown_crew(self, title: str, description: str, points: int) -> Crew:
        """
        Create crew for breaking down a story into subtasks.
        
        Args:
            title: Story title
            description: Story description
            points: Estimated story points
            
        Returns:
            Crew configured for breakdown
        """
        agent = self._create_breakdown_agent()
        
        task = Task(
            description=f"""Break down this {points}-point story into 4-8 subtasks:
            
            Title: {title}
            Description: {description}
            
            Categories: Frontend, Backend, Testing, Documentation, DevOps
            
            Each subtask should be 1-3 points and independently deliverable.
            
            Respond in JSON format with a "subtasks" array:
            {{
              "subtasks": [
                {{
                  "title": "Brief subtask title",
                  "description": "What needs to be done",
                  "category": "Frontend|Backend|Testing|Documentation|DevOps",
                  "points": 1-3
                }}
              ]
            }}""",
            agent=agent,
            expected_output="JSON object with subtasks array"
        )
        
        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
    
    def create_assignment_crew(
        self,
        issue_key: str,
        title: str,
        required_skills: List[str],
        points: int,
        team_members: List[Dict]
    ) -> Crew:
        """
        Create crew for intelligent ticket assignment.
        
        Args:
            issue_key: Jira issue key
            title: Story title
            required_skills: Required technical skills
            points: Story points
            team_members: List of available team members with their info
            
        Returns:
            Crew configured for assignment
        """
        agent = self._create_assignment_agent()
        
        team_info = "\n".join([
            f"- {m['username']}: Skills={m.get('skills', [])}, "
            f"Capacity={m.get('available_capacity', 0)}/{m.get('max_capacity', 0)}, "
            f"Performance={m.get('performance_score', 0)}"
            for m in team_members
        ])
        
        task = Task(
            description=f"""Assign this ticket to the best team member:
            
            Ticket: {issue_key} - {title}
            Required Skills: {', '.join(required_skills)}
            Story Points: {points}
            
            Available Team Members:
            {team_info}
            
            Consider:
            1. Skill match (most important)
            2. Available capacity
            3. Past performance
            4. Workload balance
            
            Respond in JSON format:
            {{
              "assigned_to": "username",
              "score": 0.0-1.0,
              "reasoning": "Why this person is the best choice"
            }}""",
            agent=agent,
            expected_output="JSON object with assigned_to, score, and reasoning"
        )
        
        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
    
    # =========================================================================
    # EXECUTION
    # =========================================================================
    
    async def run_crew(self, crew: Crew) -> str:
        """
        Execute a crew and return the result.
        
        Args:
            crew: Configured crew to execute
            
        Returns:
            Result as string (usually JSON)
        """
        try:
            result = crew.kickoff()
            return str(result)
        except Exception as e:
            logger.error(f"Error running crew: {e}", exc_info=True)
            raise
    
    # =========================================================================
    # CONVENIENCE METHODS
    # =========================================================================
    
    async def generate_story(self, prompt: str) -> Dict:
        """Generate a story from natural language (convenience method)."""
        crew = self.create_story_generation_crew(prompt)
        result = await self.run_crew(crew)
        
        # Parse JSON from result
        import json
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown
            import re
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            raise ValueError("Could not parse JSON from crew result")
    
    async def estimate_story(
        self, 
        title: str, 
        description: str, 
        similar_stories: Optional[List[Dict]] = None
    ) -> Dict:
        """Estimate story points (convenience method)."""
        crew = self.create_estimation_crew(title, description, similar_stories)
        result = await self.run_crew(crew)
        
        import json
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            raise ValueError("Could not parse JSON from crew result")
    
    async def breakdown_story(self, title: str, description: str, points: int) -> List[Dict]:
        """Break down story into subtasks (convenience method)."""
        crew = self.create_breakdown_crew(title, description, points)
        result = await self.run_crew(crew)
        
        import json
        try:
            parsed = json.loads(result)
            return parsed.get("subtasks", [])
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group(0))
                return parsed.get("subtasks", [])
            raise ValueError("Could not parse JSON from crew result")
