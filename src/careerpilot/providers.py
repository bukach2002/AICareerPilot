"""Provider registry for OpenAI-compatible model APIs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from importlib.metadata import entry_points
from typing import Any


class ProviderError(Exception):
    """A provider is missing, invalid, or failed to load."""


@dataclass(frozen=True)
class Provider:
    id: str
    name: str
    base_url: str
    key_env: str
    key_url: str = ""
    default_model: str = "deepseek-v4.1-flash"


_PROVIDERS: dict[str, Provider] = {}
_PLUGINS_LOADED = False


def register_provider(provider: Provider) -> None:
    """Register an OpenAI-compatible provider, typically from an `careerpilot.providers` entry point."""
    if not re.fullmatch(r"[a-z][a-z0-9_-]*", provider.id):
        raise ProviderError(f"invalid provider id: {provider.id!r}")
    if not provider.name.strip() or not re.fullmatch(r"[A-Z_][A-Z0-9_]*", provider.key_env):
        raise ProviderError(f"provider {provider.id!r} needs a name and a valid key environment variable")
    if provider.id != "custom" and not provider.base_url.strip():
        raise ProviderError(f"provider {provider.id!r} needs an API base URL")
    if provider.id in _PROVIDERS:
        raise ProviderError(f"provider {provider.id!r} is already registered")
    _PROVIDERS[provider.id] = provider


def _load_plugins() -> None:
    global _PLUGINS_LOADED
    if _PLUGINS_LOADED:
        return
    _PLUGINS_LOADED = True
    for entry_point in entry_points(group="careerpilot.providers"):
        try:
            loaded: Any = entry_point.load()
            provider = loaded() if callable(loaded) else loaded
            if not isinstance(provider, Provider):
                raise ProviderError("entry point must provide a Provider or a zero-argument factory")
            register_provider(provider)
        except Exception as error:
            raise ProviderError(f"could not load provider plugin {entry_point.name!r}: {error}") from error


def get_provider(provider_id: str) -> Provider:
    _load_plugins()
    try:
        return _PROVIDERS[provider_id]
    except KeyError:
        raise ProviderError(f"unknown provider {provider_id!r}; choose from {', '.join(sorted(_PROVIDERS))}") from None


def credential_env_names() -> frozenset[str]:
    """The provider key variables that must not be inherited by the browser process."""
    _load_plugins()
    return frozenset(provider.key_env for provider in _PROVIDERS.values())


for _provider in (
    Provider("zro", "MoonMath Zro", "https://zro.moonmath.ai/v1", "ZRO_API_KEY", "https://zro.moonmath.ai/api-keys"),
    Provider("nvidia", "NVIDIA NIM", "https://integrate.api.nvidia.com/v1", "NVIDIA_API_KEY", "https://build.nvidia.com/", "deepseek-ai/deepseek-v4-flash"),
    Provider("openrouter", "OpenRouter", "https://openrouter.ai/api/v1", "OPENROUTER_API_KEY", "https://openrouter.ai/keys", "deepseek/deepseek-v4.1-flash"),
    Provider("custom", "Custom OpenAI-compatible API", "", "CAREERPILOT_API_KEY"),
):
    register_provider(_provider)
