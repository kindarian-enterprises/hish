"""
Main index compiler for SBMI system.
"""

import fnmatch
from pathlib import Path
from typing import Dict, Set, Optional

from sbmi.compiler.config import CompressionConfig
from sbmi.compiler.strategies import CompressionStrategy, CompressionStrategyFactory
from sbmi.compiler.cache import CompilationCache


class IndexCompiler:
    """Compiles workflow indexes into compressed .compact format."""

    def __init__(
        self,
        hish_root: Path,
        config: Optional[CompressionConfig] = None,
        use_cache: bool = True
    ):
        """
        Initialize compiler.

        Args:
            hish_root: Root directory of hish framework
            config: CompressionConfig instance (uses default if None)
            use_cache: Enable hash-based incremental compilation
        """
        self.hish_root = hish_root
        self.workflow_indexes = hish_root / "local" / "workflow-indexes"
        self.config = config or CompressionConfig()

        # Build scan directories from config
        self.scan_dirs = [
            hish_root / scan_dir
            for scan_dir in self.config.scan_directories
        ]

        self.excluded_files: Set[Path] = set()
        self.processed_files: Dict[str, dict] = {}

        # Initialize cache for incremental compilation
        self.use_cache = use_cache
        if use_cache:
            cache_file = hish_root / "local" / ".sbmi-cache.json"
            self.cache = CompilationCache(cache_file)
        else:
            self.cache = None

    def is_excluded(self, filepath: Path) -> bool:
        """
        Check if file matches exclusion patterns or is in excluded directory.

        Args:
            filepath: Path to check

        Returns:
            True if file should be excluded from compression
        """
        filepath_str = str(filepath)

        # Check excluded directories first
        for excluded_dir in self.config.excluded_directories:
            # Handle wildcard patterns like **/node_modules
            if excluded_dir.startswith('**/'):
                dir_name = excluded_dir[3:]
                if f"/{dir_name}/" in filepath_str or filepath_str.endswith(f"/{dir_name}"):
                    return True
            # Handle exact directory matches
            else:
                excluded_path = self.hish_root / excluded_dir
                try:
                    # Check if filepath is relative to excluded directory
                    filepath.relative_to(excluded_path)
                    return True
                except ValueError:
                    # Not relative to this excluded dir
                    pass

        # Check file exclusion patterns
        for pattern in self.config.exclusion_patterns:
            # Handle directory patterns
            if pattern.endswith('/**'):
                dir_pattern = pattern[:-3]
                if dir_pattern.startswith('**/'):
                    dir_name = dir_pattern[3:]
                    if f"/{dir_name}/" in filepath_str:
                        return True
            # Handle file patterns
            elif fnmatch.fnmatch(filepath_str, pattern):
                return True
            # Handle simple contains
            elif pattern.replace('**/', '') in filepath_str:
                return True

        return False

    def compress_index(
        self,
        source_file: Path,
        level: str = "level2",
        strategy: Optional[CompressionStrategy] = None
    ) -> Path:
        """
        Compress a workflow index file OR copy if excluded.

        For excluded files (behavioral context), creates a verbatim .compact copy
        so agents can uniformly read *.compact files.

        Args:
            source_file: Path to source index file
            level: Compression level name (e.g., 'level1', 'level2')
            strategy: CompressionStrategy to use (creates from config if None)

        Returns:
            Path to output .compact file
        """
        if self.is_excluded(source_file):
            # Copy excluded files verbatim with .compact extension
            content = source_file.read_text()

            # Add header noting this is a verbatim copy
            header = f"""# {source_file.stem} (Behavioral Context - Uncompressed)
#
# AUTOMATICALLY COPIED - DO NOT EDIT
# Source: {source_file.name}
# Status: EXCLUDED from compression (behavioral layer)
#
# This file is preserved in full to maintain agent behavioral context.
# For compression rules, see: compression-exclusion-rules.md
#

"""
            full_content = header + content
            line_count = len(full_content.split('\n'))

            # Determine weight level for excluded file
            weight_level = self.config.get_weight_level(line_count)

            # Create output path with weight level
            output_file = source_file.parent / f"{source_file.stem}.L{weight_level}.compact"
            output_file.write_text(full_content)

            # Track as excluded but processed
            self.excluded_files.add(source_file)
            self.processed_files[source_file.name] = {
                'source': source_file,
                'output': output_file,
                'original_lines': len(content.split('\n')),
                'compressed_lines': len(content.split('\n')),
                'original_chars': len(content),
                'compressed_chars': len(content),
                'reduction_pct': 0.0,
                'level': 'excluded',
                'strategy': 'verbatim_copy',
                'weight_level': weight_level
            }

            # Update cache
            if self.cache:
                self.cache.mark_compiled(source_file, output_file, 0.0)

            print(f"  ≡ {source_file.name} → {output_file.name} (VERBATIM L{weight_level})")

            return output_file

        # Create strategy from config if not provided
        if strategy is None:
            strategy_names = self.config.get_level_strategies(level)
            if not strategy_names:
                # Fall back to default
                strategy = CompressionStrategyFactory.create(
                    self.config.default_strategy
                )
            else:
                strategy = CompressionStrategyFactory.create_from_list(
                    strategy_names
                )

        # Read and compress
        content = source_file.read_text()
        original_lines = len(content.split('\n'))
        original_chars = len(content)

        compressed = strategy.compress(content, self.config.as_dict())

        # Add header to compressed version
        header = f"""# {source_file.stem} (Compressed - {level.upper()})
#
# AUTOMATICALLY GENERATED - DO NOT EDIT
# Source: {source_file.name}
# Strategy: {strategy.name}
# Target: {self._get_target_reduction(level)}
#
# For human-readable version, see: {source_file.name}
# For compression rules, see: compression-exclusion-rules.md
#

"""
        compressed = header + compressed

        # Calculate size stats before writing
        compressed_lines = len(compressed.split('\n'))
        compressed_chars = len(compressed)
        reduction_pct = ((original_chars - compressed_chars) / original_chars) * 100 if original_chars > 0 else 0

        # Determine weight level based on output size
        weight_level = self.config.get_weight_level(compressed_lines)

        # Determine output filename with weight level
        output_name = self._get_output_name(source_file.stem, level, weight_level)
        output_file = source_file.parent / output_name
        output_file.write_text(compressed)

        self.processed_files[source_file.name] = {
            'source': source_file,
            'output': output_file,
            'original_lines': original_lines,
            'compressed_lines': compressed_lines,
            'original_chars': original_chars,
            'compressed_chars': compressed_chars,
            'reduction_pct': reduction_pct,
            'level': level,
            'strategy': strategy.name
        }

        # Update cache
        if self.cache:
            self.cache.mark_compiled(source_file, output_file, reduction_pct)

        print(f"  ✓ {source_file.name} → {output_name}")
        print(f"    {original_lines}L → {compressed_lines}L ({reduction_pct:.1f}% char reduction)")

        return output_file

    def _find_all_markdown_files(self) -> Set[Path]:
        """
        Find all markdown files in scan directories.

        Includes files that will be:
        - Compressed (regular framework files)
        - Copied verbatim (excluded via patterns like *persona.md)

        Excludes files in:
        - Excluded directories (e.g., style-and-philosophy/)
        - Already processed (.compact files)
        """
        all_md_files = set()

        for scan_dir in self.scan_dirs:
            if not scan_dir.exists():
                continue

            for md_file in scan_dir.rglob("*.md"):
                # Skip already compressed/copied files
                if md_file.stem.endswith(('-level1', '-level2')):
                    continue
                if md_file.name.endswith('.compact'):
                    continue

                # Skip files in excluded directories (e.g., style-and-philosophy/)
                # but INCLUDE files matching exclusion patterns (e.g., *persona.md)
                # Those will be copied verbatim in compress_index()
                if self._is_in_excluded_directory(md_file):
                    continue

                all_md_files.add(md_file)

        return all_md_files

    def _is_in_excluded_directory(self, filepath: Path) -> bool:
        """Check if file is in an excluded directory (not pattern-based exclusion)."""
        filepath_str = str(filepath)

        for excluded_dir in self.config.excluded_directories:
            # Handle wildcard patterns like **/node_modules
            if excluded_dir.startswith('**/'):
                dir_name = excluded_dir[3:]
                if f"/{dir_name}/" in filepath_str or filepath_str.endswith(f"/{dir_name}"):
                    return True
            # Handle exact directory matches
            else:
                excluded_path = self.hish_root / excluded_dir
                try:
                    # Check if filepath is relative to excluded directory
                    filepath.relative_to(excluded_path)
                    return True
                except ValueError:
                    # Not relative to this excluded dir
                    pass

        return False

    def compile_changed_indexes(self, level: str = "level2") -> Dict[str, dict]:
        """
        Incrementally compile only changed/new framework documentation files.

        Uses hash-based cache to detect changes. Perfect for session-end workflows.
        Scans: docs/, templates/, prompts/, local/ (excluding behavioral files)

        Args:
            level: Compression level to use

        Returns:
            Dict of compilation results for changed files
        """
        if not self.use_cache:
            print("⚠️  Cache disabled - falling back to compile_all_indexes")
            return self.compile_all_indexes(level)

        print("\n" + "=" * 70)
        print("SBMI INCREMENTAL COMPILATION (Session End)")
        print("=" * 70)
        print(f"\nFramework root: {self.hish_root}")
        print(f"Scan dirs: templates/, prompts/, local/")
        print(f"Excluded: docs/, personas, style-and-philosophy/")
        print(f"Config: {self.config.config_path}")
        print(f"Level: {level}")

        # Get cache stats
        stats = self.cache.get_stats()
        print(f"\nCache stats:")
        print(f"  Total previously compiled: {stats['total_compiled']}")
        print(f"  Avg reduction: {stats['avg_reduction']:.1f}%")
        if stats['last_compiled']:
            print(f"  Last compiled: {stats['last_compiled']}")
        print()

        # Find all eligible markdown files
        all_md_files = self._find_all_markdown_files()

        # Get changed/new files
        changed_files = self.cache.get_changed_files(all_md_files)

        if not changed_files:
            print("✓ No changes detected - all framework docs up to date!")
            print()
            return {}

        print(f"📝 Detected {len(changed_files)} changed/new files:\n")
        for f in sorted(changed_files):
            status = "NEW" if str(f) not in self.cache.cache else "CHANGED"
            rel_path = f.relative_to(self.hish_root)
            print(f"  {status}: {rel_path}")
        print()

        # Compile changed files
        for md_file in sorted(changed_files):
            self.compress_index(md_file, level=level)

        # Report summary
        self._print_incremental_summary(len(all_md_files), len(changed_files))

        return self.processed_files

    def compile_all_indexes(self, level: str = "level2") -> Dict[str, dict]:
        """
        Compile all framework documentation files using config-driven scanning.

        Args:
            level: Compression level to use

        Returns:
            Dict of compilation results
        """
        print("\n" + "=" * 70)
        print("SBMI FRAMEWORK COMPILATION")
        print("=" * 70)
        print(f"\nScan directories: {', '.join(str(d) for d in self.scan_dirs)}")
        print(f"Config: {self.config.config_path}")
        print(f"Level: {level}")
        print()

        # Find all .md files using config-driven scanning
        index_files = self._find_all_markdown_files()

        # Filter out already compressed files
        index_files = [
            f for f in index_files
            if not f.stem.endswith(('-level1', '-level2'))
            and not f.name.endswith('.compact')
        ]

        if not index_files:
            print("No framework files found to compile.")
            return {}

        print(f"Found {len(index_files)} framework files to compile:\n")

        # Compile each index
        for index_file in sorted(index_files):
            self.compress_index(index_file, level=level)

        # Report summary
        self._print_summary()

        return self.processed_files

    def _get_target_reduction(self, level: str) -> str:
        """Get target reduction percentage for level."""
        level_config = self.config.get_level_config(level)
        if level_config:
            return level_config.get('target_reduction', 'N/A')
        return 'N/A'

    def _get_output_name(self, stem: str, level: str, weight_level: int) -> str:
        """
        Determine output filename based on weight level.

        Args:
            stem: Base filename without extension
            level: Compression level (e.g., 'level2') - currently unused
            weight_level: Weight level based on output size (1, 2, 3, etc.)

        Returns:
            Output filename with .L{weight}.compact extension
        """
        return f"{stem}.L{weight_level}.compact"

    def _print_incremental_summary(self, total_files: int, changed_files: int) -> None:
        """Print incremental compilation summary."""
        print("\n" + "=" * 70)
        print("INCREMENTAL COMPILATION SUMMARY")
        print("=" * 70)
        print()

        print(f"Total framework files: {total_files}")
        print(f"Changed/new files: {changed_files}")
        print(f"Up-to-date files: {total_files - changed_files}")
        print()

        if self.processed_files:
            # Separate compressed vs verbatim
            compressed = {k: v for k, v in self.processed_files.items() if v['strategy'] != 'verbatim_copy'}
            verbatim = {k: v for k, v in self.processed_files.items() if v['strategy'] == 'verbatim_copy'}

            if compressed:
                total_original = sum(f['original_chars'] for f in compressed.values())
                total_compressed_chars = sum(f['compressed_chars'] for f in compressed.values())
                overall_reduction = ((total_original - total_compressed_chars) / total_original) * 100 if total_original > 0 else 0

                print(f"Files compressed: {len(compressed)}")
                print(f"Overall reduction: {overall_reduction:.1f}%")
                print()
                print("Compressed files:")
                for name, stats in compressed.items():
                    print(f"  ✓ {name}: {stats['reduction_pct']:.1f}% reduction ({stats['strategy']})")

            if verbatim:
                print()
                print(f"Files copied verbatim (behavioral context): {len(verbatim)}")
                for name, stats in verbatim.items():
                    print(f"  ≡ {name}: preserved in full")

        print("\n" + "=" * 70)
        print()

    def _print_summary(self) -> None:
        """Print compilation summary."""
        print("\n" + "=" * 70)
        print("COMPILATION SUMMARY")
        print("=" * 70)
        print()

        if self.processed_files:
            total_original = sum(f['original_chars'] for f in self.processed_files.values())
            total_compressed = sum(f['compressed_chars'] for f in self.processed_files.values())
            overall_reduction = ((total_original - total_compressed) / total_original) * 100

            print(f"Files compiled: {len(self.processed_files)}")
            print(f"Overall reduction: {overall_reduction:.1f}%")
            print()
            print("Individual results:")
            for name, stats in self.processed_files.items():
                print(f"  {name}: {stats['reduction_pct']:.1f}% reduction ({stats['strategy']})")

        if self.excluded_files:
            print(f"\nFiles excluded (behavioral): {len(self.excluded_files)}")
            for excluded in sorted(self.excluded_files):
                print(f"  ⊗ {excluded.name}")

        print("\n" + "=" * 70)
        print("NEXT STEPS")
        print("=" * 70)
        print("""
1. Review compressed .compact files for correctness
2. Test compressed indexes in agent session
3. Verify agent can navigate using compressed indexes
4. Confirm behavioral files still load in full
5. Document expansion protocol (L1→L2→L3)
6. Update init prompts to use compressed indexes
""")
