"""
Configuração da persistência do LangGraph.

Este módulo centraliza a configuração do SQLite Checkpointer
utilizado para persistir o estado das execuções do workflow.
"""

from contextlib import AbstractContextManager
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATABASE_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATABASE_DIR / "checkpoints.db"


def get_checkpointer() -> AbstractContextManager[SqliteSaver]:
    """
    Retorna o context manager responsável pelo SQLite Checkpointer.

    O banco de dados é armazenado em:

        data/checkpoints.db

    Returns:
        Context manager que fornece uma instância de SqliteSaver.
    """
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    return SqliteSaver.from_conn_string(str(DATABASE_PATH))