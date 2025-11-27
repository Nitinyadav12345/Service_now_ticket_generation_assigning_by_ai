# LLM Providers Guide

This application supports multiple LLM providers including OpenAI, DeepSeek, and any OpenAI-compatible API.

---

## Supported Providers

### 1. OpenAI (Default)
- **Models:** GPT-4, GPT-4-Turbo, GPT-3.5-Turbo
- **Best for:** Highest quality, most reliable
- **Cost:** ~$0.20-0.50 per story (GPT-4), ~$0.01-0.03 (GPT-3.5)

### 2. DeepSeek ⭐ (Recommended Alternative)
- **Models:** deepseek-chat, deepseek-coder
- **Best for:** Cost-effective, good quality
- **Cost:** ~$0.14 per 1M tokens (much cheaper than OpenAI)

### 3. Local Models (Ollama, LM Studio)
- **Models:** Llama 2, Mistral, CodeLlama, etc.
- **Best for:** Privacy, no API costs, offline usage
- **Cost:** Free (requires local GPU)

### 4. Other OpenAI-Compatible APIs
- Azure OpenAI
- Anthropic Claude (via proxy)
- Together AI
- Anyscale Endpoints
- Any custom OpenAI-compatible endpoint

---

## Configuration

### Option 1: OpenAI (Default)

```env
# Backend/.env
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_API_BASE=
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_TEMPERATURE=0.7
```

**Get API Key:** https://platform.openai.com/api-keys

**Recommended Models:**
- `gpt-4-turbo-preview` - Best quality
- `gpt-4` - High quality, slower
- `gpt-3.5-turbo` - Fast, cheaper

---

### Option 2: DeepSeek ⭐

```env
# Backend/.env
OPENAI_API_KEY=your-deepseek-api-key-here
OPENAI_API_BASE=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_TEMPERATURE=0.7
```

**Get API Key:** https://platform.deepseek.com/api_keys

**Available Models:**
- `deepseek-chat` - General purpose chat model
- `deepseek-coder` - Optimized for code generation

**Pricing:**
- Input: $0.14 per 1M tokens
- Output: $0.28 per 1M tokens
- **~10x cheaper than GPT-4!**

**Performance:**
- Quality: Comparable to GPT-3.5-Turbo, sometimes better
- Speed: Fast response times
- Context: 32K tokens context window

---

### Option 3: Local Models (Ollama)

#### Step 1: Install Ollama
```bash
# Windows/Mac/Linux
# Download from: https://ollama.ai/download

# Or using curl (Linux/Mac):
curl https://ollama.ai/install.sh | sh
```

#### Step 2: Pull a Model
```bash
# Recommended models:
ollama pull llama2          # General purpose
ollama pull mistral         # Fast and capable
ollama pull codellama       # Code-focused
ollama pull deepseek-coder  # DeepSeek local version
```

#### Step 3: Configure
```env
# Backend/.env
OPENAI_API_KEY=not-needed
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_MODEL=llama2
OPENAI_EMBEDDING_MODEL=nomic-embed-text
OPENAI_TEMPERATURE=0.7
```

**Pros:**
- ✅ Free (no API costs)
- ✅ Private (data stays local)
- ✅ Offline usage
- ✅ No rate limits

**Cons:**
- ❌ Requires GPU (recommended)
- ❌ Slower than cloud APIs
- ❌ Lower quality than GPT-4

---

### Option 4: LM Studio

#### Step 1: Install LM Studio
Download from: https://lmstudio.ai/

#### Step 2: Download a Model
- Open LM Studio
- Browse models
- Download: `TheBloke/Mistral-7B-Instruct-v0.2-GGUF` (recommended)

#### Step 3: Start Local Server
- In LM Studio, go to "Local Server"
- Click "Start Server"
- Default port: 1234

#### Step 4: Configure
```env
# Backend/.env
OPENAI_API_KEY=not-needed
OPENAI_API_BASE=http://localhost:1234/v1
OPENAI_MODEL=local-model
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_TEMPERATURE=0.7
```

---

### Option 5: Azure OpenAI

