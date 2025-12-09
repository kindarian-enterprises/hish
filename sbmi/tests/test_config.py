"""Test configuration loading and management."""

import pytest
from pathlib import Path
from sbmi.compiler.config import CompressionConfig


class TestCompressionConfig:
    """Test configuration loading from YAML."""

    def test_loads_default_config(self):
        """Test loading default config file."""
        config = CompressionConfig()
        assert config.exclusion_patterns is not None
        assert config.phrase_mappings is not None
        assert config.default_strategy is not None

    def test_exclusion_patterns_loaded(self):
        """Test that exclusion patterns are loaded."""
        config = CompressionConfig()
        patterns = config.exclusion_patterns

        # Critical behavioral files must be excluded
        assert any('dev_agent_persona.md' in p for p in patterns)
        assert any('dev_agent_init_prompt.md' in p for p in patterns)
        assert any('dev_agent_context.md' in p for p in patterns)

    def test_phrase_mappings_loaded(self):
        """Test that phrase mappings are loaded."""
        config = CompressionConfig()
        mappings = config.phrase_mappings

        assert isinstance(mappings, dict)
        assert len(mappings) > 0

    def test_level_config_retrieval(self):
        """Test retrieving level-specific configuration."""
        config = CompressionConfig()

        level1 = config.get_level_config('level1')
        level2 = config.get_level_config('level2')

        assert level1 is not None
        assert level2 is not None
        assert 'strategies' in level1
        assert 'strategies' in level2

    def test_level_strategies_retrieval(self):
        """Test retrieving strategy list for a level."""
        config = CompressionConfig()

        strategies = config.get_level_strategies('level2')

        assert isinstance(strategies, list)
        assert len(strategies) > 0

    def test_config_as_dict(self):
        """Test getting raw config dictionary."""
        config = CompressionConfig()
        config_dict = config.as_dict()

        assert isinstance(config_dict, dict)
        assert 'exclusion_patterns' in config_dict
        assert 'phrase_mappings' in config_dict


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
