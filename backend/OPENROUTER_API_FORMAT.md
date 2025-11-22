# OpenRouter API Format Guide

## Correct API Format

The OpenRouter API requires using `data=json.dumps()` instead of `json=` parameter. Here's the correct format:

### Python - Correct Format

```python
import requests
import json

response = requests.post(
    url="https://openrouter.io/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer <YOUR_OPENROUTER_API_KEY>",
        "HTTP-Referer": "http://localhost:8000",  # Optional but recommended
        "X-Title": "AI Education System",          # Optional but recommended
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "What is the meaning of life?"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    })
)

print(response.status_code)
print(response.json())
```

### Key Points

1. **Use `data=json.dumps()`** - NOT `json=`
2. **Include `Content-Type: application/json`** header
3. **Include `HTTP-Referer`** header (optional but recommended)
4. **Include `X-Title`** header (optional but recommended)
5. **Model format** - Use model names like `gpt-3.5-turbo`, not `openai/gpt-3.5-turbo`

## Response Format

```json
{
  "id": "gen-...",
  "choices": [
    {
      "message": {
        "content": "The meaning of life is...",
        "role": "assistant"
      },
      "finish_reason": "stop",
      "index": 0
    }
  ],
  "created": 1234567890,
  "model": "gpt-3.5-turbo",
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 50,
    "total_tokens": 70
  }
}
```

## Available Models

### Popular Models

| Model | ID | Speed | Cost | Quality |
|-------|-----|-------|------|---------|
| GPT-3.5 Turbo | `gpt-3.5-turbo` | ⚡⚡⚡ | $ | ⭐⭐⭐ |
| GPT-4 | `gpt-4` | ⚡ | $$$$ | ⭐⭐⭐⭐⭐ |
| Claude 2 | `claude-2` | ⚡⚡ | $$ | ⭐⭐⭐⭐ |
| Llama 2 70B | `meta-llama/llama-2-70b-chat` | ⚡⚡ | $ | ⭐⭐⭐ |
| Mistral 7B | `mistralai/mistral-7b-instruct` | ⚡⚡⚡ | $ | ⭐⭐⭐ |

### Model Selection

- **Fast & Cheap**: `gpt-3.5-turbo`, `mistralai/mistral-7b-instruct`
- **Balanced**: `meta-llama/llama-2-70b-chat`
- **High Quality**: `gpt-4`, `claude-2`

## Request Parameters

### Required Parameters

```python
{
    "model": "gpt-3.5-turbo",           # Model to use
    "messages": [                        # Array of messages
        {
            "role": "system",            # or "user" or "assistant"
            "content": "..."             # Message content
        }
    ]
}
```

### Optional Parameters

```python
{
    "temperature": 0.7,                 # 0.0 to 2.0 (default: 1.0)
                                        # Lower = more deterministic
                                        # Higher = more creative
    
    "max_tokens": 500,                  # Max response length
    
    "top_p": 1.0,                       # Nucleus sampling (0.0 to 1.0)
    
    "frequency_penalty": 0.0,           # -2.0 to 2.0
                                        # Penalize repeated tokens
    
    "presence_penalty": 0.0,            # -2.0 to 2.0
                                        # Penalize new tokens
    
    "stop": ["\\n"],                    # Stop sequences
}
```

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | Success | ✓ Request worked |
| 400 | Bad Request | Check request format |
| 401 | Unauthorized | Check API key |
| 405 | Method Not Allowed | Check API key validity |
| 429 | Rate Limited | Wait and retry |
| 500 | Server Error | OpenRouter issue, retry later |

## Common Issues & Fixes

### Issue 1: Using `json=` instead of `data=json.dumps()`

❌ **Wrong:**
```python
response = requests.post(url, json=payload, headers=headers)
```

✓ **Correct:**
```python
response = requests.post(url, data=json.dumps(payload), headers=headers)
```

### Issue 2: Missing Content-Type Header

❌ **Wrong:**
```python
headers = {
    "Authorization": "Bearer ...",
}
```

✓ **Correct:**
```python
headers = {
    "Authorization": "Bearer ...",
    "Content-Type": "application/json",
}
```

### Issue 3: Invalid Model Name

❌ **Wrong:**
```python
"model": "openai/gpt-3.5-turbo"
```

✓ **Correct:**
```python
"model": "gpt-3.5-turbo"
```

### Issue 4: Invalid API Key

❌ **Wrong:**
```python
"Authorization": "Bearer your-api-key"
```

✓ **Correct:**
```python
"Authorization": "Bearer sk-or-your-actual-key-here"
```

## Testing with cURL

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

## Testing with Postman

1. **Method**: POST
2. **URL**: `https://openrouter.io/api/v1/chat/completions`
3. **Headers**:
   - `Authorization: Bearer sk-or-your-key-here`
   - `Content-Type: application/json`
   - `HTTP-Referer: http://localhost:8000`
   - `X-Title: AI Education System`
4. **Body** (raw JSON):
```json
{
  "model": "gpt-3.5-turbo",
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
  "max_tokens": 100
}
```

## Implementation in Our System

Our AI Education System uses this format in `app/services/ai_service.py`:

```python
def _make_request(self, messages: list, temperature: float = 0.7, max_tokens: int = 500) -> str:
    url = f"{self.base_url}/chat/completions"
    payload = {
        "model": self.model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    
    # Correct format: data=json.dumps()
    response = requests.post(
        url,
        data=json.dumps(payload),
        headers=self.headers,
        timeout=30
    )
    response.raise_for_status()
    
    data = response.json()
    return data["choices"][0]["message"]["content"]
```

## Quick Reference

### Setup
```bash
# 1. Set API key in .env
OPENROUTER_API_KEY=sk-or-your-key-here

# 2. Test connection
python test_openrouter_connection.py

# 3. Start server
uvicorn uvicorn_app:app --reload --port 8000
```

### Test API
```bash
# Chat endpoint
curl -X POST http://localhost:8000/api/education/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is photosynthesis?"}'

# Generate material
curl -X POST http://localhost:8000/api/education/generate-material \
  -H "Content-Type: application/json" \
  -d '{"topic": "Photosynthesis", "level": "beginner"}'
```

## Resources

- OpenRouter Docs: https://openrouter.ai/docs
- OpenRouter Models: https://openrouter.ai/docs#models
- OpenRouter Status: https://status.openrouter.io/
- OpenRouter Support: https://openrouter.ai/support

---

**Key Takeaway**: Always use `data=json.dumps()` with OpenRouter API, not `json=` parameter!
