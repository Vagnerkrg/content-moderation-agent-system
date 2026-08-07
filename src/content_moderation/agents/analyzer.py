"""
Agente responsável pela análise inicial de comentários.

Este agente identifica possíveis problemas
antes da pesquisa de políticas.
"""

from content_moderation.state.agent_state import AgentState


def analyze_comment(state: AgentState) -> AgentState:
    """
    Analisa o comentário recebido.

    Primeira versão baseada em regras simples.
    Posteriormente será substituída por um LLM.
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