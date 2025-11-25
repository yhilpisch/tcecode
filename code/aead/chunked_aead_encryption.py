#!/usr/bin/env python3
"""
Crypto Engineering Notes – AEAD

Chunked AEAD encryption with derived nonces and associated data.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

from typing import Iterable, Iterator, Tuple

from cryptography.hazmat.primitives.ciphers.aead import AESGCM  # type: ignore[import-not-found]


def derive_nonce(stream_id: bytes, index: int) -> bytes:
    return (stream_id + index.to_bytes(4, "big"))[:12]


def encrypt_chunks(
    dek: bytes, stream_id: bytes, chunks: Iterable[bytes]
) -> Iterator[Tuple[int, bytes]]:
    aesgcm = AESGCM(dek)
    for index, chunk in enumerate(chunks):
        nonce = derive_nonce(stream_id, index)
        aad = b"stream:" + stream_id + b";index:" + index.to_bytes(4, "big")
        ciphertext = aesgcm.encrypt(nonce, chunk, aad)
        yield index, ciphertext


def main() -> None:
    dek = b"\x00" * 32
    stream_id = b"stream-1"
    for idx, ct in encrypt_chunks(dek, stream_id, [b"a", b"b", b"c"]):
        print(idx, ct.hex())


if __name__ == "__main__":
    main()

