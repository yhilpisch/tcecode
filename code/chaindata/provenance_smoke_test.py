#!/usr/bin/env python3
"""
Crypto Engineering Notes – Chaindata

Provenance smoke test comparing local row counts to chain data.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

from datetime import datetime
import os

import requests


RPC_ENDPOINT = os.environ.get("RPC_ENDPOINT", "https://rpc.testnet.example")
LOCAL_COUNT = int(os.environ.get("LOCAL_COUNT", "123456"))
BLOCK_HEIGHT = int(os.environ.get("BLOCK_HEIGHT", "10500"))
EXPECTED_TX_PER_BLOCK = float(os.environ.get("EXPECTED_TX_PER_BLOCK", "42"))


def main() -> None:
    payload = requests.post(
        RPC_ENDPOINT,
        json={
            "method": "eth_getBlockByNumber",
            "params": [hex(BLOCK_HEIGHT), False],
        },
        timeout=10,
    )
    payload.raise_for_status()
    chain_hash = payload.json()["result"]["hash"]

    print("Checked at      :", datetime.utcnow().isoformat() + "Z")
    print("Chain hash      :", chain_hash)
    print("Local row count :", LOCAL_COUNT)

    if LOCAL_COUNT < BLOCK_HEIGHT * EXPECTED_TX_PER_BLOCK:
        raise SystemExit("Row count looks stale—rerun the ingestion job.")


if __name__ == "__main__":
    main()

