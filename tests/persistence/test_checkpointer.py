"""Testes para a persistência do workflow."""

from pathlib import Path

from content_moderation.persistence.checkpointer import (
    DATABASE_PATH,
    get_checkpointer,
)


def test_checkpointer_database_path_is_configured():
    """O caminho do banco SQLite deve estar configurado corretamente."""

    assert DATABASE_PATH.name == "checkpoints.db"
    assert DATABASE_PATH.parent.name == "data"


def test_checkpointer_context_manager_is_available():
    """O checkpointer deve fornecer um context manager funcional."""

    checkpointer_context = get_checkpointer()

    assert checkpointer_context is not None


def test_checkpointer_database_directory_is_created():
    """O diretório de persistência deve existir após obter o checkpointer."""

    get_checkpointer()

    assert Path(DATABASE_PATH).parent.exists()