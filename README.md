# Jira AI Assistant

**AI-Powered Intelligent Ticket Management System**

Automate Jira ticket creation, estimation, and assignment using AI agents, machine learning, and intelligent automation.

---

## 🎯 Features

- ✅ **AI Story Generation** - Convert natural language to structured user stories
- ✅ **Smart Estimation** - AI estimates story points using historical data (RAG)
- ✅ **Auto Breakdown** - Split large stories into manageable subtasks
- ✅ **Intelligent Assignment** - Assign tickets based on capacity, skills, and performance
- ✅ **Team Capacity Management** - Real-time workload tracking
- ✅ **Learning System** - Improves from human feedback
- ✅ **Slack Integration** - Create tickets from Slack
- ✅ **Analytics Dashboard** - Track estimation and assignment accuracy
- ✅ **Background Processing** - Celery tasks for automation
- ✅ **Vector Database** - RAG for similar story search

---

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Copy environment template
cp Backend/.env.example Backend/.env

# Edit Backend/.env with your credentials:
# - JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT_KEY
# - OPENAI_API_KEY (or other LLM provider)
# - Database and Redis URLs (defaults work for Docker)
```

### 2. Start Application
```bash
# Windows
start-dev.bat

# Linux/Mac
chmod +x start-dev.sh
./start-dev.sh
```

### 3. Access Application
- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 4. First Time Setup
1. Go to **Team Capacity** page
2. Click **"Sync from Jira"** to import your team
3. Click **Edit** on team members to add skills
4. Start creating stories!

### Access the Application
- **Frontend:** http://localhost:4200
- **Backend API:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/health

---

## 📋 Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **Docker Desktop** (for Redis, PostgreSQL, Qdrant)
- **Jira Account** with API access
- **OpenAI API Key**

---

## 🔑 Required Credentials

You need these credentials to run the application:

1. **Jira API Token** - Get from https://id.atlassian.com/manage-profile/security/api-tokens
2. **LLM API Key** - Choose one:
   - **DeepSeek** ⭐ (Recommended - 10x cheaper) - Get from https://platform.deepseek.com/api_keys
   - **OpenAI** (Higher quality) - Get from https://platform.openai.com/api-keys
   - **Local Models** (Free) - See [LLM_PROVIDERS_GUIDE.md](LLM_PROVIDERS_GUIDE.md)
3. **Slack Bot Token** (Optional) - For Slack integration

📖 See **[CREDENTIALS_TEMPLATE.md](CREDENTIALS_TEMPLATE.md)** for detailed instructions on obtaining each credential.
📖 See **[LLM_PROVIDERS_GUIDE.md](LLM_PROVIDERS_GUIDE.md)** for complete LLM provider setup guide.

---

## 📚 Documentation

- **[RUN_APPLICATION.md](RUN_APPLICATION.md)** ⭐ - Complete guide to run the application
- **[LLM_PROVIDERS_GUIDE.md](LLM_PROVIDERS_GUIDE.md)** - DeepSeek, OpenAI, local models setup
- **[Backend/BACKEND_SETUP.md](Backend/BACKEND_SETUP.md)** - Backend setup details
- **[jira-ai-frontend/UI_SETUP.md](jira-ai-frontend/UI_SETUP.md)** - Frontend setup details
- Redis 7+
- Docker (optional but recommended)

### Option 1: One-Command Start (Recommended)

```bash
# Make script executable
chmod +x start-all.sh

# Start everything
./start-all.sh
# Choose option 1 (Full System)
```

### Option 2: Docker

```bash
cd Backend
./start.sh
# Choose option 1 or 2

# In another terminal
cd jira-ai-frontend
npm install
npm start
```

### Option 3: Manual

See [COMPLETE_SYSTEM_GUIDE.md](COMPLETE_SYSTEM_GUIDE.md) for detailed instructions.

---

## 🌐 Access Points

Once running:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:4200 | Angular UI |
| **API Docs** | http://localhost:8000/api/docs | Swagger UI |
| **Flower** | http://localhost:5555 | Celery monitoring |
| **Health** | http://localhost:8000/api/health | Health check |

---

## 📋 Configuration

### 1. Backend Configuration

```bash
cd Backend
cp .env.example .env
# Edit .env with your credentials
```

Required variables:
```env
# LLM Configuration
OPENAI_API_KEY=sk-...

# Jira Configuration
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-token
JIRA_PROJECT_KEY=PROJ

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/jira_ai_db

