"""
Testes do agente responsável pela pesquisa de políticas.
"""

import pytest

from content_moderation.agents.policy_researcher import (
    PolicyResearchError,
    research_policies,
)
from content_moderation.state.agent_state import AgentState


def create_state(
    analysis: str = "Comentário potencialmente problemático detectado.",
) -> AgentState:
    """Cria um estado base para os testes."""
    return {
        "comentario_original": "Este comentário contém spam.",
        "politicas_relevantes": "",
        "analise_do_agente": analysis,
        "status_da_moderacao": "",
        "justificativa_final": "",
    }


def test_policy_researcher_returns_policies():
    """Deve preencher as políticas retornadas pela pesquisa."""

    state = create_state()

    def fake_search(comment: str) -> str:
        assert comment == "Este comentário contém spam."
        return "Política de spam: conteúdo promocional não autorizado."

    result = research_policies(
        state,
        search_fn=fake_search,
    )

    assert (
        result["politicas_relevantes"]
        == "Política de spam: conteúdo promocional não autorizado."
    )


def test_policy_researcher_preserves_state():
    """Deve preservar os demais campos do estado."""

    state = create_state()

    result = research_policies(
        state,
        search_fn=lambda _: "Política relevante.",
    )

    assert result["comentario_original"] == state["comentario_original"]
    assert result["analise_do_agente"] == state["analise_do_agente"]
    assert result["status_da_moderacao"] == state["status_da_moderacao"]
    assert result["justificativa_final"] == state["justificativa_final"]


def test_policy_researcher_skips_neutral_comment():
    """Não deve pesquisar políticas para comentário não problemático."""

    state = create_state(
        "Comentário classificado como positivo ou neutro."
    )

    def fake_search(_: str) -> str:
        raise AssertionError("A pesquisa não deveria ser executada.")

    result = research_policies(
        state,
        search_fn=fake_search,
    )

    assert result["politicas_relevantes"] == ""


def test_policy_researcher_handles_empty_result():
    """Deve informar quando nenhuma política for encontrada."""

    state = create_state()

    result = research_policies(
        state,
        search_fn=lambda _: "",
    )

    assert (
        result["politicas_relevantes"]
        == "Nenhuma política relevante encontrada."
    )


def test_policy_researcher_raises_controlled_error():
    """Deve transformar falhas da ferramenta em erro controlado."""

    state = create_state()

    def failing_search(_: str) -> str:
        raise RuntimeError("Tavily indisponível.")

    with pytest.raises(PolicyResearchError):
        research_policies(
            state,
            search_fn=failing_search,
        )