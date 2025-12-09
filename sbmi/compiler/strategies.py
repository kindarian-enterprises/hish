"""
Compression strategies for SBMI index compilation.

Uses strategy pattern with simple, composable passes for optimal token reduction.
Each strategy does ONE thing well, then they're composed together.
"""

import re
from abc import ABC, abstractmethod
from typing import Dict, List


class CompressionStrategy(ABC):
    """Base class for compression strategies."""

    @abstractmethod
    def compress(self, content: str, config: Dict) -> str:
        """
        Compress content using this strategy.

        Args:
            content: Text content to compress
            config: Configuration dict with strategy-specific params

        Returns:
            Compressed content
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Strategy name for logging."""
        pass


# ============================================================================
# SIMPLE PASS STRATEGIES - Each does ONE thing
# ============================================================================

class RemoveFormattingMarkersPass(CompressionStrategy):
    """Remove emoji and formatting markers but preserve text."""

    # Comprehensive emoji regex pattern covering all Unicode emoji ranges
    EMOJI_PATTERN = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )

    @property
    def name(self) -> str:
        return "remove_markers"

    def compress(self, content: str, config: Dict) -> str:
        lines = []
        for line in content.split('\n'):
            # Skip separator lines
            if re.match(r'^[\-=]{3,}$', line.strip()):
                continue

            # Strip all emojis from line but keep the text
            cleaned_line = self.EMOJI_PATTERN.sub('', line)

            # Remove extra spaces left after emoji removal
            cleaned_line = re.sub(r'\s+', ' ', cleaned_line).strip()

            # Only skip line if it becomes empty after emoji removal
            if cleaned_line:
                lines.append(cleaned_line)
            elif not line.strip():
                # Preserve intentional empty lines
                lines.append('')

        return '\n'.join(lines)


class RemoveCodeBlockMarkersPass(CompressionStrategy):
    """Remove code block markers (```bash, ```, etc.) but keep content."""

    @property
    def name(self) -> str:
        return "remove_codeblocks"

    def compress(self, content: str, config: Dict) -> str:
        lines = []
        for line in content.split('\n'):
            if re.match(r'^```\w*$', line.strip()):
                continue
            lines.append(line)
        return '\n'.join(lines)


class RemoveVerbosePrefixesPass(CompressionStrategy):
    """Remove verbose prefixes like 'Description:', 'Purpose:', etc."""

    @property
    def name(self) -> str:
        return "remove_prefixes"

    def compress(self, content: str, config: Dict) -> str:
        prefixes = [
            'Description:', 'Purpose:', 'Location:', 'Use:', 'Note:',
            'Example:', 'Format:', 'Usage:', 'Rationale:', 'Context:',
            'Prerequisites:', 'Requires:', 'Depends on:'
        ]

        lines = []
        for line in content.split('\n'):
            cleaned = line
            for prefix in prefixes:
                if cleaned.strip().startswith(prefix):
                    cleaned = cleaned.replace(prefix, '', 1).strip()
                    break
            lines.append(cleaned)
        return '\n'.join(lines)


class RemoveEmptyLinesPass(CompressionStrategy):
    """Aggressively remove empty lines and excessive whitespace."""

    @property
    def name(self) -> str:
        return "remove_empty"

    def compress(self, content: str, config: Dict) -> str:
        lines = []
        prev_empty = False

        for line in content.split('\n'):
            # Keep headers even if separated
            if line.strip().startswith('#'):
                lines.append(line)
                prev_empty = False
                continue

            # Skip empty lines completely (aggressive)
            if not line.strip():
                if not prev_empty:
                    prev_empty = True
                continue

            lines.append(line)
            prev_empty = False

        return '\n'.join(lines)


class CompactWhitespacePass(CompressionStrategy):
    """Compact inline whitespace and normalize spacing."""

    @property
    def name(self) -> str:
        return "compact_whitespace"

    def compress(self, content: str, config: Dict) -> str:
        # Multiple spaces to single space
        result = re.sub(r' {2,}', ' ', content)
        # Multiple newlines to double newline max
        result = re.sub(r'\n{3,}', '\n\n', result)
        return result


class ReplacePhrasesPass(CompressionStrategy):
    """Replace common phrases with abbreviations from config."""

    @property
    def name(self) -> str:
        return "replace_phrases"

    def compress(self, content: str, config: Dict) -> str:
        result = content
        phrase_mappings = config.get('phrase_mappings', {})

        # Sort by length (longest first) to avoid partial matches
        for phrase, abbrev in sorted(
            phrase_mappings.items(),
            key=lambda x: len(x[0]),
            reverse=True
        ):
            # Word boundary replacement
            result = re.sub(
                r'\b' + re.escape(phrase) + r'\b',
                abbrev,
                result,
                flags=re.IGNORECASE
            )

        return result


class CompactSyntaxPass(CompressionStrategy):
    """Compact syntax: arrows, colons, operators."""

    @property
    def name(self) -> str:
        return "compact_syntax"

    def compress(self, content: str, config: Dict) -> str:
        result = content
        # -> to →
        result = re.sub(r'\s*->\s*', '→', result)
        # Compact colons
        result = re.sub(r'\s*:\s*', ':', result)
        # Compact assignment-like patterns
        result = re.sub(r'\s*=\s*', '=', result)
        return result


class RemoveCommentsPass(CompressionStrategy):
    """Remove shell/markdown comment lines (preserves code parens)."""

    @property
    def name(self) -> str:
        return "remove_comments"

    def compress(self, content: str, config: Dict) -> str:
        lines = []
        for line in content.split('\n'):
            # Keep markdown headers
            if line.strip().startswith('#') and not line.strip().startswith('# '):
                lines.append(line)
                continue

            # Remove shell/markdown comment lines (start with "# ")
            if line.strip().startswith('# '):
                continue

            # Keep the line as-is (don't remove code parentheses)
            if line.strip():
                lines.append(line)

        return '\n'.join(lines)


