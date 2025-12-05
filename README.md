# Jira AI Assistant

AI-powered Jira ticket creation, estimation, and assignment system with multi-model support.

## Features

✅ **AI Story Generation** - Create Jira stories from natural language  
✅ **CrewAI Agents** - Multi-agent orchestration for intelligent workflows  
✅ **Smart Estimation** - AI-powered story point estimation with RAG  
✅ **Auto Assignment** - Intelligent ticket assignment based on skills and capacity  
✅ **Multi-Model Support** - OpenAI, DeepSeek, Gemini, Grok  
✅ **Activity Tracking** - Monitor both AI and manual Jira changes  
✅ **Analytics Dashboard** - Team performance and AI learning insights  
✅ **Capacity Management** - Track team workload and availability  

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Jira Cloud account with API access
- AI model API key (DeepSeek, OpenAI, Gemini, or Grok)

### Setup

1. **Clone and configure:**
   ```bash
   cd Backend
   cp .env.example .env
   # Edit .env with your credentials
   ```

2. **Start services:**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

3. **Access:**
   - Frontend: http://localhost:4200
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Configuration

Edit `Backend/.env`:

```env
# Jira
JIRA_URL=https://your-domain.atlassian.net/
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token
JIRA_PROJECT_KEY=PROJ

# AI Model (choose one)
DEEPSEEK_API_KEY=sk-your-key-here
# OPENAI_API_KEY=sk-your-key-here
# GEMINI_API_KEY=your-key-here
# GROK_API_KEY=your-key-here
```

## Usage

### Create Stories

1. Go to **Story Creator**
2. Enter natural language description
3. AI generates title, description, acceptance criteria
4. Auto-estimates story points
5. Auto-assigns to team member
6. Creates ticket in Jira

### View Analytics

1. Go to **Analytics**
2. See estimation accuracy, assignment success
3. View recent activity (AI + manual Jira changes)
4. Get AI recommendations

### Manage Team

1. Go to **Capacity**
2. Add team members with skills
3. Set capacity and seniority
4. Track workload and availability

### Switch AI Models

1. Go to **Settings**
2. Select provider (OpenAI, DeepSeek, Gemini, Grok)
3. Enter API key
4. Test connection
5. Save

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Angular   │────▶│   FastAPI    │────▶│    Jira     │
│  Frontend   │     │   Backend    │     │     API     │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │             │
              ┌─────▼────┐  ┌────▼─────┐
              │PostgreSQL│  │  Redis   │
              └──────────┘  └──────────┘
                    │
              ┌─────▼────┐
              │  Qdrant  │
              │ (Vector) │
              └──────────┘
```

## Documentation

- **[FEATURES_GUIDE.md](FEATURES_GUIDE.md)** - Feature overview and quick reference
- **[COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)** - Detailed setup instructions
- **[AI_MODEL_INTEGRATION.md](Backend/AI_MODEL_INTEGRATION.md)** - AI model configuration
- **[CREWAI_GUIDE.md](Backend/CREWAI_GUIDE.md)** - Multi-agent orchestration
- **[RECENT_ACTIVITY_GUIDE.md](RECENT_ACTIVITY_GUIDE.md)** - Activity feed usage
- **[DOCKER_RESTART_GUIDE.md](DOCKER_RESTART_GUIDE.md)** - Docker management
- **[QUICK_FIX.md](QUICK_FIX.md)** - Troubleshooting common issues

## Development

### Rebuild Backend (Install CrewAI, Apply Changes)

```bash
cd Backend
rebuild-backend.bat
```

### Quick Restart (No Rebuild)

```bash
cd Backend
restart-backend.bat
```

### Complete Rebuild (Fresh Start)

```bash
cd Backend
rebuild-all.bat
```

### View Logs

```bash
docker-compose -f docker-compose.dev.yml logs -f api
```

### Run Tests

```bash
cd Backend
python test_model_registry.py
python test_breakdown.py
```

## Tech Stack

**Frontend:**
- Angular 18
- TypeScript
- RxJS
- SCSS

**Backend:**
- FastAPI (Python)
- PostgreSQL
- Redis
- Celery
- Qdrant (Vector DB)

**AI Models:**
- OpenAI GPT-4
- DeepSeek
- Google Gemini
- xAI Grok

**Integrations:**
- Jira Cloud API
- Multiple AI providers

## Troubleshooting

### Quick Fix for Common Issues

If you're getting errors (database, AI model, etc.):

```bash
cd Backend
fix-database.bat
```

See **[QUICK_FIX.md](QUICK_FIX.md)** for detailed troubleshooting.

### Backend not starting

```bash
docker-compose -f docker-compose.dev.yml logs api
docker-compose -f docker-compose.dev.yml up -d --build api
```

### Jira connection issues

- Check credentials in `.env`
- Test in Settings page
- Verify API token permissions

### AI model errors

- Check API key is valid in `.env`
- Verify DEEPSEEK_API_KEY is set
- Restart containers after changing `.env`
- Test connection in Settings

### Recent activity not showing

- Click refresh button
- Restart backend container
- Check Jira changelog is enabled

## Contributing

1. Make changes
2. Test locally
3. Restart Docker containers
4. Verify in frontend
5. Commit changes

## License

MIT

## Support

For issues or questions, check the documentation files or create an issue.
