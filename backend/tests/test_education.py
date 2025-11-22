"""
Tests for education API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app

client = TestClient(app)


class TestChatEndpoint:
    """Tests for the /api/education/chat endpoint"""

    def test_chat_success(self):
        """Test successful chat request"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.chat.return_value = "This is an AI-generated answer."
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/chat",
                json={"question": "What is photosynthesis?"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["question"] == "What is photosynthesis?"
            assert "answer" in data

    def test_chat_with_context(self):
        """Test chat request with context"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.chat.return_value = "Answer based on context."
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/chat",
                json={
                    "question": "Explain this concept",
                    "context": "In the context of biology...",
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["context"] == "In the context of biology..."

    def test_chat_empty_question(self):
        """Test chat with empty question"""
        response = client.post(
            "/api/education/chat",
            json={"question": ""},
        )

        assert response.status_code == 422  # Validation error

    def test_chat_missing_question(self):
        """Test chat without question field"""
        response = client.post(
            "/api/education/chat",
            json={},
        )

        assert response.status_code == 422  # Validation error


class TestGenerateMaterialEndpoint:
    """Tests for the /api/education/generate-material endpoint"""

    def test_generate_material_success(self):
        """Test successful material generation"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.generate_study_notes.return_value = "Study notes content"
            mock_instance.generate_story_explanation.return_value = "Story explanation"
            mock_instance.generate_summary.return_value = "Summary content"
            mock_instance.generate_mcqs.return_value = [
                {
                    "question": "Q1?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "A",
                    "explanation": "Explanation",
                }
            ]
            mock_instance.generate_short_questions.return_value = [
                {
                    "question": "Short Q?",
                    "expected_answer": "Answer",
                    "difficulty": "medium",
                }
            ]
            mock_instance.generate_image_url.return_value = "https://example.com/image.jpg"
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/generate-material",
                json={"topic": "Photosynthesis"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["topic"] == "Photosynthesis"
            assert "study_notes" in data
            assert "story_explanation" in data
            assert "summary" in data
            assert "mcqs" in data
            assert "short_questions" in data
            assert "image_url" in data

    def test_generate_material_with_level(self):
        """Test material generation with difficulty level"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.generate_study_notes.return_value = "Advanced notes"
            mock_instance.generate_story_explanation.return_value = "Story"
            mock_instance.generate_summary.return_value = "Summary"
            mock_instance.generate_mcqs.return_value = []
            mock_instance.generate_short_questions.return_value = []
            mock_instance.generate_image_url.return_value = None
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/generate-material",
                json={"topic": "Quantum Physics", "level": "advanced"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["level"] == "advanced"

    def test_generate_material_empty_topic(self):
        """Test material generation with empty topic"""
        response = client.post(
            "/api/education/generate-material",
            json={"topic": ""},
        )

        assert response.status_code == 422  # Validation error

    def test_generate_material_missing_topic(self):
        """Test material generation without topic"""
        response = client.post(
            "/api/education/generate-material",
            json={},
        )

        assert response.status_code == 422  # Validation error


class TestHealthEndpoint:
    """Tests for health check endpoint"""

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestRootEndpoint:
    """Tests for root endpoint"""

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
