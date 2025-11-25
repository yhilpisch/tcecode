#!/usr/bin/env python3
"""
Crypto Engineering Notes – AEAD

Signing a protocol message with HMAC over header and body fields.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import hmac
from hashlib import sha256


def sign_message(key: bytes, header: bytes, body: bytes) -> bytes:
    """Compute an HMAC tag over header and body."""
    mac = hmac.new(key, digestmod=sha256)
    mac.update(header)
    mac.update(body)
    return mac.digest()


def main() -> None:
    tag = sign_message(b"lab-key", b"hdr", b"body")
    print("tag:", tag.hex())


if __name__ == "__main__":
    main()

