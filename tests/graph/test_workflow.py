"""Testes para o workflow principal do sistema."""

from content_moderation.graph.workflow import build_workflow
from content_moderation.state.agent_state import AgentState


def test_workflow_can_be_compiled():
    """O workflow deve ser criado e compilado sem erros."""

    workflow = build_workflow()

    assert workflow is not None


def test_workflow_accepts_agent_state():
    """O workflow compilado deve aceitar o AgentState."""

    workflow = build_workflow()

    state: AgentState = {
        "comentario_original": "Este curso é excelente.",
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    result = workflow.invoke(state)

    assert result["comentario_original"] == state["comentario_original"]


def test_workflow_routes_neutral_comment_directly_to_end():
    """
    Comentários positivos ou neutros devem finalizar após o Analyzer.

    O Policy Researcher e o Reviewer não devem ser executados.
    """

    workflow = build_workflow()

    state: AgentState = {
        "comentario_original": "Este curso é excelente.",
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    result = workflow.invoke(state)

    assert result["analise_do_agente"] == (
        "Comentário classificado como positivo ou neutro."
    )
    assert result["politicas_relevantes"] == ""
    assert result["status_da_moderacao"] == ""
    assert result["justificativa_final"] == ""


def test_workflow_routes_problematic_comment_through_all_agents():
    """
    Comentários potencialmente problemáticos devem executar
    Policy Researcher e Reviewer antes de finalizar.
    """

    workflow = build_workflow()

    state: AgentState = {
        "comentario_original": "Isso é spam.",
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    result = workflow.invoke(state)

    assert "potencialmente problemático" in (
        result["analise_do_agente"].lower()
    )
    assert result["politicas_relevantes"]
    assert result["status_da_moderacao"]
    assert result["justificativa_final"]


def test_workflow_preserves_original_comment():
    """O workflow deve preservar o comentário original."""

    workflow = build_workflow()

    state: AgentState = {
        "comentario_original": "Comentário original.",
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    result = workflow.invoke(state)

    assert result["comentario_original"] == "Comentário original."