# Capacity Calculation (Optional - defaults shown)
DAILY_WORKING_HOURS=8
HOURS_PER_STORY_POINT=4.0
FOCUS_FACTOR=0.7
```

### 2. Frontend Configuration

```bash
cd jira-ai-frontend
# Edit src/environments/environment.ts if needed
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Angular)                    │
│  Dashboard | Ticket Creator | Capacity | Analytics      │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────┴────────────────────────────────────┐
│                  Backend (FastAPI)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   CrewAI     │  │    Celery    │  │   Vector DB  │ │
│  │   Agents     │  │    Tasks     │  │   (RAG)      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│              Data Layer                                  │
│  PostgreSQL  |  Redis  |  Pinecone/ChromaDB            │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│           External Services                              │
│  Jira Cloud  |  OpenAI  |  Slack (optional)            │
└─────────────────────────────────────────────────────────┘
```

---

## 🤖 AI Agents (CrewAI)

1. **Story Generator** - Creates structured user stories
2. **Requirements Analyst** - Extracts technical requirements
3. **Estimator** - Estimates story points with RAG
4. **Breakdown Agent** - Splits large stories
5. **Assignment Agent** - Assigns to best team member

---

## 📊 Tech Stack

### Frontend
- Angular 17
- TypeScript
- Tailwind CSS
- NgRx (State Management)
- Chart.js (Analytics)

### Backend
- FastAPI (Python)
- CrewAI (Multi-Agent AI)
- OpenAI GPT-4
- PostgreSQL
- Redis
- Celery (Background Tasks)
- Pinecone/ChromaDB (Vector DB)

### Integrations
- Jira Cloud API
- Slack Bolt (Optional)
- OpenAI API

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [COMPLETE_SYSTEM_GUIDE.md](COMPLETE_SYSTEM_GUIDE.md) | Complete system guide |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Quick command reference |
| [FRONTEND_BACKEND_INTEGRATION.md](FRONTEND_BACKEND_INTEGRATION.md) | Integration guide |
| [Backend/ADVANCED_FEATURES.md](Backend/ADVANCED_FEATURES.md) | Advanced features |
| [Backend/README.md](Backend/README.md) | Backend documentation |
| [jira-ai-frontend/UI_SETUP.md](jira-ai-frontend/UI_SETUP.md) | Frontend setup |

---

## 🎯 Usage Examples

### Create Ticket (Web UI)

1. Navigate to http://localhost:4200
2. Click "Create Ticket"
3. Enter: "Create user authentication with OAuth"
4. Enable AI options
5. Click "Create Ticket"
6. Watch AI process and create in Jira

### Create Ticket (Slack)

```
/create-ticket Create user profile page with avatar upload
```

### Check Team Capacity

```
/team-capacity
```

### API

```bash
curl -X POST http://localhost:8000/api/prompt/create-story \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create user login",
    "auto_estimate": true,
    "auto_assign": true
  }'
```

---

## 🔄 Background Tasks

Automated tasks running via Celery:

- **Every 15 min**: Sync team capacity from Jira
- **Every hour**: Process assignment queue
- **Daily 2 AM**: Update AI learning models
- **Weekly Sun 3 AM**: Cleanup old data

Monitor at: http://localhost:5555 (Flower)

---

## 🧪 Testing

```bash
# Backend tests
cd Backend
pytest

# Frontend tests
cd jira-ai-frontend
ng test

# E2E tests
ng e2e
```

---

## 🐳 Docker Deployment

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🔐 Security

- Environment-based secrets
- CORS configuration
- Input validation (Pydantic)
- SQL injection prevention (ORM)
- Rate limiting (recommended for production)
- HTTPS (required for production)

---

## 📈 Monitoring

- **Health Check**: http://localhost:8000/api/health
- **Celery Tasks**: http://localhost:5555
- **API Metrics**: Available in Swagger UI
- **Logs**: `docker-compose logs -f`

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🆘 Support

### Common Issues

**CORS Error**: Add frontend URL to `CORS_ORIGINS` in backend `.env`

**Port in use**: 
```bash
lsof -i :8000  # Find process
kill -9 <PID>  # Kill process
```

**Database error**: 
```bash
createdb jira_ai_db  # Create database
```

### Get Help

1. Check [COMPLETE_SYSTEM_GUIDE.md](COMPLETE_SYSTEM_GUIDE.md)
2. View logs: `docker-compose logs -f`
3. Check health: `curl http://localhost:8000/api/health`
4. Review API docs: http://localhost:8000/api/docs

---

## 🎉 Success Criteria

System is working when:

- ✅ Frontend loads at http://localhost:4200
- ✅ Backend responds at http://localhost:8000/api/health
- ✅ Can create ticket from UI
- ✅ Ticket appears in Jira
- ✅ AI generates story with acceptance criteria
- ✅ Story points estimated automatically
- ✅ Ticket assigned to team member
- ✅ Celery tasks running (check Flower)
- ✅ No errors in browser console

