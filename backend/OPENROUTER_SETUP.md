# OpenRouter API Setup & Troubleshooting Guide

## Overview
This guide helps you set up and troubleshoot the OpenRouter API integration for the AI Education System.

## Prerequisites
- OpenRouter account (https://openrouter.ai/)
- Valid API key from OpenRouter
- Python 3.8+

## Setup Steps

### 1. Get Your OpenRouter API Key

1. Visit https://openrouter.ai/
2. Sign up or log in to your account
3. Go to your account settings/dashboard
4. Find the API Keys section
5. Create a new API key or copy your existing one
6. Copy the key (it will look like: `sk-or-...`)

### 2. Configure Environment Variables

Create or update your `.env` file:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenRouter API key
OPENROUTER_API_KEY=sk-or-your-actual-key-here
OPENROUTER_MODEL=gpt-3.5-turbo
OPENROUTER_BASE_URL=https://openrouter.io/api/v1
```

### 3. Verify Configuration

Run the test script to verify your setup:

```bash
python test_openrouter_connection.py
```

## Available Models

OpenRouter supports many models. Here are some popular ones:

| Model | ID | Notes |
|-------|-----|-------|
| GPT-3.5 Turbo | `gpt-3.5-turbo` | Fast, cost-effective |
| GPT-4 | `gpt-4` | More powerful, higher cost |
| Claude 2 | `claude-2` | Good for long context |
| Llama 2 | `meta-llama/llama-2-70b-chat` | Open source |
| Mistral | `mistralai/mistral-7b-instruct` | Fast, efficient |

To use a different model, update your `.env`:

```bash
OPENROUTER_MODEL=meta-llama/llama-2-70b-chat
```

## Common Issues & Solutions

### Issue 1: 405 Method Not Allowed

**Error:**
```
ERROR:app.services.ai_service:OpenRouter API error: 405 Client Error: Method Not Allowed for url: https://openrouter.io/api/v1/chat/completions
```

**Causes:**
- Invalid API key
- API key doesn't have permission
- Incorrect endpoint URL

**Solutions:**
1. Verify your API key is correct in `.env`
2. Check that your OpenRouter account is active
3. Ensure you have credits/balance in your OpenRouter account
4. Try the test script: `python test_openrouter_connection.py`

### Issue 2: 401 Unauthorized

**Error:**
```
ERROR:app.services.ai_service:OpenRouter API error: 401 Client Error: Unauthorized
```

**Causes:**
- Invalid or expired API key
- API key not set in environment

**Solutions:**
1. Verify your API key in `.env` is correct
2. Check that the key hasn't expired
3. Generate a new API key from OpenRouter dashboard
4. Restart the application after updating `.env`

### Issue 3: 429 Rate Limited

**Error:**
```
ERROR:app.services.ai_service:OpenRouter API error: 429 Client Error: Too Many Requests
```

**Causes:**
- Too many requests in a short time
- Rate limit exceeded

**Solutions:**
1. Wait a few minutes before retrying
2. Check your OpenRouter usage dashboard
3. Implement request throttling in your application
4. Consider upgrading your OpenRouter plan

### Issue 4: 500 Internal Server Error from OpenRouter

**Error:**
```
ERROR:app.services.ai_service:OpenRouter API error: 500 Server Error
```

**Causes:**
- OpenRouter service temporarily down
- Invalid request format

**Solutions:**
1. Wait a few minutes and retry
2. Check OpenRouter status page
3. Verify your request format is correct
4. Check application logs for more details

### Issue 5: Timeout Error

**Error:**
```
ERROR:app.services.ai_service:OpenRouter API error: ConnectTimeout
```

**Causes:**
- Network connectivity issue
- OpenRouter service slow
- Request taking too long

**Solutions:**
1. Check your internet connection
2. Try again after a few seconds
3. Check OpenRouter status
4. Increase timeout in code if needed

## Testing Your Setup

### Quick Test with cURL

```bash
curl -X POST "https://openrouter.io/api/v1/chat/completions" \
  -H "Authorization: Bearer sk-or-your-key-here" \
  -H "Content-Type: application/json" \
  -H "HTTP-Referer: http://localhost:8000" \
  -H "X-Title: AI Education System" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

### Test with Python Script

Create `test_openrouter_connection.py`:

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
model = os.getenv("OPENROUTER_MODEL", "gpt-3.5-turbo")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.io/api/v1")

if not api_key:
    print("ERROR: OPENROUTER_API_KEY not set in .env")
    exit(1)

print(f"Testing OpenRouter API...")
print(f"API Key: {api_key[:20]}...")
print(f"Model: {model}")
print(f"Base URL: {base_url}")
print()

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:8000",
    "X-Title": "AI Education System",
}

payload = {
    "model": model,
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "What is 2+2?"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 100,
}

try:
    print("Sending request to OpenRouter...")
    response = requests.post(
        f"{base_url}/chat/completions",
        json=payload,
        headers=headers,
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        print(f"✓ SUCCESS!")
        print(f"Answer: {answer}")
    else:
        print(f"✗ ERROR: {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.Timeout:
    print("✗ ERROR: Request timeout")
except requests.exceptions.ConnectionError:
    print("✗ ERROR: Connection error")
except Exception as e:
    print(f"✗ ERROR: {str(e)}")
```

Run it:
```bash
python test_openrouter_connection.py
```

## Debugging Steps

### Step 1: Check Environment Variables

```bash
# On Windows (cmd)
echo %OPENROUTER_API_KEY%

# On macOS/Linux
echo $OPENROUTER_API_KEY
```

### Step 2: Check Application Logs

Look for detailed error messages in the application output:

```
ERROR:app.services.ai_service:OpenRouter API error: [detailed error message]
```

### Step 3: Enable Debug Logging

Update your `.env`:

```bash
DEBUG=true
LOG_LEVEL=debug
```

### Step 4: Test with Postman

1. Open Postman
2. Create a new POST request
3. URL: `https://openrouter.io/api/v1/chat/completions`
4. Headers:
   - `Authorization: Bearer sk-or-your-key-here`
   - `Content-Type: application/json`
   - `HTTP-Referer: http://localhost:8000`
   - `X-Title: AI Education System`
5. Body (raw JSON):
```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {"role": "user", "content": "Hello"}
  ]
}
```
6. Send and check response

## API Key Security

⚠️ **Important Security Notes:**

1. **Never commit `.env` file** to version control
2. **Never share your API key** publicly
3. **Rotate keys regularly** for security
4. **Use environment variables** for sensitive data
5. **Monitor API usage** for unauthorized access

## Monitoring & Costs

### Check Your Usage

1. Log in to OpenRouter dashboard
2. Go to "Usage" or "Billing" section
3. View your API calls and costs
4. Set spending limits if available

### Cost Estimation

Costs vary by model. Check OpenRouter pricing page for current rates.

Example (approximate):
- GPT-3.5 Turbo: ~$0.0005 per 1K tokens
- GPT-4: ~$0.03 per 1K tokens
- Llama 2: ~$0.0001 per 1K tokens

## Support

- OpenRouter Documentation: https://openrouter.ai/docs
- OpenRouter Status: https://status.openrouter.ai/
- OpenRouter Support: https://openrouter.ai/support

## Next Steps

1. ✓ Set up your API key
2. ✓ Test the connection
3. ✓ Run the application
4. ✓ Test the endpoints

```bash
# Start the server
uvicorn uvicorn_app:app --reload --port 8000

# Test in another terminal
curl -X POST http://localhost:8000/api/education/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is photosynthesis?"}'
```

---

For more help, check the main README.md or contact OpenRouter support.
