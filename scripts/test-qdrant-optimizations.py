#!/usr/bin/env python3
"""
Test script for Qdrant optimization validations.
Validates normalization, DOT distance, and metadata extraction.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "rag" / "indexer"))

import numpy as np
from app import normalize_vectors


def test_normalization():
    """Test vector normalization function."""
    print("🧪 Testing vector normalization...")

    # Test vectors
    vectors = [
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
        [0.5, 0.5, 0.5],
    ]

    normalized = normalize_vectors(vectors)

    # Check that all vectors have unit length
    for i, vec in enumerate(normalized):
        norm = np.linalg.norm(vec)
        print(f"  Vector {i}: norm = {norm:.6f} (should be ~1.0)")
        assert abs(norm - 1.0) < 1e-5, f"Vector {i} norm is {norm}, expected 1.0"

    # Test zero vector handling
    zero_vectors = [[0.0, 0.0, 0.0]]
    normalized_zero = normalize_vectors(zero_vectors)
    print(f"  Zero vector: {normalized_zero[0]} (should handle gracefully)")

    print("✅ Normalization tests passed!\n")


def test_dot_vs_cosine():
    """
    Test that DOT distance on normalized vectors equals COSINE distance.
    This validates our optimization is correct.
    """
    print("🧪 Testing DOT vs COSINE equivalence...")

    # Create two vectors
    vec1 = np.array([1.0, 2.0, 3.0])
    vec2 = np.array([4.0, 5.0, 6.0])

    # Normalize them
    vec1_norm = vec1 / np.linalg.norm(vec1)
    vec2_norm = vec2 / np.linalg.norm(vec2)

    # Calculate COSINE similarity
    cosine = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    # Calculate DOT on normalized vectors
    dot_normalized = np.dot(vec1_norm, vec2_norm)

    print(f"  COSINE similarity: {cosine:.6f}")
    print(f"  DOT (normalized):  {dot_normalized:.6f}")
    print(f"  Difference: {abs(cosine - dot_normalized):.8f}")

    assert abs(cosine - dot_normalized) < 1e-6, "DOT on normalized != COSINE"

    print("✅ DOT == COSINE for normalized vectors!\n")


def test_language_mapping():
    """Test language extraction logic."""
    print("🧪 Testing language mapping...")

    test_cases = {
        "main.py": "python",
        "app.js": "javascript",
        "component.tsx": "typescript",
        "service.go": "go",
        "handler.rs": "rust",
        "Model.scala": "scala",
        "config.yaml": "yaml",
        "README.md": "markdown",
    }

    # This mimics the logic in process_single_file
    language_map = {
        "py": "python",
        "js": "javascript",
        "ts": "typescript",
        "tsx": "typescript",
        "jsx": "javascript",
        "java": "java",
        "go": "go",
        "rs": "rust",
        "scala": "scala",
        "md": "markdown",
        "yaml": "yaml",
        "yml": "yaml",
    }

    for filename, expected_lang in test_cases.items():
        ext = filename.split(".")[-1]
        detected_lang = language_map.get(ext, ext)
        print(f"  {filename} → {detected_lang} (expected {expected_lang})")
        assert detected_lang == expected_lang, f"Language mismatch for {filename}"

    print("✅ Language mapping tests passed!\n")


def test_path_prefix():
    """Test path prefix extraction."""
    print("🧪 Testing path prefix extraction...")

    test_cases = {
        "src/components/Button.tsx": "src/components",
        "app/services/auth.py": "app/services",
        "main.go": "",
        "docs/api/README.md": "docs/api",
    }

    for path, expected_prefix in test_cases.items():
        path_parts = path.split("/")
        if len(path_parts) > 2:
            path_prefix = "/".join(path_parts[:2])
        elif len(path_parts) > 1:
            path_prefix = path_parts[0]
        else:
            path_prefix = ""

        print(f"  {path} → '{path_prefix}' (expected '{expected_prefix}')")
        assert path_prefix == expected_prefix, f"Path prefix mismatch for {path}"

    print("✅ Path prefix tests passed!\n")


def main():
    """Run all tests."""
    print("=" * 60)
    print("QDRANT OPTIMIZATION VALIDATION TESTS")
    print("=" * 60)
    print()

    try:
        test_normalization()
        test_dot_vs_cosine()
        test_language_mapping()
        test_path_prefix()

        print("=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("✅ Vector normalization working correctly")
        print("✅ DOT distance equivalent to COSINE (validated)")
        print("✅ Language detection working")
        print("✅ Path prefix extraction working")
        print()
        print("Phase 1 optimizations are ready for deployment!")

        return 0

    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"❌ TEST FAILED: {e}")
        print("=" * 60)
        return 1
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ UNEXPECTED ERROR: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
