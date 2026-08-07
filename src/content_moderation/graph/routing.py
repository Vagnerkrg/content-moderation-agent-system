"""
Funções de roteamento do workflow de moderação.

Define as decisões condicionais utilizadas pelo LangGraph
para determinar o próximo nó do fluxo.
"""

from content_moderation.state.agent_state import AgentState


def route_after_analysis(state: AgentState) -> str:
    """
    Decide o próximo passo após a análise do comentário.

    Comentários potencialmente problemáticos seguem para o
    pesquisador de políticas. Comentários positivos ou neutros
    encerram o fluxo.

    Args:
        state: Estado compartilhado do workflow.

    Returns:
        Nome do próximo nó lógico:
        - ``policy_researcher`` para comentários problemáticos.
        - ``end`` para comentários aprovados.
    """
    analysis = state["analise_do_agente"].lower()

    if "potencialmente problemático" in analysis:
        return "policy_researcher"

    return "end"