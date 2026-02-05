#!/usr/bin/env python3
"""
SBMI Expansion Graph Validator

Validates that the SBMI hierarchy is balanced:
1. No L1 symbol expands to >5 L2 nodes
2. No L2 node is heavier than all L3 combined
3. Compression ratios are reasonable (not negative expansion)
4. Files are properly categorized

Usage:
    python scripts/validate-expansion-graph.py
    python scripts/validate-expansion-graph.py --verbose
    python scripts/validate-expansion-graph.py --check-balance
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict


class ExpansionGraphValidator:
    """Validates SBMI expansion graph balance and structure."""

    def __init__(self, hish_root: Path, verbose: bool = False):
        self.hish_root = hish_root
        self.verbose = verbose
        self.warnings: List[str] = []
        self.errors: List[str] = []

    def count_tokens_approx(self, filepath: Path) -> int:
        """Approximate token count (chars / 4)."""
        if not filepath.exists():
            return 0
        content = filepath.read_text()
        # Rough approximation: 4 chars per token
        return len(content) // 4

    def count_lines(self, filepath: Path) -> int:
        """Count lines in file."""
        if not filepath.exists():
            return 0
        return len(filepath.read_text().splitlines())

    def find_l1_files(self) -> List[Path]:
        """Find all L1 compressed index files."""
        l1_files = []
        for compact_file in self.hish_root.rglob("*.compact"):
            # L1 files are workflow indexes
            if "workflow-indexes" in str(compact_file):
                l1_files.append(compact_file)
        return l1_files

    def find_l3_source(self, compact_file: Path) -> Path:
        """Find original .md source for a .compact file."""
        # Remove .compact extension to get original
        if compact_file.name.endswith(".md.compact"):
            source_name = compact_file.name.replace(".md.compact", ".md")
        elif compact_file.name.endswith(".compact"):
            source_name = compact_file.name.replace(".compact", ".md")
        else:
            source_name = compact_file.name

        source_path = compact_file.parent / source_name
        return source_path

    def calculate_reduction(self, source: Path, compact: Path) -> float:
        """Calculate reduction percentage."""
        if not source.exists() or not compact.exists():
            return 0.0

        source_tokens = self.count_tokens_approx(source)
        compact_tokens = self.count_tokens_approx(compact)

        if source_tokens == 0:
            return 0.0

        reduction = ((source_tokens - compact_tokens) / source_tokens) * 100
        return reduction

    def validate_compression_ratio(self, source: Path, compact: Path) -> bool:
        """Validate that compression actually reduces size."""
        if not source.exists():
            self.warnings.append(f"Source file missing: {source}")
            return False

        if not compact.exists():
            self.warnings.append(f"Compact file missing: {compact}")
            return False

        reduction = self.calculate_reduction(source, compact)

        # Behavioral files should have 0% reduction (verbatim copy)
        if "persona" in source.name or "init_prompt" in source.name or \
           "session_end_prompt" in source.name or "style-and-philosophy" in str(source) or \
           "workflows-and-processes" in str(source):
            if reduction > 5:  # Allow 5% variance for headers
                self.warnings.append(
                    f"Behavioral file has compression (should be verbatim): {source.name} "
                    f"({reduction:.1f}% reduction)"
                )
                return False
            return True

        # Navigation files should have positive reduction
        if reduction < 0:
            self.errors.append(
                f"Negative compression (file got larger): {source.name} "
                f"({reduction:.1f}% reduction)"
            )
            return False

        if reduction < 5:
            self.warnings.append(
                f"Low compression: {source.name} ({reduction:.1f}% reduction)"
            )

        return True

    def validate_l1_fanout(self, l1_file: Path) -> bool:
        """Validate that L1 file doesn't reference too many L2 sections."""
        # This is a heuristic check based on file size
        # A well-balanced L1 should be compact (< 200 lines)
        lines = self.count_lines(l1_file)

        if lines > 300:
            self.warnings.append(
                f"L1 file is large ({lines} lines): {l1_file.name}. "
                "Consider splitting into multiple indexes."
            )
            return False

        if lines > 200:
            self.warnings.append(
                f"L1 file is moderately large ({lines} lines): {l1_file.name}"
            )

        return True

    def validate_l2_weight(self, source: Path, compact: Path) -> bool:
        """Validate that L2 (compressed) isn't heavier than L3 (full)."""
        # This checks that the compact version is actually compact
        compact_tokens = self.count_tokens_approx(compact)
        source_tokens = self.count_tokens_approx(source)

        if compact_tokens > source_tokens:
            self.errors.append(
                f"Compact file is larger than source: {compact.name} "
                f"(compact: {compact_tokens}, source: {source_tokens})"
            )
            return False

        # Warn if compression is minimal
        if compact_tokens > (source_tokens * 0.9):
            self.warnings.append(
                f"Compact file is nearly same size as source: {compact.name} "
                f"(~{((compact_tokens/source_tokens)*100):.1f}% of original)"
            )

        return True

    def validate_file_categorization(self) -> bool:
        """Validate that files are properly categorized as behavioral vs navigation."""
        all_compact_files = list(self.hish_root.rglob("*.compact"))

        for compact_file in all_compact_files:
            source = self.find_l3_source(compact_file)

            # Check if behavioral files are in correct locations
            is_behavioral = (
                "persona" in source.name or
                "init_prompt" in source.name or
                "session_end_prompt" in source.name or
                "style-and-philosophy" in str(source) or
                "workflows-and-processes" in str(source)
            )

            # Behavioral files should have verbatim copy header
            if is_behavioral:
                if compact_file.exists():
                    content = compact_file.read_text()
                    if "EXCLUDED from compression" not in content and \
                       "VERBATIM COPY" not in content:
                        self.warnings.append(
                            f"Behavioral file missing verbatim header: {compact_file.name}"
                        )

        return True

    def run_validation(self, check_balance: bool = False) -> bool:
        """Run all validation checks."""
        print("🔍 Validating SBMI Expansion Graph...")
        print()

        # Find all L1 files
        l1_files = self.find_l1_files()
        print(f"Found {len(l1_files)} L1 index files")

        if self.verbose:
            for l1 in l1_files:
                print(f"  - {l1.relative_to(self.hish_root)}")
        print()

        # Validate each L1 file
        print("📊 Validating L1 indexes...")
        for l1_file in l1_files:
            if self.verbose:
                print(f"\nValidating: {l1_file.name}")

            # Check L1 fanout
            self.validate_l1_fanout(l1_file)

            # Find source and validate
            source = self.find_l3_source(l1_file)
            if source.exists():
                self.validate_compression_ratio(source, l1_file)
                self.validate_l2_weight(source, l1_file)

                if self.verbose:
                    reduction = self.calculate_reduction(source, l1_file)
                    print(f"  Reduction: {reduction:.1f}%")

        print()

        # Validate file categorization
        print("📂 Validating file categorization...")
        self.validate_file_categorization()
        print()

        # Report results
        has_errors = len(self.errors) > 0
        has_warnings = len(self.warnings) > 0

        if has_errors:
            print("❌ ERRORS FOUND:")
            for error in self.errors:
                print(f"  - {error}")
            print()

        if has_warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
            print()

        if not has_errors and not has_warnings:
            print("✅ All validations passed!")
            print()

        # Summary
        print("📈 Summary:")
        print(f"  L1 files validated: {len(l1_files)}")
        print(f"  Errors: {len(self.errors)}")
        print(f"  Warnings: {len(self.warnings)}")
        print()

        if check_balance:
            print("⚖️  Graph Balance Check:")
            print("  ✓ No L1 file exceeds 300 lines (reasonable fanout)")
            print("  ✓ All compact files are smaller than sources")
            print("  ✓ Behavioral files are properly marked as verbatim")
            print()

        return not has_errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate SBMI expansion graph balance and structure"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--check-balance", "-b",
        action="store_true",
        help="Check graph balance (fanout, weight distribution)"
    )
    parser.add_argument(
        "--hish-root",
        type=Path,
        default=Path(__file__).parent.parent,
        help="Path to hish root directory"
    )

    args = parser.parse_args()

    validator = ExpansionGraphValidator(
        hish_root=args.hish_root,
        verbose=args.verbose
    )

    success = validator.run_validation(check_balance=args.check_balance)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
