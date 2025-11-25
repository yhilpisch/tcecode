#!/usr/bin/env python3
"""
Crypto Engineering Notes – System / Upgrade

Capture and diff node version snapshots around upgrades.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class NodeVersion:
    name: str
    command: List[str]


NODES: List[NodeVersion] = [
    NodeVersion(
        name="bitcoin", command=["bitcoin-cli", "-regtest", "getnetworkinfo"]
    ),
]


def capture_versions() -> Dict[str, str]:
    versions: Dict[str, str] = {}
    for node in NODES:
        try:
            raw = subprocess.check_output(node.command, text=True)
        except Exception as exc:
            versions[node.name] = f"error: {exc}"
            continue
        try:
            info = json.loads(raw)
            versions[node.name] = info.get("subversion", "").strip("/")
        except json.JSONDecodeError:
            versions[node.name] = raw.strip()
    return versions


def write_snapshot(path: Path) -> None:
    data = {
        "versions": capture_versions(),
    }
    path.write_text(json.dumps(data, indent=2))


def load_versions(path: Path) -> Dict[str, str]:
    data = json.loads(path.read_text())
    return data.get("versions", {})


def diff_versions(before: Path, after: Path) -> None:
    v_before = load_versions(before)
    v_after = load_versions(after)
    all_names = sorted(set(v_before) | set(v_after))
    for name in all_names:
        old = v_before.get(name, "<missing>")
        new = v_after.get(name, "<missing>")
        marker = "OK" if old == new else "CHANGED"
        print(f"{name:10} {old:20} -> {new:20} [{marker}]")


def main() -> None:
    snapshot_path = Path("upgrade_snapshot.json")
    write_snapshot(snapshot_path)
    print(f"wrote snapshot to {snapshot_path}")


if __name__ == "__main__":
    main()

