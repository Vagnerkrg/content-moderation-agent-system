"""
Workflow principal do sistema de moderação.

Este módulo contém o StateGraph utilizado para
orquestrar os agentes de moderação.
"""

from typing import Any

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, StateGraph

from content_moderation.agents.analyzer import AnalyzerAgent
from content_moderation.agents.policy_researcher import research_policies
from content_moderation.agents.reviewer import review_moderation
from content_moderation.graph.routing import route_after_analysis
from content_moderation.state.agent_state import AgentState


def build_workflow(
    checkpointer: BaseCheckpointSaver | None = None,
    interrupt_before: list[str] | None = None,
) -> Any:
    """
    Cria e compila o StateGraph principal.

    O fluxo utiliza roteamento condicional após o Analyzer:

    - Comentário problemático:
      Analyzer → Policy Researcher → Reviewer → END

    - Comentário positivo/neutro:
      Analyzer → END

    Args:
        checkpointer: Checkpointer opcional utilizado para
            persistir o estado das execuções.

        interrupt_before: Lista opcional de nós nos quais
            a execução deve ser interrompida antes da execução.

    Returns:
        Um grafo LangGraph compilado.
    """
    workflow = StateGraph(AgentState)

    analyzer = AnalyzerAgent()

    workflow.add_node(
        "analyzer",
        analyzer.execute,
    )

    workflow.add_node(
        "policy_researcher",
        research_policies,
    )

    workflow.add_node(
        "reviewer",
        review_moderation,
    )

    workflow.set_entry_point("analyzer")

    workflow.add_conditional_edges(
        "analyzer",
        route_after_analysis,
        {
            "policy_researcher": "policy_researcher",
            "end": END,
        },
    )

    workflow.add_edge(
        "policy_researcher",
        "reviewer",
    )

    workflow.add_edge(
        "reviewer",
        END,
    )

    return workflow.compile(
        checkpointer=checkpointer,
        interrupt_before=interrupt_before,
    )