---

## 🚀 What's Next?

1. ✅ System setup complete
2. ⏳ Configure with your Jira instance
3. ⏳ Add team members to database
4. ⏳ Train with historical data
5. ⏳ Set up Slack bot (optional)
6. ⏳ Deploy to production
7. ⏳ Monitor and optimize

---

## 📞 Contact

For questions or issues, please check the documentation or create an issue.

---

**Built with ❤️ using AI, FastAPI, Angular, and CrewAI**

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: November 27, 2024


---

## 🔄 Team Sync from Jira

### Quick Sync
1. Open http://localhost:4200
2. Go to **Team Capacity** page
3. Click **"Sync from Jira"** button
4. Wait for sync to complete

### What Gets Synced
- ✅ All users from your Jira project
- ✅ Job titles/designations from Jira profiles
- ✅ Active sprint information
- ✅ Current workload (assigned tickets & story points)
- ✅ Calculated capacity based on sprint duration and velocity

### Capacity Calculation

**Formula:**
```
Sprint Capacity = (Working Days × Daily Working Hours − Leave Hours) × Focus Factor
Story Points = Available Hours / Hours Per Story Point
```

**Parameters:**
- Working Days = (Total Sprint Days / 7) × 5 (excludes weekends)
- Daily Working Hours = 8 hours (configurable)
- Leave Hours = 0 (enhanced with OOO tracking)
- Focus Factor = 0.7 (70% - accounts for meetings, emails, context switching)
- Hours Per Story Point = 4 hours (configurable)

**Example:**
- 14-day sprint = 10 working days
- Available hours = (10 × 8 − 0) × 0.7 = 56 hours
- Story points = 56 / 4 = 14 points

**Status:**
- Available: <75% capacity used
- Busy: 75-99% capacity used
- Overloaded: ≥100% capacity used

### Display on Cards
- Name from Jira
- Designation/Job Title (or seniority level fallback)
- Skills (manually configured)
- Current vs Max story points
- Availability status

---

## 🎯 Skills Management

### Add/Edit Team Member Details
1. Go to **Team Capacity** page
2. Click **Edit** button (pencil icon) on any team member
3. Update any of the following:
   - **Email**: Add real email if Jira doesn't provide it
   - **Designation**: Job title/role
   - **Skills**: Type skill name and press Enter or click Add
   - **Max Story Points**: Adjust capacity
   - **Seniority Level**: Junior/Mid/Senior/Lead/Principal
4. Click **Save Changes**

### Why Emails May Be Missing
Jira Cloud often hides emails due to privacy settings. The system:
- ✅ Generates placeholder emails (`accountId@jira.local`)
- ✅ Works perfectly without real emails
- ✅ Allows manual email updates via edit modal
- See [JIRA_EMAIL_TROUBLESHOOTING.md](JIRA_EMAIL_TROUBLESHOOTING.md) for details

### Recommended Skills
- **Languages**: Python, JavaScript, TypeScript, Java, C#, Go
- **Frontend**: React, Angular, Vue, HTML/CSS, Tailwind CSS
- **Backend**: Node.js, FastAPI, Django, Spring Boot, .NET
- **Databases**: PostgreSQL, MySQL, MongoDB, Redis
- **Cloud**: AWS, Azure, GCP, Docker, Kubernetes, CI/CD

### How Skills Are Used
- Match tickets to developers with required skills
- Calculate assignment scores (better match = higher score)
- Queue tickets if no one has required skills
- Show team skill distribution

---

## 🗄️ Database Management

### Recreate Database (Fresh Start)
```bash
cd Backend
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d
```

This will:
- Delete all existing data
- Create fresh database with latest schema
- Include all new columns (designation, etc.)

### After Recreation
1. Wait for services to start
2. Sync team from Jira
3. Configure skills for team members
4. Start using the system

---

## 🔧 Troubleshooting

### Sync Fails
- Check Jira credentials in `.env`
- Verify project key is correct
- Check backend logs: `docker-compose logs -f api`

### No Users Found
- Ensure users have access to the Jira project
- Check if project key is correct
- Verify Jira API token has proper permissions

### Backend Not Running
```bash
docker-compose -f Backend/docker-compose.dev.yml restart api
```

### Database Connection Error
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Restart database
docker-compose -f Backend/docker-compose.dev.yml restart postgres
```

---

## 📖 Additional Resources

- **Jira API Documentation**: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Angular Documentation**: https://angular.io/docs
- **CrewAI Documentation**: https://docs.crewai.com/

