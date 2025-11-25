#!/usr/bin/env python3
"""
Crypto Engineering Notes – Latency

Minimal environment check for Python and pandas installation.

© Dr. Yves J. Hilpisch | The Python Quants GmbH
The Crypto Engineer | AI-Powered by GPT 5.1.
"""

import sys


def main() -> None:
    print("Python version:", sys.version)
    try:
        import pandas as pd  # type: ignore[import-not-found]

        print("pandas version:", pd.__version__)
    except ImportError:
        print("Please install pandas, for example via `pip install pandas`.")


if __name__ == "__main__":
    main()

