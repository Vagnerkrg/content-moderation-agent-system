"""
Agente responsável pela análise inicial de comentários.

Este agente identifica possíveis problemas antes
da pesquisa de políticas.
"""

from content_moderation.agents.base import BaseAgent
from content_moderation.state.agent_state import AgentState


class AnalyzerAgent(BaseAgent):
    """
    Agente responsável pela análise inicial do comentário.

    A primeira versão utiliza regras simples baseadas
    em palavras-chave. Posteriormente, a análise poderá
    ser substituída por um LLM.
    """

    name = "analyzer"

    def execute(self, state: AgentState) -> AgentState:
        """
        Analisa o comentário recebido.

        Args:
            state: Estado atual do fluxo de moderação.

        Returns:
            Estado atualizado com a análise do agente.
        """
        comentario = state["comentario_original"].lower()

        palavras_problematicas = [
            "spam",
            "ofensa",
            "idiota",
            "burro",
        ]

        problema_detectado = any(
            palavra in comentario
            for palavra in palavras_problematicas
        )

        if problema_detectado:
            analise = (
                "Comentário potencialmente problemático "
                "detectado."
            )
        else:
            analise = (
                "Comentário classificado como positivo "
                "ou neutro."
            )

        return {
            **state,
            "analise_do_agente": analise,
        }