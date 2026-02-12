#!/usr/bin/env python3
"""Validate notebooks under notebooks/.

Default behavior lints notebooks (parse + basic structure checks).
Use --execute to run notebooks with nbclient.

Examples
  python tools/validate_notebooks.py
  python tools/validate_notebooks.py --execute --timeout 300
  python tools/validate_notebooks.py --report-json tools/nb_report.json --report-md tools/nb_report.md
"""

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

try:  # Optional for lint mode; required for execute mode.
    import nbformat  # type: ignore
except Exception:  # pragma: no cover
    nbformat = None  # type: ignore


@dataclass
class Result:
    notebook: str
    mode: str
    ok: bool
    duration: float
    message: str = ""


def discover(patterns: Iterable[str]) -> List[Path]:
    paths: List[Path] = []
    for pat in patterns:
        paths.extend(sorted(Path().glob(pat)))
    return [p for p in paths if p.is_file() and p.suffix == ".ipynb"]


def normalize_ids(nb) -> None:
    for cell in getattr(nb, "cells", []) or []:
        if isinstance(cell, dict):
            cell.setdefault("id", os.urandom(8).hex())


def lint_notebook(path: Path) -> Result:
    t0 = time.perf_counter()
    try:
        if nbformat is not None:
            nb = nbformat.read(path, as_version=4)
            normalize_ids(nb)
            cells = nb.get("cells", [])
        else:
            raw = json.loads(path.read_text(encoding="utf-8"))
            cells = raw.get("cells", [])
        if not cells:
            raise ValueError("notebook has no cells")
        has_code = any(c.get("cell_type") == "code" for c in cells)
        if not has_code:
            raise ValueError("notebook has no code cells")
        ok = True
        msg = ""
    except Exception as exc:
        ok = False
        msg = str(exc)
    dur = time.perf_counter() - t0
    print(f"[lint] {path} -> {'OK' if ok else 'FAIL'} ({dur:.2f}s)")
    return Result(str(path), "lint", ok, dur, msg)


def execute_notebook(path: Path, timeout: int, kernel: str, out_dir: Path) -> Result:
    if nbformat is None:
        raise SystemExit(
            "Execute mode requires nbformat and nbclient. Install with: "
            "python -m pip install nbclient nbformat"
        )
    try:
        from nbclient import NotebookClient  # type: ignore
        from nbclient.exceptions import CellExecutionError  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise SystemExit(
            "Missing dependencies nbclient/nbformat. Install with: python -m pip install nbclient nbformat"
        ) from exc

    os.environ.setdefault("MPLBACKEND", "Agg")
    t0 = time.perf_counter()
    msg = ""
    ok = True
    try:
        nb = nbformat.read(path, as_version=4)
        normalize_ids(nb)
        client = NotebookClient(nb, timeout=timeout, kernel_name=kernel)
        client.execute()
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{path.stem}.executed.ipynb"
        nbformat.write(nb, out_path)
    except CellExecutionError as exc:
        ok = False
        msg = str(exc)
    except Exception as exc:
        ok = False
        msg = str(exc)
    dur = time.perf_counter() - t0
    print(f"[exec] {path} -> {'OK' if ok else 'FAIL'} ({dur:.2f}s)")
    return Result(str(path), "execute", ok, dur, msg)


def print_summary(results: List[Result]) -> None:
    total = len(results)
    passed = sum(1 for r in results if r.ok)
    print("\nNotebook validation summary:")
    for r in results:
        status = "OK" if r.ok else "FAIL"
        print(f"  {Path(r.notebook).name:55} {status:5} {r.duration:6.2f}s")
    print(f"\nPassed {passed}/{total} notebooks")


def write_reports(results: List[Result], json_path: Optional[Path], md_path: Optional[Path]) -> None:
    if json_path:
        payload = [
            {
                "notebook": r.notebook,
                "mode": r.mode,
                "ok": r.ok,
                "duration": r.duration,
                "message": r.message,
            }
            for r in results
        ]
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(payload, indent=2))

    if md_path:
        lines = ["# Notebook Validation Report", ""]
        for r in results:
            status = "OK" if r.ok else "FAIL"
            lines.append(f"- {status}: `{r.notebook}` ({r.duration:.2f}s)")
            if r.message and not r.ok:
                lines.append(f"  - message: `{r.message[:300]}`")
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text("\n".join(lines))


def main(argv: Optional[Iterable[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--include",
        action="append",
        default=None,
        help="glob(s) to include (default: notebooks/*_book/*.ipynb)",
    )
    p.add_argument("--exclude", action="append", default=[], help="glob(s) to exclude")
    p.add_argument("--execute", action="store_true", help="execute notebooks instead of lint-only checks")
    p.add_argument("--timeout", type=int, default=300, help="timeout in execute mode")
    p.add_argument("--kernel", default="python3")
    p.add_argument("--executed-dir", type=Path, default=Path("tools/_executed"))
    p.add_argument("--fail-fast", action="store_true")
    p.add_argument("--list", action="store_true")
    p.add_argument("--report-json", type=Path)
    p.add_argument("--report-md", type=Path)
    args = p.parse_args(list(argv) if argv is not None else None)

    if args.execute and nbformat is None:
        print(
            "Execute mode requires nbformat and nbclient. Install with: "
            "python -m pip install nbclient nbformat"
        )
        return 1

    includes = args.include or ["notebooks/*_book/*.ipynb"]
    notebooks = discover(includes)
    excluded = {p.resolve() for pat in args.exclude for p in Path().glob(pat)}
    notebooks = [n for n in notebooks if n.resolve() not in excluded]

    if not notebooks:
        print("No notebooks found.")
        return 1

    if args.list:
        for n in notebooks:
            print(n)
        return 0

    results: List[Result] = []
    rc = 0
    for n in notebooks:
        if args.execute:
            res = execute_notebook(n, args.timeout, args.kernel, args.executed_dir)
        else:
            res = lint_notebook(n)
        results.append(res)
        if not res.ok:
            rc = 2
            if args.fail_fast:
                break

    print_summary(results)
    write_reports(results, args.report_json, args.report_md)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
