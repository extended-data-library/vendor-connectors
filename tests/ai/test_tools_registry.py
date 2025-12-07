"""Tests for vendor_connectors.ai.tools.registry module."""

import pytest

from vendor_connectors.ai.base import ToolCategory, ToolDefinition, ToolParameter
from vendor_connectors.ai.tools.registry import ToolRegistry


class TestToolRegistryClass:
    """Tests for the ToolRegistry class in tools.registry module."""

    def setup_method(self):
        """Create fresh registry and reset singleton for each test."""
        # Reset singleton for isolation
        ToolRegistry._instance = None
        self.registry = ToolRegistry()

    def teardown_method(self):
        """Clean up singleton state."""
        ToolRegistry._instance = None

    def _create_tool(
        self,
        name: str,
        category: ToolCategory = ToolCategory.UTILITY,
    ) -> ToolDefinition:
        """Helper to create test tool definitions."""
        return ToolDefinition(
            name=name,
            description=f"Test tool: {name}",
            category=category,
            parameters={
                "input": ToolParameter(
                    name="input",
                    description="Input value",
                    type=str,
                    required=True,
                ),
            },
            handler=lambda input: f"Processed: {input}",
        )

    def test_register_tool(self):
        """Test registering a tool."""
        tool = self._create_tool("test_register")
        self.registry.register(tool)

        assert "test_register" in self.registry
        assert len(self.registry) == 1

    def test_register_duplicate_raises(self):
        """Test that registering duplicate raises ValueError."""
        tool = self._create_tool("duplicate_tool")
        self.registry.register(tool)

        with pytest.raises(ValueError, match="already registered"):
            self.registry.register(tool)

    def test_unregister_tool(self):
        """Test unregistering a tool."""
        tool = self._create_tool("to_unregister")
        self.registry.register(tool)
        assert "to_unregister" in self.registry

        self.registry.unregister("to_unregister")
        assert "to_unregister" not in self.registry

    def test_unregister_nonexistent_is_safe(self):
        """Test that unregistering nonexistent tool doesn't raise."""
        self.registry.unregister("nonexistent")  # Should not raise

    def test_get_tool(self):
        """Test getting a tool by name."""
        tool = self._create_tool("get_me")
        self.registry.register(tool)

        retrieved = self.registry.get("get_me")
        assert retrieved is tool

    def test_get_nonexistent_returns_none(self):
        """Test that getting nonexistent tool returns None."""
        result = self.registry.get("nonexistent")
        assert result is None

    def test_get_tools_all(self):
        """Test getting all tools."""
        tool1 = self._create_tool("tool1", ToolCategory.AWS)
        tool2 = self._create_tool("tool2", ToolCategory.GITHUB)
        self.registry.register(tool1)
        self.registry.register(tool2)

        tools = self.registry.get_tools()
        assert len(tools) == 2

    def test_get_tools_by_category(self):
        """Test filtering tools by category."""
        aws_tool = self._create_tool("aws_tool", ToolCategory.AWS)
        github_tool = self._create_tool("github_tool", ToolCategory.GITHUB)
        meshy_tool = self._create_tool("meshy_tool", ToolCategory.MESHY)

        self.registry.register(aws_tool)
        self.registry.register(github_tool)
        self.registry.register(meshy_tool)

        aws_tools = self.registry.get_tools(categories=[ToolCategory.AWS])
        assert len(aws_tools) == 1
        assert aws_tools[0].name == "aws_tool"

    def test_get_tools_by_multiple_categories(self):
        """Test filtering by multiple categories."""
        aws_tool = self._create_tool("aws_tool", ToolCategory.AWS)
        github_tool = self._create_tool("github_tool", ToolCategory.GITHUB)
        slack_tool = self._create_tool("slack_tool", ToolCategory.SLACK)

        self.registry.register(aws_tool)
        self.registry.register(github_tool)
        self.registry.register(slack_tool)

        tools = self.registry.get_tools(categories=[ToolCategory.AWS, ToolCategory.GITHUB])
        assert len(tools) == 2
        names = {t.name for t in tools}
        assert names == {"aws_tool", "github_tool"}

    def test_get_tools_by_names(self):
        """Test filtering tools by specific names."""
        tool1 = self._create_tool("specific_1")
        tool2 = self._create_tool("specific_2")
        tool3 = self._create_tool("other")

        self.registry.register(tool1)
        self.registry.register(tool2)
        self.registry.register(tool3)

        tools = self.registry.get_tools(names=["specific_1", "specific_2"])
        assert len(tools) == 2

    def test_list_names(self):
        """Test listing tool names."""
        tool1 = self._create_tool("list_test_1")
        tool2 = self._create_tool("list_test_2")

        self.registry.register(tool1)
        self.registry.register(tool2)

        names = self.registry.list_names()
        assert "list_test_1" in names
        assert "list_test_2" in names

    def test_list_names_by_category(self):
        """Test listing tool names filtered by category."""
        aws_tool = self._create_tool("aws_list", ToolCategory.AWS)
        meshy_tool = self._create_tool("meshy_list", ToolCategory.MESHY)

        self.registry.register(aws_tool)
        self.registry.register(meshy_tool)

        aws_names = self.registry.list_names(category=ToolCategory.AWS)
        assert "aws_list" in aws_names
        assert "meshy_list" not in aws_names

    def test_list_categories(self):
        """Test listing categories with registered tools."""
        aws_tool = self._create_tool("cat_aws", ToolCategory.AWS)
        github_tool = self._create_tool("cat_github", ToolCategory.GITHUB)

        self.registry.register(aws_tool)
        self.registry.register(github_tool)

        categories = self.registry.list_categories()
        assert ToolCategory.AWS in categories
        assert ToolCategory.GITHUB in categories

    def test_clear(self):
        """Test clearing all tools."""
        tool1 = self._create_tool("clear_1")
        tool2 = self._create_tool("clear_2")

        self.registry.register(tool1)
        self.registry.register(tool2)
        assert len(self.registry) == 2

        self.registry.clear()
        assert len(self.registry) == 0

    def test_singleton_get_instance(self):
        """Test singleton access via get_instance()."""
        instance1 = ToolRegistry.get_instance()
        instance2 = ToolRegistry.get_instance()
        assert instance1 is instance2

    def test_contains_dunder(self):
        """Test __contains__ method."""
        tool = self._create_tool("contains_test")
        self.registry.register(tool)

        assert "contains_test" in self.registry
        assert "nonexistent" not in self.registry

    def test_len_dunder(self):
        """Test __len__ method."""
        assert len(self.registry) == 0

        tool1 = self._create_tool("len_1")
        self.registry.register(tool1)
        assert len(self.registry) == 1

        tool2 = self._create_tool("len_2")
        self.registry.register(tool2)
        assert len(self.registry) == 2


