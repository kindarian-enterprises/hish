"""
Index compiler for SBMI system.

Compiles workflow indexes into compressed .compact format using
configurable compression strategies and hash-based incremental compilation.
"""

from sbmi.compiler.compiler import IndexCompiler
from sbmi.compiler.config import CompressionConfig
from sbmi.compiler.cache import CompilationCache
from sbmi.compiler.strategies import (
    CompressionStrategy,
    StructuralCompressionStrategy,
    PhraseCompressionStrategy,
    CombinedCompressionStrategy,
    CompressionStrategyFactory,
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
