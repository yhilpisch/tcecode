#!/usr/bin/env python3
"""
Crypto Engineering Notes – Incident

Tiny in-memory withdrawal queue for incident-simulation labs.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Status(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    CONFIRMED = "confirmed"


@dataclass
class Withdrawal:
    wid: str
    address: str
    amount_btc: float
    status: Status = Status.PENDING
    txid: str | None = None


@dataclass
class Queue:
    items: List[Withdrawal] = field(default_factory=list)

    def pending(self) -> list[Withdrawal]:
        return [w for w in self.items if w.status == Status.PENDING]


def main() -> None:
    q = Queue()
    q.items.append(Withdrawal("w1", "bcrt1example", 0.1))
    q.items.append(Withdrawal("w2", "bcrt1example2", 0.2))
    for w in q.pending():
        print("pending:", w.wid, w.address, w.amount_btc)


if __name__ == "__main__":
    main()

