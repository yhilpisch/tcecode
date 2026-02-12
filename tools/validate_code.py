#!/usr/bin/env python3
"""Validate Python scripts under code/.

Default behavior compiles files with py_compile (safe, fast).
Use --execute to run scripts instead.

Examples
  python tools/validate_code.py
  python tools/validate_code.py --execute --timeout 60 --fail-fast
  python tools/validate_code.py --report-json tools/code_report.json --report-md tools/code_report.md
"""

from __future__ import annotations

import argparse
import json
import os
import py_compile
import re
import shutil
import subprocess as sp
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional


SKIPPABLE_REASON_PREFIXES = (
    "missing_binary:",
    "missing_input_file:",
    "missing_required_cli_args",
    "unreachable_rpc_endpoint",
)


@dataclass
class Result:
    path: str
    mode: str
    ok: bool
    duration: float
    returncode: int
    message: str = ""
    reason: str = ""
    skipped: bool = False


def discover(patterns: Iterable[str]) -> List[Path]:
    paths: List[Path] = []
    for pat in patterns:
        paths.extend(sorted(Path().glob(pat)))
    return [
        p
        for p in paths
        if p.is_file() and p.suffix == ".py" and p.name != "__init__.py"
    ]


def run_compile(path: Path) -> Result:
    t0 = time.perf_counter()
    try:
        py_compile.compile(str(path), doraise=True)
        ok = True
        rc = 0
        msg = ""
    except py_compile.PyCompileError as exc:
        ok = False
        rc = 1
        msg = str(exc)
    dur = time.perf_counter() - t0
    print(f"[compile] {path} -> rc={rc} ({dur:.2f}s)")
    reason = "" if ok else "compile_error"
    return Result(str(path), "compile", ok, dur, rc, msg, reason, False)


def classify_failure(message: str, returncode: int) -> str:
    m_mod = re.search(r"No module named '([^']+)'", message)
    if m_mod:
        return f"missing_module:{m_mod.group(1)}"
    if "No such file or directory: 'bitcoin-cli'" in message:
        return "missing_binary:bitcoin-cli"
    m_file = re.search(r"No such file or directory: '([^']+)'", message)
    if m_file:
        return f"missing_input_file:{m_file.group(1)}"
    if "the following arguments are required" in message or returncode == 2:
        return "missing_required_cli_args"
    if (
        "Failed to resolve" in message
        or "NameResolutionError" in message
        or "Max retries exceeded" in message
        or "ConnectionError" in message
        or "rpc.testnet.example" in message
    ):
        return "unreachable_rpc_endpoint"
    if "timeout" in message.lower() or returncode == 124:
        return "timeout"
    return "runtime_error"