class TestConnectorInstanceManagement:
    """Tests for connector instance registration in ToolRegistry."""

    def setup_method(self):
        """Create fresh registry for each test."""
        ToolRegistry._instance = None
        self.registry = ToolRegistry()

    def teardown_method(self):
        """Clean up singleton state."""
        ToolRegistry._instance = None

    def test_register_connector_instance(self):
        """Test registering a connector instance."""

        class MockAWSConnector:
            pass

        instance = MockAWSConnector()
        self.registry.register_instance(ToolCategory.AWS, instance)

        retrieved = self.registry.get_connector_instance(ToolCategory.AWS)
        assert retrieved is instance

    def test_get_unregistered_connector_returns_none(self):
        """Test getting unregistered connector returns None."""
        result = self.registry.get_connector_instance(ToolCategory.SLACK)
        assert result is None

    def test_multiple_connector_instances(self):
        """Test registering multiple connector instances."""

        class MockAWS:
            pass

        class MockGitHub:
            pass

        aws = MockAWS()
        github = MockGitHub()

        self.registry.register_instance(ToolCategory.AWS, aws)
        self.registry.register_instance(ToolCategory.GITHUB, github)

        assert self.registry.get_connector_instance(ToolCategory.AWS) is aws
        assert self.registry.get_connector_instance(ToolCategory.GITHUB) is github
