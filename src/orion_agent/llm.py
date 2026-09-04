"""Chat models via OpenRouter."""

from __future__ import annotations

import os

import httpx
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI

BASE_URL = "https://openrouter.ai/api/v1"
FAST = "openai/gpt-4o-mini"
STRONG = "anthropic/claude-sonnet-4.5"


def get_llm(model: str = FAST, temperature: float = 0.0, api_key: str | None = None) -> ChatOpenAI:
    """Return a chat model pointed at OpenRouter, or raise if the key is missing."""
    key = api_key or os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is not set. Copy .env.example to .env and add your key.")
    return ChatOpenAI(model=model, api_key=key, base_url=BASE_URL, temperature=temperature)


def structured(llm: ChatOpenAI, schema: type) -> Runnable:
    """Wrap a model so it returns instances of `schema` instead of free text."""
    # function_calling is the one method every OpenRouter provider translates;
    # json_schema mode is OpenAI-only.
    return llm.with_structured_output(schema, method="function_calling")


def check_models(models: tuple[str, ...] = (FAST, STRONG), client: httpx.Client | None = None) -> list[str]:
    """Return the model IDs in `models` that OpenRouter does not list."""
    client = client or httpx.Client(timeout=15)
    data = client.get(f"{BASE_URL}/models").json()["data"]
    available = {m["id"] for m in data}
    return [m for m in models if m not in available]
