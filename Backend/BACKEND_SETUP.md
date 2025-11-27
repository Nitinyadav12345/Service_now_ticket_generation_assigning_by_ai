# Jira AI Assistant - Backend Setup Guide

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- OpenAI API Key
- Jira Cloud Account with API Token

### 2. Installation

```bash
# Navigate to Backend directory
cd Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Setup

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your credentials:
# - DATABASE_URL
# - OPENAI_API_KEY
# - JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN
# - PINECONE_API_KEY (optional, for production)
```

### 4. Database Setup

```bash
# Create database
createdb jira_ai_db

# Run migrations
alembic upgrade head

# Or let SQLAlchemy create tables on first run
python -m app.main
```

### 5. Run the Application

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 6. Run Celery Workers (Optional - for background tasks)

```bash
# Terminal 1: Start Celery worker
celery -A app.celery_app worker --loglevel=info

# Terminal 2: Start Celery beat (scheduler)
celery -A app.celery_app beat --loglevel=info

# Terminal 3: Start Flower (monitoring UI)
celery -A app.celery_app flower
```

## 📁 Project Structure

```
Backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration
│   ├── database.py             # Database connection
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   │
│   ├── routers/                # API endpoints
│   │   ├── __init__.py
│   │   ├── prompt.py           # Story creation endpoints
│   │   ├── capacity.py         # Team capacity endpoints
│   │   ├── assignment.py       # Assignment endpoints
│   │   ├── analytics.py        # Analytics endpoints
│   │   └── webhook.py          # Jira webhooks
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── story_service.py    # Story creation logic
│   │   ├── ai_service.py       # AI/LLM integration
│   │   ├── jira_service.py     # Jira API integration
│   │   ├── capacity_service.py # Capacity management
│   │   ├── assignment_service.py # Assignment logic
│   │   └── vector_service.py   # Vector DB (RAG)
│   │
│   ├── agents/                 # CrewAI agents
│   │   ├── __init__.py
│   │   ├── story_generator.py  # Story generation agent
│   │   ├── estimator.py        # Estimation agent
│   │   ├── breakdown.py        # Breakdown agent
│   │   └── assignment.py       # Assignment agent
│   │
│   ├── tasks/                  # Celery tasks
│   │   ├── __init__.py
│   │   ├── capacity_sync.py    # Sync capacity from Jira
│   │   ├── assignment_queue.py # Process assignment queue
│   │   └── learning.py         # Learning from feedback
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── jira_client.py      # Jira client wrapper
│       └── openai_client.py    # OpenAI client wrapper
│
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
│
├── tests/                      # Tests
│   ├── test_api.py
│   ├── test_services.py
│   └── test_agents.py
│
├── .env.example                # Environment variables template
├── .gitignore
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose setup
└── README.md
```

## 🔌 API Endpoints

### Story/Ticket Creation
- `POST /api/prompt/create-story` - Create ticket from natural language
- `GET /api/prompt/story-status/{request_id}` - Get creation status
- `POST /api/prompt/chat` - Conversational interface
- `POST /api/prompt/suggest-estimation` - Get estimation suggestion

### Team Capacity
- `GET /api/capacity/team` - Get team capacity overview
- `GET /api/capacity/member/{username}` - Get member capacity
- `POST /api/capacity/mark-ooo` - Mark member as out of office
- `POST /api/capacity/refresh` - Refresh capacity from Jira

### Assignment
- `POST /api/assignment/assign-ticket` - Manually assign ticket
- `GET /api/assignment/queue` - Get assignment queue
- `POST /api/assignment/process-queue` - Process queued assignments

### Analytics
- `GET /api/analytics/dashboard-stats` - Dashboard statistics
- `GET /api/analytics/estimation-accuracy` - Estimation metrics
- `GET /api/analytics/assignment-accuracy` - Assignment metrics
- `GET /api/analytics/learning-insights` - AI learning insights
- `GET /api/analytics/recommendations` - System recommendations

### Webhooks
- `POST /api/webhook/jira` - Jira webhook handler

## 🤖 AI Agents (CrewAI)

