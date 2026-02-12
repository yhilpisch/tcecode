#!/usr/bin/env python3
"""
Crypto Engineering Notes – Monitoring

Quick SLO breach scan helper used in the monitoring note.
"""

from datetime import datetime, timezone


SAMPLES = [
    {"service": "withdrawals", "success_rate": 0.992, "target": 0.995},
    {"service": "deposits", "success_rate": 0.9993, "target": 0.999},
    {"service": "reconciliation", "success_rate": 0.997, "target": 0.999},
]


def main() -> None:
    now = datetime.now(timezone.utc).isoformat()
    print(f"SLO scan at {now}")
    for row in SAMPLES:
        status = "OK" if row["success_rate"] >= row["target"] else "ALERT"
        print(
            f"{row['service']:>15}  "
            f"actual={row['success_rate']:.4f}  "
            f"target={row['target']:.4f}  "
            f"status={status}"
        )


if __name__ == "__main__":
    main()
