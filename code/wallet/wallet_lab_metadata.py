#!/usr/bin/env python3
"""
Crypto Engineering Notes – Wallet

Tracking lab wallet metadata in a JSON file.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import json
from pathlib import Path
from typing import List


def add_wallet_record(
    store: Path,
    label: str,
    seed_words: str,
    network: str,
    first_addresses: List[str],
) -> None:
    if store.exists():
        data = json.loads(store.read_text())
    else:
        data = {}
    data[label] = {
        "seed_words": seed_words,
        "network": network,
        "first_addresses": first_addresses,
    }
    store.write_text(json.dumps(data, indent=2))


def main() -> None:
    lab_file = Path("wallet_lab.json")
    add_wallet_record(
        lab_file,
        label="mobile_testnet_1",
        seed_words="abandon abandon abandon ... (lab only!)",
        network="testnet",
        first_addresses=[
            "tb1qexampleaddress1",
            "tb1qexampleaddress2",
        ],
    )
    print(lab_file.read_text())


if __name__ == "__main__":
    main()

