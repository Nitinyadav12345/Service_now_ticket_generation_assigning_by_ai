# 🚀 How to Run the Jira AI Assistant

**Complete guide to start and use the application**

---

## ✅ Prerequisites Check

Before starting, make sure you have:

- [x] Docker Desktop installed and running
- [x] Node.js 18+ installed
- [x] Backend/.env file configured with your credentials
- [x] Jira API token
- [x] LLM API key (DeepSeek or OpenAI)

---

## 🎯 Quick Start (2 Steps)

### Step 1: Start Backend Services (Docker)

Open PowerShell and run:

```powershell
cd Backend
docker-compose -f docker-compose.dev.yml up -d
```

**Wait 30-60 seconds** for services to start.

**Verify backend is running:**
```powershell
# Check status
docker-compose -f docker-compose.dev.yml ps

# Test API
curl http://localhost:8000/api/health
```

You should see: `{"status":"healthy"}`

### Step 2: Start Frontend

Open a **NEW PowerShell window** and run:

```powershell
cd jira-ai-frontend
npm start
```

**Wait 30-60 seconds** for compilation.

When you see:
```
✔ Browser application bundle generation complete.
** Angular Live Development Server is listening on localhost:4200 **
```

You're ready! 🎉

---

## 🌐 Access the Application

Open your browser and go to:

### **http://localhost:4200**

You should see the Jira AI Assistant dashboard!

---

## 📊 Available Services

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:4200 | Main application UI |
| **Backend API** | http://localhost:8000 | REST API |
| **API Documentation** | http://localhost:8000/docs | Swagger UI - Test APIs |
| **Qdrant Dashboard** | http://localhost:6333/dashboard | Vector database UI |

---

## 🎮 Using the Application

### 1. Create Your First Story

1. Click **"Story Creator"** in the sidebar
2. Enter a prompt, for example:
   ```
   Create a user authentication system with email and password login
   ```
3. Select options:
   - **Issue Type:** Story
   - **Priority:** High
   - ☑️ **Auto Estimate** (AI estimates story points)
   - ☑️ **Auto Breakdown** (Creates subtasks)
   - ☑️ **Auto Assign** (Assigns to best team member)
4. Click **"Generate Story"**
5. Wait 10-30 seconds for AI to generate
6. View the generated story with:
   - Title and description
   - Acceptance criteria
   - Story point estimation
   - Assigned team member
   - Subtasks breakdown

### 2. View Team Capacity

1. Click **"Capacity"** in the sidebar
2. See team members with:
   - Current workload
   - Available capacity
   - Skills
   - Availability status
3. Mark members as out-of-office
4. Refresh capacity from Jira

### 3. View Analytics

1. Click **"Analytics"** in the sidebar
2. See metrics:
   - Stories created
   - Estimation accuracy
   - Assignment success rate
   - Team performance
3. View charts and insights

### 4. Dashboard Overview

1. Click **"Dashboard"** in the sidebar
2. See quick stats:
   - Recent stories
   - Team capacity overview
   - Quick actions

---

## 🔧 Common Tasks

### View Backend Logs

```powershell
cd Backend
docker-compose -f docker-compose.dev.yml logs -f api
```

Press `Ctrl+C` to stop viewing logs.

### Restart Backend

```powershell
cd Backend
docker-compose -f docker-compose.dev.yml restart api
```

### Restart Frontend

In the frontend terminal, press `Ctrl+C`, then:
```powershell
npm start
```

### Update Backend Code

The backend auto-reloads when you change code. Just edit files in `Backend/app/` and save.

### Update Frontend Code

The frontend auto-reloads when you change code. Just edit files in `jira-ai-frontend/src/` and save.

---

## 🛑 Stopping the Application

### Stop Frontend

In the frontend terminal, press: **Ctrl+C**

### Stop Backend

```powershell
cd Backend
docker-compose -f docker-compose.dev.yml down
```

This stops all Docker containers (API, PostgreSQL, Redis, Qdrant).

---

## 🔄 Restarting the Application

### Start Backend

```powershell
cd Backend
docker-compose -f docker-compose.dev.yml up -d
```

### Start Frontend

```powershell
cd jira-ai-frontend
npm start
```

---

## 🐛 Troubleshooting

### Backend not responding

**Check if containers are running:**
```powershell
cd Backend
docker-compose -f docker-compose.dev.yml ps
```

