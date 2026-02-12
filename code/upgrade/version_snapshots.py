#!/usr/bin/env python3
"""
Compatibility entry point for upgrade note tooling.

The canonical implementation lives in ``code/system/version_snapshots.py``.
This thin wrapper keeps paths aligned with the active ``upgrade`` note.
"""

from pathlib import Path
import runpy


if __name__ == "__main__":
    target = Path(__file__).resolve().parents[1] / "system" / "version_snapshots.py"
    runpy.run_path(str(target), run_name="__main__")
