"""Testes de inspeção e atualização do estado durante Human-in-the-Loop."""

from content_moderation.graph.workflow import build_workflow
from content_moderation.persistence.checkpointer import get_checkpointer
from content_moderation.state.agent_state import AgentState


def test_human_reviewer_can_inspect_paused_state():
    """O humano deve conseguir consultar o estado interrompido."""

    state: AgentState = {
        "comentario_original": "Compre agora! Isso é spam.",
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    config = {
        "configurable": {
            "thread_id": "test-human-inspection",
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

        current_state = workflow.get_state(config)

        assert current_state.values["comentario_original"] == (
            "Compre agora! Isso é spam."
        )
        assert current_state.values["analise_do_agente"]
        assert current_state.values["politicas_relevantes"]
        assert current_state.next == ("reviewer",)


def test_human_reviewer_can_update_paused_state():
    """O humano deve conseguir atualizar o estado antes da revisão."""

    state: AgentState = {
        "comentario_original": "Compre agora! Isso é spam.",
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    config = {
        "configurable": {
            "thread_id": "test-human-update",
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
                "justificativa_final": (
                    "Revisão humana solicitada antes da decisão final."
                ),
            },
        )

        current_state = workflow.get_state(config)

        assert current_state.values["justificativa_final"] == (
            "Revisão humana solicitada antes da decisão final."
        )
        assert current_state.next == ("reviewer",)


def test_updated_state_survives_workflow_resume():
    """O estado atualizado deve continuar disponível após o resume."""

    state: AgentState = {
        "comentario_original": "Compre agora! Isso é spam.",
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    config = {
        "configurable": {
            "thread_id": "test-human-update-resume",
        }
    }

    human_note = "Conteúdo confirmado como spam durante revisão humana."

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
                "justificativa_final": human_note,
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