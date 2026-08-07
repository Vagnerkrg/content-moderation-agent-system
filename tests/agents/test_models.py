"""
Testes dos modelos utilizados pelos agentes.
"""

import pytest
from pydantic import ValidationError

from content_moderation.agents.models import CommentAnalysis


def test_comment_analysis_accepts_valid_classification():
    """Valida uma análise estruturada válida."""

    analysis = CommentAnalysis(
        classification="problematic",
        category="offensive",
        explanation="O comentário contém linguagem ofensiva.",
    )

    assert analysis.classification == "problematic"
    assert analysis.category == "offensive"


def test_comment_analysis_accepts_positive_classification():
    """Valida uma classificação positiva."""

    analysis = CommentAnalysis(
        classification="positive",
        category="positive",
        explanation="O comentário contribui positivamente para a discussão.",
    )

    assert analysis.classification == "positive"


def test_comment_analysis_rejects_invalid_classification():
    """Valida que classificações desconhecidas sejam rejeitadas."""

    with pytest.raises(ValidationError):
        CommentAnalysis(
            classification="invalid",
            category="unknown",
            explanation="Classificação inválida.",
        )