<p align="right"><img src="https://hilpisch.com/tce_logo.png" alt="The Crypto Engineer" width="25%"></p>

# The Crypto Engineer &mdash; Companion Code Base

Welcome! This repository ships the runnable material that goes hand in hand with the four volumes of **The Crypto Engineer (TCE)**:

1. **Crypto Foundations** &mdash; hashing, symmetric crypto, MACs, key generation, probability intuition.
2. **Bitcoin Foundations** &mdash; UTXOs, scripts, mempools, mining, wallet drills.
3. **Cryptomarkets & Systems** &mdash; market plumbing, execution metrics, DeFi tooling.
4. **Crypto Engineering** &mdash; reviews, monitoring, incidents, governance, production runbooks.

Each directory mirrors the structure of the books so you can jump from a chapter to the corresponding notebook or script without hunting for files.

---

## Repository Layout

The folder structure mirrors the narrative arc of the books. Use it as your map: when a chapter references a notebook or script, you can find it instantly here.

```
code/
  hashing/, aead/, entropy/, ...     # Python scripts for the labs and drills
notebooks/
  1_book/, 2_book/, 3_book/, 4_book/ # Jupyter notebooks aligned with each volume
tools/
  validate_*.py, README_quality.md    # Validation helpers and usage notes
README.md                            # Learner-facing overview (this document)
```

### Notebooks (`notebooks/`)

These are your guided workbooks. Each one pairs directly with a chapter so you can move from reading to running code without guessing what to open.

- Named after book and chapter (e.g., `1_book/chapter05_message_authentication_codes.ipynb`).
- Designed to run top-to-bottom in Google Colab or any local Jupyter environment.
- Contain the same callouts, diagrams, and exercises you see in the PDFs, plus runnable cells that demonstrate the algorithms step by step.

### Python Scripts (`code/`)

Short, composable helpers live here. They back the lab notes and let you rehearse the same drills you read about in the books.

- Small, focused utilities used in the lab notes (hash diagnostics, fee policy helpers, wallet drills, etc.).
- Each subdirectory corresponds to a lab cluster, making it easy to locate the exact script referenced in a book margin or lab checklist.

---

## Working in Google Colab

Colab is the fastest way to get started &mdash; no local setup, just a browser. Pick whichever approach matches your workflow.

### Option 1: Open a Notebook Directly in Colab

1. Navigate to the notebook in GitHub (e.g., `notebooks/2_book/chapter04_scripts_and_spending_conditions.ipynb`).
2. Replace the `github.com` portion of the URL with `colab.research.google.com/github`.
3. Click “Run anyway” when prompted &mdash; all notebooks assume Python 3.10+ and standard scientific packages.

### Option 2: Clone the Entire Repo in a Colab Notebook

```python
from pathlib import Path
import subprocess, sys

repo_url = "https://github.com/yhilpisch/tcecode.git"
target = Path("/content/tce")

if not target.exists():
    subprocess.run(["git", "clone", repo_url, str(target)], check=True)

sys.path.append(str(target / "code"))
print("Repo ready at", target)
```

Once cloned:

- Open any notebook under `/content/tce/notebooks/...`.
- To run a script, use `!python /content/tce/code/entropy/combined_entropy_bits.py`.
- Modify notebooks directly in Colab and download/save copies to keep a personal record of experiments.

### Recommended Colab Settings

These tweaks keep runtime surprises to a minimum.

- **Runtime → Change runtime type → GPU (optional):** only needed for heavier simulations; most notebooks run fine on CPU.
- **Install requirements:** when a notebook needs extra packages, the first cell installs them via `pip`. Let the cell finish before continuing.

---

## Running Locally

Prefer your own machine? This path gives you full control, from IDE integration to offline work.

```bash
git clone https://github.com/thepythonquants/tce-code-companion.git
cd tce-code-companion
python -m venv .venv
source .venv/bin/activate
pip install jupyterlab pandas requests cryptography
# optional: required only for notebook execution validation tooling
pip install nbformat nbclient
jupyter lab
```

Launch the matching notebook, follow the chapter instructions, and drop into the `code/` scripts whenever the book references a specific helper.

---

## Staying in Sync with the Books

Treat this repo as the living lab companion: when the manuscripts evolve, so do these assets.

- The notebooks are intentionally short and focused; they echo the diagrams and equations in the PDFs so you can iterate between reading and executing without context switching.
- Each lab note includes a “Major Benefit” callout so you can decide whether to run the drill solo or with a team.
- When the books are updated, this companion repo is refreshed in lockstep. Simply `git pull` (or re-clone in Colab) to pick up the latest code.

Enjoy the build journey, and remember: if you can rehearse it here, you can ship it in production.

<p align="right"><img src="https://hilpisch.com/tce_logo.png" alt="The Crypto Engineer" width="25%"></p>


## Validation Tools

- `tools/validate_code.py` validates scripts under `code/` (compile-safe default, optional execution mode).
- `tools/validate_notebooks.py` validates notebooks under `notebooks/` (lint-safe default, optional execution mode).
- `tools/README_quality.md` provides usage examples and report commands.
