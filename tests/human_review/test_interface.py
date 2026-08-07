"""Testes da interface de aprovação humana."""

from content_moderation.human_review.interface import (
    collect_human_review,
    display_review,
    request_human_decision,
)
from content_moderation.state.agent_state import AgentState


def create_review_state() -> AgentState:
    """Cria um estado representativo para os testes."""
    return {
        "comentario_original": "Isso é spam.",
        "politicas_relevantes": "A política de spam recomenda remoção.",
        "analise_do_agente": (
            "Comentário potencialmente problemático "
            "classificado como spam."
        ),
        "status_da_moderacao": "Remover",
        "justificativa_final": (
            "Comentário recomendado para remoção por spam."
        ),
        "decisao_humana": "",
        "observacao_humana": "",
    }


def test_display_review_shows_moderation_information(capsys):
    """A interface deve exibir as informações da revisão."""
    state = create_review_state()

    display_review(state)

    captured = capsys.readouterr()

    assert state["comentario_original"] in captured.out
    assert state["analise_do_agente"] in captured.out
    assert state["politicas_relevantes"] in captured.out
    assert state["status_da_moderacao"] in captured.out
    assert state["justificativa_final"] in captured.out


def test_request_human_decision_accepts_approval(monkeypatch):
    """A interface deve reconhecer uma aprovação."""
    monkeypatch.setattr("builtins.input", lambda _: "sim")

    decision = request_human_decision()

    assert decision == "aprovado"


def test_request_human_decision_accepts_rejection(monkeypatch):
    """A interface deve reconhecer uma rejeição."""
    monkeypatch.setattr("builtins.input", lambda _: "não")

    decision = request_human_decision()

    assert decision == "rejeitado"


def test_request_human_decision_accepts_short_answers(monkeypatch):
    """A interface deve aceitar respostas curtas."""
    monkeypatch.setattr("builtins.input", lambda _: "s")

    decision = request_human_decision()

    assert decision == "aprovado"


def test_request_human_decision_rejects_invalid_input(
    monkeypatch,
    capsys,
):
    """A interface deve solicitar novamente uma entrada inválida."""
    answers = iter(["talvez", "sim"])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    decision = request_human_decision()

    captured = capsys.readouterr()

    assert decision == "aprovado"
    assert "Entrada inválida" in captured.out


def test_collect_human_review_records_approval(monkeypatch):
    """A revisão humana deve registrar uma aprovação no estado."""
    state = create_review_state()

    monkeypatch.setattr("builtins.input", lambda _: "sim")

    result = collect_human_review(state)

    assert result["decisao_humana"] == "aprovado"
    assert result["observacao_humana"] == ""
    assert result["comentario_original"] == state["comentario_original"]


def test_collect_human_review_records_rejection(monkeypatch):
    """A revisão humana deve registrar uma rejeição no estado."""
    state = create_review_state()

    monkeypatch.setattr("builtins.input", lambda _: "não")

    result = collect_human_review(state)

    assert result["decisao_humana"] == "rejeitado"
    assert result["observacao_humana"] == ""
    assert result["status_da_moderacao"] == state["status_da_moderacao"]