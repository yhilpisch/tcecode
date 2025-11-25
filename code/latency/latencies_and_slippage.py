#!/usr/bin/env python3
"""
Crypto Engineering Notes – Latency

Per-order latency calculations and a simple top-of-book slippage estimator.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import pandas as pd  # type: ignore[import-not-found]


def load_events(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["ts"] = pd.to_datetime(df["ts_ns"], unit="ns", utc=True)
    return df


def order_latencies(events: pd.DataFrame) -> pd.DataFrame:
    sent = events[events["event"] == "sent"].set_index("order_id")
    ack = events[events["event"] == "ack"].set_index("order_id")
    joined = sent[["venue_id", "ts"]].join(
        ack[["ts"]].rename(columns={"ts": "ts_ack"}),
        how="inner",
        lsuffix="_sent",
    )
    joined["latency_ms"] = (
        joined["ts_ack"] - joined["ts_sent"]
    ).dt.total_seconds() * 1000
    return joined.reset_index()


def join_with_tob(latencies: pd.DataFrame, tob: pd.DataFrame) -> pd.DataFrame:
    l = latencies.copy()
    l = l.set_index("ts_sent").join(tob, how="left").rename(
        columns={"mid": "mid_at_send"}
    )
    l = l.reset_index().rename(columns={"index": "ts_sent"})
    l = l.set_index("ts_ack").join(tob, how="left").rename(
        columns={"best_bid": "best_bid_ack", "best_ask": "best_ask_ack"}
    )
    return l.reset_index().rename(columns={"index": "ts_ack"})


def estimate_slippage(lat_tob: pd.DataFrame, side: str) -> pd.Series:
    if side == "buy":
        exec_price = lat_tob["best_ask_ack"]
    else:
        exec_price = lat_tob["best_bid_ack"]
    ref = lat_tob["mid_at_send"]
    return (exec_price - ref) / ref * 10_000  # basis points


def main() -> None:
    events = load_events("client_events.csv")
    lat = order_latencies(events)
    print(lat[["order_id", "venue_id", "latency_ms"]].head())


if __name__ == "__main__":
    main()

