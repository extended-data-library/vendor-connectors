#!/usr/bin/env python3
"""Example: Running the Meshy MCP Server.

This example demonstrates how to run the Model Context Protocol (MCP)
server for Meshy AI, enabling integration with Claude Desktop and
other MCP-compatible clients.

Requirements:
    pip install vendor-connectors[meshy,mcp]

Environment Variables:
    MESHY_API_KEY: Your Meshy API key

Usage:
    # Run the server (connects via stdio)
    python examples/mcp_server.py

    # Or use the installed command
    meshy-mcp

    # Configure in Claude Desktop's config.json:
    {
        "mcpServers": {
            "meshy": {
                "command": "meshy-mcp",
                "env": {
                    "MESHY_API_KEY": "your-api-key"
                }
            }
        }
    }
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    """Run the Meshy MCP server."""
    # Check for required environment variables
    if not os.getenv("MESHY_API_KEY"):
        print("Error: MESHY_API_KEY not set", file=sys.stderr)
        print("Get your API key at https://meshy.ai", file=sys.stderr)
        return 1

    try:
        from vendor_connectors.meshy.mcp import run_server
    except ImportError as e:
        print(f"Error: Missing dependencies: {e}", file=sys.stderr)
        print(
            "Install with: pip install vendor-connectors[meshy,mcp]",
            file=sys.stderr,
        )
        return 1

    print("Starting Meshy MCP Server...", file=sys.stderr)
    print("Connect via stdio (e.g., from Claude Desktop)", file=sys.stderr)
    print("Press Ctrl+C to stop\n", file=sys.stderr)

    try:
        # Run the server (blocks until stopped)
        run_server()
    except KeyboardInterrupt:
        print("\nServer stopped", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
