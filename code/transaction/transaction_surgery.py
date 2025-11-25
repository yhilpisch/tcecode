#!/usr/bin/env python3
"""
Crypto Engineering Notes – Transaction

Helpers for selecting UTXOs, inspecting transactions, building templates,
funding/signing, and inspecting the mempool via bitcoin-cli.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import json
from typing import Dict, List, Tuple, TypedDict

from code.transaction.cli_wrapper import cli


class UTXO(TypedDict):
    txid: str
    vout: int
    amount: float
    address: str


def first_utxo() -> UTXO:
    utxos: List[Dict] = cli("listunspent", "1", "9999999")
    if not utxos:
        raise RuntimeError("No UTXOs found; mine a few blocks first.")
    u = utxos[0]
    return {
        "txid": u["txid"],
        "vout": u["vout"],
        "amount": u["amount"],
        "address": u["address"],
    }


def fetch_tx(txid: str) -> Tuple[str, Dict]:
    raw = cli("getrawtransaction", txid)
    decoded = cli("decoderawtransaction", raw)
    return raw, decoded


def build_template(utxo: UTXO, dest_address: str, send_amount: float) -> str:
    inputs = [{"txid": utxo["txid"], "vout": utxo["vout"]}]
    outputs = {dest_address: send_amount}
    return cli("createrawtransaction", json.dumps(inputs), json.dumps(outputs))


def fund_and_sign(raw_hex: str) -> str:
    funded = cli("fundrawtransaction", raw_hex)
    signed = cli("signrawtransactionwithwallet", funded["hex"])
    if not signed.get("complete", False):
        raise RuntimeError("Signing failed")
    return signed["hex"]


def mempool_snapshot() -> List[str]:
    return cli("getrawmempool")


def main() -> None:
    utxo = first_utxo()
    dest = cli("getnewaddress")
    template = build_template(utxo, dest, send_amount=0.1)
    final = fund_and_sign(template)
    txid = cli("sendrawtransaction", final)
    print("broadcast txid:", txid)
    print("mempool txids:", mempool_snapshot())


if __name__ == "__main__":
    main()

