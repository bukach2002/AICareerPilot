from __future__ import annotations

from pathlib import Path

import pytest

from careerpilot.config import ConfigError, load_config
from careerpilot.llm import make_client
from careerpilot.providers import Provider, ProviderError, get_provider, register_provider


def test_nvidia_provider_selects_its_endpoint_key_and_default_model(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NVIDIA_API_KEY", raising=False)
    (tmp_path / "careerpilot.yaml").write_text("provider: nvidia\n", encoding="utf-8")
    config = load_config(tmp_path)
    config.save_key("nvidia-test-key")

    client = make_client(load_config(tmp_path))
    assert str(client.base_url) == "https://integrate.api.nvidia.com/v1/"
    assert client.api_key == "nvidia-test-key"
    assert load_config(tmp_path).model == "deepseek-ai/deepseek-v4-flash"
    assert "NVIDIA_API_KEY=nvidia-test-key" in (tmp_path / ".env").read_text(encoding="utf-8")


def test_openrouter_provider_uses_namespaced_default_model(tmp_path: Path) -> None:
    (tmp_path / "careerpilot.yaml").write_text("provider: openrouter\n", encoding="utf-8")
    assert load_config(tmp_path).model == "deepseek/deepseek-v4.1-flash"


def test_switching_providers_uses_provider_specific_defaults_and_rebuilds_the_client(tmp_path: Path) -> None:
    from careerpilot.session import Session

    session = Session(tmp_path)
    session._client = object()  # type: ignore[assignment]
    session.change_setting("provider", "nvidia")
    assert session.config.provider == "nvidia"
    assert session.config.model == "deepseek-ai/deepseek-v4-flash"
    assert session._client is None
    session.close()


def test_provider_keys_are_kept_separately_and_environment_overrides_saved_key(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NVIDIA_API_KEY", raising=False)
    (tmp_path / "careerpilot.yaml").write_text("provider: nvidia\n", encoding="utf-8")
    nvidia = load_config(tmp_path)
    nvidia.save_key("nvidia-key")
    (tmp_path / "careerpilot.yaml").write_text("provider: zro\n", encoding="utf-8")
    zro = load_config(tmp_path)
    zro.save_key("zro-key")

    monkeypatch.setenv("NVIDIA_API_KEY", "environment-key")
    (tmp_path / "careerpilot.yaml").write_text("provider: nvidia\n", encoding="utf-8")
    assert load_config(tmp_path).api_key() == "environment-key"
    monkeypatch.delenv("NVIDIA_API_KEY")
    assert load_config(tmp_path).api_key() == "nvidia-key"
    assert "ZRO_API_KEY=zro-key" in (tmp_path / ".env").read_text(encoding="utf-8")


def test_custom_provider_uses_configured_openai_compatible_endpoint(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CAREERPILOT_API_KEY", raising=False)
    (tmp_path / "careerpilot.yaml").write_text(
        "provider: custom\napi_base_url: http://127.0.0.1:20128/v1\nmodel: local/model\n",
        encoding="utf-8",
    )
    config = load_config(tmp_path)
    config.save_key("local-key")

    client = make_client(load_config(tmp_path))
    assert str(client.base_url) == "http://127.0.0.1:20128/v1/"
    assert client.api_key == "local-key"
    assert load_config(tmp_path).model == "local/model"


def test_custom_provider_requires_an_endpoint(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CAREERPILOT_API_KEY", raising=False)
    (tmp_path / "careerpilot.yaml").write_text("provider: custom\n", encoding="utf-8")
    config = load_config(tmp_path)
    config.save_key("local-key")
    with pytest.raises(ConfigError, match="api_base_url"):
        make_client(load_config(tmp_path))


def test_provider_plugins_register_with_the_public_provider_api() -> None:
    provider = Provider("test-plugin", "Test plugin", "https://models.example/v1", "TEST_PLUGIN_API_KEY", default_model="test/model")
    register_provider(provider)
    assert get_provider("test-plugin") == provider
    with pytest.raises(ProviderError, match="already registered"):
        register_provider(provider)