class StripDescriptionsPass(CompressionStrategy):
    """Remove explanatory text after commands, keep only commands."""

    @property
    def name(self) -> str:
        return "strip_descriptions"

    def compress(self, content: str, config: Dict) -> str:
        lines = []
        for line in content.split('\n'):
            # Keep headers
            if line.strip().startswith('#'):
                lines.append(line)
                continue

            # For command lines with " - " explanations, keep only the command
            if ' - ' in line and not line.strip().startswith('-'):
                command_part = line.split(' - ')[0].strip()
                if command_part:
                    lines.append(command_part)
                continue

            lines.append(line)

        return '\n'.join(lines)


# ============================================================================
# COMPOSED STRATEGIES - Built from simple passes
# ============================================================================

class StructuralCompressionStrategy(CompressionStrategy):
    """
    Level 1 structural compression.

    Composed of simple passes:
    1. Remove formatting markers
    2. Remove code block markers
    3. Remove verbose prefixes
    4. Strip descriptions (keep commands only)
    5. Remove comments
    6. Remove empty lines
    7. Compact whitespace
    """

    def __init__(self):
        self.passes: List[CompressionStrategy] = [
            RemoveFormattingMarkersPass(),
            RemoveCodeBlockMarkersPass(),
            RemoveVerbosePrefixesPass(),
            StripDescriptionsPass(),
            RemoveCommentsPass(),
            RemoveEmptyLinesPass(),
            CompactWhitespacePass(),
        ]

    @property
    def name(self) -> str:
        return "structural"

    def compress(self, content: str, config: Dict) -> str:
        """Apply all structural passes in sequence."""
        result = content
        for pass_strategy in self.passes:
            result = pass_strategy.compress(result, config)
        return result


class PhraseCompressionStrategy(CompressionStrategy):
    """
    Level 2 phrase compression.

    Composed of simple passes:
    1. Replace phrases with abbreviations
    2. Compact syntax (arrows, operators)
    3. Final whitespace compact
    """

    def __init__(self):
        self.passes: List[CompressionStrategy] = [
            ReplacePhrasesPass(),
            CompactSyntaxPass(),
            CompactWhitespacePass(),
        ]

    @property
    def name(self) -> str:
        return "phrase"

    def compress(self, content: str, config: Dict) -> str:
        """Apply all phrase passes in sequence."""
        result = content
        for pass_strategy in self.passes:
            result = pass_strategy.compress(result, config)
        return result


class CombinedCompressionStrategy(CompressionStrategy):
    """
    Combined strategy that applies multiple strategies or passes in sequence.

    Can combine:
    - High-level strategies (Structural, Phrase)
    - Individual passes (for fine-grained control)
    """

    def __init__(self, strategies: List[CompressionStrategy]):
        """Initialize with list of strategies/passes to apply in order."""
        self.strategies = strategies

    @property
    def name(self) -> str:
        return "combined[" + ",".join(s.name for s in self.strategies) + "]"

    def compress(self, content: str, config: Dict) -> str:
        """Apply all strategies/passes in sequence."""
        result = content
        for strategy in self.strategies:
            result = strategy.compress(result, config)
        return result


# ============================================================================
# FACTORY - Create strategies by name
# ============================================================================

class CompressionStrategyFactory:
    """Factory for creating compression strategies and passes."""

    _STRATEGIES = {
        # Composed strategies
        'structural': StructuralCompressionStrategy,
        'phrase': PhraseCompressionStrategy,

        # Individual passes (for fine-grained control)
        'remove_markers': RemoveFormattingMarkersPass,
        'remove_codeblocks': RemoveCodeBlockMarkersPass,
        'remove_prefixes': RemoveVerbosePrefixesPass,
        'strip_descriptions': StripDescriptionsPass,
        'remove_empty': RemoveEmptyLinesPass,
        'remove_comments': RemoveCommentsPass,
        'compact_whitespace': CompactWhitespacePass,
        'replace_phrases': ReplacePhrasesPass,
        'compact_syntax': CompactSyntaxPass,
    }

    @classmethod
    def create(cls, strategy_name: str) -> CompressionStrategy:
        """
        Create a compression strategy by name.

        Args:
            strategy_name: Name of strategy or pass

        Returns:
            CompressionStrategy instance

        Raises:
            ValueError: If strategy name not recognized
        """
        if strategy_name == 'combined':
            # Default combined strategy: structural + phrase
            return CombinedCompressionStrategy([
                cls._STRATEGIES['structural'](),
                cls._STRATEGIES['phrase'](),
            ])

        if strategy_name not in cls._STRATEGIES:
            raise ValueError(
                f"Unknown strategy: {strategy_name}. "
                f"Available: {list(cls._STRATEGIES.keys()) + ['combined']}"
            )

        return cls._STRATEGIES[strategy_name]()

    @classmethod
    def create_from_list(cls, strategy_names: List[str]) -> CompressionStrategy:
        """
        Create combined strategy from list of strategy/pass names.

        Args:
            strategy_names: List of strategy/pass names to combine

        Returns:
            CompressionStrategy (single if 1 item, combined if multiple)
        """
        if len(strategy_names) == 1:
            return cls.create(strategy_names[0])

        strategies = [cls.create(name) for name in strategy_names]
        return CombinedCompressionStrategy(strategies)

    @classmethod
    def register_strategy(
        cls,
        name: str,
        strategy_class: type
    ) -> None:
        """
        Register a custom compression strategy or pass.

        Args:
            name: Name to register strategy under
            strategy_class: CompressionStrategy subclass
        """
        cls._STRATEGIES[name] = strategy_class
