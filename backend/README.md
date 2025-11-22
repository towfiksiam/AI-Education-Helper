# AI-Powered Education System Backend

A production-ready FastAPI backend for an AI-powered education platform. Provides intelligent content generation, chat-based Q&A, and comprehensive educational material creation using OpenRouter's API (supports multiple AI models).

## Overview

- **FastAPI** framework for high-performance async APIs
- **OpenRouter Integration** for AI-powered content generation (supports multiple models)
- **CORS Middleware** for frontend integration
- **Pydantic Models** for request/response validation
- **Comprehensive Logging** for debugging and monitoring
- **Unit Tests** with pytest
- **Production-Ready** configuration with Gunicorn

## Project Structure

```
app/
├── core/
│   └── config.py              # Settings management (environment variables)
├── api/
│   └── v1/
│       ├── routes.py          # Basic health check routes
│       └── education.py       # Education endpoints (chat, generate-material)
├── services/
│   └── ai_service.py          # OpenAI API integration and content generation
├── schemas/
│   └── education.py           # Pydantic models for requests/responses
└── main.py                    # FastAPI app factory with CORS middleware

tests/
├── test_health.py             # Health endpoint tests
└── test_education.py          # Education endpoint tests

.env.example                   # Example environment variables
requirements.txt               # Python dependencies
uvicorn_app.py                 # Development server entrypoint
gunicorn_conf.py               # Production server configuration
README.md                      # This file
```

## Features

### 1. Chat Endpoint (`/api/education/chat`)
- **POST** request with a question
- Optional context parameter for better answers
- Returns AI-generated answer using GPT-3.5-turbo
- Request validation with Pydantic

### 2. Generate Material Endpoint (`/api/education/generate-material`)
- **POST** request with a topic
- Generates comprehensive educational content:
  - **Study Notes**: Detailed, structured notes with key concepts
  - **Story Explanation**: Engaging narrative explanation
  - **Summary**: Concise overview of the topic
  - **MCQs**: Multiple choice questions with explanations
  - **Short Questions**: Short answer questions with expected answers
  - **Image URL**: Optional AI-generated image (DALL-E)
- Configurable difficulty levels: beginner, intermediate, advanced

## Getting Started

### Prerequisites
- Python 3.8+
- OpenRouter API key (get from https://openrouter.ai/)

### Installation

1. **Create and activate a virtual environment**
   ```bash
   # Windows (cmd)
   python -m venv .venv
   .venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Copy example to .env
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   
   # Edit .env and add your OpenRouter API key
   OPENROUTER_API_KEY=your-openrouter-api-key-here
   OPENROUTER_MODEL=gpt-3.5-turbo  # or any other supported model
   ```

### Running the Application

**Development (with hot-reload)**
```bash
uvicorn uvicorn_app:app --reload --port 8000
```

**Production (with Gunicorn)**
```bash
# Linux/macOS only
gunicorn -c gunicorn_conf.py uvicorn_app:app
```

**Access the API**
- API Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## API Endpoints

### 1. Chat Endpoint
**POST** `/api/education/chat`

Request:
```json
{
  "question": "What is photosynthesis?",
  "context": "In the context of biology..."  // optional
}
```

Response:
```json
{
  "question": "What is photosynthesis?",
  "answer": "Photosynthesis is the process by which plants...",
  "context": "In the context of biology..."
}
```

### 2. Generate Material Endpoint
**POST** `/api/education/generate-material`

Request:
```json
{
  "topic": "Photosynthesis",
  "level": "intermediate",  // optional: beginner, intermediate, advanced
  "language": "english"     // optional
}
```

Response:
```json
{
  "topic": "Photosynthesis",
  "level": "intermediate",
  "study_notes": "Detailed study notes...",
  "story_explanation": "An engaging story about photosynthesis...",
  "summary": "Concise summary...",
  "mcqs": [
    {
      "question": "What is the primary function of chlorophyll?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A",
      "explanation": "Explanation of why this is correct..."
    }
  ],
  "short_questions": [
    {
      "question": "Explain the light-dependent reactions.",
      "expected_answer": "Expected answer...",
      "difficulty": "medium"
    }
  ],
  "image_url": "https://example.com/image.jpg"  // optional
}
```

### 3. Health Check
**GET** `/api/v1/health`

Response:
```json
{
  "status": "ok",
  "service": "AI Education System",
  "version": "0.1.0"
}
```

## Configuration

Environment variables (in `.env` file):

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | AI Education System | Application name |
| `APP_VERSION` | 0.1.0 | Application version |
| `DEBUG` | false | Enable debug mode |
| `LOG_LEVEL` | info | Logging level |
| `OPENROUTER_API_KEY` | (required) | OpenRouter API key |
| `OPENROUTER_MODEL` | gpt-3.5-turbo | Model to use (see OpenRouter docs for available models) |
| `OPENROUTER_BASE_URL` | https://openrouter.io/api/v1 | OpenRouter API base URL |
| `CORS_ORIGINS` | ["http://localhost:3000", "http://localhost:8080"] | Allowed CORS origins |

## Testing

Run all tests:
```bash
pytest -v
```

Run specific test file:
```bash
pytest tests/test_education.py -v
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## Error Handling

The API includes comprehensive error handling:
- **422 Unprocessable Entity**: Invalid request data
- **500 Internal Server Error**: Server-side errors (e.g., OpenRouter API issues)
- **Detailed error messages** in response body

## Security Notes

- **Never commit `.env` file** with real API keys
- Use environment variables for sensitive data
- CORS is configured to allow specific origins
- Input validation is enforced via Pydantic models
- API keys should be rotated regularly

## Performance Considerations

- OpenRouter API calls may take 2-10 seconds depending on content length and model
- Consider implementing caching for frequently requested topics
- Use async/await for non-blocking operations
- Monitor API usage and costs on OpenRouter dashboard

## Extending the Application

### Adding a New Endpoint

1. Create a new route in `app/api/v1/education.py`:
```python
@router.get("/new-endpoint")
async def new_endpoint():
    return {"message": "New endpoint"}
```

2. Add corresponding Pydantic models in `app/schemas/education.py`

3. Add tests in `tests/test_education.py`

### Adding a New AI Service Method

1. Add method to `AIEducationService` in `app/services/ai_service.py`
2. Use the existing pattern with error handling
3. Add tests for the new method

### Changing the AI Model

To use a different model from OpenRouter:

1. Update `.env`:
   ```
   OPENROUTER_MODEL=meta-llama/llama-2-70b-chat
   ```

2. Available models: https://openrouter.ai/docs#models

## Troubleshooting

**"OpenRouter API key not configured"**
- Ensure `OPENROUTER_API_KEY` is set in `.env` file
- Verify the API key is valid at https://openrouter.ai/

**"Rate limit exceeded"**
- OpenRouter has rate limits; wait before retrying
- Check your usage at https://openrouter.ai/account/usage

**"Model not found"**
- Verify the model name in `OPENROUTER_MODEL` is correct
- Check available models at https://openrouter.ai/docs#models

**CORS errors**
- Add your frontend URL to `CORS_ORIGINS` in `.env`
- Format: `["http://localhost:3000", "http://example.com"]`

## Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **requests**: HTTP client for OpenRouter API
- **pydantic**: Data validation
- **python-dotenv**: Environment variable management
- **pytest**: Testing framework
- **gunicorn**: Production WSGI/ASGI server

## License

MIT

## Support

For issues or questions, please refer to the FastAPI documentation: https://fastapi.tiangolo.com/
