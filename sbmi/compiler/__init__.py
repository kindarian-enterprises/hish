"""
Index compiler for SBMI system.

Compiles workflow indexes into compressed .compact format using
configurable compression strategies and hash-based incremental compilation.
"""

from sbmi.compiler.cache import CompilationCache
from sbmi.compiler.compiler import IndexCompiler
from sbmi.compiler.config import CompressionConfig
from sbmi.compiler.strategies import (
    CombinedCompressionStrategy,
    CompressionStrategy,
    CompressionStrategyFactory,
    PhraseCompressionStrategy,
    StructuralCompressionStrategy,
)

__all__ = [
    "IndexCompiler",
    "CompressionConfig",
    "CompilationCache",
    "CompressionStrategy",
    "StructuralCompressionStrategy",
    "PhraseCompressionStrategy",
    "CombinedCompressionStrategy",
    "CompressionStrategyFactory",
]
