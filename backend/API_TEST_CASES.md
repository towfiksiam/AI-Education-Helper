# AI Education System - API Test Cases

## Overview
This document contains comprehensive test cases for all API endpoints of the AI Education System backend. Each test case includes request details, expected responses, and validation criteria.

---

## Table of Contents
1. [Health & Status Endpoints](#health--status-endpoints)
2. [Chat Endpoint](#chat-endpoint)
3. [Generate Material Endpoint](#generate-material-endpoint)
4. [Error Handling](#error-handling)
5. [Performance Tests](#performance-tests)

---

## Health & Status Endpoints

### Test Case 1.1: Health Check
**Endpoint:** `GET /health`

**Description:** Verify that the API is running and healthy

**Request:**
```
GET http://localhost:8000/health
```

**Expected Response (200 OK):**
```json
{
  "status": "ok",
  "service": "AI Education System",
  "version": "0.1.0"
}
```

**Validation Criteria:**
- Status code: 200
- Response contains "status" field with value "ok"
- Response contains "service" field
- Response contains "version" field

---

### Test Case 1.2: Root Endpoint
**Endpoint:** `GET /`

**Description:** Get welcome message and API information

**Request:**
```
GET http://localhost:8000/
```

**Expected Response (200 OK):**
```json
{
  "message": "Welcome to AI Education System",
  "version": "0.1.0",
  "docs": "/docs"
}
```

**Validation Criteria:**
- Status code: 200
- Response contains "message" field
- Response contains "version" field
- Response contains "docs" field pointing to documentation

---

### Test Case 1.3: API Documentation
**Endpoint:** `GET /docs`

**Description:** Access interactive API documentation (Swagger UI)

**Request:**
```
GET http://localhost:8000/docs
```

**Expected Response (200 OK):**
- HTML page with Swagger UI interface

**Validation Criteria:**
- Status code: 200
- Content-Type: text/html
- Page contains interactive API documentation

---

### Test Case 1.4: API v1 Health Check
**Endpoint:** `GET /api/v1/health`

**Description:** Check health status of API v1

**Request:**
```
GET http://localhost:8000/api/v1/health
```

**Expected Response (200 OK):**
```json
{
  "status": "ok",
  "service": "AI Education System",
  "version": "0.1.0"
}
```

**Validation Criteria:**
- Status code: 200
- Response contains "status" field with value "ok"
- Response contains "service" field
- Response contains "version" field

---

## Chat Endpoint

### Test Case 2.1: Basic Chat Question
**Endpoint:** `POST /api/education/chat`

**Description:** Ask a simple question without context

**Request:**
```json
{
  "question": "What is photosynthesis?"
}
```

**Expected Response (200 OK):**
```json
{
  "question": "What is photosynthesis?",
  "answer": "Photosynthesis is the process by which plants, algae, and some bacteria convert light energy from the sun into chemical energy stored in glucose...",
  "context": null
}
```

**Validation Criteria:**
- Status code: 200
- Response contains "question" field matching the input
- Response contains "answer" field with non-empty string
- Response contains "context" field (can be null)
- Answer length > 50 characters

---

### Test Case 2.2: Chat with Context
**Endpoint:** `POST /api/education/chat`

**Description:** Ask a question with additional context for better answers

**Request:**
```json
{
  "question": "Explain the light-dependent reactions",
  "context": "In the context of photosynthesis, specifically the process that occurs in the thylakoid membranes of chloroplasts"
}
```

**Expected Response (200 OK):**
```json
{
  "question": "Explain the light-dependent reactions",
  "answer": "The light-dependent reactions are the first stage of photosynthesis that occur in the thylakoid membranes of chloroplasts...",
  "context": "In the context of photosynthesis, specifically the process that occurs in the thylakoid membranes of chloroplasts"
}
```

**Validation Criteria:**
- Status code: 200
- Response contains "question" field
- Response contains "answer" field with non-empty string
- Response contains "context" field matching the input
- Answer is contextually relevant

---

### Test Case 2.3: Long Question
**Endpoint:** `POST /api/education/chat`

**Description:** Test with a longer, more complex question

**Request:**
```json
{
  "question": "Can you explain the complete process of how plants convert sunlight into chemical energy, including all the major steps and the molecules involved?"
}
```

**Expected Response (200 OK):**
```json
{
  "question": "Can you explain the complete process of how plants convert sunlight into chemical energy, including all the major steps and the molecules involved?",
  "answer": "Photosynthesis is a complex process that involves multiple steps and molecules...",
  "context": null
}
```

**Validation Criteria:**
- Status code: 200
- Response contains comprehensive answer
- Answer covers multiple steps of photosynthesis
- Answer mentions key molecules (ATP, NADPH, glucose, etc.)

---

### Test Case 2.4: Empty Question (Validation Error)
**Endpoint:** `POST /api/education/chat`

**Description:** Test validation - empty question should fail

**Request:**
```json
{
  "question": ""
}
```

**Expected Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "question"],
      "msg": "String should have at least 1 character",
      "input": ""
    }
  ]
}
```

**Validation Criteria:**
- Status code: 422
- Response contains "detail" array with validation errors
- Error message indicates minimum length requirement

---

### Test Case 2.5: Missing Question Field (Validation Error)
**Endpoint:** `POST /api/education/chat`

**Description:** Test validation - missing required question field

**Request:**
```json
{
  "context": "Some context"
}
```

**Expected Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "question"],
      "msg": "Field required",
      "input": {"context": "Some context"}
    }
  ]
}
```

**Validation Criteria:**
- Status code: 422
- Response indicates missing required field
- Error specifies "question" field is required

---

### Test Case 2.6: Question Exceeds Max Length (Validation Error)
**Endpoint:** `POST /api/education/chat`

**Description:** Test validation - question exceeds max length (1000 characters)

**Request:**
```json
{
  "question": "This is a very long question that exceeds the maximum allowed length of 1000 characters. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
}
```

**Expected Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "string_too_long",
      "loc": ["body", "question"],
      "msg": "String should have at most 1000 characters",
      "input": "This is a very long question..."
    }
  ]
}
```

**Validation Criteria:**
- Status code: 422
- Response indicates maximum length exceeded
- Error specifies maximum length is 1000 characters

---

### Test Case 2.7: Invalid Content-Type (Error)
**Endpoint:** `POST /api/education/chat`

**Description:** Test with invalid content type

**Request:**
```
Content-Type: text/plain

