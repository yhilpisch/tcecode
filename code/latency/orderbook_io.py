#!/usr/bin/env python3
"""
Crypto Engineering Notes – Latency

Loading orderbook_ticks.csv and deriving best bid/ask and mid time series.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

from typing import Optional

import pandas as pd  # type: ignore[import-not-found]


def load_orderbook(path: str, venue: Optional[str] = None) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["ts"] = pd.to_datetime(df["ts_ns"], unit="ns", utc=True)
    if venue is not None:
        df = df[df["venue_id"] == venue].copy()
    return df.set_index("ts").sort_index()


def top_of_book(ob: pd.DataFrame) -> pd.DataFrame:
    bids = ob[ob["side"] == "B"].groupby(ob.index)["price"].max()
    asks = ob[ob["side"] == "A"].groupby(ob.index)["price"].min()
    tob = pd.concat({"best_bid": bids, "best_ask": asks}, axis=1).ffill()
    tob["mid"] = (tob["best_bid"] + tob["best_ask"]) / 2
    return tob


def main() -> None:
    ob = load_orderbook("orderbook_ticks.csv", venue="CEX_A")
    print(ob.head())
    tob = top_of_book(ob)
    print(tob.head())


if __name__ == "__main__":
    main()

