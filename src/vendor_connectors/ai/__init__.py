"""AI Sub-Package for vendor-connectors.

This package provides AI framework integrations for vendor connectors,
enabling them to be used as tools in LangChain, CrewAI, MCP, and other
AI agent frameworks.

Example:
    from vendor_connectors.ai import ToolCategory, ToolDefinition, ToolParameter
    from vendor_connectors.ai.tools.meshy_tools import get_meshy_tools

    tools = get_meshy_tools()
    for tool in tools:
        print(f"{tool.name}: {tool.description}")
"""

from vendor_connectors.ai.base import (
    AIMessage,
    AIProvider,
    AIResponse,
    AIRole,
    ToolCategory,
    ToolDefinition,
    ToolParameter,
    ToolResult,
)

__all__ = [
    # AI types
    "AIMessage",
    "AIProvider",
    "AIResponse",
    "AIRole",
    # Tool types
    "ToolCategory",
    "ToolDefinition",
    "ToolParameter",
    "ToolResult",
]
