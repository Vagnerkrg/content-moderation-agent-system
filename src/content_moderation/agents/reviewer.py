"""
Agente responsável pela revisão e recomendação de moderação.

Este agente consolida a análise realizada pelo Analyzer e as
políticas relevantes encontradas pelo Policy Researcher para
produzir uma recomendação de ação.
"""

from content_moderation.state.agent_state import AgentState


def review_moderation(state: AgentState) -> AgentState:
    """
    Consolida análise e políticas para gerar uma recomendação.

    Args:
        state: Estado compartilhado do fluxo de moderação.

    Returns:
        Uma cópia do estado contendo a recomendação em
        ``status_da_moderacao`` e sua justificativa em
        ``justificativa_final``.
    """
    analysis = state["analise_do_agente"].lower()
    policies = state["politicas_relevantes"].lower()

    if "potencialmente problemático" not in analysis:
        status = "Aprovado"
        justificativa = (
            "Comentário classificado como positivo ou neutro, "
            "sem indicação de violação das políticas."
        )

    elif "spam" in policies:
        status = "Remover"
        justificativa = (
            "Comentário recomendado para remoção por apresentar "
            "características de spam conforme as políticas relevantes."
        )

    elif any(
        palavra in policies
        for palavra in ("ofensa", "linguagem inadequada", "abuso")
    ):
        status = "Editar"
        justificativa = (
            "Comentário recomendado para edição devido à presença "
            "de linguagem potencialmente inadequada."
        )

    else:
        status = "Editar"
        justificativa = (
            "Comentário potencialmente problemático. "
            "Recomenda-se revisão e possível edição antes da publicação."
        )

    return {
        **state,
        "status_da_moderacao": status,
        "justificativa_final": justificativa,
    }