#!/usr/bin/env python3
"""
Crypto Engineering Notes – Failures

Minimal MAC test harness for truncation length and canonical JSON equivalence.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

from code.failures.mac_helpers import (
    hmac_sha256,
    truncated_mac,
    mac_over_payload,
)


def test_truncation_length() -> None:
    key = b"lab-key-3"
    mac = hmac_sha256(key, b"message-1")
    short = truncated_mac(mac, 8)
    assert len(short) == 8


def test_canonical_json_equivalence() -> None:
    key = b"lab-key-3"
    p1 = {"user": "alice", "amount": 10}
    p2 = {"amount": 10, "user": "alice"}
    assert mac_over_payload(key, p1) == mac_over_payload(key, p2)


def main() -> None:
    test_truncation_length()
    test_canonical_json_equivalence()
    print("basic MAC checks passed")


if __name__ == "__main__":
    main()

