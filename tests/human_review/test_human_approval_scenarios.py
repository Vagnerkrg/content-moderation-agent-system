"""Testes de cenários completos de aprovação humana."""

from content_moderation.graph.workflow import build_workflow
from content_moderation.persistence.checkpointer import get_checkpointer
from content_moderation.runtime.threads import create_thread_config
from content_moderation.state.agent_state import AgentState


def create_problematic_state(comment: str) -> AgentState:
    """Cria um estado inicial para um comentário problemático."""
    return {
        "comentario_original": comment,
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
        "decisao_humana": "",
        "observacao_humana": "",
    }


def test_human_approval_keeps_recommendation() -> None:
    """A aprovação humana deve preservar a recomendação do agente."""
    state = create_problematic_state("Compre agora! Isso é spam.")
    config = create_thread_config()

    with get_checkpointer() as checkpointer:
        workflow = build_workflow(
            checkpointer=checkpointer,
            interrupt_before=["executar_acao_final"],
        )

        workflow.invoke(
            state,
            config=config,
        )

        workflow.update_state(
            config,
            {
                "decisao_humana": "aprovado",
                "observacao_humana": (
                    "Recomendação aprovada pelo moderador."
                ),
            },
        )

        workflow.invoke(
            None,
            config=config,
        )

        final_state = workflow.get_state(config)

        assert final_state.next == ()
        assert final_state.values["decisao_humana"] == "aprovado"
        assert (
            final_state.values["observacao_humana"]
            == "Recomendação aprovada pelo moderador."
        )
        assert final_state.values["status_da_moderacao"] == "Remover"
        assert final_state.values["comentario_original"] == (
            "Compre agora! Isso é spam."
        )


def test_human_rejection_preserves_human_decision() -> None:
    """A rejeição humana deve ser registrada no estado final."""
    state = create_problematic_state("Compre agora! Isso é spam.")
    config = create_thread_config()

    with get_checkpointer() as checkpointer:
        workflow = build_workflow(
            checkpointer=checkpointer,
            interrupt_before=["executar_acao_final"],
        )

        workflow.invoke(
            state,
            config=config,
        )

        workflow.update_state(
            config,
            {
                "decisao_humana": "rejeitado",
                "observacao_humana": (
                    "Moderador rejeitou a recomendação automática."
                ),
                "status_da_moderacao": "Aprovado",
                "justificativa_final": (
                    "Após revisão humana, o comentário foi considerado "
                    "adequado."
                ),
            },
        )

        workflow.invoke(
            None,
            config=config,
        )

        final_state = workflow.get_state(config)

        assert final_state.next == ()
        assert final_state.values["decisao_humana"] == "rejeitado"
        assert final_state.values["status_da_moderacao"] == "Aprovado"
        assert (
            final_state.values["observacao_humana"]
            == "Moderador rejeitou a recomendação automática."
        )
        assert final_state.values["justificativa_final"]
        assert final_state.values["comentario_original"] == (
            "Compre agora! Isso é spam."
        )


def test_ambiguous_comment_requires_human_decision() -> None:
    """Comentários ambíguos devem chegar à decisão humana."""
    state = create_problematic_state(
        "Talvez seja uma promoção, mas não tenho certeza."
    )
    config = create_thread_config()

    with get_checkpointer() as checkpointer:
        workflow = build_workflow(
            checkpointer=checkpointer,
            interrupt_before=["executar_acao_final"],
        )

        workflow.invoke(
            state,
            config=config,
        )

        paused_state = workflow.get_state(config)

        assert paused_state.next == ("executar_acao_final",)
        assert paused_state.values["comentario_original"] == (
            "Talvez seja uma promoção, mas não tenho certeza."
        )
        assert paused_state.values["analise_do_agente"]
        assert paused_state.values["politicas_relevantes"]
        assert paused_state.values["status_da_moderacao"]
        assert paused_state.values["justificativa_final"]

        workflow.update_state(
            config,
            {
                "decisao_humana": "aprovado",
                "observacao_humana": (
                    "Comentário ambíguo revisado manualmente e aprovado."
                ),
            },
        )

        workflow.invoke(
            None,
            config=config,
        )

        final_state = workflow.get_state(config)

        assert final_state.next == ()
        assert final_state.values["decisao_humana"] == "aprovado"
        assert (
            final_state.values["observacao_humana"]
            == "Comentário ambíguo revisado manualmente e aprovado."
        )


def test_human_decision_preserves_original_comment() -> None:
    """A decisão humana não deve alterar o comentário original."""
    original_comment = (
        "Este comentário deve permanecer exatamente como foi recebido."
    )

    state = create_problematic_state(original_comment)
    config = create_thread_config()

    with get_checkpointer() as checkpointer:
        workflow = build_workflow(
            checkpointer=checkpointer,
            interrupt_before=["executar_acao_final"],
        )

        workflow.invoke(
            state,
            config=config,
        )

        workflow.update_state(
            config,
            {
                "decisao_humana": "aprovado",
                "observacao_humana": "Aprovado após revisão.",
            },
        )

        workflow.invoke(
            None,
            config=config,
        )

        final_state = workflow.get_state(config)

        assert final_state.next == ()
        assert final_state.values["comentario_original"] == (
            original_comment
        )


def test_human_review_produces_complete_final_state() -> None:
    """A execução final deve manter as informações da moderação."""
    state = create_problematic_state("Você é um idiota.")
    config = create_thread_config()

    with get_checkpointer() as checkpointer:
        workflow = build_workflow(
            checkpointer=checkpointer,
            interrupt_before=["executar_acao_final"],
        )

        workflow.invoke(
            state,
            config=config,
        )

        workflow.update_state(
            config,
            {
                "decisao_humana": "aprovado",
                "observacao_humana": (
                    "Ação recomendada aprovada pelo moderador."
                ),
            },
        )

        workflow.invoke(
            None,
            config=config,
        )

        final_state = workflow.get_state(config)

        values = final_state.values

        assert final_state.next == ()
        assert values["comentario_original"]
        assert values["analise_do_agente"]
        assert values["politicas_relevantes"]
        assert values["status_da_moderacao"]
        assert values["justificativa_final"]
        assert values["decisao_humana"] == "aprovado"
        assert values["observacao_humana"]