# Quality Checks (Scripts + Notebooks)

Use these tools to validate companion code under `code/` and notebooks under `notebooks/`.

## Quick start via Make

```bash
make check-quality
```

Additional targets:

- `make check-code` (compile/lint scripts only)
- `make check-notebooks` (lint notebooks only)
- `make check-quality-exec` (execute scripts + notebooks; heavier)
- `make PYTHON=python check-quality-exec` (force active virtualenv interpreter)

## 1) Validate Python scripts

Default (safe): syntax/bytecode compile check only (no execution).

```bash
python tools/validate_code.py
```

Execute scripts (heavier):

```bash
python tools/validate_code.py --execute --timeout 60
```

By default, execute mode uses the active shell `python` interpreter (so it follows your currently activated environment).

If you keep multiple Python environments, pin the interpreter explicitly:

```bash
python tools/validate_code.py --execute --python "$(which python)" --timeout 60
```

By default, execute mode marks environment/input-gated failures as `SKIP` (for example missing `bitcoin-cli`, missing local data files, or missing required CLI args). Use strict mode to fail on those as well:

```bash
python tools/validate_code.py --execute --strict-execute --timeout 60
```

Execution failures are categorized in output/reports, e.g.:
- `missing_module:<name>`
- `missing_binary:bitcoin-cli`
- `missing_input_file:<path>`
- `missing_required_cli_args`
- `unreachable_rpc_endpoint`

Write reports:

```bash
python tools/validate_code.py \
  --report-json tools/code_report.json \
  --report-md tools/code_report.md
```

## 2) Validate notebooks

Default (safe): lint notebooks (parse + basic structure checks, no execution).

```bash
python tools/validate_notebooks.py
```

Execute notebooks (requires `nbclient`):

```bash
python tools/validate_notebooks.py --execute --timeout 300
```

Write reports:

```bash
python tools/validate_notebooks.py \
  --report-json tools/nb_report.json \
  --report-md tools/nb_report.md
```

## Optional dependencies

For notebook execution mode:

```bash
python -m pip install nbclient nbformat
```
