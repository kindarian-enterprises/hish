#!/usr/bin/env python3
"""
SBMI Index Compiler CLI.

Thin wrapper around sbmi.compiler package for command-line usage.
"""

import sys
from pathlib import Path

# Add parent directory to path to import sbmi package
sys.path.insert(0, str(Path(__file__).parent.parent))

from sbmi.compiler import IndexCompiler, CompressionConfig


def main():
    """Main entry point."""
    # Find hish root
    script_dir = Path(__file__).parent
    hish_root = script_dir.parent

    if not (hish_root / "local" / "workflow-indexes").exists():
        print(f"Error: workflow-indexes not found at {hish_root / 'local'}")
        sys.exit(1)

    # Load configuration
    try:
        config = CompressionConfig()
    except FileNotFoundError as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)

    # Create compiler and run
    compiler = IndexCompiler(hish_root, config=config)
    results = compiler.compile_all_indexes(level="level2")

    if not results:
        print("\nNo files compiled.")
        sys.exit(1)

    # Success
    print(f"\n✓ Compilation complete: {len(results)} files")
    sys.exit(0)


if __name__ == "__main__":
    main()
