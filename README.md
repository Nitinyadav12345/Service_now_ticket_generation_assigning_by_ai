# Jira AI Assistant

AI-powered Jira ticket creation, estimation, and assignment system.

## Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for frontend development)
- Jira Cloud account with API access
- AI model API key (DeepSeek, OpenAI, Gemini, or Grok)

## Backend Setup

1. **Configure environment:**
   ```bash
   cd Backend
   cp .env.example .env
   ```

2. **Edit `Backend/.env` with your credentials:**
   ```env
   # Database
   DATABASE_URL=postgresql://postgres:postgres@db:5432/jira_ai_db

   # Jira
   JIRA_URL=https://your-domain.atlassian.net/
   JIRA_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your-api-token
   JIRA_PROJECT_KEY=YOUR_PROJECT_KEY

   # AI Model (set at least one)
   DEEPSEEK_API_KEY=your-key
   # OPENAI_API_KEY=your-key
   # GEMINI_API_KEY=your-key
   # GROK_API_KEY=your-key
   ```

3. **Start backend services:**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

4. **Verify backend is running:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/api/docs

## Frontend Setup

1. **Install dependencies:**
   ```bash
   cd jira-ai-frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm start
   ```

3. **Access frontend:**
   - http://localhost:4200

## Running the Full Stack

```bash
# Start backend (from project root)
docker-compose -f docker-compose.dev.yml up -d

# Start frontend (in separate terminal)
cd jira-ai-frontend
npm start
```

## Useful Commands

```bash
# View backend logs
docker-compose -f docker-compose.dev.yml logs -f api

# Restart backend
docker-compose -f docker-compose.dev.yml restart api

# Rebuild backend
docker-compose -f docker-compose.dev.yml up -d --build 

# Stop all services
docker-compose -f docker-compose.dev.yml down
```

## License

MIT
