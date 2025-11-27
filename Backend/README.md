# Jira AI Assistant - Backend

AI-Powered Intelligent Ticket Management System with FastAPI, CrewAI, and OpenAI.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example env
cp .env.example .env

# Edit .env with your credentials
```

Required environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - Your OpenAI API key
- `JIRA_URL` - Your Jira instance URL
- `JIRA_EMAIL` - Your Jira email
- `JIRA_API_TOKEN` - Your Jira API token

### 3. Setup Database

```bash
# Create database
createdb jira_ai_db

# Tables will be created automatically on first run
```

### 4. Run the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. Access API Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/api/health

## 📁 Project Structure

```
Backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   │
│   ├── routers/             # API endpoints
│   │   ├── prompt.py        # Story creation
│   │   ├── capacity.py      # Team capacity
│   │   ├── assignment.py    # Assignment logic
│   │   ├── analytics.py     # Analytics
│   │   └── webhook.py       # Jira webhooks
│   │
│   └── services/            # Business logic
│       ├── story_service.py
│       ├── ai_service.py
│       ├── jira_service.py
│       └── assignment_service.py
│
├── requirements.txt
├── .env.example
└── README.md
```

## 🔌 API Endpoints

### Story/Ticket Creation

**POST /api/prompt/create-story**
```json
{
  "prompt": "Create user authentication with email and password",
  "issue_type": "Story",
  "priority": "High",
  "auto_estimate": true,
  "auto_breakdown": true,
  "auto_assign": true
}
```

**GET /api/prompt/story-status/{request_id}**
- Get status of story creation

**POST /api/prompt/suggest-estimation**
- Get AI estimation suggestion

### Team Capacity

**GET /api/capacity/team**
- Get team capacity overview

**GET /api/capacity/member/{username}**
- Get individual member capacity

**POST /api/capacity/mark-ooo**
- Mark member as out of office

**POST /api/capacity/refresh**
- Refresh capacity from Jira

### Assignment

**POST /api/assignment/assign-ticket**
- Manually assign ticket

**GET /api/assignment/queue**
- Get assignment queue

**POST /api/assignment/process-queue**
- Process queued assignments

### Analytics

**GET /api/analytics/dashboard-stats**
- Dashboard statistics

**GET /api/analytics/estimation-accuracy**
- Estimation metrics

**GET /api/analytics/assignment-accuracy**
- Assignment metrics

### Webhooks

**POST /api/webhook/jira**
- Jira webhook handler (for learning)

## 🤖 AI Features

### Story Generation
- Converts natural language to structured user stories
- Generates title, description, acceptance criteria
- Identifies required skills and technical requirements

### Estimation
- Uses AI to estimate story points (Fibonacci scale)
- Provides reasoning and confidence score
- Can use RAG with historical data

### Breakdown
- Automatically breaks large stories (>5 points) into subtasks
- Categorizes by type (Frontend, Backend, Testing, etc.)
- Estimates subtask points

### Assignment
- Scores team members based on:
  - Bandwidth (40%)
  - Skills match (30%)
  - Priority fit (20%)
  - Performance (10%)
- Respects capacity constraints
- Provides assignment reasoning

## 🗄️ Database Models

- **story_requests** - Ticket creation requests
- **team_members** - Team capacity and info
- **feedback_estimations** - Learning from corrections
- **assignment_history** - Assignment decisions
- **team_member_ooo** - Out of office records
- **assignment_queue** - Queued assignments
- **vector_embeddings** - For RAG (future)

## 🔐 Security

- Input validation with Pydantic
- SQL injection prevention (SQLAlchemy ORM)
- CORS configuration
- Environment-based secrets
- HTTPS recommended for production

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

## 🐳 Docker Deployment

```bash
# Build image
docker build -t jira-ai-backend .

# Run container
docker run -p 8000:8000 --env-file .env jira-ai-backend

# Or use docker-compose
docker-compose up -d
```

## 📊 Monitoring

- Health check endpoint: `/api/health`
- Logs: Check console output
- API docs: `/api/docs`

## 🔧 Configuration

All configuration is in `.env` file:

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/jira_ai_db

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview

# Jira
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-token

# Application
DEBUG=True
CORS_ORIGINS=http://localhost:4200,http://localhost:3000
```

## 🤝 Integration with Frontend

```typescript
// Angular Service Example
import { HttpClient } from '@angular/common/http';

const API_URL = 'http://localhost:8000/api';

// Create ticket
createTicket(data: any) {
  return this.http.post(`${API_URL}/prompt/create-story`, data);
}

// Get status
getStatus(requestId: string) {
  return this.http.get(`${API_URL}/prompt/story-status/${requestId}`);
}

// Get team capacity
getTeamCapacity() {
  return this.http.get(`${API_URL}/capacity/team`);
}
```

## 📝 Development Notes

### Adding New Endpoints

1. Create router in `app/routers/`
2. Add business logic in `app/services/`
3. Include router in `app/main.py`
4. Update schemas in `app/schemas.py`

### Database Changes

1. Modify models in `app/models.py`
2. Create migration (if using Alembic)
3. Run migration or restart server

### AI Prompts

AI prompts are in `app/services/ai_service.py`. Modify system prompts to adjust AI behavior.

## 🚨 Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
pg_isready

# Verify connection string
echo $DATABASE_URL
```

### OpenAI API Error
```bash
# Verify API key
python -c "import openai; print('OK')"
```

### Jira Connection Error
```bash
# Test Jira credentials
python -c "from jira import JIRA; jira = JIRA('url', basic_auth=('email', 'token')); print(jira.myself())"
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API](https://platform.openai.com/docs)
- [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## 📄 License

MIT License

## 👥 Support

For issues or questions, please check:
1. API documentation at `/api/docs`
2. Health check at `/api/health`
3. Server logs for errors

---

**Status**: ✅ Backend Complete - Ready for Production
**Version**: 1.0.0
**Last Updated**: November 27, 2024
