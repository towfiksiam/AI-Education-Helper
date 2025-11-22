# Frontend-Backend Integration Guide

## Project Structure

```
i:\MT\
├── frontend/                    # Next.js Frontend (Port 3000)
│   ├── app/
│   │   ├── page.tsx            # Chat page with AI Q&A
│   │   └── study-materials/    # Study materials generation page
│   ├── components/             # Reusable UI components
│   ├── lib/
│   │   └── api-client.ts       # Backend API client
│   ├── .env.local              # Environment configuration
│   └── package.json
│
└── Job Project/                # FastAPI Backend (Port 8000)
    ├── app/
    │   ├── main.py             # FastAPI application
    │   ├── api/v1/
    │   │   ├── routes.py       # API routes
    │   │   └── education.py    # Education endpoints
    │   ├── services/
    │   │   └── ai_service.py   # AI service (Groq)
    │   ├── schemas/
    │   │   └── education.py    # Data models
    │   └── core/
    │       └── config.py       # Configuration
    ├── .env                    # Backend environment variables
    └── requirements.txt
```

## Setup Instructions

### 1. Backend Setup

Navigate to the backend directory:
```bash
cd "i:\MT\Job Project"
```

Create a Python virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Configure environment variables in `.env`:
```env
APP_NAME="AI Education System"
APP_VERSION="0.1.0"
DEBUG=false
LOG_LEVEL=info
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=mixtral-8x7b-32768
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
```

**Note**: Get your Groq API key from https://console.groq.com/

Start the backend server:
```bash
python -m uvicorn app.main:app --reload --port 8000
```

The backend will be available at: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### 2. Frontend Setup

Navigate to the frontend directory:
```bash
cd "i:\MT\frontend"
```

Install dependencies:
```bash
pnpm install
# or
npm install
```

The `.env.local` file is already configured with the backend URL:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the development server:
```bash
pnpm dev
# or
npm run dev
```

The frontend will be available at: `http://localhost:3000`

## API Integration Details

### API Client (`lib/api-client.ts`)

The frontend uses a centralized API client for all backend communication:

```typescript
import { educationAPI } from "@/lib/api-client";

// Chat endpoint
const response = await educationAPI.chat({
  question: "What is photosynthesis?",
  context: "optional context"
});

// Generate study materials endpoint
const material = await educationAPI.generateMaterial({
  topic: "Photosynthesis",
  level: "intermediate",
  language: "english"
});
```

### Backend Endpoints

#### Health Check
```
GET /health
GET /api/v1/health
```

#### Chat Endpoint
```
POST /api/education/chat
Content-Type: application/json

{
  "question": "What is photosynthesis?",
  "context": "optional context"
}
```

Response:
```json
{
  "question": "What is photosynthesis?",
  "answer": "Photosynthesis is the process by which plants...",
  "context": "optional context"
}
```

#### Generate Material Endpoint
```
POST /api/education/generate-material
Content-Type: application/json

{
  "topic": "Photosynthesis",
  "level": "intermediate",
  "language": "english"
}
```

Response:
```json
{
  "topic": "Photosynthesis",
  "level": "intermediate",
  "study_notes": "...",
  "story_explanation": "...",
  "summary": "...",
  "mcqs": [
    {
      "question": "What is the primary product of photosynthesis?",
      "options": ["Glucose", "Oxygen", "Water", "CO2"],
      "correct_answer": "Glucose",
      "explanation": "..."
    }
  ],
  "short_questions": [
    {
      "question": "Explain the light-dependent reactions",
      "expected_answer": "...",
      "difficulty": "medium"
    }
  ],
  "image_url": null
}
```

## Frontend Features

### 1. Chat Page (`app/page.tsx`)
- Real-time chat interface with AI responses
- Uses backend `/api/education/chat` endpoint
- Features:
  - User and assistant message display
  - Loading state with animation
  - Error handling with user-friendly messages
  - Smooth scrolling to new messages

### 2. Study Materials Page (`app/study-materials/page.tsx`)
- Generate comprehensive study materials on demand
- Uses backend `/api/education/generate-material` endpoint
- Features:
  - Topic input with difficulty level selection
  - Tabbed interface for different content types:
    - Overview (summary + image)
    - Study Notes
    - Story-based Explanation
    - Multiple Choice Questions
    - Short Answer Questions
  - Expandable answers/explanations
  - Loading skeleton animation
  - Error handling

## CORS Configuration

The backend CORS middleware is configured to accept requests from:
- `http://localhost:3000` (Frontend dev server)
- `http://localhost:8000` (Backend)
- `http://127.0.0.1:3000` (Localhost alternative)
- `http://127.0.0.1:8000` (Localhost alternative)

To add more origins, update the `CORS_ORIGINS` environment variable in `.env`:
```env
CORS_ORIGINS=["http://localhost:3000", "http://your-domain.com"]
```

## Environment Variables

### Frontend (.env.local)
```env
# Backend API URL - Change based on environment
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)
```env
# Application Settings
APP_NAME="AI Education System"
APP_VERSION="0.1.0"
DEBUG=false
LOG_LEVEL=info

# AI Service Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=mixtral-8x7b-32768

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
```

## Troubleshooting

### CORS Errors
If you see CORS-related errors in the browser console:
1. Ensure the backend is running on `http://localhost:8000`
2. Check that `NEXT_PUBLIC_API_URL` in frontend `.env.local` matches
3. Verify CORS_ORIGINS in backend `.env` includes the frontend URL

### Connection Refused
If you get "Connection refused" errors:
1. Ensure backend server is running: `python -m uvicorn app.main:app --reload --port 8000`
2. Check that port 8000 is not blocked by firewall
3. Verify frontend `.env.local` has correct API URL

### API Not Found (404)
1. Check backend server logs for errors
2. Visit `http://localhost:8000/docs` to verify endpoints are registered
3. Ensure backend requirements are installed: `pip install -r requirements.txt`

### Missing Groq API Key
1. Get your Groq API key from https://console.groq.com/
2. Add it to backend `.env`: `GROQ_API_KEY=your_key_here`
3. Restart the backend server

## Development Workflow

1. **Terminal 1 - Backend**:
   ```bash
   cd "i:\MT\Job Project"
   .venv\Scripts\activate
   python -m uvicorn app.main:app --reload --port 8000
   ```

2. **Terminal 2 - Frontend**:
   ```bash
   cd "i:\MT\frontend"
   pnpm dev
   ```

3. Open browser and navigate to `http://localhost:3000`

## Production Deployment

For production deployment:

### Backend
- Build: `gunicorn app.main:app --workers 4`
- Environment: Set `DEBUG=false` in `.env`
- Database: Add database configuration if needed

### Frontend
- Build: `pnpm build`
- Start: `pnpm start`
- Update `NEXT_PUBLIC_API_URL` to point to production backend

## Additional Resources

- [Groq Documentation](https://console.groq.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [React Hook Form](https://react-hook-form.com/)
- [Shadcn/ui Components](https://ui.shadcn.com/)
