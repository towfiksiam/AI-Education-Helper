"""
AI Service module for handling Groq API interactions.
Provides methods for generating educational content.
"""

import json
import logging
from typing import Optional
from groq import Groq

logger = logging.getLogger(__name__)


class AIEducationService:
    """Service for generating AI-powered educational content using Groq"""

    def __init__(self, api_key: str, model: str = "mixtral-8x7b-32768"):
        """
        Initialize the AI service with Groq API key.
        
        Args:
            api_key: Groq API key
            model: Model to use (default: mixtral-8x7b-32768)
        """
        if not api_key:
            raise ValueError("Groq API key is required")
        self.api_key = api_key
        self.model = model
        self.client = Groq(api_key=api_key)

    def _make_request(self, messages: list, temperature: float = 0.7, max_tokens: int = 500) -> str:
        """
        Make a request to Groq API.
        
        Args:
            messages: List of message dictionaries
            temperature: Temperature for response generation
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated text response
        """
        try:
            logger.info(f"Making request to Groq with model: {self.model}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            return response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            raise

    def chat(self, question: str, context: Optional[str] = None) -> str:
        """
        Generate an AI response to a user's question.
        
        Args:
            question: User's question
            context: Optional context for the question
            
        Returns:
            AI-generated answer
        """
        prompt = question
        if context:
            prompt = f"Context: {context}\n\nQuestion: {question}"

        messages = [
            {
                "role": "system",
                "content": "You are an expert educational assistant. Provide clear, concise, and accurate answers to educational questions.",
            },
            {"role": "user", "content": prompt},
        ]
        
        return self._make_request(messages, temperature=0.7, max_tokens=500)

    def generate_study_notes(self, topic: str, level: str = "intermediate") -> str:
        """
        Generate comprehensive study notes for a topic.
        
        Args:
            topic: Topic to generate notes for
            level: Difficulty level (beginner, intermediate, advanced)
            
        Returns:
            Study notes as formatted text
        """
        prompt = f"""Generate detailed study notes for the topic: "{topic}" at {level} level.
        
Format the notes with:
- Clear headings and subheadings
- Key concepts and definitions
- Important points highlighted
- Examples where applicable

Keep the notes concise but comprehensive."""

        messages = [
            {
                "role": "system",
                "content": "You are an expert educator. Create well-structured, clear study notes.",
            },
            {"role": "user", "content": prompt},
        ]
        
        return self._make_request(messages, temperature=0.7, max_tokens=1000)

    def generate_story_explanation(self, topic: str) -> str:
        """
        Generate a story-based explanation of a topic.
        
        Args:
            topic: Topic to explain through a story
            
        Returns:
            Story-based explanation
        """
        prompt = f"""Create an engaging story-based explanation for the topic: "{topic}".
        
The story should:
- Be relatable and easy to understand
- Incorporate the key concepts naturally
- Be memorable and interesting
- Be suitable for educational purposes

Write the story in a narrative format."""

        messages = [
            {
                "role": "system",
                "content": "You are a creative educator who explains complex topics through engaging stories.",
            },
            {"role": "user", "content": prompt},
        ]
        
        return self._make_request(messages, temperature=0.8, max_tokens=800)

    def generate_summary(self, topic: str) -> str:
        """
        Generate a concise summary of a topic.
        
        Args:
            topic: Topic to summarize
            
        Returns:
            Concise summary
        """
        prompt = f"""Create a concise summary of the topic: "{topic}".
        
The summary should:
- Cover the main points
- Be 2-3 paragraphs maximum
- Be clear and easy to understand
- Highlight the most important concepts"""

        messages = [
            {
                "role": "system",
                "content": "You are an expert at creating concise, informative summaries.",
            },
            {"role": "user", "content": prompt},
        ]
        
        return self._make_request(messages, temperature=0.7, max_tokens=400)

    def generate_mcqs(self, topic: str, count: int = 3) -> list:
        """
        Generate multiple choice questions for a topic.
        
        Args:
            topic: Topic to generate MCQs for
            count: Number of MCQs to generate (default: 3)
            
        Returns:
            List of MCQ dictionaries with question, options, correct_answer, and explanation
        """
        prompt = f"""Generate {count} multiple choice questions for the topic: "{topic}".
        
For each question, provide:
1. A clear question
2. 4 options (A, B, C, D)
3. The correct answer (A, B, C, or D)
4. A brief explanation of why the answer is correct

Format the response as a JSON array with objects containing:
- "question": the question text
- "options": array of 4 options
- "correct_answer": the correct option text
- "explanation": explanation of the correct answer

Return ONLY valid JSON, no additional text."""

        messages = [
            {
                "role": "system",
                "content": "You are an expert at creating educational multiple choice questions. Always respond with valid JSON only.",
            },
            {"role": "user", "content": prompt},
        ]
        
        try:
            content = self._make_request(messages, temperature=0.7, max_tokens=1500)
            mcqs = json.loads(content)
            return mcqs if isinstance(mcqs, list) else [mcqs]
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Error generating MCQs: {str(e)}")
            return self._get_default_mcqs(topic)

    def generate_short_questions(self, topic: str, count: int = 3) -> list:
        """
        Generate short answer questions for a topic.
        
        Args:
            topic: Topic to generate questions for
            count: Number of questions to generate (default: 3)
            
        Returns:
            List of short question dictionaries
        """
        prompt = f"""Generate {count} short answer questions for the topic: "{topic}".
        
For each question, provide:
1. A clear, concise question
2. The expected answer (2-3 sentences)
3. Difficulty level (easy, medium, or hard)

Format the response as a JSON array with objects containing:
- "question": the question text
- "expected_answer": the expected answer
- "difficulty": the difficulty level

Return ONLY valid JSON, no additional text."""

        messages = [
            {
                "role": "system",
                "content": "You are an expert at creating educational short answer questions. Always respond with valid JSON only.",
            },
            {"role": "user", "content": prompt},
        ]
        
        try:
            content = self._make_request(messages, temperature=0.7, max_tokens=1000)
            questions = json.loads(content)
            return questions if isinstance(questions, list) else [questions]
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Error generating short questions: {str(e)}")
            return self._get_default_short_questions(topic)

    def generate_image_url(self, topic: str) -> Optional[str]:
        """
        Generate an image URL for a topic.
        Note: Groq does not support image generation. Returns None.
        
        Args:
            topic: Topic to generate image for
            
        Returns:
            Image URL or None if generation fails
        """
        logger.info(f"Image generation not supported via Groq for topic: {topic}")
        return None

    @staticmethod
    def _get_default_mcqs(topic: str) -> list:
        """Return default MCQs when API fails"""
        return [
            {
                "question": f"What is the main concept of {topic}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A",
                "explanation": "This is a default MCQ. Please check your Groq API key.",
            }
        ]

    @staticmethod
    def _get_default_short_questions(topic: str) -> list:
        """Return default short questions when API fails"""
        return [
            {
                "question": f"Explain the key aspects of {topic}.",
                "expected_answer": "A comprehensive explanation of the topic.",
                "difficulty": "medium",
            }
        ]
