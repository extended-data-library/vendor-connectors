"""Unified AI Connector interface.

This module provides AIConnector, the main interface for interacting
with AI providers through a unified API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vendor_connectors.ai.base import AIProvider, AIResponse, ToolCategory
from vendor_connectors.ai.providers import get_provider
from vendor_connectors.ai.tools.factory import ToolFactory
from vendor_connectors.ai.tools.registry import ToolRegistry

if TYPE_CHECKING:
    from vendor_connectors.ai.providers.base import BaseLLMProvider

__all__ = ["AIConnector"]


class AIConnector:
    """Unified interface for AI provider interactions.

    Provides a consistent API across all supported AI providers,
    with automatic tool registration and LangGraph workflow support.

    Thread Safety:
        AIConnector instances are NOT thread-safe during tool registration.
        Tool registration (register_connector_tools, register_tool) should
        be done in a single thread during initialization. Once tools are
        registered, chat() and invoke() methods can be called from multiple
        threads as they delegate to thread-safe LangChain components.

        The underlying ToolRegistry uses a singleton pattern and should be
        considered thread-safe for read operations after initialization.

    Example - Basic Chat:
        >>> connector = AIConnector(provider="anthropic")
        >>> response = connector.chat("Hello!")
        >>> print(response.content)

    Example - Chat with Tools:
        >>> from vendor_connectors.github import GithubConnector
        >>>
        >>> connector = AIConnector(provider="anthropic")
        >>> github = GithubConnector()
        >>> connector.register_connector_tools(github, ToolCategory.GITHUB)
        >>>
        >>> response = connector.invoke(
        ...     "List my repos and create an issue for the first one",
        ...     use_tools=True
        ... )
        >>> print(response.content)

    Example - Multiple Connectors:
        >>> from vendor_connectors.github import GithubConnector
        >>> from vendor_connectors.slack import SlackConnector
        >>>
        >>> ai = AIConnector(provider="openai", model="gpt-4o")
        >>>
        >>> # Register multiple connector types
        >>> ai.register_connector_tools(GithubConnector(), ToolCategory.GITHUB)
        >>> ai.register_connector_tools(SlackConnector(), ToolCategory.SLACK)
        >>>
        >>> # AI can now use both GitHub and Slack tools
        >>> response = ai.invoke(
        ...     "Check CI status on vendor-connectors repo and post to #dev",
        ...     use_tools=True
        ... )
    """

    def __init__(
        self,
        provider: str | AIProvider = "anthropic",
        model: str | None = None,
        api_key: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        langsmith_api_key: str | None = None,
        langsmith_project: str | None = None,
        **kwargs,
    ):
        """Initialize the AI connector.

        Args:
            provider: Provider name or AIProvider enum.
            model: Model identifier (uses provider default if not specified).
            api_key: API key for the provider.
            temperature: Sampling temperature (0-1).
            max_tokens: Maximum tokens to generate.
            langsmith_api_key: Optional LangSmith API key for tracing.
            langsmith_project: Optional LangSmith project name.
            **kwargs: Additional provider-specific arguments.
        """
        # Normalize provider to string
        provider_name = provider.value if isinstance(provider, AIProvider) else provider

        # Get and instantiate provider
        provider_class = get_provider(provider_name)
        self._provider: BaseLLMProvider = provider_class(
            model=model,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

        # Tool management - use singleton registry for workflow compatibility
        self._registry = ToolRegistry.get_instance()
        self._factory = ToolFactory()
        self._connector_instances: dict[ToolCategory, Any] = {}

        # LangSmith setup
        self._langsmith_api_key = langsmith_api_key
        self._langsmith_project = langsmith_project
        if langsmith_api_key:
            self._setup_langsmith()

    def _setup_langsmith(self) -> None:
        """Configure LangSmith tracing if API key is provided."""
        import os

        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = self._langsmith_api_key
        if self._langsmith_project:
            os.environ["LANGCHAIN_PROJECT"] = self._langsmith_project

    @property
    def provider(self) -> BaseLLMProvider:
        """Get the underlying provider instance."""
        return self._provider

    @property
    def model(self) -> str:
        """Get the current model identifier."""
        return self._provider.model

    @property
    def registry(self) -> ToolRegistry:
        """Get the tool registry."""
        return self._registry

    def chat(
        self,
        message: str,
        system_prompt: str | None = None,
        history: list | None = None,
    ) -> AIResponse:
        """Send a chat message without tools.

        Args:
            message: The user message.
            system_prompt: Optional system prompt.
            history: Optional conversation history (list of AIMessage).

        Returns:
            AIResponse with the model's response.
        """
        return self._provider.chat(
            message=message,
            system_prompt=system_prompt,
            history=history,
        )

    def invoke(
        self,
        message: str,
        use_tools: bool = True,
        categories: list[ToolCategory | None] = None,
        tool_names: list[str | None] = None,
        system_prompt: str | None = None,
        max_iterations: int = 10,
    ) -> AIResponse:
        """Invoke the AI with optional tool use.

        This creates a ReAct-style agent that can call tools and
        iterate until the task is complete.

        Args:
            message: The user message/task.
            use_tools: Whether to enable tool use.
            categories: Filter tools by categories.
            tool_names: Filter tools by specific names.
            system_prompt: Optional system prompt.
            max_iterations: Maximum tool-calling iterations.

        Returns:
            AIResponse with the final result.
        """
        if not use_tools or len(self._registry) == 0:
            return self.chat(message, system_prompt=system_prompt)

        # Get filtered tools
        tool_defs = self._registry.get_tools(categories=categories, names=tool_names)

        if not tool_defs:
            return self.chat(message, system_prompt=system_prompt)

        # Convert to LangChain tools with bound instances
        lc_tools = []
        for tool_def in tool_defs:
            instance = self._connector_instances.get(tool_def.category)
            tools = self._factory.to_langchain_tools([tool_def], connector_instance=instance)
            lc_tools.extend(tools)

        return self._provider.invoke_with_tools(
            message=message,
            tools=lc_tools,
            max_iterations=max_iterations,
            system_prompt=system_prompt,
        )

    def register_connector_tools(
        self,
        connector_instance: Any,
        category: ToolCategory,
        method_filter: callable | None = None,
    ) -> list[str]:
        """Register tools from a connector instance.

        Scans the connector class and registers tools for its methods.

        Args:
            connector_instance: The connector instance.
            category: Category for the tools.
            method_filter: Optional filter for method names.

        Returns:
            List of registered tool names.
        """
        # Store instance for method binding (both locally and in registry for workflows)
        self._connector_instances[category] = connector_instance
        self._registry.register_instance(category, connector_instance)

        # Generate tools from the class
        tools = self._factory.from_connector(
            type(connector_instance),
            category=category,
            method_filter=method_filter,
        )

        # Register all tools
        registered = []
        for tool in tools:
            try:
                self._registry.register(tool)
                registered.append(tool.name)
            except ValueError:
                # Tool already registered
                pass

        return registered

    def register_tool(
        self,
        name: str,
        description: str,
        handler: callable,
        category: ToolCategory,
    ) -> None:
        """Register a custom tool manually.

        Args:
            name: Unique tool name.
            description: Human-readable description.
            handler: Function that implements the tool.
            category: Tool category.
        """
        from vendor_connectors.ai.tools.factory import create_tool

        tool = create_tool(
            name=name,
            description=description,
            handler=handler,
            category=category,
        )
        self._registry.register(tool)

    def list_tools(self, category: ToolCategory | None = None) -> list[str]:
        """List registered tool names.

        Args:
            category: Optional category filter.

        Returns:
            List of tool names.
        """
        return self._registry.list_names(category=category)
