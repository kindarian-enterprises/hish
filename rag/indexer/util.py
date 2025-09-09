import os
from typing import Iterable

import pathspec


def compile_globs(includes: str, excludes: str):
    inc = [g.strip() for g in (includes or "").split(",") if g.strip()]
    exc = [g.strip() for g in (excludes or "").split(",") if g.strip()]
    return pathspec.PathSpec.from_lines(
        "gitwildmatch", inc
    ), pathspec.PathSpec.from_lines("gitwildmatch", exc)


def iter_files(root: str, inc_spec, exc_spec) -> Iterable[str]:
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            rel = os.path.relpath(os.path.join(dirpath, f), root)
            if exc_spec.match_file(rel):
                continue
            if inc_spec.match_file(rel):
                yield rel


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        return fh.read()
