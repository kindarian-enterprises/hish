#!/usr/bin/env python3
"""
Tokenization testing script for SBMI Phase 0 validation.
Tests various compression strategies and symbols against actual tokenizers.
"""

import sys
from pathlib import Path

def count_tokens_simple(text: str) -> int:
    """
    Simple word-based token estimation (approximation).
    Real tokenizers will be more accurate but this gives us a baseline.

    GPT-style tokenizers typically:
    - 1 token per 4 characters for English
    - Whitespace and punctuation count
    - Special chars may be multiple tokens
    """
    # Rough approximation: count words, add punctuation, divide total chars by 4
    words = len(text.split())
    chars = len(text)

    # Weighted formula based on typical BPE behavior
    estimated_tokens = int((chars / 4.0) + (words * 0.3))
    return estimated_tokens


def test_file_compression(filepath: Path) -> dict:
    """Test compression ratios for a given file."""
    if not filepath.exists():
        print(f"File not found: {filepath}")
        return {}

    content = filepath.read_text()
    tokens = count_tokens_simple(content)
    lines = len(content.split('\n'))
    chars = len(content)

    return {
        'file': filepath.name,
        'lines': lines,
        'chars': chars,
        'estimated_tokens': tokens,
        'content': content
    }


def test_symbol_tokenization():
    """Test various symbol candidates for tokenization efficiency."""
    print("=" * 70)
    print("SYMBOL TOKENIZATION TEST")
    print("=" * 70)
    print("\nNOTE: Using simple estimation. For production, use actual tokenizer.")
    print()

    test_cases = {
        "Short codes": ["mi", "nc", "mk", "ap", "idx", "ctx", "coll"],
        "Phrases": ["make-index", "new-context", "newctx", "coll-mgmt", "repo-idx"],
        "Full words": ["make", "index", "Makefile", "collection", "management"],
        "Greek letters": ["α", "β", "γ", "δ", "ε", "Σ", "Ψ", "Ω"],
        "Special chars": ["⚡", "⚙", "⚕", "⚖", "⛏", "§"],
    }

    for category, symbols in test_cases.items():
        print(f"{category}:")
        for symbol in symbols:
            tokens = count_tokens_simple(symbol)
            print(f"  {symbol:20} → ~{tokens} tokens (simple estimate)")
        print()


def main():
    """Run Phase 0 tokenization tests."""
    print("\n" + "=" * 70)
    print("SBMI PHASE 0 - TOKENIZATION VALIDATION")
    print("=" * 70)
    print()

    # Test symbol tokenization first
    test_symbol_tokenization()

    # Test actual index file compressions
    hish_root = Path(__file__).parent.parent
    workflow_indexes = hish_root / "local" / "workflow-indexes"

    files_to_test = [
        "framework-command-index.md",
        "command-index-level1.compact",
        "command-index-level2.compact",
        "session-workflow-enforcement.md",
        "enforcement-level1.compact",
        "enforcement-level2.compact",
    ]

    print("=" * 70)
    print("FILE COMPRESSION COMPARISON")
    print("=" * 70)
    print()

    results = {}
    for filename in files_to_test:
        filepath = workflow_indexes / filename
        if filepath.exists():
            result = test_file_compression(filepath)
            results[filename] = result
            print(f"✓ {filename}")
            print(f"  Lines: {result['lines']}, Chars: {result['chars']}, "
                  f"Est. Tokens: {result['estimated_tokens']}")
        else:
            print(f"✗ {filename} (not created yet)")

    # Calculate compression ratios
    print()
    print("=" * 70)
    print("COMPRESSION ANALYSIS")
    print("=" * 70)
    print()

    if "framework-command-index.md" in results:
        baseline = results["framework-command-index.md"]
        baseline_tokens = baseline['estimated_tokens']

        print(f"Baseline: {baseline['file']}")
        print(f"  {baseline_tokens} tokens\n")

        for level, filename in [
            ("Level 1 (Structural)", "command-index-level1.compact"),
            ("Level 1+2 (Structural+Phrase)", "command-index-level2.compact")
        ]:
            if filename in results:
                compressed = results[filename]
                compressed_tokens = compressed['estimated_tokens']
                reduction_pct = ((baseline_tokens - compressed_tokens) / baseline_tokens) * 100

                print(f"{level}: {filename}")
                print(f"  {compressed_tokens} tokens ({reduction_pct:.1f}% reduction)")
                print()

    if "session-workflow-enforcement.md" in results:
        baseline = results["session-workflow-enforcement.md"]
        baseline_tokens = baseline['estimated_tokens']

        print(f"Baseline: {baseline['file']}")
        print(f"  {baseline_tokens} tokens\n")

        for level, filename in [
            ("Level 1 (Structural)", "enforcement-level1.compact"),
            ("Level 1+2 (Structural+Phrase)", "enforcement-level2.compact")
        ]:
            if filename in results:
                compressed = results[filename]
                compressed_tokens = compressed['estimated_tokens']
                reduction_pct = ((baseline_tokens - compressed_tokens) / baseline_tokens) * 100

                print(f"{level}: {filename}")
                print(f"  {compressed_tokens} tokens ({reduction_pct:.1f}% reduction)")
                print()

    print("=" * 70)
    print("RECOMMENDATIONS")
    print("=" * 70)
    print("""
Based on results:
- If Level 1 achieves 40-60% reduction: Proceed with structural only
- If Level 1+2 achieves 70-80% reduction: Proceed with both (RECOMMENDED)
- Level 3 symbols only if L1+2 insufficient
""")


if __name__ == "__main__":
    main()
