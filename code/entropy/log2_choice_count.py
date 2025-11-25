#!/usr/bin/env python3
"""
Crypto Engineering Notes – Entropy

Computing log2 of a choice count to estimate bits of entropy.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import math


def bits_for_choices(n: int) -> float:
    """Return log2(n) for a positive choice count."""
    if n <= 0:
        raise ValueError("choice count must be positive")
    return math.log2(n)


def main() -> None:
    for n in (6, 10, 2048, 2**128):
        print(f"N={n:>8}: {bits_for_choices(n):6.2f} bits")


if __name__ == "__main__":
    main()

