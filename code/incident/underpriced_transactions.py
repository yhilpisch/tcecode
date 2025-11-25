#!/usr/bin/env python3
"""
Crypto Engineering Notes – Incident

Sketch for creating deliberately underpriced transactions using fee policy helpers.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

from code.policy.fee_policy import suggest_fee  # type: ignore[import-not-found]
from code.transaction.cli_wrapper import cli  # type: ignore[import-not-found]
from code.incident.withdrawal_queue import Withdrawal


def broadcast_underpriced(withdrawal: Withdrawal) -> None:
    """Compute an intentionally low fee rate for a withdrawal.

    This is a structural sketch; filling in raw transaction construction
    is left to the lab notebook and transaction helpers.
    """
    rate, _ = suggest_fee("low")
    bad_rate = max(1.0, rate / 5.0)  # far below normal suggestion
    print("suggested low-band rate:", rate, "sat/vB; using underpriced:", bad_rate)
    # Build, fund, and sign a transaction here (omitted),
    # then broadcast via cli("sendrawtransaction", raw_hex).


def main() -> None:
    w = Withdrawal(wid="lab-1", address="bcrt1example", amount_btc=0.1)
    broadcast_underpriced(w)


if __name__ == "__main__":
    main()

