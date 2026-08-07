"""
Testes do Agente Analisador.
"""

from content_moderation.agents.analyzer import AnalyzerAgent
from content_moderation.state.agent_state import AgentState


def create_state(comment: str) -> AgentState:
    """Cria um estado mínimo para os testes."""
    return {
        "comentario_original": comment,
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }


def test_analyzer_detects_problematic_comment():
    """Verifica a detecção de comentário potencialmente problemático."""

    agent = AnalyzerAgent()

    state = create_state("Esse comentário é um spam idiota.")

    result = agent.execute(state)

    assert (
        result["analise_do_agente"]
        == "Comentário potencialmente problemático detectado."
    )


def test_analyzer_accepts_neutral_comment():
    """Verifica a classificação de comentário neutro."""

    agent = AnalyzerAgent()

    state = create_state("A aula foi muito interessante.")

    result = agent.execute(state)

    assert (
        result["analise_do_agente"]
        == "Comentário classificado como positivo ou neutro."
    )


def test_analyzer_preserves_original_state():
    """Verifica que o agente preserva os demais campos do estado."""

    agent = AnalyzerAgent()

    state = create_state("A aula foi muito interessante.")
    state["politicas_relevantes"] = "Política de comentários."

    result = agent.execute(state)

    assert result["comentario_original"] == state["comentario_original"]
    assert result["politicas_relevantes"] == "Política de comentários."