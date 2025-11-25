#!/usr/bin/env python3
"""
Crypto Engineering Notes – Hashing

File integrity helper streaming a file and checking a published digest.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

from hashlib import sha256
from pathlib import Path


EXPECTED_SHA256 = (
    "ab407e4bf408c44dd7e3fdd52d1de99a7f6e5286c8b3ad21fb3d8a6c6e3b4c9a"
)


def file_digest(path: Path, chunk_size: int = 65_536) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    artifact = Path("dataset.zip")
    digest = file_digest(artifact)
    status = "OK" if digest == EXPECTED_SHA256 else "MISMATCH"
    print(f"{artifact.name}: {digest} -> {status}")


if __name__ == "__main__":
    main()

