# Unicode and font contract

## Contents

1. Project encoding
2. Text-state inventory
3. Font charset and identity
4. `txt_maxl`
5. Runtime payloads
6. Visual acceptance

## 1. Project encoding

Freeze one encoding for the HMI project, event source, font library, and MCU payloads. For Unicode-mode TJC projects in this workflow, use UTF-8 consistently. Do not mix GBK event bytes with a UTF-8 project or assume that a font generated in another mode is compatible.

Keep page/object identifiers ASCII. Set `object_name_limit_bytes` in the text contract to the byte limit verified for the target editor/toolchain; use 14 only when that limit has been confirmed for the project.

## 2. Text-state inventory

List every text a control can display, not only its default. Include:

- normal, disabled, disconnected, unknown, warning, and fault states;
- mode labels and confirmed actuator states;
- units and boundary numeric values;
- dates, weekdays, time, firmware/product versions, and serial numbers;
- confirmation titles, consequences, progress, success, rejection, and error messages.

Prefer a JSON text contract and run `scripts/audit_text_contract.py`. The script checks identifier safety, the configured object-name byte limit, UTF-8 byte lengths, `txt_maxl`, and charset coverage.

## 3. Font charset and identity

Generate the `.zi` with the official Font Maker when official binary compatibility is required. Retain:

- the exact charset text file;
- source font family/file and license review;
- pixel height and antialiasing choice;
- project encoding;
- output `.zi` SHA-256;
- assigned HMI font ID.

Include all punctuation, digits, Latin letters, symbols, units, and future version characters used by the product. For dynamic version strings, include `0-9`, `.`, `-`, `_`, `V`, and relevant product letters even when today's version does not use them all.

Do not assume a desktop font preview proves target coverage. Validate the embedded `.zi` through HMI object readback and the official simulator.

## 4. `txt_maxl`

Treat `txt_maxl` as a byte-capacity limit in UTF-8 mode:

```text
required_bytes = max(len(text.encode("utf-8")) for every runtime state)
recommended_txt_maxl = required_bytes + explicit_headroom
```

Use project-specific headroom. Four to eight bytes is a reasonable starting point for fixed labels; version, error, and date fields usually need more. Never infer capacity from the number of Chinese characters because each commonly occupies three UTF-8 bytes.

Treat truncation, missing closing punctuation, or a string that only works at the default value as a failed contract.

## 5. Runtime payloads

MCU command structure:

```text
ASCII object/property syntax + UTF-8 quoted text + FF FF FF
```

Escape quotes and backslashes according to the HMI language. Avoid splitting a multibyte UTF-8 character across UART chunks unless the receiver buffers the complete command before parsing.

Keep user-facing localization separate from internal enums. Either firmware emits a frozen localized state string or the HMI maps a stable numeric enum to localized text; never expose raw enum values accidentally.

## 6. Visual acceptance

For every text state, verify:

- glyphs exist and render consistently;
- text fits its native control at the actual font ID and size;
- baseline and vertical centering are correct on the target canvas;
- foreground/background contrast survives the target panel;
- changing MCU values does not reveal stale defaults or cause overlap;
- the longest valid string and all boundary numbers remain legible.

