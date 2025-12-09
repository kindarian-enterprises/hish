"""
Hash-based cache for incremental compilation.

Tracks which source files have been compiled and their hashes,
enabling smart recompilation of only changed/new files.
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Set, Optional
from datetime import datetime, timezone


class CompilationCache:
    """Manages hash-based cache for incremental compilation."""

    def __init__(self, cache_file: Path):
        """
        Initialize cache.

        Args:
            cache_file: Path to .sbmi-cache.json
        """
        self.cache_file = cache_file
        self.cache: Dict[str, Dict] = self._load_cache()

    def _load_cache(self) -> Dict[str, Dict]:
        """Load cache from disk."""
        if not self.cache_file.exists():
            return {}

        try:
            return json.loads(self.cache_file.read_text())
        except (json.JSONDecodeError, OSError):
            # Corrupted cache - start fresh
            return {}

    def _save_cache(self):
        """Save cache to disk."""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache_file.write_text(
            json.dumps(self.cache, indent=2, sort_keys=True)
        )

    @staticmethod
    def compute_hash(file_path: Path) -> str:
        """
        Compute SHA256 hash of file contents.

        Args:
            file_path: Path to file

        Returns:
            Hex digest of file hash
        """
        sha256 = hashlib.sha256()
        sha256.update(file_path.read_bytes())
        return sha256.hexdigest()

    def has_changed(self, source_file: Path) -> bool:
        """
        Check if source file has changed since last compilation.

        Args:
            source_file: Path to source .md file

        Returns:
            True if file is new or hash differs
        """
        if not source_file.exists():
            return False

        key = str(source_file)
        current_hash = self.compute_hash(source_file)

        if key not in self.cache:
            return True  # New file

        return self.cache[key].get('hash') != current_hash

    def mark_compiled(
        self,
        source_file: Path,
        output_file: Path,
        reduction_pct: float
    ):
        """
        Mark a file as compiled and update cache.

        Args:
            source_file: Path to source .md file
            output_file: Path to output .compact file
            reduction_pct: Compression reduction percentage
        """
        key = str(source_file)
        self.cache[key] = {
            'hash': self.compute_hash(source_file),
            'output': str(output_file),
            'compiled_at': datetime.now(timezone.utc).isoformat(),
            'reduction_pct': reduction_pct
        }
        self._save_cache()

    def get_changed_files(self, source_files: Set[Path]) -> Set[Path]:
        """
        Get set of files that need recompilation.

        Args:
            source_files: Set of all source .md files

        Returns:
            Set of files that are new or changed
        """
        return {f for f in source_files if self.has_changed(f)}

    def get_stats(self) -> Dict:
        """Get compilation statistics from cache."""
        if not self.cache:
            return {
                'total_compiled': 0,
                'avg_reduction': 0.0,
                'last_compiled': None
            }

        total = len(self.cache)
        avg_reduction = sum(
            entry.get('reduction_pct', 0)
            for entry in self.cache.values()
        ) / total if total > 0 else 0

        last_compiled = max(
            (entry.get('compiled_at', '') for entry in self.cache.values()),
            default=None
        )

        return {
            'total_compiled': total,
            'avg_reduction': avg_reduction,
            'last_compiled': last_compiled
        }

    def invalidate(self, source_file: Optional[Path] = None):
        """
        Invalidate cache entry or entire cache.

        Args:
            source_file: Specific file to invalidate, or None for all
        """
        if source_file:
            key = str(source_file)
            self.cache.pop(key, None)
        else:
            self.cache.clear()

        self._save_cache()
