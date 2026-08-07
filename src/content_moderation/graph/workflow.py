"""
Workflow principal do sistema de moderação.

Este módulo contém a orquestração dos agentes de moderação
utilizando LangGraph e um estado compartilhado.
"""

from langgraph.graph import END, StateGraph

from content_moderation.agents.analyzer import AnalyzerAgent
from content_moderation.agents.policy_researcher import research_policies
from content_moderation.agents.reviewer import review_moderation
from content_moderation.state.agent_state import AgentState


def build_workflow():
    """
    Cria e compila o StateGraph principal.

    O workflow conecta os agentes especializados utilizando
    AgentState como estado compartilhado.

    Returns:
        Grafo LangGraph compilado.
    """

    analyzer = AnalyzerAgent()

    workflow = StateGraph(AgentState)

    workflow.add_node("analyzer", analyzer.execute)
    workflow.add_node("policy_researcher", research_policies)
    workflow.add_node("reviewer", review_moderation)

    workflow.set_entry_point("analyzer")

    workflow.add_edge("analyzer", "policy_researcher")
    workflow.add_edge("policy_researcher", "reviewer")
    workflow.add_edge("reviewer", END)

    return workflow.compile()