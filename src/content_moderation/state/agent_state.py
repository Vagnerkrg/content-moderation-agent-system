"""
Estado compartilhado do sistema multiagente.

Define as informações que serão transportadas
entre os nós do LangGraph.
"""

from typing import TypedDict


class AgentState(TypedDict):
    """
    Estado principal do fluxo de moderação.

    Cada agente recebe este estado e retorna
    atualizações nos campos sob sua responsabilidade.
    """

    comentario_original: str
    politicas_relevantes: str
    analise_do_agente: str
    status_da_moderacao: str
    justificativa_final: str
    decisao_humana: str
    observacao_humana: str