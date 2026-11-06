"""The one model gateway: MoonMath Zro's OpenAI-compatible chat API."""

from __future__ import annotations

import json
from typing import Any

from openai import (
    APIConnectionError,
    APITimeoutError,
    AsyncOpenAI,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    RateLimitError,
)

from careerpilot.config import Config, ConfigError

# The SDK's own default is ten minutes a try, and a model that hangs would hold a judgment that long.
TIMEOUT = 180.0


def refused(error: BaseException) -> bool:
    """Whether the provider refused its key: the one failure that must be fixed before anything can work."""
    return isinstance(error, AuthenticationError)


def explain(error: Exception) -> str:
    """What a failed model call says in plain words. The detail stays after it, and the key is never in it."""
    if isinstance(error, APITimeoutError):
        return f"The model provider did not answer in time. Try again in a moment. ({error})"
    if isinstance(error, APIConnectionError):
        return f"The model provider cannot be reached: check your internet connection and try again. ({error})"
    if isinstance(error, RateLimitError):
        return f"The model provider is asking CareerPilot to slow down: wait a few minutes and try again. ({error})"
    if isinstance(error, InternalServerError):
        return f"The model provider failed on its side: try again in a few minutes. ({error})"
    if isinstance(error, BadRequestError):
        return f"The model provider rejected the request. ({error})"
    return f"Something failed: {error}"


def make_client(config: Config) -> AsyncOpenAI:
    key = config.api_key()
    if not key:
        key_url = f" at {config.provider_key_url}" if config.provider_key_url else ""
        raise ConfigError(f"no {config.provider_name} API key: set {config.provider_key_env}{key_url}")
    if not config.base_url:
        raise ConfigError("set api_base_url for the custom provider")
    # The SDK retries 429s and 5xx itself and honours Retry-After.
    return AsyncOpenAI(base_url=config.base_url, api_key=key, max_retries=5, timeout=TIMEOUT)


async def structured(client: AsyncOpenAI, model: str, system: str, user: str, name: str, schema: dict[str, Any]) -> dict[str, Any]:
    """One answer that follows `schema`. A reply that is not that JSON raises: nothing is guessed from it."""
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        response_format={"type": "json_schema", "json_schema": {"name": name, "strict": True, "schema": schema}},
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError(f"the model gave no {name}")
    return json.loads(content)