### 1. Story Generator Agent
- **Role**: Story Creation Specialist
- **Goal**: Generate well-structured stories from natural language
- **Tasks**:
  - Parse user prompt
  - Generate title in user story format
  - Create detailed description
  - Generate acceptance criteria (3-7 items)
  - Extract technical requirements
  - Identify required skills

### 2. Estimator Agent
- **Role**: Estimation Expert
- **Goal**: Accurately estimate story points using historical data
- **Tasks**:
  - Analyze story complexity
  - Search similar stories (RAG)
  - Calculate story points (Fibonacci: 1,2,3,5,8,13,21)
  - Provide reasoning and confidence score

### 3. Breakdown Agent
- **Role**: Task Decomposition Specialist
- **Goal**: Break large stories into manageable subtasks
- **Tasks**:
  - Triggered when estimated_points > 5
  - Create 4-8 subtasks
  - Categorize tasks (Frontend, Backend, Testing, etc.)
  - Estimate subtask points

### 4. Assignment Agent
- **Role**: Team Assignment Optimizer
- **Goal**: Assign tickets to best-fit team members
- **Tasks**:
  - Calculate assignment scores:
    - Bandwidth × 40%
    - Skills × 30%
    - Priority Fit × 20%
    - Performance × 10%
  - Check capacity constraints
  - Provide assignment reasoning

## 🔄 Background Tasks (Celery)

### Periodic Tasks (Celery Beat)
- **Capacity Sync**: Every 15 minutes
  - Sync current workload from Jira
  - Update team member capacity
  - Update availability status

- **Assignment Queue Processing**: Every hour
  - Retry failed assignments
  - Check if capacity freed up
  - Assign queued tickets

- **Learning Updates**: Daily
  - Analyze feedback patterns
  - Update AI prompts
  - Adjust scoring weights

### Async Tasks (Celery Workers)
- Story processing (generation, estimation, breakdown)
- Jira ticket creation
- Assignment calculation
- Vector embedding updates

## 🗄️ Database Schema

See `app/models.py` for complete schema. Key tables:

- **story_requests**: Ticket creation requests
- **team_members**: Team capacity and info
- **feedback_estimations**: Learning from human corrections
- **assignment_history**: Assignment decisions and outcomes
- **team_member_ooo**: Out of office records
- **assignment_queue**: Tickets waiting for assignment
- **vector_embeddings**: Embeddings for RAG

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_api.py
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## 📊 Monitoring

- **API Docs**: http://localhost:8000/api/docs
- **Flower (Celery)**: http://localhost:5555
- **Health Check**: http://localhost:8000/api/health

## 🔐 Security

- API authentication (JWT tokens)
- Rate limiting (100 req/min per user)
- Input validation (Pydantic)
- SQL injection prevention (SQLAlchemy ORM)
- HTTPS only in production

## 🚨 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
pg_isready

# Check connection string in .env
echo $DATABASE_URL
```

### OpenAI API Issues
```bash
# Verify API key
python -c "import openai; openai.api_key='your-key'; print(openai.Model.list())"
```

### Jira Connection Issues
```bash
# Test Jira connection
python -c "from jira import JIRA; jira = JIRA('https://your-domain.atlassian.net', basic_auth=('email', 'token')); print(jira.myself())"
```

## 📝 Next Steps

1. ✅ Set up environment variables
2. ✅ Create database
3. ✅ Run migrations
4. ✅ Start FastAPI server
5. ✅ Test API endpoints
6. ⏳ Set up Celery workers
7. ⏳ Configure Jira webhooks
8. ⏳ Train AI with historical data
9. ⏳ Deploy to production

## 🤝 Integration with Frontend

The backend is designed to work seamlessly with your Angular frontend:

```typescript
// Frontend API Service Example
const API_URL = 'http://localhost:8000/api';

// Create ticket
const response = await http.post(`${API_URL}/prompt/create-story`, {
  prompt: 'Create user authentication...',
  issue_type: 'Story',
  priority: 'High',
  auto_estimate: true,
  auto_breakdown: true,
  auto_assign: true
});

// Check status
const status = await http.get(`${API_URL}/prompt/story-status/${response.request_id}`);
```

---

**Status**: ✅ Backend Structure Complete - Ready for Implementation
**Last Updated**: November 27, 2024
