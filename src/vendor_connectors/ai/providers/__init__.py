<<<<<<< HEAD
"""LLM Provider implementations.

Available providers:
- AnthropicProvider: Claude models via langchain-anthropic
- OpenAIProvider: GPT models via langchain-openai
- GoogleProvider: Gemini models via langchain-google-genai
- XAIProvider: Grok models via langchain-xai
- OllamaProvider: Local models via langchain-ollama
"""

from vendor_connectors.ai.providers.base import BaseLLMProvider

__all__ = ["BaseLLMProvider", "get_provider"]

# Lazy imports to avoid requiring all provider dependencies
_PROVIDER_MAP = {
    "anthropic": ("vendor_connectors.ai.providers.anthropic", "AnthropicProvider"),
    "openai": ("vendor_connectors.ai.providers.openai", "OpenAIProvider"),
    "google": ("vendor_connectors.ai.providers.google", "GoogleProvider"),
    "xai": ("vendor_connectors.ai.providers.xai", "XAIProvider"),
    "ollama": ("vendor_connectors.ai.providers.ollama", "OllamaProvider"),
}


def get_provider(name: str) -> type[BaseLLMProvider]:
    """Get a provider class by name.

    Args:
        name: Provider name (anthropic, openai, google, xai, ollama).

    Returns:
        Provider class.

    Raises:
        ValueError: If provider name is unknown.
        ImportError: If provider dependencies are not installed.
    """
    if name not in _PROVIDER_MAP:
        raise ValueError(f"Unknown provider: {name}. Available: {', '.join(_PROVIDER_MAP.keys())}")

    module_path, class_name = _PROVIDER_MAP[name]

    import importlib

    module = importlib.import_module(module_path)
    return getattr(module, class_name)
=======
"""AI Framework Providers for vendor connector tools.

This package contains integrations with various AI agent frameworks:
- crewai: CrewAI tool provider
- mcp: Model Context Protocol server

These providers convert tool definitions into framework-specific formats.

Example:
    from vendor_connectors.ai.providers.crewai import get_tools

    tools = get_tools()  # Returns CrewAI BaseTool instances
"""

from __future__ import annotations

__all__ = ["crewai", "mcp"]
>>>>>>> 0cfc317 (feat(meshy): Add Meshy connector and AI package foundation (#23))
