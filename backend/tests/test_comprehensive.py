"""
Comprehensive test suite for AI Education System API.
Tests all endpoints with various scenarios including success cases, validation errors, and edge cases.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json

from app.main import app

client = TestClient(app)


# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

class TestHealthEndpoints:
    """Test suite for health check endpoints"""

    def test_health_check_success(self):
        """Test GET /health returns 200 with correct structure"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "service" in data
        assert "version" in data
        assert data["service"] == "AI Education System"

    def test_health_check_response_type(self):
        """Test health check response has correct content type"""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_root_endpoint_success(self):
        """Test GET / returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert "Welcome" in data["message"]

    def test_api_v1_health_check(self):
        """Test GET /api/v1/health returns 200"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_docs_endpoint_exists(self):
        """Test GET /docs returns documentation"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


# ============================================================================
# CHAT ENDPOINT - SUCCESS CASES
# ============================================================================

class TestChatEndpointSuccess:
    """Test suite for successful chat endpoint requests"""

    def test_chat_basic_question(self):
        """Test chat with basic question"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.chat.return_value = "Photosynthesis is the process by which plants convert sunlight into chemical energy."
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/chat",
                json={"question": "What is photosynthesis?"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["question"] == "What is photosynthesis?"
            assert len(data["answer"]) > 0
            assert data["context"] is None

    def test_chat_with_context(self):
        """Test chat with context parameter"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.chat.return_value = "In the context of biology, photosynthesis occurs in chloroplasts."
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/chat",
                json={
                    "question": "Explain photosynthesis",
                    "context": "In the context of biology"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["question"] == "Explain photosynthesis"
            assert data["context"] == "In the context of biology"
            assert len(data["answer"]) > 0

    def test_chat_response_structure(self):
        """Test chat response has correct structure"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.chat.return_value = "Test answer"
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/chat",
                json={"question": "Test question?"}
            )

            assert response.status_code == 200
            data = response.json()
            assert set(data.keys()) == {"question", "answer", "context"}

    def test_chat_with_special_characters(self):
        """Test chat with special characters and unicode"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.chat.return_value = "Answer with special chars: @#$%^&*()"
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/chat",
                json={"question": "What is 光合作用? 🌱"}
            )

            assert response.status_code == 200
            data = response.json()
            assert "光合作用" in data["question"]

    def test_chat_with_numbers(self):
        """Test chat with numbers in question"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.chat.return_value = "The answer is 42"
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/chat",
                json={"question": "What is 2 + 2?"}
            )

            assert response.status_code == 200
            data = response.json()
            assert "2 + 2" in data["question"]

    def test_chat_long_answer(self):
        """Test chat with long answer"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            long_answer = "A" * 1000
            mock_instance = MagicMock()
            mock_instance.chat.return_value = long_answer
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/chat",
                json={"question": "Tell me everything about photosynthesis"}
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data["answer"]) == 1000


# ============================================================================
# CHAT ENDPOINT - VALIDATION ERRORS
# ============================================================================

class TestChatEndpointValidation:
    """Test suite for chat endpoint validation"""

    def test_chat_empty_question(self):
        """Test chat with empty question fails validation"""
        response = client.post(
            "/api/education/chat",
            json={"question": ""}
        )

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert len(data["detail"]) > 0

    def test_chat_missing_question_field(self):
        """Test chat without question field fails"""
        response = client.post(
            "/api/education/chat",
            json={"context": "Some context"}
        )

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_chat_question_too_long(self):
        """Test chat with question exceeding max length"""
        long_question = "A" * 1001
        response = client.post(
            "/api/education/chat",
            json={"question": long_question}
        )

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_chat_context_too_long(self):
        """Test chat with context exceeding max length"""
        long_context = "A" * 2001
        response = client.post(
            "/api/education/chat",
            json={
                "question": "What is this?",
                "context": long_context
            }
        )

        assert response.status_code == 422

    def test_chat_invalid_json(self):
        """Test chat with invalid JSON"""
        response = client.post(
            "/api/education/chat",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 422

    def test_chat_null_question(self):
        """Test chat with null question"""
        response = client.post(
            "/api/education/chat",
            json={"question": None}
        )

        assert response.status_code == 422

    def test_chat_numeric_question(self):
        """Test chat with numeric question"""
        response = client.post(
            "/api/education/chat",
            json={"question": 123}
        )

        assert response.status_code == 422

    def test_chat_array_question(self):
        """Test chat with array as question"""
        response = client.post(
            "/api/education/chat",
            json={"question": ["What", "is", "this"]}
        )

        assert response.status_code == 422


# ============================================================================
# GENERATE MATERIAL ENDPOINT - SUCCESS CASES
# ============================================================================

class TestGenerateMaterialSuccess:
    """Test suite for successful generate material requests"""

    def test_generate_material_basic(self):
        """Test basic material generation"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.generate_study_notes.return_value = "Study notes"
            mock_instance.generate_story_explanation.return_value = "Story"
            mock_instance.generate_summary.return_value = "Summary"
            mock_instance.generate_mcqs.return_value = [
                {
                    "question": "Q1?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "A",
                    "explanation": "Exp"
                }
            ]
            mock_instance.generate_short_questions.return_value = [
                {
                    "question": "SQ1?",
                    "expected_answer": "Answer",
                    "difficulty": "easy"
                }
            ]
            mock_instance.generate_image_url.return_value = None
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/generate-material",
                json={"topic": "Photosynthesis"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["topic"] == "Photosynthesis"
            assert data["level"] == "intermediate"  # default
            assert "study_notes" in data
            assert "story_explanation" in data
            assert "summary" in data
            assert "mcqs" in data
            assert "short_questions" in data
            assert "image_url" in data

    def test_generate_material_beginner_level(self):
        """Test material generation for beginner level"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.generate_study_notes.return_value = "Simple notes"
            mock_instance.generate_story_explanation.return_value = "Simple story"
            mock_instance.generate_summary.return_value = "Simple summary"
            mock_instance.generate_mcqs.return_value = []
            mock_instance.generate_short_questions.return_value = []
            mock_instance.generate_image_url.return_value = None
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/generate-material",
                json={"topic": "Biology", "level": "beginner"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["level"] == "beginner"

    def test_generate_material_intermediate_level(self):
        """Test material generation for intermediate level"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.generate_study_notes.return_value = "Detailed notes"
            mock_instance.generate_story_explanation.return_value = "Detailed story"
            mock_instance.generate_summary.return_value = "Detailed summary"
            mock_instance.generate_mcqs.return_value = []
            mock_instance.generate_short_questions.return_value = []
            mock_instance.generate_image_url.return_value = None
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/generate-material",
                json={"topic": "Physics", "level": "intermediate"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["level"] == "intermediate"

    def test_generate_material_advanced_level(self):
        """Test material generation for advanced level"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.generate_study_notes.return_value = "Advanced notes"
            mock_instance.generate_story_explanation.return_value = "Advanced story"
            mock_instance.generate_summary.return_value = "Advanced summary"
            mock_instance.generate_mcqs.return_value = []
            mock_instance.generate_short_questions.return_value = []
            mock_instance.generate_image_url.return_value = None
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/generate-material",
                json={"topic": "Quantum Physics", "level": "advanced"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["level"] == "advanced"

    def test_generate_material_with_language(self):
        """Test material generation with language parameter"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.generate_study_notes.return_value = "Notes"
            mock_instance.generate_story_explanation.return_value = "Story"
            mock_instance.generate_summary.return_value = "Summary"
            mock_instance.generate_mcqs.return_value = []
            mock_instance.generate_short_questions.return_value = []
            mock_instance.generate_image_url.return_value = None
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/generate-material",
                json={
                    "topic": "Chemistry",
                    "level": "intermediate",
                    "language": "english"
                }
            )

            assert response.status_code == 200

    def test_generate_material_response_structure(self):
        """Test material response has correct structure"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.generate_study_notes.return_value = "Notes"
            mock_instance.generate_story_explanation.return_value = "Story"
            mock_instance.generate_summary.return_value = "Summary"
            mock_instance.generate_mcqs.return_value = []
            mock_instance.generate_short_questions.return_value = []
            mock_instance.generate_image_url.return_value = None
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/generate-material",
                json={"topic": "Test"}
            )

            assert response.status_code == 200
            data = response.json()
            required_fields = {
                "topic", "level", "study_notes", "story_explanation",
                "summary", "mcqs", "short_questions", "image_url"
            }
            assert set(data.keys()) == required_fields

    def test_generate_material_mcq_structure(self):
        """Test MCQ structure in material response"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.generate_study_notes.return_value = "Notes"
            mock_instance.generate_story_explanation.return_value = "Story"
            mock_instance.generate_summary.return_value = "Summary"
            mock_instance.generate_mcqs.return_value = [
                {
                    "question": "What is X?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "A",
                    "explanation": "Because..."
                }
            ]
            mock_instance.generate_short_questions.return_value = []
            mock_instance.generate_image_url.return_value = None
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/generate-material",
                json={"topic": "Test"}
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data["mcqs"]) > 0
            mcq = data["mcqs"][0]
            assert "question" in mcq
            assert "options" in mcq
            assert "correct_answer" in mcq
            assert "explanation" in mcq

    def test_generate_material_short_questions_structure(self):
        """Test short questions structure in material response"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.generate_study_notes.return_value = "Notes"
            mock_instance.generate_story_explanation.return_value = "Story"
            mock_instance.generate_summary.return_value = "Summary"
            mock_instance.generate_mcqs.return_value = []
            mock_instance.generate_short_questions.return_value = [
                {
                    "question": "Explain X",
                    "expected_answer": "X is...",
                    "difficulty": "medium"
                }
            ]
            mock_instance.generate_image_url.return_value = None
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/generate-material",
                json={"topic": "Test"}
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data["short_questions"]) > 0
            sq = data["short_questions"][0]
            assert "question" in sq
            assert "expected_answer" in sq
            assert "difficulty" in sq


# ============================================================================
# GENERATE MATERIAL ENDPOINT - VALIDATION ERRORS
# ============================================================================

class TestGenerateMaterialValidation:
    """Test suite for generate material validation"""

    def test_generate_material_empty_topic(self):
        """Test material generation with empty topic"""
        response = client.post(
            "/api/education/generate-material",
            json={"topic": ""}
        )

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_generate_material_missing_topic(self):
        """Test material generation without topic field"""
        response = client.post(
            "/api/education/generate-material",
            json={"level": "intermediate"}
        )

        assert response.status_code == 422

    def test_generate_material_topic_too_long(self):
        """Test material generation with topic exceeding max length"""
        long_topic = "A" * 501
        response = client.post(
            "/api/education/generate-material",
            json={"topic": long_topic}
        )

        assert response.status_code == 422

    def test_generate_material_null_topic(self):
        """Test material generation with null topic"""
        response = client.post(
            "/api/education/generate-material",
            json={"topic": None}
        )

        assert response.status_code == 422

    def test_generate_material_numeric_topic(self):
        """Test material generation with numeric topic"""
        response = client.post(
            "/api/education/generate-material",
            json={"topic": 123}
        )

        assert response.status_code == 422

    def test_generate_material_invalid_json(self):
        """Test material generation with invalid JSON"""
        response = client.post(
            "/api/education/generate-material",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 422


# ============================================================================
# HTTP METHOD TESTS
# ============================================================================

class TestHTTPMethods:
    """Test suite for HTTP method validation"""

    def test_chat_get_method_not_allowed(self):
        """Test GET method on chat endpoint returns 405"""
        response = client.get("/api/education/chat")
        assert response.status_code == 405

    def test_generate_material_get_method_not_allowed(self):
        """Test GET method on generate-material endpoint returns 405"""
        response = client.get("/api/education/generate-material")
        assert response.status_code == 405

    def test_health_post_method_not_allowed(self):
        """Test POST method on health endpoint returns 405"""
        response = client.post("/health")
        assert response.status_code == 405


# ============================================================================
# ENDPOINT NOT FOUND TESTS
# ============================================================================

class TestEndpointNotFound:
    """Test suite for non-existent endpoints"""

    def test_nonexistent_endpoint(self):
        """Test request to non-existent endpoint returns 404"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404

    def test_nonexistent_education_endpoint(self):
        """Test request to non-existent education endpoint returns 404"""
        response = client.get("/api/education/nonexistent")
        assert response.status_code == 404


