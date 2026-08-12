# TJC Unicode UI as Code

A reusable Codex skill and deterministic audit tool for Unicode/UTF-8 TJC USART HMI development.

The project captures a workflow proven useful when a vendor editor remains the authoritative compiler and renderer, but UI structure, text states, binary patches, firmware mappings, and acceptance evidence need to be reproducible and reviewable as code.

## What it covers

- UTF-8 text-state contracts and `txt_maxl` byte-capacity checks
- font charset coverage before generating or importing `.zi` resources
- ASCII-safe page and object identifiers
- immutable donor and exact-candidate binary discipline
- page-safe CRC/CFS and resource-integrity gates
- official editor and simulator acceptance tied to an exact HMI SHA-256
- MCU display, touch, acknowledgement, and safety-gate separation

It does **not** claim to be a universal replacement compiler for proprietary HMI/TFT formats. The official editor and simulator remain required acceptance gates.

## Install as a Codex skill

Copy `tjc-unicode-ui-as-code/` into your Codex skills directory, or install the repository through Codex's skill installer.

## Audit a text contract

```bash
python tjc-unicode-ui-as-code/scripts/audit_text_contract.py \
  tjc-unicode-ui-as-code/references/example-text-contract.json
```

Add one or more charset files when checking font coverage:

```bash
python tjc-unicode-ui-as-code/scripts/audit_text_contract.py \
  path/to/text-contract.json \
  --charset path/to/font-charset.txt \
  --out build/text-audit.json
```

The audit exits with status `0` on success and `2` when the contract is unsafe.

## Test

```bash
python -m unittest discover -s tests -v
```

## Repository boundary

This public repository intentionally excludes proprietary HMI/TFT binaries, donor projects, fonts, product artwork, firmware, private protocols, and vendor executables. The included contract is synthetic.

Licensed under Apache-2.0.

