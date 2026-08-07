"""
Workflow principal do sistema de moderação.

Este módulo contém a fundação do StateGraph utilizado
para orquestrar os agentes de moderação.
"""

from langgraph.graph import END, StateGraph

from content_moderation.state.agent_state import AgentState


def build_workflow():
    """
    Cria e compila o StateGraph principal.

    Returns:
        Um grafo LangGraph compilado.
    """

    workflow = StateGraph(AgentState)

    workflow.set_entry_point("start")
    workflow.add_node("start", lambda state: state)
    workflow.add_edge("start", END)

    return workflow.compile()