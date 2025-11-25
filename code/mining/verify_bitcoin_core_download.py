#!/usr/bin/env python3
"""
Crypto Engineering Notes – Mining

Verifying a Bitcoin Core download via SHA-256 checksum.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import hashlib
from pathlib import Path


EXPECTED_SHA256 = "PUT_REAL_CHECKSUM_HERE"  # TODO: replace with the real checksum


def sha256_file(path: Path) -> str:
    """Return the hex-encoded SHA-256 digest of a file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    archive = Path("bitcoin-<version>-x86_64-apple-darwin.dmg")
    if not archive.exists():
        raise SystemExit(f"Archive not found: {archive}")
    digest = sha256_file(archive)
    print("digest :", digest)
    print("matches:", digest == EXPECTED_SHA256)


if __name__ == "__main__":
    main()

