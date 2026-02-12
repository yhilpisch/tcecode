#!/usr/bin/env python3
"""
Crypto Engineering Notes – Mining

Verifying a Bitcoin Core download via SHA-256 checksum.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import argparse
import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    """Return the hex-encoded SHA-256 digest of a file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a Bitcoin Core archive against an expected SHA-256 digest."
    )
    parser.add_argument(
        "archive",
        type=Path,
        help="Path to the downloaded archive (e.g. bitcoin-<version>-x86_64-apple-darwin.dmg).",
    )
    parser.add_argument(
        "expected_sha256",
        help="Expected SHA-256 hex digest from the official release checksums.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    archive = args.archive
    if not archive.exists():
        raise SystemExit(f"Archive not found: {archive}")
    digest = sha256_file(archive)
    expected = args.expected_sha256.lower().strip()
    if len(expected) != 64:
        raise SystemExit("Expected SHA-256 must be a 64-character hex string.")
    print("digest :", digest)
    print("matches:", digest == expected)


if __name__ == "__main__":
    main()
