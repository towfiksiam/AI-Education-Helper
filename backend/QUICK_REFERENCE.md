# Quick Reference Card

## ✓ Current Setup

```
Model: Llama 3.3 70B (Free)
Status: ✓ Working
Cost: FREE
Quality: ⭐⭐⭐⭐
```

## 🚀 Start Server

```bash
uvicorn uvicorn_app:app --reload --port 8000
```

## 🧪 Test API

### Health Check
```bash
curl http://localhost:8000/health
```

### Chat
```bash
curl -X POST http://localhost:8000/api/education/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is photosynthesis?"}'
```

### Generate Material
```bash
curl -X POST http://localhost:8000/api/education/generate-material \
  -H "Content-Type: application/json" \
  -d '{"topic": "Photosynthesis", "level": "beginner"}'
```

### API Docs
```
http://localhost:8000/docs
```

## 🔧 Configuration

### File: `.env`

```bash
# Current model (free)
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free

# Alternative models
# OPENROUTER_MODEL=mistralai/mistral-7b-instruct:free
# OPENROUTER_MODEL=meta-llama/llama-3-70b-instruct:free
```

## 📊 Model Comparison

| Model | Speed | Quality | Cost |
|-------|-------|---------|------|
| Llama 3.3 70B | ⚡�� | ⭐⭐⭐⭐ | FREE |
| Mistral 7B | ⚡⚡⚡ | ⭐⭐⭐ | FREE |
| Llama 3 70B | ⚡⚡ | ⭐⭐⭐⭐ | FREE |

## 🧪 Test Scripts

### Test Free Model
```bash
python test_free_model.py
```

### Diagnose Issues
```bash
python diagnose_openrouter.py
```

### Test Connection
```bash
python test_openrouter_connection.py
```

## 📁 Project Structure

```
i:\Job Project\
├── app/
│   ├── core/config.py
│   ├── api/v1/education.py
│   ├── services/ai_service.py
│   └── main.py
├── tests/
├── .env                          # Your config
├── requirements.txt
├── uvicorn_app.py
└── README.md
```

## 🔑 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/v1/health` | GET | API v1 health |
| `/api/education/chat` | POST | Ask questions |
| `/api/education/generate-material` | POST | Generate content |
| `/docs` | GET | API documentation |

## 📝 Request Examples

### Chat Request
```json
{
  "question": "What is photosynthesis?",
  "context": "Optional context"
}
```

### Generate Material Request
```json
{
  "topic": "Photosynthesis",
  "level": "beginner",
  "language": "english"
}
```

## 🎯 Common Tasks

### Change Model
1. Edit `.env`
2. Change `OPENROUTER_MODEL` line
3. Restart server

### Test Different Model
```bash
# Edit .env
OPENROUTER_MODEL=mistralai/mistral-7b-instruct:free

# Restart server
# Test again
```

### View API Docs
```
http://localhost:8000/docs
```

### Run Tests
```bash
pytest -v
```

### Import Postman Collection
1. Open Postman
2. Click Import
3. Select `postman_collection.json`
4. Set `base_url` to `http://localhost:8000`
5. Run tests

## ⚡ Performance

| Task | Time |
|------|------|
| Chat response | 5-10 sec |
| Generate material | 15-30 sec |
| First token | 2-3 sec |

## 🐛 Troubleshooting

### 405 Error?
- Check `.env` has correct model
- Restart server
- Run `python test_free_model.py`

### Slow Response?
- Try `mistralai/mistral-7b-instruct:free`
- Check internet connection
- Try again in a moment

### Model Not Found?
- Check model name spelling
- Visit https://openrouter.ai/docs#models
- Try different model

## 📚 Documentation

| File | Purpose |
|------|---------|
| `README.md` | Full documentation |
| `QUICK_START.md` | 5-minute setup |
| `FREE_MODELS_GUIDE.md` | Free models info |
| `OPENROUTER_SETUP.md` | Setup & troubleshooting |
| `API_TEST_CASES.md` | Test cases |
| `SOLUTION_SUMMARY.md` | This solution |

## 🔗 Links

- OpenRouter: https://openrouter.ai/
- Models: https://openrouter.ai/docs#models
- Status: https://status.openrouter.io/
- Support: https://openrouter.ai/support

## ✅ Checklist

- [ ] `.env` configured with free model
- [ ] Server running on port 8000
- [ ] Health check returns 200
- [ ] Chat endpoint works
- [ ] Generate material works
- [ ] API docs accessible at `/docs`

---

**Everything is ready!** Start the server and enjoy! 🚀
