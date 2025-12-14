# Building Connector Tools

This guide explains how to add AI-callable tools to a connector in vendor-connectors.

## Overview

Each connector can expose tools that AI agents can call. Tools are framework-agnostic Python functions with wrappers for:
- **LangChain** - `StructuredTool` objects
- **CrewAI** - CrewAI `@tool` decorated functions
- **Strands/Plain** - Raw Python functions with type hints

## Pattern: One `tools.py` Per Connector

Each connector with AI tools has a `tools.py` file:

```
vendor_connectors/
├── aws/
│   ├── __init__.py      # AWSConnector class
│   └── tools.py         # AI tools ← YOU ADD THIS
├── github/
│   ├── __init__.py
│   └── tools.py
└── meshy/
    ├── __init__.py
    └── tools.py          # Reference implementation
```

## Step-by-Step Guide

### 1. Identify Key Operations

Choose operations that are:
- **Safe** - Prefer read operations over writes for AI agents
- **Useful** - Common operations agents would want to perform
- **Self-contained** - Don't require complex state management

Good examples:
- `list_*` - List resources
- `get_*` - Get specific resource
- `search_*` - Search/filter resources

### 2. Create `tools.py`

Use this template structure:

```python
"""AI framework tools for {CONNECTOR_NAME} operations.

This module provides tools for {CONNECTOR_NAME} operations that work with
multiple AI agent frameworks.

Supported Frameworks:
- LangChain (via langchain-core) - get_langchain_tools()
- CrewAI - get_crewai_tools()
- AWS Strands - get_strands_tools() (plain functions)
- Auto-detection - get_tools() picks the best available

Tools provided:
- tool_one: Description
- tool_two: Description

Usage:
    from vendor_connectors.{connector}.tools import get_tools
    tools = get_tools()  # Returns best format for installed framework
"""

from __future__ import annotations

from typing import Any


# =============================================================================
# Tool Implementation Functions
# =============================================================================


def list_something(
    prefix: str = "",
    max_results: int = 100,
) -> list[dict[str, Any]]:
    """List something from the service.

    Args:
        prefix: Filter by prefix
        max_results: Maximum results to return

    Returns:
        List of items with their properties
    """
    from vendor_connectors.{connector} import {Connector}Full
    
    connector = {Connector}Full()
    items = connector.list_something()
    
    # Transform to consistent output format
    result = []
    for item_id, data in list(items.items())[:max_results]:
        result.append(
            {
                "id": item_id,
                "name": data.get("name", ""),
                # ... other fields
            }
        )
    
    return result


# =============================================================================
# Tool Definitions
# =============================================================================

TOOL_DEFINITIONS = [
    {
        "name": "{connector}_list_something",
        "description": "List something from {Service}. Returns items with their properties.",
        "func": list_something,
    },
    # Add more tools...
]


# =============================================================================
# Framework-Specific Getters
# =============================================================================


def get_langchain_tools() -> list[Any]:
    """Get all tools as LangChain StructuredTools."""
    try:
        from langchain_core.tools import StructuredTool
    except ImportError as e:
        raise ImportError(
            "langchain-core is required for LangChain tools.\nInstall with: pip install vendor-connectors[langchain]"
        ) from e

    return [
        StructuredTool.from_function(
            func=defn["func"],
            name=defn["name"],
            description=defn["description"],
        )
        for defn in TOOL_DEFINITIONS
    ]


def get_crewai_tools() -> list[Any]:
    """Get all tools as CrewAI tools."""
    try:
        from crewai.tools import tool as crewai_tool
    except ImportError as e:
        raise ImportError(
            "crewai is required for CrewAI tools.\nInstall with: pip install vendor-connectors[crewai]"
        ) from e

    tools = []
    for defn in TOOL_DEFINITIONS:
        wrapped = crewai_tool(defn["name"])(defn["func"])
        wrapped.description = defn["description"]
        tools.append(wrapped)

    return tools


def get_strands_tools() -> list[Any]:
    """Get all tools as plain Python functions for AWS Strands."""
    return [defn["func"] for defn in TOOL_DEFINITIONS]


def get_tools(framework: str = "auto") -> list[Any]:
    """Get tools for the specified or auto-detected framework.

    Args:
        framework: Framework to use. Options:
            - "auto" (default): Auto-detect based on installed packages
            - "langchain": Force LangChain StructuredTools
            - "crewai": Force CrewAI tools
            - "strands": Force plain functions for Strands
            - "functions": Force plain functions (alias for strands)

    Returns:
        List of tools in the appropriate format.
    """
    from vendor_connectors._compat import is_available

    if framework == "auto":
        if is_available("crewai"):
            return get_crewai_tools()
        if is_available("langchain_core"):
            return get_langchain_tools()
        return get_strands_tools()

    if framework == "langchain":
        return get_langchain_tools()
    if framework == "crewai":
        return get_crewai_tools()
    if framework in ("strands", "functions"):
        return get_strands_tools()

    raise ValueError(f"Unknown framework: {framework}")


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "get_tools",
    "get_langchain_tools",
    "get_crewai_tools",
    "get_strands_tools",
    "TOOL_DEFINITIONS",
    # Add raw functions here
]
```

