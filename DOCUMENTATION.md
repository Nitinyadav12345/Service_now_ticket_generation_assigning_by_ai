# Documentation Index

## 📚 Main Documentation

### Essential Guides
1. **[README.md](README.md)** ⭐ - Start here! Complete project overview
   - Quick start guide
   - Team sync from Jira
   - Skills management
   - Database management
   - Troubleshooting

2. **[RUN_APPLICATION.md](RUN_APPLICATION.md)** - Detailed run instructions
   - Step-by-step setup
   - Docker commands
   - Service URLs

3. **[LLM_PROVIDERS_GUIDE.md](LLM_PROVIDERS_GUIDE.md)** - LLM configuration
   - DeepSeek setup (recommended)
   - OpenAI setup
   - Local models
   - Cost comparison

### Requirements
4. **[Jira AI Assistant - Requirements Document.md](Jira AI Assistant - Requirements Document.md)** - Original requirements

## 🎯 Quick Links

### Getting Started
- **First time?** → Read [README.md](README.md) Quick Start section
- **Need to run?** → See [RUN_APPLICATION.md](RUN_APPLICATION.md)
- **Configure LLM?** → Check [LLM_PROVIDERS_GUIDE.md](LLM_PROVIDERS_GUIDE.md)

### Common Tasks
- **Sync team from Jira** → README.md → Team Sync section
- **Add skills** → README.md → Skills Management section
- **Reset database** → README.md → Database Management section
- **Troubleshoot** → README.md → Troubleshooting section

## 📁 Backend Documentation
- **[Backend/README.md](Backend/README.md)** - Backend overview
- **[Backend/BACKEND_SETUP.md](Backend/BACKEND_SETUP.md)** - Backend setup details

## 🎨 Frontend Documentation
- **[jira-ai-frontend/UI_SETUP.md](jira-ai-frontend/UI_SETUP.md)** - Frontend setup
- **[jira-ai-frontend/TERMINOLOGY_UPDATE.md](jira-ai-frontend/TERMINOLOGY_UPDATE.md)** - UI terminology

## 🚀 Quick Commands

### Start Application
```bash
# Windows
start-dev.bat

# Linux/Mac
./start-dev.sh
```

### Recreate Database
```bash
cd Backend
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d
```

### Check Status
```bash
# Health check
curl http://localhost:8000/api/health

# View logs
docker-compose -f Backend/docker-compose.dev.yml logs -f api
```

## 📞 Need Help?

1. Check [README.md](README.md) Troubleshooting section
2. Review [RUN_APPLICATION.md](RUN_APPLICATION.md)
3. Check backend logs
4. Verify environment variables in `.env`

---

**All documentation is now consolidated in README.md for easy access!**
