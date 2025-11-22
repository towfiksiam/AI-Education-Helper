"""
Education API routes for AI-powered learning endpoints.
Includes chat and material generation endpoints.
"""

import logging
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.education import (
    ChatRequest,
    ChatResponse,
    GenerateMaterialRequest,
    GenerateMaterialResponse,
)
from app.services.ai_service import AIEducationService
from app.core.config import get_settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/education", tags=["education"])


def get_ai_service() -> AIEducationService:
    """Dependency to get AI service instance"""
    settings = get_settings()
    if not settings.groq_api_key:
        raise HTTPException(
            status_code=500,
            detail="Groq API key not configured. Please set GROQ_API_KEY environment variable.",
        )
    return AIEducationService(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, ai_service: AIEducationService = Depends(get_ai_service)):
    """
    Chat endpoint for answering user questions.
    
    Args:
        request: ChatRequest containing question and optional context
        ai_service: AI service dependency
        
    Returns:
        ChatResponse with the AI-generated answer
    """
    try:
        logger.info(f"Processing chat request: {request.question[:50]}...")
        answer = ai_service.chat(request.question, request.context)
        return ChatResponse(
            question=request.question,
            answer=answer,
            context=request.context,
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")


@router.post("/generate-material", response_model=GenerateMaterialResponse)
async def generate_material(
    request: GenerateMaterialRequest,
    ai_service: AIEducationService = Depends(get_ai_service),
):
    """
    Generate comprehensive educational material for a topic.
    
    Generates:
    - Study notes
    - Story-based explanation
    - Summary
    - Multiple choice questions
    - Short answer questions
    - Optional: AI-generated image
    
    Args:
        request: GenerateMaterialRequest containing topic and optional level
        ai_service: AI service dependency
        
    Returns:
        GenerateMaterialResponse with all generated content
    """
    try:
        logger.info(f"Generating material for topic: {request.topic}")

        # Generate all content in parallel (conceptually)
        study_notes = ai_service.generate_study_notes(request.topic, request.level)
        story_explanation = ai_service.generate_story_explanation(request.topic)
        summary = ai_service.generate_summary(request.topic)
        mcqs = ai_service.generate_mcqs(request.topic, count=3)
        short_questions = ai_service.generate_short_questions(request.topic, count=3)
        image_url = ai_service.generate_image_url(request.topic)

        # Convert MCQs and short questions to proper models
        from app.schemas.education import MCQ, ShortQuestion

        mcq_objects = []
        for mcq in mcqs:
            try:
                mcq_objects.append(
                    MCQ(
                        question=mcq.get("question", ""),
                        options=mcq.get("options", []),
                        correct_answer=mcq.get("correct_answer", ""),
                        explanation=mcq.get("explanation", ""),
                    )
                )
            except Exception as e:
                logger.warning(f"Error parsing MCQ: {str(e)}")

        short_question_objects = []
        for sq in short_questions:
            try:
                short_question_objects.append(
                    ShortQuestion(
                        question=sq.get("question", ""),
                        expected_answer=sq.get("expected_answer", ""),
                        difficulty=sq.get("difficulty", "medium"),
                    )
                )
            except Exception as e:
                logger.warning(f"Error parsing short question: {str(e)}")

        return GenerateMaterialResponse(
            topic=request.topic,
            level=request.level,
            study_notes=study_notes,
            story_explanation=story_explanation,
            summary=summary,
            mcqs=mcq_objects,
            short_questions=short_question_objects,
            image_url=image_url,
        )
    except Exception as e:
        logger.error(f"Error generating material: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating educational material: {str(e)}",
        )
