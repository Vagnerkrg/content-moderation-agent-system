"""Testes do fluxo Human-in-the-Loop."""

from content_moderation.graph.workflow import build_workflow
from content_moderation.persistence.checkpointer import get_checkpointer
from content_moderation.state.agent_state import AgentState


def test_workflow_pauses_before_reviewer():
    """O workflow deve pausar antes da execução do Reviewer."""

    state: AgentState = {
        "comentario_original": "Isso é spam.",
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    config = {
        "configurable": {
            "thread_id": "test-human-review",
        }
    }

    with get_checkpointer() as checkpointer:
        workflow = build_workflow(
            checkpointer=checkpointer,
            interrupt_before=["reviewer"],
        )

        result = workflow.invoke(
            state,
            config=config,
        )

        assert result["comentario_original"] == state["comentario_original"]

        current_state = workflow.get_state(config)

        assert current_state.next == ("reviewer",)


def test_workflow_can_resume_after_human_review():
    """O workflow deve continuar após a interrupção humana."""

    state: AgentState = {
        "comentario_original": "Isso é spam.",
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    config = {
        "configurable": {
            "thread_id": "test-human-review-resume",
        }
    }

    with get_checkpointer() as checkpointer:
        workflow = build_workflow(
            checkpointer=checkpointer,
            interrupt_before=["reviewer"],
        )

        workflow.invoke(
            state,
            config=config,
        )

        workflow.update_state(
            config,
            {
                "status_da_moderacao": "Aguardando revisão humana",
            },
        )

        workflow.invoke(
            None,
            config=config,
        )

        current_state = workflow.get_state(config)

        assert current_state.next == ()
        assert current_state.values["status_da_moderacao"] == "Remover"
        assert current_state.values["justificativa_final"]