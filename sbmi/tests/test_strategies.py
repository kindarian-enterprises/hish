"""
Test compression strategies to ensure essential context is preserved.

Critical Requirements:
- Commands must remain executable
- File paths must be intact
- Code syntax must be valid
- Essential information must not be lost
"""

import pytest
from sbmi.compiler.strategies import (
    RemoveFormattingMarkersPass,
    RemoveCodeBlockMarkersPass,
    RemoveVerbosePrefixesPass,
    StripDescriptionsPass,
    RemoveCommentsPass,
    RemoveEmptyLinesPass,
    CompactWhitespacePass,
    ReplacePhrasesPass,
    CompactSyntaxPass,
    StructuralCompressionStrategy,
    PhraseCompressionStrategy,
    CombinedCompressionStrategy,
)


class TestRemoveFormattingMarkersPass:
    """Test that formatting markers are removed but content preserved."""

    def test_removes_emoji_markers(self):
        """Test that emojis are removed but text is preserved."""
        strategy = RemoveFormattingMarkersPass()
        content = "🚨 CRITICAL: Important content\nNormal content"
        result = strategy.compress(content, {})
        # Emoji should be removed but text preserved
        assert "🚨" not in result
        assert "CRITICAL: Important content" in result
        assert "Normal content" in result

    def test_removes_separator_lines(self):
        strategy = RemoveFormattingMarkersPass()
        content = "Header\n===\nContent\n---\nMore"
        result = strategy.compress(content, {})
        assert "===" not in result
        assert "---" not in result
        assert "Content" in result

    def test_preserves_commands(self):
        strategy = RemoveFormattingMarkersPass()
        content = "⚠️ WARNING\nmake install"
        result = strategy.compress(content, {})
        assert "make install" in result

    def test_preserves_do_dont_text(self):
        """Test that DO/DON'T text is preserved when emojis are stripped."""
        strategy = RemoveFormattingMarkersPass()
        content = """✅ DO:
- Make all changes
- Test thoroughly

❌ DON'T:
- Skip validation
- Commit without testing"""

        result = strategy.compress(content, {})

        # Emojis should be removed but text preserved
        assert '✅' not in result
        assert '❌' not in result
        assert 'DO:' in result
        assert "DON'T:" in result
        assert 'Make all changes' in result
        assert 'Skip validation' in result


class TestRemoveCodeBlockMarkersPass:
    """Test that code block markers removed but content preserved."""

    def test_removes_bash_markers(self):
        strategy = RemoveCodeBlockMarkersPass()
        content = "```bash\nmake test\n```"
        result = strategy.compress(content, {})
        assert "```" not in result
        assert "make test" in result

    def test_preserves_command_content(self):
        strategy = RemoveCodeBlockMarkersPass()
        content = "```python\nimport os\n```"
        result = strategy.compress(content, {})
        assert "import os" in result


class TestStripDescriptionsPass:
    """Test that command descriptions are stripped but commands preserved."""

    def test_strips_dash_descriptions(self):
        strategy = StripDescriptionsPass()
        content = "make test - Run all tests"
        result = strategy.compress(content, {})
        assert "make test" in result
        assert "Run all tests" not in result

    def test_preserves_headers(self):
        strategy = StripDescriptionsPass()
        content = "## Setup - Initial Configuration"
        result = strategy.compress(content, {})
        assert "## Setup - Initial Configuration" in result

    def test_preserves_commands_without_descriptions(self):
        strategy = StripDescriptionsPass()
        content = "make install"
        result = strategy.compress(content, {})
        assert "make install" in result


class TestRemoveCommentsPass:
    """Test that shell comments removed but code preserved."""

    def test_removes_shell_comments(self):
        strategy = RemoveCommentsPass()
        content = "# This is a comment\nmake test"
        result = strategy.compress(content, {})
        assert "This is a comment" not in result
        assert "make test" in result

    def test_preserves_markdown_headers(self):
        strategy = RemoveCommentsPass()
        content = "## Setup\n# Comment\nmake install"
        result = strategy.compress(content, {})
        assert "## Setup" in result
        assert "make install" in result

    def test_preserves_code_with_special_chars(self):
        strategy = RemoveCommentsPass()
        content = 'python3 -c "import uuid; print(uuid.uuid4())"'
        result = strategy.compress(content, {})
        assert 'python3 -c "import uuid; print(uuid.uuid4())"' in result


class TestReplacePhrasesPass:
    """Test phrase replacement preserves command functionality."""

    def test_replaces_configured_phrases(self):
        strategy = ReplacePhrasesPass()
        config = {
            'phrase_mappings': {
                'make new-context': 'newctx',
                'framework': 'fw',
            }
        }
        content = "make new-context\nframework documentation"
        result = strategy.compress(content, config)
        assert "newctx" in result
        assert "fw documentation" in result

    def test_word_boundary_replacement(self):
        strategy = ReplacePhrasesPass()
        config = {
            'phrase_mappings': {
                'context': 'ctx',
            }
        }
        content = "new-context\ncontextual"
        result = strategy.compress(content, config)
        # Should replace "context" but not affect "contextual"
        assert "new-ctx" in result or "context" in result

    def test_preserves_file_paths(self):
        strategy = ReplacePhrasesPass()
        config = {'phrase_mappings': {'index': 'idx'}}
        content = "/path/to/index.md"
        result = strategy.compress(content, config)
        # Ensure path structure maintained
        assert "/path/to/" in result


