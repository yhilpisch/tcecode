#!/usr/bin/env python3
"""
Crypto Engineering Notes – Risk

Helpers for AMM reserve rebalancing, impermanent loss, and fee comparisons.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import math


def rebalance_to_price(
    x0: float, y0: float, new_price: float
) -> tuple[float, float]:
    k = x0 * y0
    x1 = (k / new_price) ** 0.5
    y1 = new_price * x1
    return x1, y1


def impermanent_loss(alpha: float) -> float:
    if alpha <= 0:
        raise ValueError("alpha must be positive")
    numerator = 2 * math.sqrt(alpha)
    denominator = 1 + alpha
    return 1.0 - numerator / denominator


def fee_revenue(notional: float, fee_rate: float, volume_turns: float) -> float:
    """Approximate fee revenue over a horizon."""
    return notional * fee_rate * volume_turns


def main() -> None:
    x0, y0 = 10.0, 10_000.0
    x1, y1 = rebalance_to_price(x0, y0, new_price=1500.0)
    print("after move: x =", x1, "y =", y1)


if __name__ == "__main__":
    main()