```env
# Backend/.env
OPENAI_API_KEY=your-azure-api-key
OPENAI_API_BASE=https://your-resource.openai.azure.com
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_TEMPERATURE=0.7
```

**Note:** Azure OpenAI requires additional configuration for API version.

---

## Comparison Table

| Provider | Cost/Story | Quality | Speed | Privacy | Setup |
|----------|-----------|---------|-------|---------|-------|
| **OpenAI GPT-4** | $0.20-0.50 | ⭐⭐⭐⭐⭐ | Fast | Cloud | Easy |
| **OpenAI GPT-3.5** | $0.01-0.03 | ⭐⭐⭐⭐ | Very Fast | Cloud | Easy |
| **DeepSeek** | $0.001-0.01 | ⭐⭐⭐⭐ | Fast | Cloud | Easy |
| **Ollama (Local)** | Free | ⭐⭐⭐ | Medium | Local | Medium |
| **LM Studio** | Free | ⭐⭐⭐ | Medium | Local | Easy |
| **Azure OpenAI** | Similar to OpenAI | ⭐⭐⭐⭐⭐ | Fast | Cloud | Complex |

---

## Detailed Setup: DeepSeek

### Step 1: Create DeepSeek Account
1. Go to: https://platform.deepseek.com
2. Sign up with email
3. Verify your email

### Step 2: Get API Key
1. Go to: https://platform.deepseek.com/api_keys
2. Click "Create API Key"
3. Copy the key (starts with `sk-`)

### Step 3: Add Credits (Optional)
1. Go to: https://platform.deepseek.com/top_up
2. Add credits (minimum $5)
3. **Note:** DeepSeek is very cheap, $5 can last months!

### Step 4: Configure Application
Edit `Backend/.env`:
```env
OPENAI_API_KEY=sk-your-deepseek-key-here
OPENAI_API_BASE=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_TEMPERATURE=0.7
```

### Step 5: Test
```bash
# Start backend
cd Backend
python -m uvicorn app.main:app --reload

# Test API
curl -X POST http://localhost:8000/api/prompt/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, can you help me create a story?"}'
```

---

## Detailed Setup: Ollama (Local)

### Step 1: Install Ollama

**Windows:**
1. Download from: https://ollama.ai/download
2. Run installer
3. Ollama will start automatically

**Mac:**
```bash
brew install ollama
ollama serve
```

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

### Step 2: Pull Models
```bash
# Recommended for Jira AI Assistant:
ollama pull mistral        # 7B params, fast, good quality
ollama pull llama2         # 7B params, general purpose
ollama pull codellama      # 7B params, code-focused
ollama pull deepseek-coder # 6.7B params, excellent for code

# Larger models (better quality, slower):
ollama pull llama2:13b
ollama pull mistral:7b-instruct
```

### Step 3: Test Ollama
```bash
# Test the model
ollama run mistral "Write a user story for a login feature"
```

### Step 4: Configure Application
Edit `Backend/.env`:
```env
OPENAI_API_KEY=not-needed
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_MODEL=mistral
OPENAI_EMBEDDING_MODEL=nomic-embed-text
OPENAI_TEMPERATURE=0.7
```

### Step 5: Pull Embedding Model (for RAG)
```bash
ollama pull nomic-embed-text
```

### Step 6: Start Application
```bash
# Ollama should be running (check with: ollama list)
# Start backend
cd Backend
python -m uvicorn app.main:app --reload
```

---

## Model Recommendations

### For Production (Best Quality)
```env
OPENAI_MODEL=gpt-4-turbo-preview
```
- Highest quality
- Best reasoning
- Most reliable
- Cost: ~$0.30 per story

### For Development (Fast & Cheap)
```env
OPENAI_MODEL=gpt-3.5-turbo
```
- Good quality
- Very fast
- Cheap
- Cost: ~$0.02 per story

### For Cost Optimization (Best Value)
```env
OPENAI_API_BASE=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat
```
- Good quality
- Fast
- Very cheap
- Cost: ~$0.001 per story

### For Privacy (Local)
```env
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_MODEL=mistral
```
- Free
- Private
- Offline
- Requires GPU

---

## Troubleshooting

### DeepSeek Issues

