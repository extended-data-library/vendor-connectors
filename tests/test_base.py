"""Tests for VendorConnectorBase."""

from __future__ import annotations

from enum import Enum
from unittest.mock import patch

import httpx
import pytest

from vendor_connectors.base import ConnectorConfigurationError, VendorConnectorBase


class TestVendorConnectorBase:
    """Tests for VendorConnectorBase."""

    def test_api_key_property(self):
        """api_key property should return API key or raise error."""

        class MyConnector(VendorConnectorBase):
            API_KEY_ENV = "MY_API_KEY"

        # Test with API key provided
        connector = MyConnector(api_key="test-key")
        assert connector.api_key == "test-key"

        # Test with API key from environment
        with patch.dict("os.environ", {"MY_API_KEY": "env-key"}):
            connector = MyConnector()
            assert connector.api_key == "env-key"

        # Test without API key
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ConnectorConfigurationError, match="MY_API_KEY not set"):
                connector = MyConnector()
                connector.api_key

    def test_client_property(self):
        """client property should return httpx.Client instance."""

        class MyConnector(VendorConnectorBase):
            pass

        connector = MyConnector()
        assert isinstance(connector.client, httpx.Client)

    def test_tool_definitions(self):
        """Tool definition methods should return correct formats."""

        class MyEnum(Enum):
            OPTION1 = "option1"
            OPTION2 = "option2"

        class MyConnector(VendorConnectorBase):
            def my_tool(self, param1: str, param2: int, param3: bool, param4: list, param5: dict, param6: MyEnum):
                """A test tool."""
                pass

        connector = MyConnector()
        connector.register_tool(connector.my_tool)

        # Test Vercel AI SDK tool definitions
        vercel_tools = connector.get_vercel_ai_tool_definitions()
        assert len(vercel_tools) == 1
        tool = vercel_tools[0]
        assert tool.name == "my_tool"
        assert tool.description == "A test tool."
        assert tool.parameters.properties["param1"].type == "string"
        assert tool.parameters.properties["param2"].type == "number"
        assert tool.parameters.properties["param3"].type == "boolean"
        assert tool.parameters.properties["param4"].type == "array"
        assert tool.parameters.properties["param5"].type == "object"
        assert tool.parameters.properties["param6"].enum == ["option1", "option2"]

        # Test MCP tool definitions
        mcp_tools = connector.get_mcp_tool_definitions()
        assert len(mcp_tools) == 1
        tool = mcp_tools[0]
        assert tool["name"] == "my_tool"
        assert tool["description"] == "A test tool."
        assert tool["inputSchema"]["properties"]["param1"]["type"] == "string"
        assert tool["inputSchema"]["properties"]["param2"]["type"] == "number"
        assert tool["inputSchema"]["properties"]["param3"]["type"] == "boolean"
        assert tool["inputSchema"]["properties"]["param4"]["type"] == "array"
        assert tool["inputSchema"]["properties"]["param5"]["type"] == "object"
        assert tool["inputSchema"]["properties"]["param6"]["enum"] == ["option1", "option2"]
