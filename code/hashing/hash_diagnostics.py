#!/usr/bin/env python3
"""
Crypto Engineering Notes – Hashing

Hashing diagnostics across SHA-256, SHA3-256, and BLAKE2b-256.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

from hashlib import blake2b, sha256, sha3_256
from time import perf_counter


def digest_report(message: bytes) -> None:
    cases = {
        "sha256": sha256,
        "sha3_256": sha3_256,
        "blake2b-256": lambda: blake2b(digest_size=32),
    }
    print(f"Message ({len(message)} bytes): {message!r}")
    for name, factory in cases.items():
        h = factory()
        start = perf_counter()
        h.update(message)
        digest = h.hexdigest()
        elapsed = (perf_counter() - start) * 1e6
        print(f"{name:>12} {digest} ({elapsed:8.2f} µs)")


def main() -> None:
    digest_report(b"TPQ Hash Clinic")


if __name__ == "__main__":
    main()

