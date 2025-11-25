#!/usr/bin/env python3
"""
Crypto Engineering Notes – Compliance

Seed a controls evidence binder as CSV from discovered artefacts.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import csv
from pathlib import Path

from code.compliance.collect_artefacts import ROOT, iter_artefacts


def write_seed(path: Path) -> None:
    """Write a binder.csv skeleton with one row per discovered artefact."""
    headers = [
        "control_id",
        "question",
        "domain",
        "evidence_links",
        "owner",
        "last_reviewed_at",
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for idx, art in enumerate(iter_artefacts(ROOT), start=1):
            writer.writerow(
                {
                    "control_id": f"C-{idx:04d}",
                    "question": "",
                    "domain": "",
                    "evidence_links": art.path,
                    "owner": "",
                    "last_reviewed_at": "",
                }
            )


def main() -> None:
    target = Path("binder.csv")
    write_seed(target)
    print(f"wrote {target}")


if __name__ == "__main__":
    main()