What is photosynthesis?
```

**Expected Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "json_invalid",
      "loc": ["body"],
      "msg": "Invalid JSON"
    }
  ]
}
```

**Validation Criteria:**
- Status code: 422
- Response indicates JSON parsing error

---

### Test Case 2.8: Special Characters in Question
**Endpoint:** `POST /api/education/chat`

**Description:** Test with special characters and unicode

**Request:**
```json
{
  "question": "What is 光合作用 (photosynthesis in Chinese)? 🌱"
}
```

**Expected Response (200 OK):**
```json
{
  "question": "What is 光合作用 (photosynthesis in Chinese)? 🌱",
  "answer": "Photosynthesis is the process by which plants convert sunlight into chemical energy...",
  "context": null
}
```

**Validation Criteria:**
- Status code: 200
- Special characters are preserved in response
- Answer is generated correctly

---

## Generate Material Endpoint

### Test Case 3.1: Generate Material - Beginner Level
**Endpoint:** `POST /api/education/generate-material`

**Description:** Generate educational material for beginners

**Request:**
```json
{
  "topic": "Photosynthesis",
  "level": "beginner"
}
```

**Expected Response (200 OK):**
```json
{
  "topic": "Photosynthesis",
  "level": "beginner",
  "study_notes": "# Photosynthesis: A Beginner's Guide\n\n## What is Photosynthesis?\nPhotosynthesis is the process by which plants use sunlight to make their own food...",
  "story_explanation": "Imagine a tiny factory inside a plant leaf called a chloroplast...",
  "summary": "Photosynthesis is the process where plants convert sunlight, water, and carbon dioxide into glucose and oxygen...",
  "mcqs": [
    {
      "question": "What is the main purpose of photosynthesis?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A",
      "explanation": "Explanation of why this is correct..."
    }
  ],
  "short_questions": [
    {
      "question": "What are the three main inputs needed for photosynthesis?",
      "expected_answer": "The three main inputs for photosynthesis are sunlight, water, and carbon dioxide...",
      "difficulty": "easy"
    }
  ],
  "image_url": null
}
```

