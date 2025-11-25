#!/usr/bin/env python3
"""
Crypto Engineering Notes – Transaction

Thin wrapper around bitcoin-cli for regtest experiments.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import json
import subprocess
from typing import Any


def cli(*args: str) -> Any:
    """Call `bitcoin-cli -regtest` and return parsed JSON where possible."""
    out = subprocess.check_output(
        ["bitcoin-cli", "-regtest", *args],
        text=True,
    )
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return out.strip()


def main() -> None:
    info = cli("getblockchaininfo")
    print("blocks:", info["blocks"])


if __name__ == "__main__":
    main()

