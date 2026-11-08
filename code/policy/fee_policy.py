#!/usr/bin/env python3
"""
Crypto Engineering Notes – Fee Policy

Fee estimation wrapper and urgency-band-based fee suggestion helper.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import json
import subprocess
from dataclasses import dataclass


def cli(*args: str):
    """Call `bitcoin-cli -regtest` and parse JSON when possible."""
    out = subprocess.check_output(
        ["bitcoin-cli", "-regtest", *args],
        text=True,
    )
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return out.strip()


def mempool_info() -> dict:
    return cli("getmempoolinfo")


def smart_fee(conf_target: int) -> float | None:
    """Return estimated fee rate in sat/vByte for a given confirmation target.

    Returns None when the node lacks enough data.
    """
    res = cli("estimatesmartfee", str(conf_target))
    feerate_btc_per_kvbyte = res.get("feerate")
    if feerate_btc_per_kvbyte is None:
        return None
    return feerate_btc_per_kvbyte * 1e8 / 1000.0


@dataclass
class FeeBand:
    conf_target: int
    max_sat_vbyte: float


POLICY = {
    "low": FeeBand(conf_target=24, max_sat_vbyte=5.0),
    "normal": FeeBand(conf_target=6, max_sat_vbyte=25.0),
    "high": FeeBand(conf_target=2, max_sat_vbyte=100.0),
}


def suggest_fee(band_name: str) -> tuple[float, str]:
    band = POLICY[band_name]
    est = smart_fee(band.conf_target)
    info = mempool_info()
    floor = info.get("mempoolminfee", 0.0) * 1e8 / 1000.0  # BTC/kvB -> sat/vByte

    if est is None:
        rate = max(floor, 1.0)
        reason = "no estimate available; using floor with 1 sat/vByte minimum"
    else:
        rate = max(floor, est)
        reason = (
            f"estimatesmartfee for {band.conf_target} blocks, "
            "floored at mempool minimum"
        )

    if rate > band.max_sat_vbyte:
        rate = band.max_sat_vbyte
        reason += f" and capped at policy maximum for {band_name} urgency"

    return rate, reason


def main() -> None:
    for name in ("low", "normal", "high"):
        rate, why = suggest_fee(name)
        print(f"{name:6} -> {rate:5.1f} sat/vByte ({why})")


if __name__ == "__main__":
    main()

