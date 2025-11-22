# OpenRouter Free Models Guide

## Available Free Models

OpenRouter offers several free models that you can use without credits. These are perfect for testing and development!

### Currently Available Free Models

| Model | ID | Speed | Quality | Use Case |
|-------|-----|-------|---------|----------|
| Llama 3.3 70B | `meta-llama/llama-3.3-70b-instruct:free` | ⚡⚡ | ⭐⭐⭐⭐ | **Recommended** |
| Llama 3 70B | `meta-llama/llama-3-70b-instruct:free` | ⚡⚡ | ⭐⭐⭐⭐ | Good alternative |
| Mistral 7B | `mistralai/mistral-7b-instruct:free` | ⚡⚡⚡ | ⭐⭐⭐ | Fast responses |
| Neural Chat 7B | `intel/neural-chat-7b:free` | ⚡⚡⚡ | ⭐⭐⭐ | Lightweight |

## Setup with Free Model

### 1. Update .env File

```bash
OPENROUTER_API_KEY=sk-or-your-key-here
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free
OPENROUTER_BASE_URL=https://openrouter.io/api/v1
```

### 2. Restart Application

```bash
# Stop current server (Ctrl+C)
# Then restart:
uvicorn uvicorn_app:app --reload --port 8000
```

### 3. Test the API

```bash
curl -X POST http://localhost:8000/api/education/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is photosynthesis?"}'
```

## Why Use Free Models?

✓ **No Credits Required** - Use unlimited requests  
✓ **Good Quality** - Llama 3.3 70B is very capable  
✓ **Fast Enough** - Suitable for most use cases  
✓ **Perfect for Testing** - Develop without worrying about costs  
✓ **Production Ready** - Can be used in production  

## Model Comparison

### Llama 3.3 70B (Recommended)
- **Pros**: Excellent quality, good speed, free
- **Cons**: Slightly slower than smaller models
- **Best for**: Educational content, detailed explanations
- **Model ID**: `meta-llama/llama-3.3-70b-instruct:free`

### Mistral 7B
- **Pros**: Very fast, lightweight, free
- **Cons**: Lower quality than Llama 3.3
- **Best for**: Quick responses, simple queries
- **Model ID**: `mistralai/mistral-7b-instruct:free`

### Llama 3 70B
- **Pros**: Good quality, free, stable
- **Cons**: Slightly older than Llama 3.3
- **Best for**: General purpose, reliable
- **Model ID**: `meta-llama/llama-3-70b-instruct:free`

## Performance Expectations

### Response Times (Approximate)

| Model | First Token | Full Response |
|-------|-------------|---------------|
| Llama 3.3 70B | 2-3 seconds | 5-10 seconds |
| Mistral 7B | 1-2 seconds | 3-5 seconds |
| Llama 3 70B | 2-3 seconds | 5-10 seconds |

### Quality Comparison

| Task | Llama 3.3 | Mistral 7B | Llama 3 |
|------|-----------|-----------|---------|
| Educational Content | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Code Generation | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Reasoning | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Speed | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## Switching Between Models

### Quick Switch

Edit `.env` and change the model:

```bash
# For Llama 3.3 (Recommended)
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free

# For Mistral (Faster)
OPENROUTER_MODEL=mistralai/mistral-7b-instruct:free

# For Llama 3 (Stable)
OPENROUTER_MODEL=meta-llama/llama-3-70b-instruct:free
```

Then restart the server.

## Testing Different Models

Create a test script `test_models.py`:

```python
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.io/api/v1")

models = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "meta-llama/llama-3-70b-instruct:free",
]

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:8000",
    "X-Title": "AI Education System",
}

question = "What is photosynthesis? Answer in 2 sentences."

for model in models:
    print(f"\n{'='*60}")
    print(f"Testing: {model}")
    print(f"{'='*60}")
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": question}
        ],
        "temperature": 0.7,
        "max_tokens": 200,
    }
    
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            data=json.dumps(payload),
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
            print(f"✓ Success!")
            print(f"Answer: {answer}")
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
```

Run it:
```bash
python test_models.py
```

## Limitations of Free Models

⚠️ **Important Notes:**

1. **Rate Limiting** - May have rate limits
2. **Latency** - Slightly higher latency than paid models
3. **Availability** - May be taken down or changed
4. **Quality** - Lower than GPT-4 but still very good
5. **Context Length** - May have shorter context windows

## Upgrading to Paid Models

When you want better performance:

```bash
# GPT-3.5 Turbo (Cheap)
OPENROUTER_MODEL=gpt-3.5-turbo

# GPT-4 (Best quality)
OPENROUTER_MODEL=gpt-4

# Claude 2 (Good for long context)
OPENROUTER_MODEL=claude-2
```

## Troubleshooting Free Models

### Model Not Found Error

**Problem**: `Model not found` error

**Solution**:
1. Check model name spelling
2. Verify model is still available
3. Try a different free model
4. Check OpenRouter docs for latest models

### Rate Limited

**Problem**: Getting 429 errors

**Solution**:
1. Wait a few minutes
2. Reduce request frequency
3. Use a different model
4. Consider upgrading to paid model

### Slow Responses

**Problem**: Responses taking too long

**Solution**:
1. Try Mistral 7B (faster)
2. Reduce max_tokens
3. Check internet connection
4. Try during off-peak hours

## Current Configuration

Your system is configured to use:

```
Model: meta-llama/llama-3.3-70b-instruct:free
Status: ✓ Free and unlimited
Quality: ⭐⭐⭐⭐ Excellent
Speed: ⚡⚡ Good
```

## Next Steps

1. ✓ Restart the server
2. ✓ Test the chat endpoint
3. ✓ Test the generate-material endpoint
4. ✓ Try different models if needed
5. ✓ Monitor performance

## Resources

- OpenRouter Free Models: https://openrouter.ai/docs#models
- Model Benchmarks: https://openrouter.ai/benchmarks
- OpenRouter Status: https://status.openrouter.io/

---

**Enjoy using free models!** 🚀

The Llama 3.3 70B model is excellent for educational content and should work great for your AI Education System.