All should show "Up" status.

**View logs for errors:**
```powershell
docker-compose -f docker-compose.dev.yml logs api
```

**Restart backend:**
```powershell
docker-compose -f docker-compose.dev.yml restart api
```

### Frontend shows errors

**Check backend is running:**
```powershell
curl http://localhost:8000/api/health
```

**Clear and reinstall:**
```powershell
cd jira-ai-frontend
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
npm start
```

### "Cannot connect to backend"

**Check .env file has correct credentials:**
```powershell
cd Backend
notepad .env
```

Verify:
- `JIRA_URL` is correct
- `JIRA_API_TOKEN` is valid
- `OPENAI_API_KEY` or `OPENAI_API_BASE` is set

**Restart backend after changing .env:**
```powershell
docker-compose -f docker-compose.dev.yml restart api
```

### Port already in use

**For port 8000 (backend):**
```powershell
# Find process
netstat -ano | findstr :8000

# Kill it
taskkill /PID <process_id> /F
```

**For port 4200 (frontend):**
```powershell
# Find process
netstat -ano | findstr :4200

# Kill it
taskkill /PID <process_id> /F
```

### Docker containers won't start

**Make sure Docker Desktop is running.**

**Reset Docker:**
```powershell
cd Backend
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d --build
```

---

## 📝 Configuration

### Backend Configuration (Backend/.env)

```env
# Jira
JIRA_URL=https://your-company.atlassian.net
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=your-jira-token
JIRA_PROJECT_KEY=PROJ

# LLM (DeepSeek recommended)
OPENAI_API_KEY=sk-your-deepseek-key
OPENAI_API_BASE=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat

# Or OpenAI
# OPENAI_API_KEY=sk-your-openai-key
# OPENAI_API_BASE=
# OPENAI_MODEL=gpt-3.5-turbo

# Database (Docker defaults - don't change)
DATABASE_URL=postgresql://jira_user:jira_password@postgres:5432/jira_ai_db
REDIS_URL=redis://redis:6379/0
QDRANT_URL=http://qdrant:6333
```

### Frontend Configuration

Default configuration works out of the box. If you need to change the backend URL:

Edit: `jira-ai-frontend/src/environments/environment.ts`

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

---

## 🎯 Testing the Setup

### 1. Test Backend API

Open: http://localhost:8000/docs

Try the `/api/health` endpoint - should return `{"status":"healthy"}`

### 2. Test Story Generation

In the Swagger UI (http://localhost:8000/docs):

1. Find `POST /api/prompt/create-story`
2. Click "Try it out"
3. Enter request body:
```json
{
  "prompt": "Create a login page",
  "issue_type": "Story",
  "priority": "High",
  "auto_estimate": true,
  "auto_breakdown": false,
  "auto_assign": false
}
```
4. Click "Execute"
5. Should return a `request_id`

### 3. Test Frontend

1. Go to http://localhost:4200
2. Navigate to "Story Creator"
3. Enter a prompt and generate a story
4. Should see AI-generated content

---

## 📚 Additional Resources

- **LLM Setup:** [LLM_PROVIDERS_GUIDE.md](LLM_PROVIDERS_GUIDE.md)
- **DeepSeek Setup:** [DEEPSEEK_QUICKSTART.md](DEEPSEEK_QUICKSTART.md)
- **Full Setup:** [WINDOWS_FULL_SETUP.md](WINDOWS_FULL_SETUP.md)
- **Troubleshooting:** [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
- **All Docs:** [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)

---

## 🎉 You're All Set!

Your Jira AI Assistant is now running!

**Quick Access:**
- **Application:** http://localhost:4200
- **API Docs:** http://localhost:8000/docs

**Next Steps:**
1. Create your first AI-generated story
2. Explore team capacity management
3. View analytics and insights
4. Configure advanced features

---

## 💡 Tips

1. **Use DeepSeek** for cost-effective AI (10x cheaper than OpenAI)
2. **Keep Docker running** in the background
3. **Check logs** if something doesn't work
4. **Restart services** after changing .env
5. **Use API docs** to test endpoints directly

---

## 🆘 Need Help?

1. Check logs: `docker-compose -f docker-compose.dev.yml logs -f api`
2. Verify .env credentials
3. Restart services
4. Check [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
5. Review error messages in browser console (F12)

---

**Happy automating! 🚀**
