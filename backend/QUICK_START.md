# Quick Start Guide - AI Education System

## 5-Minute Setup

### 1. Get OpenRouter API Key (2 minutes)
```
1. Go to https://openrouter.ai/
2. Sign up or log in
3. Copy your API key (looks like: sk-or-...)
```

### 2. Configure Environment (1 minute)
```bash
# Copy example config
copy .env.example .env

# Edit .env and add your key
OPENROUTER_API_KEY=sk-or-your-key-here
```

### 3. Install & Run (2 minutes)
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test OpenRouter connection
python test_openrouter_connection.py

# Start server
uvicorn uvicorn_app:app --reload --port 8000
```

### 4. Test API
```bash
# In another terminal
curl -X POST http://localhost:8000/api/education/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is photosynthesis?"}'
```

## Common Issues

### 405 Method Not Allowed
**Problem:** API key is invalid or doesn't have permission

**Solution:**
1. Check your API key in `.env`
2. Run: `python test_openrouter_connection.py`
3. Verify your OpenRouter account is active
4. Check you have credits in your account

### 401 Unauthorized
**Problem:** API key is missing or expired

**Solution:**
1. Verify API key is in `.env`
2. Generate a new key from OpenRouter dashboard
3. Restart the application

### Connection Timeout
**Problem:** Request is taking too long

**Solution:**
1. Check internet connection
2. Try again in a few seconds
3. Check OpenRouter status page

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Chat
```bash
curl -X POST http://localhost:8000/api/education/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Your question here?"}'
```

### Generate Material
```bash
curl -X POST http://localhost:8000/api/education/generate-material \
  -H "Content-Type: application/json" \
  -d '{"topic": "Photosynthesis", "level": "beginner"}'
```

### API Documentation
```
http://localhost:8000/docs
```

## File Structure
```
i:\Job Project\
├── app/
│   ├── core/config.py          # Settings
│   ├── api/v1/education.py     # API endpoints
│   ├── services/ai_service.py  # OpenRouter integration
│   └── main.py                 # FastAPI app
├── tests/                       # Test files
├── .env                         # Your configuration (create from .env.example)
├── requirements.txt             # Dependencies
├── test_openrouter_connection.py # Connection test
└── README.md                    # Full documentation
```

## Next Steps

1. ✓ Set up API key
2. ✓ Run `test_openrouter_connection.py`
3. ✓ Start the server
4. ✓ Test endpoints
5. ✓ Check `/docs` for interactive API docs
6. ✓ Import `postman_collection.json` into Postman for testing

## Support

- **Setup Issues:** See `OPENROUTER_SETUP.md`
- **API Documentation:** See `README.md`
- **Test Cases:** See `API_TEST_CASES.md`
- **OpenRouter Help:** https://openrouter.ai/docs

## Troubleshooting

### Step 1: Test Connection
```bash
python test_openrouter_connection.py
```

### Step 2: Check Logs
Look for error messages in the terminal output

### Step 3: Verify Configuration
```bash
# Check if .env file exists
dir .env

# Check if API key is set
echo %OPENROUTER_API_KEY%
```

### Step 4: Test with Postman
1. Import `postman_collection.json`
2. Set `base_url` to `http://localhost:8000`
3. Run a test request

## Models Available

Change the model in `.env`:

```bash
# Fast and cheap
OPENROUTER_MODEL=gpt-3.5-turbo

# More powerful
OPENROUTER_MODEL=gpt-4

# Open source
OPENROUTER_MODEL=meta-llama/llama-2-70b-chat

# Fast and efficient
OPENROUTER_MODEL=mistralai/mistral-7b-instruct
```

See https://openrouter.ai/docs#models for all available models.

## Performance Tips

1. **Use gpt-3.5-turbo** for faster responses
2. **Reduce max_tokens** for shorter responses
3. **Batch requests** if possible
4. **Monitor usage** on OpenRouter dashboard

## Security Reminders

⚠️ **Important:**
- Never commit `.env` to git
- Never share your API key
- Rotate keys regularly
- Monitor API usage

---

**Ready to go!** Start the server and visit http://localhost:8000/docs
