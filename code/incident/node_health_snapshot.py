#!/usr/bin/env python3
"""
Crypto Engineering Notes – Incident

Quick node health snapshot combining blockchain and mempool information.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import json

from code.policy.fee_policy import mempool_info  # type: ignore[import-not-found]
from code.transaction.cli_wrapper import cli  # type: ignore[import-not-found]


def node_health() -> dict:
    info = cli("getblockchaininfo")
    mem = mempool_info()
    return {
        "blocks": info["blocks"],
        "initial_block_download": info.get("initialblockdownload", False),
        "mempool_size": mem["size"],
        "mempool_min_fee": mem.get("mempoolminfee", 0.0),
    }


def main() -> None:
    print(json.dumps(node_health(), indent=2))


if __name__ == "__main__":
    main()
