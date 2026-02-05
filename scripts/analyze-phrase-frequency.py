#!/usr/bin/env python3
"""
SBMI Phrase Frequency Analyzer CLI.

Analyzes framework documentation to identify high-value compression targets
and generate optimized phrase mappings.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sbmi.analyzer import PhraseFrequencyAnalyzer


def main():
    """Run phrase frequency analysis on framework documentation."""
    hish_root = Path(__file__).parent.parent

    # Directories to analyze
    docs_dirs = [
        hish_root / "docs",
        hish_root / "templates",
        hish_root / "local" / "workflow-indexes",
        hish_root / "local" / "workflows-and-processes",
        hish_root / "prompts",
    ]

    # Create analyzer and run
    analyzer = PhraseFrequencyAnalyzer(docs_dirs)
    analyzer.analyze()

    # Print comprehensive report
    analyzer.print_report(top_n=50)

    # Generate optimized mappings
    print("=" * 70)
    print("OPTIMIZED CONFIG GENERATION")
    print("=" * 70)
    print()

    mappings = analyzer.generate_phrase_mappings(top_n=30)
    total_savings = sum(s for _, _, _, s in mappings)

    print("Add to config/sbmi-compression.yaml:")
    print()
    print("phrase_mappings:")
    for phrase, abbrev, count, savings in mappings:
        print(f'  "{phrase}": "{abbrev}"  # {count}x, save {savings} chars')

    print()
    print(f"Total potential savings: ~{total_savings:,} chars")
    print()
    print("=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("""
1. Review suggested mappings for readability
2. Add high-impact mappings to config/sbmi-compression.yaml
3. Re-run: make sbmi-compile
4. Measure actual compression improvement
5. Iterate based on results
""")


if __name__ == "__main__":
    main()