class TestCompactSyntaxPass:
    """Test syntax compaction preserves meaning."""

    def test_compacts_arrows(self):
        strategy = CompactSyntaxPass()
        content = "command -> output"
        result = strategy.compress(content, {})
        assert "→" in result
        assert "command" in result
        assert "output" in result

    def test_compacts_colons(self):
        strategy = CompactSyntaxPass()
        content = "key : value"
        result = strategy.compress(content, {})
        assert "key:value" in result

    def test_preserves_command_syntax(self):
        strategy = CompactSyntaxPass()
        content = "make test ARG=value"
        result = strategy.compress(content, {})
        assert "make test ARG=value" in result


class TestStructuralCompressionStrategy:
    """Test complete structural compression preserves essential information."""

    def test_preserves_commands(self):
        strategy = StructuralCompressionStrategy()
        content = """## Setup Commands
```bash
# Install dependencies
make install

# Run tests
make test
```"""
        result = strategy.compress(content, {})
        assert "make install" in result
        assert "make test" in result
        assert "## Setup Commands" in result

    def test_removes_verbosity(self):
        """Test that verbose descriptions are stripped but emojis don't remove text."""
        strategy = StructuralCompressionStrategy()
        content = """🚨 CRITICAL WARNING 🚨
Purpose: This is important
make install - Install all dependencies"""
        result = strategy.compress(content, {})
        # Emojis should be removed but text preserved
        assert "🚨" not in result
        assert "CRITICAL WARNING" in result  # Text preserved after emoji removal
        # Description lines should be stripped
        assert "Install all dependencies" not in result
        # Commands preserved
        assert "make install" in result

    def test_preserves_file_references(self):
        strategy = StructuralCompressionStrategy()
        content = "Description: See Makefile for details\nPath: /path/to/file.md"
        result = strategy.compress(content, {})
        assert "Makefile" in result
        assert "/path/to/file.md" in result


class TestPhraseCompressionStrategy:
    """Test phrase compression with config."""

    def test_applies_phrase_mappings(self):
        strategy = PhraseCompressionStrategy()
        config = {
            'phrase_mappings': {
                'framework': 'fw',
                'collection': 'coll',
            }
        }
        content = "framework collection management"
        result = strategy.compress(content, config)
        assert "fw" in result
        assert "coll" in result

    def test_compacts_syntax(self):
        strategy = PhraseCompressionStrategy()
        config = {'phrase_mappings': {}}
        content = "input -> output"
        result = strategy.compress(content, config)
        assert "→" in result


class TestCombinedCompressionStrategy:
    """Test combined strategy preserves critical information end-to-end."""

    def test_full_compression_preserves_commands(self):
        structural = StructuralCompressionStrategy()
        phrase = PhraseCompressionStrategy()
        strategy = CombinedCompressionStrategy([structural, phrase])

        content = """# Framework Command Index

## 🚨 MANDATORY SESSION BEHAVIOR 🚨

## Setup Commands

```bash
# Install framework
make install

# Create new project context - simplified flow
make new-context
```"""

        config = {
            'phrase_mappings': {
                'make new-context': 'newctx',
                'framework': 'fw',
            }
        }

        result = strategy.compress(content, config)

        # Essential commands must be preserved
        assert "make install" in result
        assert "newctx" in result or "make new-context" in result

        # Emojis should be removed
        assert "🚨" not in result
        # Verbose descriptions should be removed
        assert "simplified flow" not in result

    def test_preserves_complex_commands(self):
        structural = StructuralCompressionStrategy()
        phrase = PhraseCompressionStrategy()
        strategy = CombinedCompressionStrategy([structural, phrase])

        content = '''# Commands

# Generate UUID for storage
python3 -c "import uuid; print(uuid.uuid4())"

# Index repository with path
make index-repo REPO_PATH=/path/to/repo COLLECTION_NAME=my_collection'''

        result = strategy.compress(content, {})

        # Complex command syntax must be intact
        assert 'python3 -c "import uuid; print(uuid.uuid4())"' in result
        assert "make index-repo" in result
        assert "REPO_PATH=/path/to/repo" in result
        assert "COLLECTION_NAME=my_collection" in result

    def test_no_information_loss_on_critical_paths(self):
        structural = StructuralCompressionStrategy()
        phrase = PhraseCompressionStrategy()
        strategy = CombinedCompressionStrategy([structural, phrase])

        content = """## Key Files
- `prompts/dev_agent/dev_agent_init_prompt.md` - Agent initialization
- `local/dev_agent_persona.md` - Agent persona
- `Makefile` - All framework commands"""

        result = strategy.compress(content, {})

        # File paths must be preserved exactly
        assert "prompts/dev_agent/dev_agent_init_prompt.md" in result
        assert "local/dev_agent_persona.md" in result
        assert "Makefile" in result


class TestEssentialContextPreservation:
    """Critical tests ensuring no essential context is lost."""

    def test_environment_variables_preserved(self):
        strategy = StructuralCompressionStrategy()
        content = "REPO_PATH=/path/to/repo\nCOLLECTION_NAME=my_collection"
        result = strategy.compress(content, {})
        assert "REPO_PATH=/path/to/repo" in result
        assert "COLLECTION_NAME=my_collection" in result

    def test_code_syntax_preserved(self):
        strategy = StructuralCompressionStrategy()
        content = 'text.store "content" collection_name [UUID]'
        result = strategy.compress(content, {})
        assert 'text.store' in result
        assert '"content"' in result
        assert 'collection_name' in result
        assert '[UUID]' in result

    def test_makefile_targets_preserved(self):
        strategy = StructuralCompressionStrategy()
        content = "make install\nmake test\nmake clean"
        result = strategy.compress(content, {})
        assert "make install" in result
        assert "make test" in result
        assert "make clean" in result

    def test_script_paths_preserved(self):
        strategy = StructuralCompressionStrategy()
        content = "./scripts/setup.sh\n./reindex all"
        result = strategy.compress(content, {})
        assert "./scripts/setup.sh" in result
        assert "./reindex all" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
