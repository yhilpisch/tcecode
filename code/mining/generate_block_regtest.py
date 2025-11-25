#!/usr/bin/env python3
"""
Crypto Engineering Notes – Mining

Generate blocks on Bitcoin Core regtest and print the new block hashes.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import json
import subprocess
from typing import Any, Dict, List


def cli(*args: str) -> Dict[str, Any]:
    """Call bitcoin-cli with -regtest and parse JSON output when possible."""
    out = subprocess.check_output(["bitcoin-cli", "-regtest", *args], text=True)
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"raw": out.strip()}


def main() -> None:
    addr_info = cli("getnewaddress")
    addr = addr_info.get("raw") or addr_info
    if isinstance(addr, dict):
        raise SystemExit(f"Unexpected address structure: {addr!r}")
    print("mining to:", addr)
    result: List[str] = cli("generatetoaddress", "1", addr).get("raw") or []
    print("new blocks:", result)


if __name__ == "__main__":
    main()