**Validation Criteria:**
- Status code: 200
- Response contains "topic" field matching input
- Response contains "level" field with value "beginner"
- Response contains "study_notes" field with non-empty string
- Response contains "story_explanation" field with non-empty string
- Response contains "summary" field with non-empty string
- Response contains "mcqs" array with at least 1 MCQ
- Each MCQ has "question", "options", "correct_answer", "explanation"
- Response contains "short_questions" array with at least 1 question
- Each short question has "question", "expected_answer", "difficulty"
- Response contains "image_url" field (can be null)

---

### Test Case 3.2: Generate Material - Intermediate Level
**Endpoint:** `POST /api/education/generate-material`

**Description:** Generate educational material for intermediate level

**Request:**
```json
{
  "topic": "Quantum Mechanics",
  "level": "intermediate"
}
```

**Expected Response (200 OK):**
```json
{
  "topic": "Quantum Mechanics",
  "level": "intermediate",
  "study_notes": "# Quantum Mechanics\n\n## Introduction\nQuantum mechanics is the branch of physics that deals with the behavior of matter and energy at the atomic and subatomic scales...",
  "story_explanation": "...",
  "summary": "...",
  "mcqs": [...],
  "short_questions": [...],
  "image_url": null
}
```

**Validation Criteria:**
- Status code: 200
- Response contains "level" field with value "intermediate"
- Study notes are more detailed than beginner level
- Content is appropriate for intermediate learners

---

### Test Case 3.3: Generate Material - Advanced Level
**Endpoint:** `POST /api/education/generate-material`

**Description:** Generate educational material for advanced level

**Request:**
```json
{
  "topic": "Quantum Entanglement",
  "level": "advanced"
}
```

**Expected Response (200 OK):**
```json
{
  "topic": "Quantum Entanglement",
  "level": "advanced",
  "study_notes": "# Quantum Entanglement\n\n## Theoretical Foundation\nQuantum entanglement is a phenomenon where two or more quantum particles become correlated in such a way that the quantum state of each particle cannot be described independently...",
  "story_explanation": "...",
  "summary": "...",
  "mcqs": [...],
  "short_questions": [...],
  "image_url": null
}
```

**Validation Criteria:**
- Status code: 200
- Response contains "level" field with value "advanced"
- Study notes include advanced concepts and mathematical references
- Content is appropriate for advanced learners

---

### Test Case 3.4: Generate Material - Default Level
**Endpoint:** `POST /api/education/generate-material`

**Description:** Generate material with default level (intermediate)

**Request:**
```json
{
  "topic": "Machine Learning"
}
```

**Expected Response (200 OK):**
```json
{
  "topic": "Machine Learning",
  "level": "intermediate",
  "study_notes": "...",
  "story_explanation": "...",
  "summary": "...",
  "mcqs": [...],
  "short_questions": [...],
  "image_url": null
}
```

**Validation Criteria:**
- Status code: 200
- Response contains "level" field with default value "intermediate"
- All required fields are present

---

### Test Case 3.5: Generate Material - With Language
**Endpoint:** `POST /api/education/generate-material`

**Description:** Generate material with specified language

**Request:**
```json
{
  "topic": "Artificial Intelligence",
  "level": "intermediate",
  "language": "english"
}
```

**Expected Response (200 OK):**
```json
{
  "topic": "Artificial Intelligence",
  "level": "intermediate",
  "study_notes": "...",
  "story_explanation": "...",
  "summary": "...",
  "mcqs": [...],
  "short_questions": [...],
  "image_url": null
}
```

**Validation Criteria:**
- Status code: 200
- Content is in specified language
- All required fields are present

---

### Test Case 3.6: Empty Topic (Validation Error)
**Endpoint:** `POST /api/education/generate-material`

**Description:** Test validation - empty topic should fail

**Request:**
```json
{
  "topic": ""
}
```

