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