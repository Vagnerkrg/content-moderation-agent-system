"""
Testes do agente responsável pela revisão de moderação.
"""

from content_moderation.agents.reviewer import review_moderation
from content_moderation.state.agent_state import AgentState


def create_state(
    analysis: str,
    policies: str = "",
) -> AgentState:
    """Cria um estado base para os testes."""
    return {
        "comentario_original": "Comentário de teste.",
        "politicas_relevantes": policies,
        "analise_do_agente": analysis,
        "status_da_moderacao": "",
        "justificativa_final": "",
    }


def test_reviewer_approves_neutral_comment():
    """Deve aprovar comentários positivos ou neutros."""

    state = create_state(
        "Comentário classificado como positivo ou neutro."
    )

    result = review_moderation(state)

    assert result["status_da_moderacao"] == "Aprovado"
    assert "positivo ou neutro" in result["justificativa_final"]


def test_reviewer_removes_spam():
    """Deve recomendar remoção para conteúdo identificado como spam."""

    state = create_state(
        "Comentário potencialmente problemático detectado.",
        "Política de spam: conteúdo promocional não autorizado.",
    )

    result = review_moderation(state)

    assert result["status_da_moderacao"] == "Remover"
    assert "spam" in result["justificativa_final"].lower()


def test_reviewer_recommends_edit_for_inappropriate_language():
    """Deve recomendar edição para linguagem inadequada."""

    state = create_state(
        "Comentário potencialmente problemático detectado.",
        "Política sobre linguagem inadequada e abuso.",
    )

    result = review_moderation(state)

    assert result["status_da_moderacao"] == "Editar"
    assert "inadequada" in result["justificativa_final"].lower()


def test_reviewer_handles_unknown_problem():
    """Deve recomendar revisão para problemas sem política específica."""

    state = create_state(
        "Comentário potencialmente problemático detectado.",
        "Nenhuma política relevante encontrada.",
    )

    result = review_moderation(state)

    assert result["status_da_moderacao"] == "Editar"
    assert "revisão" in result["justificativa_final"].lower()


def test_reviewer_preserves_original_state():
    """Deve preservar os campos existentes do estado."""

    state = create_state(
        "Comentário potencialmente problemático detectado.",
        "Política de spam.",
    )

    result = review_moderation(state)

    assert result["comentario_original"] == state["comentario_original"]
    assert result["analise_do_agente"] == state["analise_do_agente"]
    assert result["politicas_relevantes"] == state["politicas_relevantes"]