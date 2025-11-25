#!/usr/bin/env python3
"""
Crypto Engineering Notes – Entropy

Combining dice-roll and hardware entropy estimates for a seed.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

from code.entropy.log2_choice_count import bits_for_choices


def combined_entropy_bits(
    dice_rolls: int,
    hardware_bits: float,
    key_size_bits: int = 256,
) -> float:
    """Return a conservative combined entropy estimate, capped at key size."""
    dice_bits = dice_rolls * bits_for_choices(6)
    total = dice_bits + hardware_bits
    return min(total, float(key_size_bits))


def main() -> None:
    for rolls in (10, 20, 40):
        est = combined_entropy_bits(dice_rolls=rolls, hardware_bits=64.0)
        print(f"{rolls:2d} dice rolls + 64 hardware bits -> {est:6.2f} effective bits")


if __name__ == "__main__":
    main()

