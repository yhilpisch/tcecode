#!/usr/bin/env python3
"""
Crypto Engineering Notes – Hashing

Toy hash explorer for tracing a simple ARX-style compression function.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

from textwrap import wrap


INIT = (0x61707865, 0x3320646E, 0x79622D32, 0x6B206574)


def rol(x: int, k: int) -> int:
    return ((x << k) | (x >> (32 - k))) & 0xFFFFFFFF


def toy_hash(msg: bytes) -> bytes:
    pad_len = (4 - len(msg) % 4) % 4
    padded = msg + b"\x00" * pad_len
    words = [
        int.from_bytes(padded[i : i + 4], "little")
        for i in range(0, len(padded), 4)
    ]
    a, b, c, d = INIT
    for idx, word in enumerate(words):
        a = (a + word) & 0xFFFFFFFF
        b = rol(b ^ a, 5)
        c = (c + b) & 0xFFFFFFFF
        d = rol(d ^ c, 8)
        print(f"step {idx:02d}: a={a:08x} b={b:08x} c={c:08x} d={d:08x}")
    return (
        a.to_bytes(4, "little")
        + b.to_bytes(4, "little")
        + c.to_bytes(4, "little")
        + d.to_bytes(4, "little")
    )


def main() -> None:
    digest = toy_hash(b"TPQ")
    print("digest:", " ".join(wrap(digest.hex(), 8)))


if __name__ == "__main__":
    main()

