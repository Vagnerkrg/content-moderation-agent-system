"""
Interface de aprovação humana para o sistema de moderação.

Este módulo apresenta ao moderador as informações produzidas
pelos agentes e captura a decisão humana antes da execução
de uma ação crítica.
"""

from content_moderation.state.agent_state import AgentState


def display_review(state: AgentState) -> None:
    """
    Exibe as informações necessárias para a revisão humana.

    Args:
        state: Estado atual do fluxo de moderação.
    """
    print("\n" + "=" * 60)
    print("REVISÃO HUMANA — MODERAÇÃO DE CONTEÚDO")
    print("=" * 60)

    print("\nComentário original:")
    print(state["comentario_original"])

    print("\nAnálise do agente:")
    print(state["analise_do_agente"])

    print("\nPolíticas relevantes:")
    print(state["politicas_relevantes"])

    print("\nRecomendação do revisor:")
    print(state["status_da_moderacao"])

    print("\nJustificativa:")
    print(state["justificativa_final"])

    print("\n" + "-" * 60)


def request_human_decision() -> str:
    """
    Solicita ao moderador uma decisão de aprovação ou rejeição.

    Returns:
        ``"aprovado"`` quando a decisão for positiva.
        ``"rejeitado"`` quando a decisão for negativa.

    A função continua solicitando a entrada até receber
    uma resposta válida.
    """
    while True:
        resposta = input(
            "\nDeseja aprovar a recomendação? [sim/não]: "
        ).strip().lower()

        if resposta in {"sim", "s"}:
            return "aprovado"

        if resposta in {"não", "nao", "n"}:
            return "rejeitado"

        print("Entrada inválida. Digite 'sim' ou 'não'.")


def collect_human_review(state: AgentState) -> AgentState:
    """
    Executa a interação completa de revisão humana.

    Exibe o estado atual, solicita a decisão do moderador e
    registra a decisão no estado.

    Args:
        state: Estado atual do fluxo de moderação.

    Returns:
        Estado atualizado com a decisão humana.
    """
    display_review(state)

    decisao = request_human_decision()

    return {
        **state,
        "decisao_humana": decisao,
        "observacao_humana": "",
    }