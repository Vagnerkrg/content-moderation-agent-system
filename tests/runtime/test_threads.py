"""Testes do gerenciamento dinâmico de threads."""

from uuid import UUID

from content_moderation.runtime.threads import (
    create_thread_config,
    create_thread_id,
    is_valid_thread_id,
)


def test_create_thread_id_returns_valid_uuid():
    """A função deve gerar um UUID válido."""

    thread_id = create_thread_id()

    UUID(thread_id)


def test_create_thread_id_generates_unique_ids():
    """Cada chamada deve gerar um identificador diferente."""

    first_thread_id = create_thread_id()
    second_thread_id = create_thread_id()

    assert first_thread_id != second_thread_id


def test_create_thread_config_generates_thread_id():
    """A configuração deve criar automaticamente um thread_id."""

    config = create_thread_config()

    assert "configurable" in config
    assert "thread_id" in config["configurable"]

    thread_id = config["configurable"]["thread_id"]

    assert isinstance(thread_id, str)
    assert is_valid_thread_id(thread_id)


def test_create_thread_config_preserves_existing_thread_id():
    """Uma configuração existente deve preservar o thread_id."""

    thread_id = create_thread_id()

    config = create_thread_config(thread_id)

    assert config["configurable"]["thread_id"] == thread_id


def test_different_configs_have_isolated_thread_ids():
    """Execuções diferentes devem possuir IDs independentes."""

    first_config = create_thread_config()
    second_config = create_thread_config()

    first_thread_id = first_config["configurable"]["thread_id"]
    second_thread_id = second_config["configurable"]["thread_id"]

    assert first_thread_id != second_thread_id


def test_is_valid_thread_id_accepts_valid_uuid():
    """UUIDs válidos devem ser aceitos."""

    thread_id = create_thread_id()

    assert is_valid_thread_id(thread_id) is True


def test_is_valid_thread_id_rejects_invalid_uuid():
    """Identificadores inválidos devem ser rejeitados."""

    assert is_valid_thread_id("invalid-thread-id") is False


def test_thread_id_can_be_reused_for_resume():
    """
    O mesmo thread_id deve poder ser reutilizado
    durante a retomada de uma execução.
    """

    thread_id = create_thread_id()

    initial_config = create_thread_config(thread_id)
    resume_config = create_thread_config(thread_id)

    assert (
        initial_config["configurable"]["thread_id"]
        == resume_config["configurable"]["thread_id"]
    )