#!/usr/bin/env python3
"""
SBMI Session-End Compaction Script.

Incrementally recompiles framework .md files that are new or have changed.
Designed to be run at end of agent sessions to keep .compact files in sync.

Usage:
    python3 scripts/compact-framework.py [--force] [--level LEVEL]

Options:
    --force     Force full recompilation (ignore cache)
    --level     Compression level (default: level2)
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sbmi.compiler import IndexCompiler
from sbmi.compiler.config import CompressionConfig


def main():
    """Run incremental compilation on framework docs."""
    parser = argparse.ArgumentParser(
        description="Incrementally compact framework documentation"
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force full recompilation (ignore cache)'
    )
    parser.add_argument(
        '--level',
        default='level2',
        choices=['level1', 'level2'],
        help='Compression level (default: level2)'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show cache statistics only (no compilation)'
    )

    args = parser.parse_args()

    # Initialize
    hish_root = Path(__file__).parent.parent
    config = CompressionConfig()
    compiler = IndexCompiler(hish_root, config, use_cache=not args.force)

    # Stats mode
    if args.stats:
        if compiler.cache:
            stats = compiler.cache.get_stats()
            print("\n" + "=" * 70)
            print("SBMI COMPILATION CACHE STATISTICS")
            print("=" * 70)
            print()
            print(f"Total files compiled: {stats['total_compiled']}")
            print(f"Average reduction: {stats['avg_reduction']:.1f}%")
            print(f"Last compilation: {stats['last_compiled'] or 'Never'}")
            print()
        else:
            print("Cache disabled (--force mode)")
        return

    # Compile
    if args.force:
        print("🔄 FORCE MODE: Full recompilation of all framework docs")
        # Invalidate cache to force full recompilation
        if compiler.cache:
            compiler.cache.invalidate()
        results = compiler.compile_changed_indexes(level=args.level)

        if not results:
            print("No files found to compile.")
            print()
        else:
            print(f"✅ Recompiled {len(results)} file(s)")
            print()
    else:
        print("⚡ INCREMENTAL MODE: Recompiling changed/new files only")
        results = compiler.compile_changed_indexes(level=args.level)

        if not results:
            print("✅ All framework docs are up to date!")
            print()
        else:
            print(f"✅ Recompiled {len(results)} file(s)")
            print()


if __name__ == "__main__":
    main()
