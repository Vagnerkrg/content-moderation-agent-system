"""Testes do fluxo Human-in-the-Loop."""

from content_moderation.graph.workflow import build_workflow
from content_moderation.persistence.checkpointer import get_checkpointer
from content_moderation.state.agent_state import AgentState


def test_workflow_pauses_before_final_action():
    """O workflow deve pausar antes da execução da ação final."""

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
            interrupt_before=["executar_acao_final"],
        )

        result = workflow.invoke(
            state,
            config=config,
        )

        assert result["comentario_original"] == state["comentario_original"]

        current_state = workflow.get_state(config)

        assert current_state.next == ("executar_acao_final",)


def test_workflow_can_resume_after_human_review():
    """O workflow deve continuar após a intervenção humana."""

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
            interrupt_before=["executar_acao_final"],
        )

        workflow.invoke(
            state,
            config=config,
        )

        current_state = workflow.get_state(config)

        assert current_state.next == ("executar_acao_final",)

        workflow.update_state(
            config,
            {
                "status_da_moderacao": "Remover",
                "justificativa_final": (
                    "Removido por conter conteúdo identificado "
                    "como spam durante a revisão humana."
                ),
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