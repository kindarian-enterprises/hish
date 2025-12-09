"""
Phrase frequency analysis for compression optimization.

Analyzes markdown documentation to find the most frequent words and phrases
for optimal compression mapping generation.
"""

import re
from pathlib import Path
from collections import Counter
from typing import List, Dict, Tuple, Optional


class PhraseFrequencyAnalyzer:
    """Analyzes phrase frequency in documentation for compression optimization."""

    # Common stop words to filter out
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'from', 'by', 'as', 'is', 'was', 'are', 'be', 'this',
        'that', 'it', 'be', 'have', 'has', 'had', 'do', 'does', 'can', 'will',
        'if', 'when', 'where', 'how', 'what', 'which', 'who', 'should', 'would'
    }

    def __init__(self, docs_dirs: List[Path]):
        """
        Initialize analyzer with directories to scan.

        Args:
            docs_dirs: List of directories containing markdown files
        """
        self.docs_dirs = [d for d in docs_dirs if d.exists()]
        self.results: Optional[Dict] = None

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean text for analysis - preserve words and basic punctuation."""
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        # Remove inline code
        text = re.sub(r'`[^`]+`', '', text)
        # Remove URLs
        text = re.sub(r'https?://\S+', '', text)
        # Remove markdown formatting
        text = re.sub(r'[*_#]', '', text)
        return text

    @staticmethod
    def extract_ngrams(text: str, n: int) -> List[str]:
        """Extract n-grams from text."""
        words = re.findall(r'\b[a-z]+(?:-[a-z]+)?\b', text.lower())
        if n == 1:
            return words
        return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]

    def analyze(self) -> Dict:
        """
        Analyze all markdown files in configured directories.

        Returns:
            Dict with unigrams, bigrams, trigrams counters and stats
        """
        all_text = ""
        file_count = 0

        for docs_dir in self.docs_dirs:
            for md_file in docs_dir.rglob("*.md"):
                try:
                    content = md_file.read_text()
                    all_text += " " + self.clean_text(content)
                    file_count += 1
                except Exception:
                    pass  # Skip files we can't read

        # Extract n-grams
        unigrams = self.extract_ngrams(all_text, 1)
        bigrams = self.extract_ngrams(all_text, 2)
        trigrams = self.extract_ngrams(all_text, 3)

        self.results = {
            'unigrams': Counter(unigrams),
            'bigrams': Counter(bigrams),
            'trigrams': Counter(trigrams),
            'total_words': len(unigrams),
            'file_count': file_count
        }

        return self.results

    def get_top_unigrams(self, limit: int = 50) -> List[Tuple[str, int]]:
        """Get top single words excluding stop words."""
        if not self.results:
            raise ValueError("Must call analyze() first")

        filtered = [
            (w, c) for w, c in self.results['unigrams'].items()
            if w not in self.STOP_WORDS and len(w) > 2
        ]
        return sorted(filtered, key=lambda x: x[1], reverse=True)[:limit]

    def get_top_bigrams(self, limit: int = 50) -> List[Tuple[str, int]]:
        """Get top two-word phrases excluding stop words."""
        if not self.results:
            raise ValueError("Must call analyze() first")

        filtered = [
            (p, c) for p, c in self.results['bigrams'].items()
            if not any(w in self.STOP_WORDS for w in p.split())
        ]
        return sorted(filtered, key=lambda x: x[1], reverse=True)[:limit]

    def get_top_trigrams(self, limit: int = 50) -> List[Tuple[str, int]]:
        """Get top three-word phrases."""
        if not self.results:
            raise ValueError("Must call analyze() first")

        filtered = [
            (p, c) for p, c in self.results['trigrams'].items()
            if len(p.split()) == 3
        ]
        return sorted(filtered, key=lambda x: x[1], reverse=True)[:limit]

    def calculate_savings(
        self,
        phrases: List[Tuple[str, int]],
        abbrev_length: int
    ) -> List[Tuple[str, int, int, int]]:
        """
        Calculate potential savings for phrases.

        Args:
            phrases: List of (phrase, count) tuples
            abbrev_length: Assumed abbreviation length

        Returns:
            List of (phrase, count, savings_per, total_score) tuples
        """
        scored = []
        for phrase, count in phrases:
            savings_per = len(phrase) - abbrev_length
            if savings_per > 2:  # Only if we save at least 3 chars
                score = count * savings_per
                scored.append((phrase, count, savings_per, score))

        return sorted(scored, key=lambda x: x[3], reverse=True)

    def generate_phrase_mappings(
        self,
        top_n: int = 30,
        bigram_abbrev_len: int = 4,
        trigram_abbrev_len: int = 5
    ) -> List[Tuple[str, str, int, int]]:
        """
        Generate optimized phrase mappings based on analysis.

        Args:
            top_n: Number of top phrases to include
            bigram_abbrev_len: Target abbreviation length for bigrams
            trigram_abbrev_len: Target abbreviation length for trigrams

        Returns:
            List of (phrase, abbreviation, count, savings) tuples
        """
        if not self.results:
            raise ValueError("Must call analyze() first")

        # Score bigrams and trigrams
        bigrams = self.get_top_bigrams(100)
        scored_bigrams = self.calculate_savings(bigrams, bigram_abbrev_len)

        trigrams = self.get_top_trigrams(50)
        scored_trigrams = self.calculate_savings(trigrams, trigram_abbrev_len)

        # Combine and sort by score
        all_scored = (
            [(p, c, s, sc, 2) for p, c, s, sc in scored_bigrams] +
            [(p, c, s, sc, 3) for p, c, s, sc in scored_trigrams]
        )
        all_scored.sort(key=lambda x: x[3], reverse=True)

        # Generate mappings
        mappings = []
        for phrase, count, savings_per, score, ngram_size in all_scored[:top_n]:
            # Simple abbreviation: first 2 letters of each word
            abbrev = ''.join(w[:2] for w in phrase.split())
            total_savings = count * savings_per
            mappings.append((phrase, abbrev, count, total_savings))

        return mappings

    def print_report(self, top_n: int = 50):
        """Print comprehensive analysis report."""
        if not self.results:
            raise ValueError("Must call analyze() first")

        print("=" * 70)
        print("PHRASE FREQUENCY ANALYSIS REPORT")
        print("=" * 70)
        print()
        print(f"Files analyzed: {self.results['file_count']}")
        print(f"Total words: {self.results['total_words']:,}")
        print()

        # Top unigrams
        print("=" * 70)
        print(f"TOP {top_n} SINGLE WORDS (excluding stop words)")
        print("=" * 70)
        for i, (word, count) in enumerate(self.get_top_unigrams(top_n), 1):
            print(f"{i:2}. {word:20} → {count:5} occurrences")
        print()

        # Top bigrams
        print("=" * 70)
        print(f"TOP {top_n} TWO-WORD PHRASES")
        print("=" * 70)
        for i, (phrase, count) in enumerate(self.get_top_bigrams(top_n), 1):
            savings = (len(phrase) - 4) * count
            print(f"{i:2}. {phrase:30} → {count:4}x (save ~{savings:5} chars)")
        print()

        # Suggested mappings
        print("=" * 70)
        print("SUGGESTED PHRASE MAPPINGS (Top 30 by impact)")
        print("=" * 70)
        print()
        mappings = self.generate_phrase_mappings(30)
        total_savings = sum(s for _, _, _, s in mappings)

        print("phrase_mappings:")
        for phrase, abbrev, count, savings in mappings:
            print(f'  "{phrase}": "{abbrev}"  # {count}x, save {savings} chars')

        print()
        print(f"Total potential savings: ~{total_savings:,} chars")
        print()
