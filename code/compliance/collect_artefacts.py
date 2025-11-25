#!/usr/bin/env python3
"""
Crypto Engineering Notes – Compliance

Collect candidate documentation, tests, and monitoring artefacts from a repo tree.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator


ROOT = Path(".")


@dataclass
class Artefact:
    kind: str
    path: str


def iter_artefacts(root: Path) -> Iterator[Artefact]:
    """Yield Artefact records discovered under root."""
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel.endswith((".md", ".rst")):
            yield Artefact(kind="doc", path=rel)
        elif "tests" in rel and rel.endswith(".py"):
            yield Artefact(kind="test", path=rel)
        elif "dashboards" in rel or "grafana" in rel:
            yield Artefact(kind="dashboard", path=rel)
        elif "alerts" in rel or "prometheus" in rel:
            yield Artefact(kind="alert", path=rel)


def main() -> None:
    for art in iter_artefacts(ROOT):
        print(art.kind, "->", art.path)


if __name__ == "__main__":
    main()

