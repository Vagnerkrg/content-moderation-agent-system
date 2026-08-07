"""Testes de execução completa do fluxo LangGraph."""

from content_moderation.graph.workflow import build_workflow
from content_moderation.state.agent_state import AgentState


def test_approved_comment_finishes_after_analyzer():
    """Comentários aprovados devem finalizar sem passar pelos demais agentes."""

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
    assert result["analise_do_agente"] == (
        "Comentário classificado como positivo ou neutro."
    )
    assert result["politicas_relevantes"] == ""
    assert result["status_da_moderacao"] == ""
    assert result["justificativa_final"] == ""


def test_problematic_comment_executes_complete_flow():
    """Comentários problemáticos devem percorrer todos os agentes."""

    workflow = build_workflow()

    state: AgentState = {
        "comentario_original": "Isso é spam.",
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    result = workflow.invoke(state)

    assert result["comentario_original"] == state["comentario_original"]
    assert "potencialmente problemático" in (
        result["analise_do_agente"].lower()
    )
    assert result["politicas_relevantes"]
    assert result["status_da_moderacao"]
    assert result["justificativa_final"]


def test_spam_comment_reaches_remove_recommendation():
    """Comentários identificados como spam devem resultar em remoção."""

    workflow = build_workflow()

    state: AgentState = {
        "comentario_original": "Compre agora! Isso é spam.",
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    result = workflow.invoke(state)

    assert result["status_da_moderacao"] == "Remover"
    assert result["justificativa_final"]


def test_inappropriate_language_reaches_edit_recommendation():
    """Linguagem inadequada deve resultar em recomendação de edição."""

    workflow = build_workflow()

    state: AgentState = {
        "comentario_original": "Você é um idiota.",
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    result = workflow.invoke(state)

    assert result["status_da_moderacao"] == "Editar"
    assert result["justificativa_final"]


def test_workflow_preserves_all_original_input_data():
    """O fluxo não deve alterar o comentário original recebido."""

    workflow = build_workflow()

    original_comment = "Este comentário precisa permanecer intacto."

    state: AgentState = {
        "comentario_original": original_comment,
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    result = workflow.invoke(state)

    assert result["comentario_original"] == original_comment