def run_execute(path: Path, timeout: int, interpreter: str) -> Result:
    env = os.environ.copy()
    env.setdefault("MPLBACKEND", "Agg")
    repo_root = Path(__file__).resolve().parent.parent
    old_pp = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(repo_root) if not old_pp else f"{repo_root}:{old_pp}"
    t0 = time.perf_counter()
    try:
        proc = sp.run(
            [interpreter, str(path)],
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
        rc = proc.returncode
        ok = rc == 0
        msg = (proc.stderr or proc.stdout or "").strip()[-4000:]
    except sp.TimeoutExpired:
        dur = time.perf_counter() - t0
        print(f"[run] {path} -> timeout ({timeout}s)")
        return Result(str(path), "run", False, dur, 124, "timeout", "timeout", False)
    dur = time.perf_counter() - t0
    print(f"[run] {path} -> rc={rc} ({dur:.2f}s)")
    reason = "" if ok else classify_failure(msg, rc)
    return Result(str(path), "run", ok, dur, rc, msg, reason, False)


def default_execute_python() -> str:
    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
        candidate = Path(venv) / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        if candidate.exists():
            return str(candidate)
    path_python = shutil.which("python")
    if path_python:
        return path_python
    return sys.executable


def should_skip(result: Result, strict_execute: bool) -> bool:
    if result.mode != "run" or strict_execute:
        return False
    if result.ok:
        return False
    return any(
        result.reason == prefix or result.reason.startswith(prefix)
        for prefix in SKIPPABLE_REASON_PREFIXES
    )


def print_summary(results: List[Result]) -> None:
    total = len(results)
    passed = sum(1 for r in results if r.ok)
    skipped = sum(1 for r in results if r.skipped)
    failed = total - passed - skipped
    print("\nCode validation summary:")
    for r in results:
        if r.ok:
            status = "OK"
        elif r.skipped:
            status = f"SKIP({r.returncode})"
        else:
            status = f"FAIL({r.returncode})"
        print(f"  {Path(r.path).name:40} {status:10} {r.duration:6.2f}s")
        if (not r.ok or r.skipped) and r.reason:
            print(f"    reason: {r.reason}")
    print(f"\nPassed {passed}/{total} files")
    if skipped:
        print(f"Skipped {skipped}/{total} files")
    if failed:
        print(f"Failed {failed}/{total} files")


def write_reports(results: List[Result], json_path: Optional[Path], md_path: Optional[Path]) -> None:
    if json_path:
        payload = [
            {
                "path": r.path,
                "mode": r.mode,
                "ok": r.ok,
                "duration": r.duration,
                "returncode": r.returncode,
                "message": r.message,
                "reason": r.reason,
                "skipped": r.skipped,
            }
            for r in results
        ]
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(payload, indent=2))

    if md_path:
        lines = ["# Code Validation Report", ""]
        for r in results:
            if r.ok:
                status = "OK"
            elif r.skipped:
                status = f"SKIP ({r.returncode})"
            else:
                status = f"FAIL ({r.returncode})"
            lines.append(f"- {status}: `{r.path}` ({r.duration:.2f}s)")
            if r.message and (not r.ok or r.skipped):
                lines.append(f"  - message: `{r.message[:300]}`")
            if r.reason and (not r.ok or r.skipped):
                lines.append(f"  - reason: `{r.reason}`")
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text("\n".join(lines))


def main(argv: Optional[Iterable[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--include", action="append", help="glob(s) to include (default: code/**/*.py)")
    p.add_argument("--exclude", action="append", default=[], help="glob(s) to exclude")
    p.add_argument("--execute", action="store_true", help="execute scripts instead of compile-only checks")
    p.add_argument(
        "--python",
        default=default_execute_python(),
        help="Python interpreter to use in execute mode (default: active shell python)",
    )
    p.add_argument(
        "--strict-execute",
        action="store_true",
        help="in execute mode, treat missing binaries/input files/required args as failures",
    )
    p.add_argument("--timeout", type=int, default=60, help="timeout in execute mode")
    p.add_argument("--fail-fast", action="store_true")
    p.add_argument("--list", action="store_true")
    p.add_argument("--report-json", type=Path)
    p.add_argument("--report-md", type=Path)
    args = p.parse_args(list(argv) if argv is not None else None)

    includes = args.include or ["code/**/*.py"]
    files = discover(includes)
    excluded = {p.resolve() for pat in args.exclude for p in Path().glob(pat)}
    files = [f for f in files if f.resolve() not in excluded]

    if not files:
        print("No files found.")
        return 1

    if args.list:
        for f in files:
            print(f)
        return 0

    results: List[Result] = []
    rc = 0
    if args.execute:
        print(f"Execute mode interpreter: {args.python}")
    for f in files:
        res = run_execute(f, args.timeout, args.python) if args.execute else run_compile(f)
        res.skipped = should_skip(res, args.strict_execute)
        results.append(res)
        if (not res.ok) and (not res.skipped):
            rc = 2
            if args.fail_fast:
                break

    print_summary(results)
    write_reports(results, args.report_json, args.report_md)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
