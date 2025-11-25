#!/usr/bin/env python3
"""
Crypto Engineering Notes – Failures

HMAC helpers for truncation, encoding, and canonical JSON MAC computation.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import hmac
import json
import unicodedata
from hashlib import sha256
from typing import Any, Dict


def hmac_sha256(key: bytes, message: bytes) -> bytes:
    mac = hmac.new(key, message, sha256)
    return mac.digest()


def truncated_mac(mac: bytes, length_bytes: int) -> bytes:
    return mac[:length_bytes]


def mac_of_text(key: bytes, text: str) -> bytes:
    data = text.encode("utf-8")
    return hmac_sha256(key, data)


def canonical_json(payload: Dict[str, Any]) -> bytes:
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")


def mac_over_payload(key: bytes, payload: Dict[str, Any]) -> bytes:
    return hmac_sha256(key, canonical_json(payload))


def main() -> None:
    key = b"lab-key-1"
    s1 = "café"
    s2 = unicodedata.normalize("NFD", s1)
    print("len(s1):", len(s1), "len(s2):", len(s2))
    print("mac(s1):", mac_of_text(key, s1).hex())
    print("mac(s2):", mac_of_text(key, s2).hex())


if __name__ == "__main__":
    main()