**Error: "Invalid API key"**
- Check key starts with `sk-`
- Verify key at: https://platform.deepseek.com/api_keys
- Make sure you have credits

**Error: "Rate limit exceeded"**
- DeepSeek has rate limits
- Wait a few seconds and retry
- Consider upgrading plan

**Error: "Model not found"**
- Use `deepseek-chat` or `deepseek-coder`
- Check model name spelling

### Ollama Issues

**Error: "Connection refused"**
- Make sure Ollama is running: `ollama serve`
- Check port 11434 is not blocked
- Try: `curl http://localhost:11434/api/tags`

**Error: "Model not found"**
- Pull the model first: `ollama pull mistral`
- List available models: `ollama list`
- Use exact model name from list

**Slow responses**
- Use smaller models (7B instead of 13B)
- Ensure GPU is being used
- Close other GPU-intensive apps

### General Issues

**Error: "JSON decode error"**
- Some models don't format JSON well
- The app has fallback JSON extraction
- Try different model or temperature

**Poor quality responses**
- Increase model size (e.g., llama2:13b)
- Adjust temperature (try 0.5-0.9)
- Use better model (GPT-4, DeepSeek)

---

## Cost Comparison (100 Stories/Month)

| Provider | Model | Cost |
|----------|-------|------|
| OpenAI | GPT-4 | ~$30-50 |
| OpenAI | GPT-3.5-Turbo | ~$2-3 |
| DeepSeek | deepseek-chat | ~$0.10-0.50 |
| Ollama | Local | $0 (electricity) |
| LM Studio | Local | $0 (electricity) |

---

## Performance Comparison

### Story Generation Quality
1. **GPT-4** - ⭐⭐⭐⭐⭐ (Best)
2. **DeepSeek** - ⭐⭐⭐⭐ (Very Good)
3. **GPT-3.5** - ⭐⭐⭐⭐ (Good)
4. **Mistral (Local)** - ⭐⭐⭐ (Decent)
5. **Llama2 (Local)** - ⭐⭐⭐ (Decent)

### Response Speed
1. **GPT-3.5** - ⭐⭐⭐⭐⭐ (Fastest)
2. **DeepSeek** - ⭐⭐⭐⭐⭐ (Very Fast)
3. **GPT-4** - ⭐⭐⭐⭐ (Fast)
4. **Ollama** - ⭐⭐⭐ (Medium, depends on GPU)
5. **LM Studio** - ⭐⭐⭐ (Medium, depends on GPU)

---

## Switching Providers

You can easily switch between providers by changing the `.env` file:

```bash
# Stop backend (Ctrl+C)

# Edit Backend/.env with new provider settings

# Restart backend
cd Backend
python -m uvicorn app.main:app --reload
```

No code changes needed!

---

## Best Practices

### 1. Start with DeepSeek
- Great quality/cost ratio
- Easy to set up
- Very affordable

### 2. Use GPT-4 for Production
- When quality is critical
- For customer-facing features
- When budget allows

### 3. Use Local Models for Development
- When testing features
- For privacy-sensitive data
- When offline

### 4. Monitor Costs
- Check API usage regularly
- Set up billing alerts
- Use cheaper models for testing

---

## FAQ

**Q: Can I use multiple providers?**
A: Not simultaneously, but you can switch by changing `.env`

**Q: Which is the best value?**
A: DeepSeek offers the best quality/cost ratio

**Q: Do I need a GPU for local models?**
A: Recommended but not required. CPU works but is slower.

**Q: Can I use Anthropic Claude?**
A: Yes, via an OpenAI-compatible proxy

**Q: Is my data private with cloud providers?**
A: Check each provider's privacy policy. Use local models for maximum privacy.

**Q: How do I know which model to use?**
A: Start with DeepSeek, upgrade to GPT-4 if needed

---

## Support

For provider-specific issues:
- **OpenAI:** https://help.openai.com
- **DeepSeek:** https://platform.deepseek.com/docs
- **Ollama:** https://github.com/ollama/ollama/issues
- **LM Studio:** https://lmstudio.ai/docs

---

**Ready to use DeepSeek? Update your `Backend/.env` and restart the backend!**
