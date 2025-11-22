# Getting Started - AI Education System

## 🚀 Quick Start (5 Minutes)

### Step 1: Activate Virtual Environment
```bash
.venv\Scripts\activate
```

### Step 2: Start the Server
```bash
uvicorn uvicorn_app:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Step 3: Test the API
Open a new terminal and run:

```bash
# Health check
curl http://localhost:8000/health

# Chat
curl -X POST http://localhost:8000/api/education/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is photosynthesis?"}'

# Generate material
curl -X POST http://localhost:8000/api/education/generate-material \
  -H "Content-Type: application/json" \
  -d '{"topic": "Photosynthesis", "level": "beginner"}'
```

### Step 4: Access API Documentation
Open your browser and go to:
```
http://localhost:8000/docs
```

You'll see an interactive API documentation where you can test all endpoints!

---

## 📊 System Overview

```
┌─────────────────────────────────────────────────────────┐
│         AI Education System Backend                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  FastAPI Server (Port 8000)                             │
│  ├── /health                    (Health Check)          │
│  ├── /api/v1/health             (API v1 Health)        │
│  ├── /api/education/chat        (Chat Endpoint)        │
│  ├── /api/education/generate-material (Material Gen)   │
│  └── /docs                      (API Documentation)    │
│                                                          │
│  ↓                                                       │
│                                                          │
│  OpenRouter API                                         │
│  ├── Model: Llama 3.3 70B (Free)                       │
│  ├── Timeout: 120 seconds                              │
│  ├── Retries: 3 attempts                               │
│  └── Status: ✓ Working                                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🧪 Testing

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "ok",
  "service": "AI Education System",
  "version": "0.1.0"
}
```

### Test 2: Chat
```bash
curl -X POST http://localhost:8000/api/education/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is 2+2?"}'
```

Expected response:
```json
{
  "question": "What is 2+2?",
  "answer": "2+2 equals 4.",
  "context": null
}
```

### Test 3: Generate Material
```bash
curl -X POST http://localhost:8000/api/education/generate-material \
  -H "Content-Type: application/json" \
  -d '{"topic": "Photosynthesis", "level": "beginner"}'
```

Expected response:
```json
{
  "topic": "Photosynthesis",
  "level": "beginner",
  "study_notes": "...",
  "story_explanation": "...",
  "summary": "...",
  "mcqs": [...],
  "short_questions": [...],
  "image_url": null
}
```

---

## 📁 Project Structure

```
i:\Job Project\
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # Settings
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── routes.py          # Health endpoints
│   │       └── education.py       # Chat & material endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── ai_service.py          # OpenRouter integration
│   └── schemas/
│       ├── __init__.py
│       └── education.py           # Request/response models
├── tests/
│   ├── __init__.py
│   ├── test_health.py
│   ├── test_education.py
│   └── test_comprehensive.py
├── .env                           # Your configuration
├── .env.example                   # Example configuration
├── requirements.txt               # Dependencies
├── uvicorn_app.py                 # Server entrypoint
├── gunicorn_conf.py               # Production config
├── pytest.ini                     # Test configuration
├─��� postman_collection.json        # Postman tests
└── README.md                      # Full documentation
```

---

## 🔧 Configuration

### File: `.env`

```bash
# Application
APP_NAME="AI Education System"
APP_VERSION="0.1.0"
DEBUG=false
LOG_LEVEL=info

# OpenRouter (Free Model)
OPENROUTER_API_KEY=sk-or-your-key-here
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free
OPENROUTER_BASE_URL=https://openrouter.io/api/v1

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

---

## 📚 API Endpoints

### Health Check
```
GET /health
GET /api/v1/health
```

### Chat
```
POST /api/education/chat

Request:
{
  "question": "Your question here?",
  "context": "Optional context"
}

Response:
{
  "question": "Your question here?",
  "answer": "AI-generated answer",
  "context": "Optional context"
}
```

### Generate Material
```
POST /api/education/generate-material

Request:
{
  "topic": "Topic name",
  "level": "beginner|intermediate|advanced",
  "language": "english"
}

Response:
{
  "topic": "Topic name",
  "level": "beginner",
  "study_notes": "...",
  "story_explanation": "...",
  "summary": "...",
  "mcqs": [...],
  "short_questions": [...],
  "image_url": null
}
```

### API Documentation
```
GET /docs
GET /redoc
```

---

## 🧪 Running Tests

### Run All Tests
```bash
pytest -v
```

### Run Specific Test File
```bash
pytest tests/test_education.py -v
```

### Run with Coverage
```bash
pytest --cov=app tests/
```

### Test Free Model
```bash
python test_free_model.py
```

---

## 🐛 Troubleshooting

### Server Won't Start?
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Use different port
uvicorn uvicorn_app:app --port 8001
```

### Timeout Errors?
- This is normal during peak hours
- System will automatically retry
- Check `TIMEOUT_SOLUTIONS.md` for details

### 405 Method Not Allowed?
- Verify `.env` has correct model
- Restart server
- Run `python test_free_model.py`

### Slow Responses?
- Try faster model: `mistralai/mistral-7b-instruct:free`
- Reduce `max_tokens` in requests
- Try during off-peak hours

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| `README.md` | Full documentation |
| `QUICK_START.md` | 5-minute setup |
| `QUICK_REFERENCE.md` | Quick reference |
| `FREE_MODELS_GUIDE.md` | Free models info |
| `TIMEOUT_SOLUTIONS.md` | Timeout handling |
| `FINAL_STATUS.md` | System status |
| `GETTING_STARTED.md` | This file |

---

## 🚀 Next Steps

1. ✓ Start the server
2. ✓ Test the endpoints
3. ✓ Import Postman collection
4. ✓ Run the tests
5. ✓ Deploy to production

---

## 💡 Tips

### Use Postman for Testing
1. Import `postman_collection.json`
2. Set `base_url` to `http://localhost:8000`
3. Run requests interactively

### Monitor Logs
```bash
# Look for INFO, WARNING, ERROR messages
# Helps diagnose issues
```

### Test Different Models
Edit `.env` and change `OPENROUTER_MODEL`:
```bash
# Fast
OPENROUTER_MODEL=mistralai/mistral-7b-instruct:free

# Balanced (current)
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free

# Stable
OPENROUTER_MODEL=meta-llama/llama-3-70b-instruct:free
```

---

## ✅ Checklist

- [ ] Virtual environment activated
- [ ] Server running on port 8000
- [ ] Health check returns 200
- [ ] Chat endpoint works
- [ ] Generate material works
- [ ] API docs accessible
- [ ] Tests pass
- [ ] Postman collection imported

---

## 🎉 You're Ready!

Your AI Education System is fully configured and ready to use!

**Start the server:**
```bash
uvicorn uvicorn_app:app --reload --port 8000
```

**Access the API:**
```
http://localhost:8000/docs
```

**Enjoy!** 🚀

---

## Support

- OpenRouter: https://openrouter.ai/
- FastAPI: https://fastapi.tiangolo.com/
- Uvicorn: https://www.uvicorn.org/

---

**Happy coding!** 💻