### 3. Write Tests

Create `tests/test_{connector}_tools.py`:

```python
"""Tests for {CONNECTOR} AI tools."""

from unittest.mock import MagicMock, patch

import pytest

CONNECTOR_PATCH = "vendor_connectors.{connector}.{Connector}Full"


class TestToolDefinitions:
    """Test tool definitions."""

    def test_tool_definitions_exist(self):
        from vendor_connectors.{connector}.tools import TOOL_DEFINITIONS
        assert len(TOOL_DEFINITIONS) > 0

    def test_all_tools_have_required_fields(self):
        from vendor_connectors.{connector}.tools import TOOL_DEFINITIONS
        for defn in TOOL_DEFINITIONS:
            assert "name" in defn
            assert "description" in defn
            assert "func" in defn
            assert callable(defn["func"])

    def test_tool_names_prefixed(self):
        from vendor_connectors.{connector}.tools import TOOL_DEFINITIONS
        for defn in TOOL_DEFINITIONS:
            assert defn["name"].startswith("{connector}_")


class TestListSomething:
    """Test list_something tool."""

    @patch(CONNECTOR_PATCH)
    def test_list_something_basic(self, mock_connector_class):
        from vendor_connectors.{connector}.tools import list_something

        mock_connector = MagicMock()
        mock_connector.list_something.return_value = {
            "item-1": {"name": "Test Item"},
        }
        mock_connector_class.return_value = mock_connector

        result = list_something()

        assert len(result) == 1
        assert result[0]["id"] == "item-1"


class TestGetTools:
    """Test framework getters."""

    def test_get_strands_tools(self):
        from vendor_connectors.{connector}.tools import get_strands_tools
        tools = get_strands_tools()
        assert len(tools) > 0
        assert all(callable(t) for t in tools)

    def test_get_tools_invalid_framework(self):
        from vendor_connectors.{connector}.tools import get_tools
        with pytest.raises(ValueError, match="Unknown framework"):
            get_tools(framework="invalid")
```

### 4. Naming Conventions

- **Tool names**: `{connector}_{action}_{resource}` (e.g., `aws_list_secrets`, `github_get_repository`)
- **Function names**: `{action}_{resource}` (e.g., `list_secrets`, `get_repository`)
- **Prefix all tools** with the connector name to avoid conflicts

### 5. Return Format Guidelines

- Return **lists of dicts** for collection operations
- Use **consistent field names** (snake_case)
- Include an **id** or unique identifier for each item
- Keep responses **JSON-serializable** (no datetime objects, use strings)

### 6. Error Handling

Let connector exceptions propagate - the AI framework will handle them.
Don't catch and re-raise with custom messages unless adding value.

## Reference Implementations

- **AWS**: `src/vendor_connectors/aws/tools.py` - Secrets, S3, Organizations, SSO
- **Meshy**: `src/vendor_connectors/meshy/tools.py` - 3D generation tools

## Checklist

Before submitting your PR:

- [ ] Created `{connector}/tools.py` following the template
- [ ] All tool names prefixed with connector name
- [ ] Tool functions have docstrings with Args and Returns
- [ ] Added `TOOL_DEFINITIONS` list with all tools
- [ ] Implemented all four getters (`get_tools`, `get_langchain_tools`, etc.)
- [ ] Created tests in `tests/test_{connector}_tools.py`
- [ ] Tests mock the connector class, not real API calls
- [ ] All tests pass: `uv run pytest tests/test_{connector}_tools.py`
- [ ] Lint passes: `uvx ruff check && uvx ruff format`
