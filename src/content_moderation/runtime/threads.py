"""
Gerenciamento de identificadores de execução.

Este módulo fornece a criação de identificadores únicos
para cada execução do workflow de moderação.

O thread_id é utilizado pelo LangGraph como identificador
da execução e permite associar o estado persistido ao
checkpoint correto.
"""

from uuid import UUID, uuid4

from langgraph.types import RunnableConfig


def create_thread_id() -> str:
    """
    Gera um identificador único para uma execução.

    Returns:
        Uma string contendo um UUID válido.
    """
    return str(uuid4())


def create_thread_config(thread_id: str | None = None) -> RunnableConfig:
    """
    Cria a configuração utilizada pelo LangGraph.

    Quando nenhum thread_id é informado, um novo identificador
    é criado automaticamente.

    Args:
        thread_id: Identificador opcional da execução.

    Returns:
        Configuração contendo o thread_id no formato esperado
        pelo LangGraph.
    """
    execution_id = thread_id or create_thread_id()

    return {
        "configurable": {
            "thread_id": execution_id,
        }
    }


def is_valid_thread_id(thread_id: str) -> bool:
    """
    Verifica se uma string representa um UUID válido.

    Args:
        thread_id: Identificador que será validado.

    Returns:
        True quando o identificador é um UUID válido.
        False caso contrário.
    """
    try:
        UUID(thread_id)
    except (ValueError, AttributeError, TypeError):
        return False

    return True