#!/usr/bin/env python3
"""
Crypto Engineering Notes – Entropy

Estimating passphrase entropy from word count and effective dictionary size.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

from code.entropy.log2_choice_count import bits_for_choices


def passphrase_bits(words: int, effective_dict_size: int = 2048) -> float:
    """Return an entropy estimate in bits for a passphrase."""
    return words * bits_for_choices(effective_dict_size)


def main() -> None:
    for k in (3, 4, 6, 8):
        bits = passphrase_bits(k)
        print(f"{k} words from 2048 entries -> {bits:5.1f} bits")


if __name__ == "__main__":
    main()

