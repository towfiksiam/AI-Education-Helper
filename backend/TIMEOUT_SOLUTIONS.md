# Timeout Solutions Guide

## Problem
Getting timeout errors when calling OpenRouter API:
```
Read timed out. (read timeout=30)
```

## Root Cause
- Free models are slower during peak hours
- Default timeout (30 seconds) is too short
- API is processing the request but taking longer

## Solution Applied

### 1. Increased Timeout
- **Before**: 30 seconds
- **After**: 120 seconds (2 minutes)

### 2. Added Retry Logic
- Automatically retries up to 3 times
- Waits 5 seconds between retries
- Logs each attempt

### 3. Better Error Handling
- Distinguishes timeout errors from other errors
- Provides helpful logging
- Graceful fallback to default content

## How It Works Now

```python
# Retry logic
for attempt in range(3):
    try:
        # Make request with 120 second timeout
        response = requests.post(..., timeout=120)
        return response
    except Timeout:
        # If timeout, wait 5 seconds and retry
        if attempt < 2:
            time.sleep(5)
            continue
        else:
            raise
```

## Expected Behavior

### First Request (Slow)
```
INFO: API request attempt 1/3
[Wait 5-30 seconds]
✓ Response received
```

### Timeout During Peak Hours
```
INFO: API request attempt 1/3
[Wait 120 seconds]
WARNING: Timeout on attempt 1/3
INFO: Retrying in 5 seconds...
INFO: API request attempt 2/3
[Wait 120 seconds]
✓ Response received
```

## Performance Expectations

### Response Times by Model

| Model | Typical | Peak Hours | Max |
|-------|---------|-----------|-----|
| Llama 3.3 70B | 5-10 sec | 30-60 sec | 120 sec |
| Mistral 7B | 3-5 sec | 15-30 sec | 120 sec |
| Llama 3 70B | 5-10 sec | 30-60 sec | 120 sec |

### When to Expect Timeouts
- Peak hours (evenings, weekends)
- High server load
- Complex requests
- Large max_tokens values

## Optimization Tips

### 1. Reduce Response Length
```python
# Instead of 500 tokens
"max_tokens": 500

# Use 300 tokens
"max_tokens": 300
```

### 2. Use Faster Model
```bash
# Current (slower but better quality)
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free

# Faster alternative
OPENROUTER_MODEL=mistralai/mistral-7b-instruct:free
```

### 3. Simplify Prompts
```python
# Complex prompt (slower)
prompt = """Generate detailed study notes with:
- Headings
- Definitions
- Examples
- Key points
"""

# Simple prompt (faster)
prompt = "Generate study notes for this topic"
```

### 4. Reduce Temperature
```python
# More creative (slower)
"temperature": 0.9

# More deterministic (faster)
"temperature": 0.5
```

## Monitoring Timeouts

### Check Logs
```bash
# Look for timeout messages
ERROR: OpenRouter API timeout after 3 attempts
WARNING: Timeout on attempt 1/3
INFO: Retrying in 5 seconds...
```

### Track Patterns
- Note when timeouts occur
- Identify peak hours
- Adjust strategy accordingly

## Fallback Strategy

If all retries fail, the system returns default content:

```python
# Default MCQ
{
    "question": "What is the main concept?",
    "options": ["A", "B", "C", "D"],
    "correct_answer": "A",
    "explanation": "Default MCQ"
}

# Default short question
{
    "question": "Explain the topic",
    "expected_answer": "Default answer",
    "difficulty": "medium"
}
```

## Testing Timeout Handling

### Test 1: Normal Request
```bash
curl -X POST http://localhost:8000/api/education/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is 2+2?"}'
```

Expected: Response in 5-30 seconds

### Test 2: Complex Request
```bash
curl -X POST http://localhost:8000/api/education/generate-material \
  -H "Content-Type: application/json" \
  -d '{"topic": "Quantum Physics", "level": "advanced"}'
```

Expected: Response in 15-60 seconds (may retry)

### Test 3: During Peak Hours
- Try requests during evening/weekend
- Observe retry behavior
- Check logs for timeout messages

## Configuration Options

### Adjust Timeout (in `app/services/ai_service.py`)

```python
# Current: 120 seconds
timeout = 120

# For faster response (risky)
timeout = 60

# For slower networks
timeout = 180
```

### Adjust Retries (in `app/services/ai_service.py`)

```python
# Current: 3 retries
max_retries = 3

# More retries
max_retries = 5

# Fewer retries
max_retries = 2
```

### Adjust Retry Delay (in `app/services/ai_service.py`)

```python
# Current: 5 seconds
time.sleep(5)

# Shorter delay
time.sleep(2)

# Longer delay
time.sleep(10)
```

## Best Practices

### ✓ Do
- Use reasonable max_tokens (300-500)
- Test during off-peak hours first
- Monitor logs for patterns
- Use faster models for quick responses
- Set realistic expectations

### ✗ Don't
- Set timeout too low (< 60 seconds)
- Use max_tokens > 1000 for free models
- Make too many concurrent requests
- Expect instant responses during peak hours
- Ignore timeout warnings

## Troubleshooting

### Still Getting Timeouts?

1. **Check Model**
   ```bash
   # Try faster model
   OPENROUTER_MODEL=mistralai/mistral-7b-instruct:free
   ```

2. **Reduce Complexity**
   ```bash
   # Shorter max_tokens
   "max_tokens": 200
   ```

3. **Try Off-Peak Hours**
   - Test during morning/afternoon
   - Avoid evenings and weekends

4. **Check Internet**
   ```bash
   ping openrouter.io
   ```

5. **Check OpenRouter Status**
   - Visit https://status.openrouter.io/
   - Look for service issues

### Timeout Still Happening?

1. **Increase Timeout Further**
   - Edit `app/services/ai_service.py`
   - Change `timeout = 120` to `timeout = 180`

2. **Increase Retries**
   - Edit `app/services/ai_service.py`
   - Change `max_retries = 3` to `max_retries = 5`

3. **Use Paid Model**
   - Switch to GPT-3.5 or GPT-4
   - Faster and more reliable
   - Requires credits

## Current Configuration

```
Timeout: 120 seconds
Retries: 3 attempts
Retry Delay: 5 seconds
Model: Llama 3.3 70B (Free)
```

## Next Steps

1. ✓ Restart server to apply changes
2. ✓ Test with simple request first
3. ✓ Monitor logs for timeout messages
4. ✓ Adjust settings if needed
5. ✓ Test during different times

## Support

- OpenRouter Status: https://status.openrouter.io/
- OpenRouter Docs: https://openrouter.ai/docs
- OpenRouter Support: https://openrouter.ai/support

---

**Note**: Timeouts are normal with free models during peak hours. The retry logic should handle most cases automatically.
