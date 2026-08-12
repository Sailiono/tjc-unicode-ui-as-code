---
name: tjc-unicode-ui-as-code
description: Build, patch, audit, and validate Unicode/UTF-8 TJC USART HMI projects with embedded .zi fonts, ASCII object names, declarative text-state contracts, donor-based binary editing, page-safe CRC/CFS preservation, official editor/simulator acceptance, and MCU display/touch alignment. Use when Codex works on a TJC or Nextion-like .HMI project that must display Chinese or other Unicode text, calculate txt_maxl safely, generate or audit a font charset, patch an existing HMI without mouse-driven editing, validate the exact HMI binary, or synchronize screen objects with firmware while preserving safety gates.
---

# TJC Unicode UI as Code

Treat the official USART HMI editor as the authoritative compiler and renderer. Use code to make the project reproducible, inspectable, and testable; do not claim a universal from-scratch HMI/TFT compiler.

## Required workflow

1. Freeze the target model, resolution, orientation, project encoding, page IDs, ASCII object names, dynamic text states, and MCU display/touch contract.
2. Read [references/unicode-contract.md](references/unicode-contract.md). Create a text-state specification from [references/example-text-contract.json](references/example-text-contract.json), then audit it with `scripts/audit_text_contract.py` before generating a font.
3. Generate or import a `.zi` font using the official Font Maker. Record its encoding, height, charset source, SHA-256, and the HMI font ID that consumes it.
4. Keep static decoration in image assets when appropriate. Use native text controls for dynamic, frequently changed, localized, or safety-relevant text.
5. Patch an immutable donor or a separately versioned candidate. Never overwrite the donor or use an HMI saved after a version/format error.
6. Read [references/binary-and-official-gates.md](references/binary-and-official-gates.md). Preserve every HMI directory entry, refresh modified page-safe CRCs, synchronize native CFS offsets/lengths and CRC, and require all offline gates.
7. Validate the exact candidate SHA-256 in the official editor and simulator. Do not rebuild another HMI immediately before acceptance and attribute that evidence to the source candidate.
8. Read [references/firmware-integration.md](references/firmware-integration.md) before enabling MCU writes or touch commands. Keep component-ID and actuator commissioning gates closed until real-panel evidence exists.

## Unicode rules

- Keep page and object names ASCII and within the vendor's verified byte limit. Put Unicode in displayed text, not identifiers.
- Encode HMI event literals and MCU text payloads as UTF-8 when the project is in Unicode/UTF-8 mode.
- Terminate every serial command with raw bytes `FF FF FF`.
- Size `txt_maxl` from UTF-8 byte length, not character count. Include every runtime state and practical version/date/error string, then leave explicit headroom.
- Audit the `.zi` charset against every static and dynamic string. Treat a missing glyph, tofu box, clipped baseline, or overflow as a failure.
- Keep one source of truth for display states. Do not expose internal numeric codes such as `0/1/2` when the display contract defines localized text.
- Test minimum, maximum, invalid, disconnected, warning, fault, long-version, date/time, and rapid-refresh states.

## Acceptance boundary

- Prefer declarative scene/manifest files, deterministic picture/font maps, and donor seeds for supported widget types.
- Add one representative graft proof per new widget type before bulk creation.
- Require page names, page-safe CRC, native CFS, object/property inventory, resource references, geometry, glyph, event, and firmware-contract tests.
- Require official editor open, `0 errors / 0 warnings`, official simulator state/interaction coverage, and a report tied to the exact HMI SHA-256.
- Treat code-only rendering as diagnostic evidence, not proof of vendor-renderer or real-panel pixels.
- Keep `safe_to_flash=false` until separate real-panel and hardware acceptance authorizes flashing.

## Deliverables

Return or update:

- the declarative scene/text-state contract and charset source;
- `.zi` identities and font-ID mapping;
- candidate HMI SHA-256 and offline reports;
- exact-HMI official editor/simulator evidence;
- display/touch maps and firmware alignment tests;
- explicit pending gates, including component-ID and actuator commissioning status.