# ============================================================================
# CONTENT TYPE TESTS
# ============================================================================

class TestContentType:
    """Test suite for content type validation"""

    def test_chat_response_content_type(self):
        """Test chat response has correct content type"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.chat.return_value = "Answer"
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/chat",
                json={"question": "Test?"}
            )

            assert "application/json" in response.headers["content-type"]

    def test_generate_material_response_content_type(self):
        """Test generate material response has correct content type"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.generate_study_notes.return_value = "Notes"
            mock_instance.generate_story_explanation.return_value = "Story"
            mock_instance.generate_summary.return_value = "Summary"
            mock_instance.generate_mcqs.return_value = []
            mock_instance.generate_short_questions.return_value = []
            mock_instance.generate_image_url.return_value = None
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/generate-material",
                json={"topic": "Test"}
            )

            assert "application/json" in response.headers["content-type"]


# ============================================================================
# EDGE CASES
# ============================================================================

class TestEdgeCases:
    """Test suite for edge cases"""

    def test_chat_single_character_question(self):
        """Test chat with single character question"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.chat.return_value = "Answer"
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/chat",
                json={"question": "?"}
            )

            assert response.status_code == 200

    def test_generate_material_single_character_topic(self):
        """Test material generation with single character topic"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.generate_study_notes.return_value = "Notes"
            mock_instance.generate_story_explanation.return_value = "Story"
            mock_instance.generate_summary.return_value = "Summary"
            mock_instance.generate_mcqs.return_value = []
            mock_instance.generate_short_questions.return_value = []
            mock_instance.generate_image_url.return_value = None
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/generate-material",
                json={"topic": "A"}
            )

            assert response.status_code == 200

    def test_chat_whitespace_only_question(self):
        """Test chat with whitespace-only question"""
        response = client.post(
            "/api/education/chat",
            json={"question": "   "}
        )

        # Should pass validation as it has characters
        assert response.status_code in [200, 422]

    def test_chat_question_with_newlines(self):
        """Test chat with question containing newlines"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.chat.return_value = "Answer"
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/chat",
                json={"question": "What is\nphotosynthesis?"}
            )

            assert response.status_code == 200

    def test_generate_material_topic_with_special_chars(self):
        """Test material generation with special characters in topic"""
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.generate_study_notes.return_value = "Notes"
            mock_instance.generate_story_explanation.return_value = "Story"
            mock_instance.generate_summary.return_value = "Summary"
            mock_instance.generate_mcqs.return_value = []
            mock_instance.generate_short_questions.return_value = []
            mock_instance.generate_image_url.return_value = None
            mock_service.return_value = mock_instance

            response = client.post(
                "/api/education/generate-material",
                json={"topic": "C++ Programming & Data Structures"}
            )

            assert response.status_code == 200


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for multiple endpoints"""

    def test_health_then_chat(self):
        """Test health check followed by chat"""
        # Check health
        health_response = client.get("/health")
        assert health_response.status_code == 200

        # Then chat
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.chat.return_value = "Answer"
            mock_service.return_value = mock_instance

            chat_response = client.post(
                "/api/education/chat",
                json={"question": "Test?"}
            )

            assert chat_response.status_code == 200

    def test_health_then_generate_material(self):
        """Test health check followed by material generation"""
        # Check health
        health_response = client.get("/health")
        assert health_response.status_code == 200

        # Then generate material
        with patch("app.api.v1.education.AIEducationService") as mock_service:
            mock_instance = MagicMock()
            mock_instance.generate_study_notes.return_value = "Notes"
            mock_instance.generate_story_explanation.return_value = "Story"
            mock_instance.generate_summary.return_value = "Summary"
            mock_instance.generate_mcqs.return_value = []
            mock_instance.generate_short_questions.return_value = []
            mock_instance.generate_image_url.return_value = None
            mock_service.return_value = mock_instance

            material_response = client.post(
                "/api/education/generate-material",
                json={"topic": "Test"}
            )

            assert material_response.status_code == 200
