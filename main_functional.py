#!/usr/bin/env python3
"""
LaunchDarkly Python Demo - Function-Based Entry Point

This demonstrates a clean, function-based architecture following
all LaunchDarkly best practices:
- Non-blocking initialization
- Safe evaluation (works even if LD unavailable)
- Dynamic context building
- Graceful shutdown
"""
from src_functional.main import main

if __name__ == "__main__":
    exit(main())