**Expected Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "topic"],
      "msg": "String should have at least 1 character",
      "input": ""
    }
  ]
}
```

**Validation Criteria:**
- Status code: 422
- Response indicates minimum length requirement

---

### Test Case 3.7: Missing Topic Field (Validation Error)
**Endpoint:** `POST /api/education/generate-material`

**Description:** Test validation - missing required topic field

**Request:**
```json
{
  "level": "intermediate"
}
```

**Expected Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "topic"],
      "msg": "Field required",
      "input": {"level": "intermediate"}
    }
  ]
}
```

**Validation Criteria:**
- Status code: 422
- Response indicates missing required field

---

### Test Case 3.8: Topic Exceeds Max Length (Validation Error)
**Endpoint:** `POST /api/education/generate-material`

**Description:** Test validation - topic exceeds max length (500 characters)

**Request:**
```json
{
  "topic": "This is an extremely long topic that exceeds the maximum allowed length of 500 characters. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit."
}
```

**Expected Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "string_too_long",
      "loc": ["body", "topic"],
      "msg": "String should have at most 500 characters",
      "input": "This is an extremely long topic..."
    }
  ]
}
```

**Validation Criteria:**
- Status code: 422
- Response indicates maximum length exceeded

---

### Test Case 3.9: Invalid Level Value
**Endpoint:** `POST /api/education/generate-material`

**Description:** Test with invalid level value

**Request:**
```json
{
  "topic": "Physics",
  "level": "expert"
}
```

**Expected Response (200 OK):**
```json
{
  "topic": "Physics",
  "level": "expert",
  "study_notes": "...",
  "story_explanation": "...",
  "summary": "...",
  "mcqs": [...],
  "short_questions": [...],
  "image_url": null
}
```

**Validation Criteria:**
- Status code: 200
- System accepts the level value (no strict validation)
- Content is generated based on the provided level

---

### Test Case 3.10: MCQ Structure Validation
**Endpoint:** `POST /api/education/generate-material`

**Description:** Validate MCQ structure in response

**Request:**
```json
{
  "topic": "Biology"
}
```

**Expected Response (200 OK):**
```json
{
  "topic": "Biology",
  "level": "intermediate",
  "study_notes": "...",
  "story_explanation": "...",
  "summary": "...",
  "mcqs": [
    {
      "question": "What is the basic unit of life?",
      "options": ["Atom", "Molecule", "Cell", "Tissue"],
      "correct_answer": "Cell",
      "explanation": "The cell is the basic unit of life..."
    }
  ],
  "short_questions": [...],
  "image_url": null
}
```

**Validation Criteria:**
- Each MCQ has exactly 4 fields: question, options, correct_answer, explanation
- "options" is an array with 4 elements
- "correct_answer" is one of the options
- "question" and "explanation" are non-empty strings

---

### Test Case 3.11: Short Questions Structure Validation
**Endpoint:** `POST /api/education/generate-material`

**Description:** Validate short questions structure in response

**Request:**
```json
{
  "topic": "Chemistry"
}
```

**Expected Response (200 OK):**
```json
{
  "topic": "Chemistry",
  "level": "intermediate",
  "study_notes": "...",
  "story_explanation": "...",
  "summary": "...",
  "mcqs": [...],
  "short_questions": [
    {
      "question": "What is an atom?",
      "expected_answer": "An atom is the smallest unit of matter that retains the properties of an element...",
      "difficulty": "easy"
    }
  ],
  "image_url": null
}
```

**Validation Criteria:**
- Each short question has exactly 3 fields: question, expected_answer, difficulty
- "difficulty" is one of: "easy", "medium", "hard"
- "question" and "expected_answer" are non-empty strings

---

## Error Handling

### Test Case 4.1: API Key Not Configured
**Endpoint:** `POST /api/education/chat`

**Description:** Test when OpenRouter API key is not configured

**Request:**
```json
{
  "question": "What is photosynthesis?"
}
```

**Expected Response (500 Internal Server Error):**
```json
{
  "detail": "OpenRouter API key not configured. Please set OPENROUTER_API_KEY environment variable."
}
```

**Validation Criteria:**
- Status code: 500
- Response contains error message about missing API key

---

### Test Case 4.2: Invalid JSON Format
**Endpoint:** `POST /api/education/chat`

**Description:** Test with malformed JSON

**Request:**
```
{
  "question": "What is photosynthesis?
}
```

**Expected Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "json_invalid",
      "loc": ["body"],
      "msg": "Invalid JSON"
    }
  ]
}
```

