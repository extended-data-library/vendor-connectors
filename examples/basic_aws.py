#!/usr/bin/env python3
"""Example: Basic AWS Connector usage.

This example demonstrates how to use the AWS connector to interact with
AWS Organizations and S3.

Requirements:
    pip install vendor-connectors[aws]

Environment Variables:
    AWS_ACCESS_KEY_ID: AWS access key
    AWS_SECRET_ACCESS_KEY: AWS secret key
    AWS_DEFAULT_REGION: AWS region (optional, defaults to us-east-1)
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    """Demonstrate AWS connector usage."""
    # Check for required environment variables
    if not os.getenv("AWS_ACCESS_KEY_ID"):
        print("Error: AWS_ACCESS_KEY_ID not set")
        print("Set your AWS credentials as environment variables")
        return 1

    try:
        from vendor_connectors import AWSConnector, AWSConnectorFull
    except ImportError:
        print("Error: AWS connector not available")
        print("Install with: pip install vendor-connectors[aws]")
        return 1

    # Basic connector - just session management
    print("=== Basic AWS Connector ===")
    connector = AWSConnector()
    print(f"Session created: {connector.session is not None}")

    # Full connector with all operations
    print("\n=== Full AWS Connector ===")
    full_connector = AWSConnectorFull()

    # List S3 buckets
    print("\nS3 Buckets:")
    try:
        buckets = full_connector.list_buckets()
        for bucket in buckets[:5]:  # Show first 5
            print(f"  - {bucket['Name']}")
        if len(buckets) > 5:
            print(f"  ... and {len(buckets) - 5} more")
    except Exception as e:
        print(f"  Could not list buckets: {e}")

    # List organization accounts (if using Organizations)
    print("\nOrganization Accounts:")
    try:
        accounts = full_connector.get_accounts()
        for account in accounts[:5]:
            print(f"  - {account['Name']} ({account['Id']})")
        if len(accounts) > 5:
            print(f"  ... and {len(accounts) - 5} more")
    except Exception as e:
        print(f"  Could not list accounts: {e}")

    print("\nDone!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
