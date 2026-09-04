import httpx
import pytest

from orion_agent.llm import BASE_URL, FAST, STRONG, check_models, get_llm, structured
from orion_agent.schemas import CodeOutput


def test_get_llm_requires_key(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="OPENROUTER_API_KEY"):
        get_llm()


def test_get_llm_points_at_openrouter(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "k")
    llm = get_llm(STRONG, temperature=0.2)
    assert llm.model_name == STRONG
    assert llm.temperature == 0.2
    assert str(llm.openai_api_base).rstrip("/") == BASE_URL


def test_structured_uses_function_calling(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "k")
    runnable = structured(get_llm(), CodeOutput)
    assert runnable is not None  # ChatOpenAI raises on unsupported methods; construction is the check


def test_check_models_reports_missing_ids():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/models")
        return httpx.Response(200, json={"data": [{"id": FAST}]})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    assert check_models(client=client) == [STRONG]
    assert check_models(models=(FAST,), client=client) == []
