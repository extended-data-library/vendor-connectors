#!/usr/bin/env python3
"""Example: Meshy AI 3D Generation.

This example demonstrates how to use the Meshy connector for AI-powered
3D asset generation.

Requirements:
    pip install vendor-connectors[meshy]

Environment Variables:
    MESHY_API_KEY: Your Meshy API key (get one at https://meshy.ai)
"""

from __future__ import annotations

import os
import sys
import time


def main() -> int:
    """Demonstrate Meshy AI 3D generation."""
    # Check for required environment variables
    if not os.getenv("MESHY_API_KEY"):
        print("Error: MESHY_API_KEY not set")
        print("Get your API key at https://meshy.ai")
        return 1

    # Import Meshy modules
    from vendor_connectors.meshy import text3d

    print("=== Meshy AI 3D Generation ===\n")

    # Generate a simple 3D model
    prompt = "a medieval sword with ornate handle"
    print(f"Generating 3D model: '{prompt}'")
    print("This may take 1-2 minutes...\n")

    try:
        # Start the generation (preview mode for faster results)
        result = text3d.generate(
            prompt=prompt,
            art_style="realistic",
            mode="preview",  # Use 'refine' for higher quality
        )

        print(f"Task ID: {result.id}")
        print(f"Status: {result.status}")

        # Poll for completion
        while result.status in ("PENDING", "IN_PROGRESS"):
            time.sleep(5)
            result = text3d.get(result.id)
            print(f"Status: {result.status}...")

        if result.status == "SUCCEEDED":
            print("\n=== Generation Complete ===")
            print(f"Model URL: {result.model_urls.get('glb', 'N/A')}")
            print(f"Thumbnail: {result.thumbnail_url}")

            # Download the model (optional)
            # text3d.download(result, output_dir="./models")

        else:
            print(f"\nGeneration failed: {result.status}")
            if hasattr(result, "task_error"):
                print(f"Error: {result.task_error}")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    print("\nDone!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
