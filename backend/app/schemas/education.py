from pydantic import BaseModel, Field
from typing import Optional, List


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    question: str = Field(..., min_length=1, max_length=1000, description="User's question")
    context: Optional[str] = Field(None, max_length=2000, description="Optional context for the question")


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    question: str
    answer: str
    context: Optional[str] = None


class MCQ(BaseModel):
    """Multiple Choice Question model"""
    question: str
    options: List[str] = Field(..., min_items=2, max_items=5)
    correct_answer: str
    explanation: str


class ShortQuestion(BaseModel):
    """Short answer question model"""
    question: str
    expected_answer: str
    difficulty: str = Field(default="medium", description="easy, medium, or hard")


class GenerateMaterialRequest(BaseModel):
    """Request model for generate-material endpoint"""
    topic: str = Field(..., min_length=1, max_length=500, description="Topic for material generation")
    level: Optional[str] = Field(default="intermediate", description="beginner, intermediate, or advanced")
    language: Optional[str] = Field(default="english", description="Language for content generation")


class GenerateMaterialResponse(BaseModel):
    """Response model for generate-material endpoint"""
    topic: str
    level: str
    study_notes: str
    story_explanation: str
    summary: str
    mcqs: List[MCQ]
    short_questions: List[ShortQuestion]
    image_url: Optional[str] = None
