"""
Configuration loading and management for SBMI compiler.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional


class CompressionConfig:
    """Loads and manages compression configuration from YAML."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to YAML config file. If None, uses default.
        """
        if config_path is None:
            # Default to config/sbmi-compression.yaml in hish root
            hish_root = Path(__file__).parent.parent.parent
            config_path = hish_root / "config" / "sbmi-compression.yaml"

        self.config_path = config_path
        self._config: Dict = {}
        self._load()

    def _load(self) -> None:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )

        with open(self.config_path, 'r') as f:
            self._config = yaml.safe_load(f)

    @property
    def scan_directories(self) -> List[str]:
        """Get list of directories to scan for markdown files."""
        return self._config.get('scan_directories', ['local/workflow-indexes'])

    @property
    def excluded_directories(self) -> List[str]:
        """Get list of directories to exclude entirely from scanning."""
        return self._config.get('excluded_directories', [])

    @property
    def exclusion_patterns(self) -> List[str]:
        """Get list of file patterns to exclude from compression."""
        return self._config.get('exclusion_patterns', [])

    @property
    def phrase_mappings(self) -> Dict[str, str]:
        """Get phrase compression mappings."""
        return self._config.get('phrase_mappings', {})

    @property
    def default_strategy(self) -> str:
        """Get default compression strategy name."""
        return self._config.get('default_strategy', 'combined')

    def get_level_config(self, level_name: str) -> Optional[Dict]:
        """
        Get configuration for a specific compression level.

        Args:
            level_name: Name of level (e.g., 'level1', 'level2')

        Returns:
            Level configuration dict or None if not found
        """
        levels = self._config.get('levels', {})
        return levels.get(level_name)

    def get_level_strategies(self, level_name: str) -> List[str]:
        """
        Get list of strategy names for a compression level.

        Args:
            level_name: Name of level (e.g., 'level1', 'level2')

        Returns:
            List of strategy names
        """
        level_config = self.get_level_config(level_name)
        if level_config is None:
            return []
        return level_config.get('strategies', [])

    def as_dict(self) -> Dict:
        """Get raw configuration dict."""
        return self._config.copy()

    @property
    def weight_level_boundaries(self) -> List[int]:
        """
        Get weight level boundaries (line count thresholds).

        Returns:
            List of line count boundaries. Files are assigned to L1, L2, L3, etc.
            based on which boundary they fall under.
        """
        weight_config = self._config.get('weight_levels', {})
        return weight_config.get('boundaries', [150, 300, 500])

    def get_weight_level(self, line_count: int) -> int:
        """
        Determine weight level based on line count.

        Args:
            line_count: Number of lines in the file

        Returns:
            Weight level (1, 2, 3, etc.)
        """
        boundaries = self.weight_level_boundaries
        for level, boundary in enumerate(boundaries, start=1):
            if line_count <= boundary:
                return level
        # If exceeds all boundaries, return level after last boundary
        return len(boundaries) + 1

    def reload(self) -> None:
        """Reload configuration from file."""
        self._load()
