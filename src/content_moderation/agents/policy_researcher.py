"""
Agente responsável pela pesquisa de políticas de moderação.

Este agente consulta as diretrizes relevantes quando o analisador
identifica um comentário potencialmente problemático ou ambíguo.

A integração com a ferramenta de pesquisa é mantida desacoplada
para permitir testes determinísticos e facilitar a evolução da
arquitetura.
"""

from collections.abc import Callable

from content_moderation.state.agent_state import AgentState


class PolicyResearchError(Exception):
    """Erro controlado durante a pesquisa de políticas."""


def research_policies(
    state: AgentState,
    search_fn: Callable[[str], str] | None = None,
) -> AgentState:
    """
    Pesquisa políticas relevantes para o comentário analisado.

    Args:
        state: Estado compartilhado do fluxo de moderação.
        search_fn: Função opcional responsável pela pesquisa externa.
            É utilizada para desacoplar a integração com Tavily e
            facilitar testes unitários.

    Returns:
        Uma cópia do estado com `politicas_relevantes` atualizada.

    Raises:
        PolicyResearchError: Quando a pesquisa é solicitada, mas a
            ferramenta de pesquisa falha.
    """
    analysis = state["analise_do_agente"].lower()

    analysis_requires_research = (
        "potencialmente problemático" in analysis
        or "potencialmente ambíguo" in analysis
    )

    if not analysis_requires_research:
        return {
            **state,
            "politicas_relevantes": "",
        }

    comentario = state["comentario_original"].lower()

    if search_fn is None:
        if "spam" in comentario:
            politica = (
                "Política interna: conteúdo identificado como spam "
                "deve ser removido."
            )
        elif any(
            palavra in comentario
            for palavra in ("ofensa", "idiota", "burro")
        ):
            politica = (
                "Política interna: linguagem ofensiva ou inadequada "
                "deve ser editada antes da publicação."
            )
        elif any(
            indicador in comentario
            for indicador in (
                "talvez",
                "não tenho certeza",
                "nao tenho certeza",
                "pode ser",
                "não sei se",
                "nao sei se",
                "parece",
                "aparentemente",
                "possivelmente",
            )
        ):
            politica = (
                "Política interna: conteúdo ambíguo deve ser "
                "encaminhado para revisão humana antes da decisão final."
            )
        else:
            politica = (
                "Pesquisa de políticas não configurada. "
                "Utilizar diretrizes internas de moderação."
            )

        return {
            **state,
            "politicas_relevantes": politica,
        }

    try:
        resultado = search_fn(state["comentario_original"])
    except Exception as exc:
        raise PolicyResearchError(
            "Falha ao pesquisar as políticas de moderação."
        ) from exc

    if not resultado:
        return {
            **state,
            "politicas_relevantes": (
                "Nenhuma política relevante encontrada."
            ),
        }

    return {
        **state,
        "politicas_relevantes": resultado,
    }