"""
Classe base para os agentes do sistema de moderação.

Define o contrato comum que todos os agentes devem seguir.
"""

from abc import ABC, abstractmethod

from content_moderation.state.agent_state import AgentState


class BaseAgent(ABC):
    """
    Interface base para todos os agentes de moderação.

    Cada agente deve possuir um nome e implementar
    o método de execução responsável por processar
    o estado compartilhado do sistema.
    """

    name: str

    @abstractmethod
    def execute(self, state: AgentState) -> AgentState:
        """
        Executa o agente sobre o estado compartilhado.

        Args:
            state: Estado atual do fluxo de moderação.

        Returns:
            Estado atualizado pelo agente.
        """
        raise NotImplementedError