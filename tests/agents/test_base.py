"""
Testes da arquitetura base dos agentes.
"""

import pytest

from content_moderation.agents.base import BaseAgent
from content_moderation.state.agent_state import AgentState


class TestAgent(BaseAgent):
    """Implementação mínima utilizada para testar o contrato."""

    name = "test-agent"

    def execute(self, state: AgentState) -> AgentState:
        """Retorna o estado recebido sem alterações."""
        return state


def test_base_agent_requires_execute():
    """Valida que uma implementação concreta pode executar."""

    agent = TestAgent()

    state: AgentState = {
        "comentario_original": "Comentário de teste.",
        "politicas_relevantes": "",
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    result = agent.execute(state)

    assert result == state
    assert agent.name == "test-agent"


def test_base_agent_cannot_be_instantiated():
    """Valida que BaseAgent é uma classe abstrata."""

    with pytest.raises(TypeError):
        BaseAgent()