"""Testes de integração do workflow com SQLite Checkpoint."""

from content_moderation.graph.workflow import build_workflow
from content_moderation.persistence.checkpointer import get_checkpointer
from content_moderation.state.agent_state import AgentState


def test_workflow_can_be_compiled_with_sqlite_checkpointer():
    """O workflow deve ser compilável utilizando SQLite Checkpoint."""

    with get_checkpointer() as checkpointer:
        workflow = build_workflow(checkpointer=checkpointer)

        assert workflow is not None


def test_workflow_persists_execution_state():
    """O workflow deve persistir o estado da execução."""

    state: AgentState = {
        "comentario_original": "Este curso é excelente.",
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    config = {
        "configurable": {
            "thread_id": "test-checkpoint-thread",
        }
    }

    with get_checkpointer() as checkpointer:
        workflow = build_workflow(checkpointer=checkpointer)

        result = workflow.invoke(
            state,
            config=config,
        )

        assert result["comentario_original"] == state["comentario_original"]

        saved_state = workflow.get_state(config)

        assert saved_state.values["comentario_original"] == (
            state["comentario_original"]
        )