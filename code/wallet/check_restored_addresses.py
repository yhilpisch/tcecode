#!/usr/bin/env python3
"""
Crypto Engineering Notes – Wallet

Checking restored addresses against the lab wallet metadata file.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import json
from pathlib import Path
from typing import List


def expected_addresses(store: Path, label: str) -> List[str]:
    data = json.loads(store.read_text())
    return data[label]["first_addresses"]


def main() -> None:
    lab_file = Path("wallet_lab.json")
    label = "mobile_testnet_1"
    expected = expected_addresses(lab_file, label)
    restored = [
        "tb1qexampleaddress1",
        "tb1qexampleaddress2",
    ]
    matches = expected == restored
    print("expected:", expected)
    print("restored:", restored)
    print("match:", matches)


if __name__ == "__main__":
    main()

