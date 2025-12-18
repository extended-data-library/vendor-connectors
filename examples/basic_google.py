#!/usr/bin/env python3
"""Example: Basic Google Cloud Connector usage.

This example demonstrates how to use the Google Cloud connector to interact
with Google Workspace and Cloud Platform.

Requirements:
    pip install vendor-connectors[google]

Environment Variables:
    GOOGLE_SERVICE_ACCOUNT: JSON service account credentials
    GOOGLE_DOMAIN: Google Workspace domain (for Workspace operations)
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    """Demonstrate Google connector usage."""
    # Check for required environment variables
    if not os.getenv("GOOGLE_SERVICE_ACCOUNT"):
        print("Error: GOOGLE_SERVICE_ACCOUNT not set")
        print("Set your service account JSON as an environment variable")
        return 1

    try:
        from vendor_connectors import GoogleConnector, GoogleConnectorFull
    except ImportError:
        print("Error: Google connector not available")
        print("Install with: pip install vendor-connectors[google]")
        return 1

    # Basic connector
    print("=== Basic Google Connector ===")
    connector = GoogleConnector()
    print(f"Project ID: {connector.project_id or 'Not set'}")

    # Full connector with all operations
    print("\n=== Full Google Connector ===")
    full_connector = GoogleConnectorFull()

    # List projects
    print("\nCloud Projects:")
    try:
        projects = full_connector.list_projects()
        for project in projects[:5]:
            print(f"  - {project.get('name', 'Unnamed')} ({project.get('projectId')})")
        if len(projects) > 5:
            print(f"  ... and {len(projects) - 5} more")
    except Exception as e:
        print(f"  Could not list projects: {e}")

    # List workspace users (if domain configured)
    if os.getenv("GOOGLE_DOMAIN"):
        print("\nWorkspace Users:")
        try:
            users = full_connector.list_users()
            for user in users[:5]:
                email = user.get("primaryEmail", "Unknown")
                print(f"  - {email}")
            if len(users) > 5:
                print(f"  ... and {len(users) - 5} more")
        except Exception as e:
            print(f"  Could not list users: {e}")

    print("\nDone!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
