"""
Modelos utilizados pelos agentes de moderação.
"""

from typing import Literal

from pydantic import BaseModel, Field


class CommentAnalysis(BaseModel):
    """
    Resultado estruturado da análise de um comentário.
    """

    classification: Literal[
        "positive",
        "neutral",
        "problematic",
    ]

    category: str = Field(
        description="Categoria identificada na análise."
    )

    explanation: str = Field(
        description="Explicação resumida da classificação."
    )