**Validation Criteria:**
- Status code: 422
- Response indicates JSON parsing error

---

### Test Case 4.3: Method Not Allowed
**Endpoint:** `GET /api/education/chat`

**Description:** Test with wrong HTTP method

**Request:**
```
GET /api/education/chat
```

**Expected Response (405 Method Not Allowed):**
```json
{
  "detail": "Method Not Allowed"
}
```

**Validation Criteria:**
- Status code: 405
- Response indicates method not allowed

---

### Test Case 4.4: Endpoint Not Found
**Endpoint:** `GET /api/education/nonexistent`

**Description:** Test with non-existent endpoint

**Request:**
```
GET /api/education/nonexistent
```

**Expected Response (404 Not Found):**
```json
{
  "detail": "Not Found"
}
```

**Validation Criteria:**
- Status code: 404
- Response indicates endpoint not found

---

### Test Case 4.5: CORS Preflight Request
**Endpoint:** `OPTIONS /api/education/chat`

**Description:** Test CORS preflight request

**Request:**
```
OPTIONS /api/education/chat
Origin: http://localhost:3000
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type
```

**Expected Response (200 OK):**
```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

**Validation Criteria:**
- Status code: 200
- Response contains CORS headers
- Allowed origin matches request origin

---

## Performance Tests

### Test Case 5.1: Response Time - Chat Endpoint
**Endpoint:** `POST /api/education/chat`

**Description:** Measure response time for chat endpoint

**Request:**
```json
{
  "question": "What is photosynthesis?"
}
```

**Performance Criteria:**
- Response time: < 10 seconds
- Average response time: 2-5 seconds

---

### Test Case 5.2: Response Time - Generate Material Endpoint
**Endpoint:** `POST /api/education/generate-material`

**Description:** Measure response time for material generation

**Request:**
```json
{
  "topic": "Photosynthesis"
}
```

**Performance Criteria:**
- Response time: < 30 seconds
- Average response time: 5-15 seconds

---

### Test Case 5.3: Concurrent Requests
**Endpoint:** `POST /api/education/chat`

**Description:** Test API with concurrent requests

**Test Setup:**
- Send 10 concurrent requests
- Each request asks a different question

**Performance Criteria:**
- All requests complete successfully
- No request times out
- Response times remain consistent

---

### Test Case 5.4: Large Response Handling
**Endpoint:** `POST /api/education/generate-material`

**Description:** Test handling of large responses

**Request:**
```json
{
  "topic": "Comprehensive History of World War II"
}
```

**Performance Criteria:**
- Response is complete and valid JSON
- Response size < 1MB
- No truncation of content

---

## Test Execution Summary

### Quick Test Checklist

- [ ] Health endpoints return 200 OK
- [ ] Chat endpoint accepts questions and returns answers
- [ ] Chat endpoint validates input (empty, too long)
- [ ] Generate material endpoint creates all required content
- [ ] Generate material endpoint supports all difficulty levels
- [ ] Error responses have correct status codes
- [ ] Error responses contain helpful messages
- [ ] CORS headers are present in responses
- [ ] Response times are within acceptable limits
- [ ] Large responses are handled correctly

---

## Notes

- All timestamps should be in ISO 8601 format
- All responses should have Content-Type: application/json
- All error responses should include a "detail" field
- All endpoints should support CORS for frontend integration
- API key must be set in .env file for OpenRouter integration

---

## Environment Setup for Testing

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
copy .env.example .env
# Edit .env and add your OpenRouter API key

# Run the server
uvicorn uvicorn_app:app --reload --port 8000

# Run tests
pytest -v
```

---

## Postman Collection

A Postman collection is provided in `postman_collection.json` with all test cases pre-configured. Import it into Postman to run tests interactively.

**Steps to import:**
1. Open Postman
2. Click "Import" button
3. Select `postman_collection.json`
4. Set the `base_url` variable to `http://localhost:8000`
5. Run the collection

---
