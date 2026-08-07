from content_moderation.graph.routing import route_after_analysis
from content_moderation.state.agent_state import AgentState


def test_route_problematic_comment_to_policy_researcher():
    state: AgentState = {
        "comentario_original": "Isso é spam.",
        "politicas_relevantes": "",
        "analise_do_agente": (
            "Comentário potencialmente problemático detectado."
        ),
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    result = route_after_analysis(state)

    assert result == "policy_researcher"


def test_route_neutral_comment_to_end():
    state: AgentState = {
        "comentario_original": "Gostei muito da aula.",
        "politicas_relevantes": "",
        "analise_do_agente": (
            "Comentário classificado como positivo ou neutro."
        ),
        "status_da_moderacao": "",
        "justificativa_final": "",
    }

    result = route_after_analysis(state)

    assert result == "end"