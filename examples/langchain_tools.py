#!/usr/bin/env python3
"""Example: Using Meshy Tools with LangChain Agents.

This example demonstrates how to use Meshy AI tools with LangChain
to create an AI agent capable of generating 3D assets.

Requirements:
    pip install vendor-connectors[meshy,langchain]
    pip install langchain-anthropic  # For Claude as the LLM

Environment Variables:
    MESHY_API_KEY: Your Meshy API key
    ANTHROPIC_API_KEY: Your Anthropic API key (for Claude)
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    """Demonstrate LangChain integration with Meshy tools."""
    # Check for required environment variables
    missing = []
    if not os.getenv("MESHY_API_KEY"):
        missing.append("MESHY_API_KEY")
    if not os.getenv("ANTHROPIC_API_KEY"):
        missing.append("ANTHROPIC_API_KEY")

    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        return 1

    try:
        from langchain_anthropic import ChatAnthropic
        from langgraph.prebuilt import create_react_agent

        from vendor_connectors.meshy.tools import get_tools
    except ImportError as e:
        print(f"Error: Missing dependencies: {e}")
        print("Install with: pip install vendor-connectors[meshy,langchain] langchain-anthropic langgraph")
        return 1

    print("=== LangChain Agent with Meshy Tools ===\n")

    # Get Meshy tools for LangChain
    tools = get_tools()
    print(f"Available tools: {[t.name for t in tools]}\n")

    # Create the LLM
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)

    # Create the agent
    agent = create_react_agent(llm, tools)

    # Run a query
    query = "Generate a 3D model of a red sports car in preview mode"
    print(f"Query: {query}\n")
    print("Running agent (this may take a minute)...\n")

    try:
        result = agent.invoke({"messages": [("user", query)]})

        # Print the response
        for message in result["messages"]:
            if hasattr(message, "content") and message.content:
                role = message.__class__.__name__.replace("Message", "")
                print(f"[{role}]: {message.content[:500]}...")
                if len(message.content) > 500:
                    print("  (truncated)")

    except Exception as e:
        print(f"Error running agent: {e}")
        return 1

    print("\nDone!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
