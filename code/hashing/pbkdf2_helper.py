#!/usr/bin/env python3
"""
Crypto Engineering Notes – Hashing

PBKDF2 helper for password hashing labs.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import os
from hashlib import pbkdf2_hmac
from typing import Tuple


def derive_password_hash(
    password: str, salt: bytes | None = None, iterations: int = 200_000
) -> Tuple[bytes, bytes]:
    if salt is None:
        salt = os.urandom(16)
    dk = pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, dklen=32)
    return salt, dk


def verify_password(
    password: str, salt: bytes, expected: bytes, iterations: int = 200_000
) -> bool:
    _, candidate = derive_password_hash(password, salt, iterations)
    return candidate == expected


def main() -> None:
    salt, digest = derive_password_hash("correct horse battery staple")
    print("salt:", salt.hex())
    print("digest:", digest.hex())


if __name__ == "__main__":
    main()

