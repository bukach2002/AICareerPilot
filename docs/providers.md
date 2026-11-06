# Model providers

CareerPilot uses the OpenAI Chat Completions API, including JSON-schema outputs and tool calls. The provider setting chooses the API endpoint and the key environment variable; each workflow continues using its own configured model ID.

## Built-in providers

| Provider ID | API base URL | Key environment variable | Default model |
|---|---|---|---|
| `zro` | `https://zro.moonmath.ai/v1` | `ZRO_API_KEY` | `deepseek-v4.1-flash` |
| `nvidia` | `https://integrate.api.nvidia.com/v1` | `NVIDIA_API_KEY` | `deepseek-ai/deepseek-v4-flash` |
| `openrouter` | `https://openrouter.ai/api/v1` | `OPENROUTER_API_KEY` | `deepseek/deepseek-v4.1-flash` |
| `custom` | Set `api_base_url` | `CAREERPILOT_API_KEY` | `deepseek-v4.1-flash` |

Model catalogs change; choose a model ID currently available from your provider. NVIDIA's model IDs include the provider namespace. Get keys from [Zro](https://zro.moonmath.ai/api-keys), [NVIDIA Build](https://build.nvidia.com/), or [OpenRouter](https://openrouter.ai/keys).

## Select a provider

Press `e` in the app and change **Model provider** to `nvidia`, `openrouter`, or `custom`. For `custom`, also set **API base URL** to the endpoint's OpenAI-compatible base URL. Then set the provider's model ID under **Forms model**, **Scoring model**, **Search plan model**, and **Shortlist model** as needed. Changing providers may require a new key; CareerPilot saves each provider's key separately in `~/.careerpilot/.env`.

For a local OmniRoute instance, set **Model provider** to `custom` and **API base URL** to the URL OmniRoute exposes for its OpenAI-compatible API. The URL depends on how that instance is configured.

Or configure the same values in `~/.careerpilot/careerpilot.yaml`:

```yaml
provider: nvidia
model: deepseek-ai/deepseek-v4-flash
quick_model: deepseek-ai/deepseek-v4-flash
judge_model: deepseek-ai/deepseek-v4-flash
decision_model: deepseek-ai/deepseek-v4-flash
```

For a custom endpoint:

```yaml
provider: custom
api_base_url: http://localhost:YOUR_PORT/v1
model: your-model-id
quick_model: your-model-id
judge_model: your-model-id
decision_model: your-model-id
```

The corresponding API key is requested in the terminal and stored in the local `.env`; do not commit that file.

## Install a provider plugin

Third-party packages can register provider presets through the `careerpilot.providers` Python entry-point group. A plugin returns a `Provider`:

```python
from careerpilot.providers import Provider


def provider() -> Provider:
    return Provider(
        id="my-provider",
        name="My Provider",
        base_url="https://api.example/v1",
        key_env="MY_PROVIDER_API_KEY",
        key_url="https://api.example/keys",
        default_model="my-model",
    )
```

Declare it in the package's `pyproject.toml`:

```toml
[project.entry-points."careerpilot.providers"]
my-provider = "my_provider:provider"
```

Provider plugins must expose an OpenAI-compatible Chat Completions API with JSON-schema response formats and tool calls. Unsupported or failing provider plugins produce an explicit startup error.
