# Agent Instructions for Vendor Connectors

## Overview

**vendor-connectors** is a Python library providing unified access to multiple vendor APIs through a consistent interface. It serves as the **bridge between TypeScript (@agentic/control) and Python ecosystems** via MCP (Model Context Protocol).

## Quick Start

```bash
# Install with all connectors
pip install vendor-connectors[all]

# Install specific connectors
pip install vendor-connectors[google,cursor,github]

# CLI usage
vendor-connectors list                    # List available connectors
vendor-connectors methods jules           # List Jules methods
vendor-connectors call jules list_sources # Call a method

# Start MCP server
vendor-connectors-mcp
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  TypeScript (@agentic/control)                              │
└─────────────────────────────────────────────────────────────┘
                         │
                    MCP over stdio
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  vendor-connectors-mcp (this package)                       │
│  Auto-discovers connectors, exposes as MCP tools            │
└─────────────────────────────────────────────────────────────┘
                         │
                    Registry
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌────────┐      ┌────────┐      ┌────────┐
    │ Jules  │      │ Cursor │      │ GitHub │ ...
    └────────┘      └────────┘      └────────┘
```

## Key Components

### Registry (`vendor_connectors/registry.py`)
Entry point-based discovery of all connectors:
```python
from vendor_connectors import get_connector, list_connectors

# Discover all
print(list_connectors().keys())

# Factory instantiation
jules = get_connector('jules', api_key='...')
```

### MCP Server (`vendor_connectors/mcp.py`)
Exposes ALL connector methods as MCP tools automatically.

### CLI (`vendor_connectors/cli.py`)
Unified command-line access to all connectors.

## Adding a New Connector

1. Create the connector class extending `VendorConnectorBase`:
```python
# vendor_connectors/myvendor/__init__.py
from vendor_connectors.base import VendorConnectorBase

class MyVendorConnector(VendorConnectorBase):
    BASE_URL = "https://api.myvendor.com"
    API_KEY_ENV = "MYVENDOR_API_KEY"
    
    def my_operation(self, param: str) -> dict:
        """Do something."""
        return self.request("GET", f"/endpoint/{param}")
```

2. Add entry point in `pyproject.toml`:
```toml
[project.entry-points."vendor_connectors.connectors"]
myvendor = "vendor_connectors.myvendor:MyVendorConnector"
```

3. The connector is now available via CLI and MCP automatically!

## Available Connectors

| Connector | Env Var | Description |
|-----------|---------|-------------|
| `jules` | `JULES_API_KEY` | Google Jules AI Agent |
| `cursor` | `CURSOR_API_KEY` | Cursor Cloud Agents |
| `github` | `GITHUB_TOKEN` | GitHub API |
| `meshy` | `MESHY_API_KEY` | Meshy 3D Generation |
| `anthropic` | `ANTHROPIC_API_KEY` | Anthropic Claude |
| `aws` | `AWS_ACCESS_KEY_ID` | AWS Services |
| `google` | (service account) | Google Cloud/Workspace |
| `slack` | `SLACK_TOKEN` | Slack API |
| `vault` | `VAULT_TOKEN` | HashiCorp Vault |
| `zoom` | `ZOOM_API_KEY` | Zoom API |

## Development Commands

```bash
# Install for development
pip install -e ".[dev,all]"

# Run tests
pytest

# Type checking
mypy src/

# Linting
ruff check src/

# Build
python -m build
```

## MCP Integration

Configure in Claude Desktop or any MCP client:
```json
{
  "mcpServers": {
    "vendor-connectors": {
      "command": "vendor-connectors-mcp",
      "env": {
        "JULES_API_KEY": "...",
        "CURSOR_API_KEY": "...",
        "GITHUB_TOKEN": "..."
      }
    }
  }
}
```

## Related Packages

- `@agentic/triage` - Sigma-weighted complexity scoring (TypeScript)
- `@agentic/control` - GitHub Actions for orchestration (TypeScript)
- `@agentic/providers` - TypeScript provider implementations

## Current Work

See open PRs:
- #29 - Unified MCP/CLI + registry + Jules connector
- #24 - AI Tools for Vercel AI SDK compatibility
