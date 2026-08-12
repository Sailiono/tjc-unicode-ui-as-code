# Binary and official acceptance gates

## Donor discipline

- Keep an immutable, hash-identified donor.
- Write candidates to a new build directory or versioned baseline.
- Never overwrite the donor.
- Never promote a file saved after a version mismatch, hidden-page, or format error.

## Mandatory binary invariants

After changing a page or resource:

1. Preserve the complete HMI directory and untouched entries.
2. Refresh the page-safe header/CRC for every modified page.
3. Recalculate directory offsets and lengths.
4. Synchronize the native CFS table with final offsets/lengths.
5. Refresh the native CFS CRC.
6. Re-open and inventory the generated HMI.
7. Confirm all expected named pages, object IDs, properties, fonts, pictures, and events.

Fail closed when a target-specific corpus, status record, or checksum cannot be verified.

## Code-only gates

Require automated checks for:

- entry count and named page set;
- page-safe and native CFS validity;
- unresolved picture/font references;
- object geometry and text overflow;
- missing glyphs and font-ID bindings;
- event encoding and release behavior;
- display/touch-map and firmware Presenter alignment;
- state, interaction, numeric-wrap, and visibility-group contracts.

Code-only rendering is diagnostic evidence. It is not proof that the vendor renderer or panel produces identical pixels.

## Exact-HMI official gate

Official acceptance must apply to the same binary identity being released:

1. Hash the source candidate.
2. Copy it byte-for-byte to an isolated editor input.
3. Confirm the isolated copy has the same SHA-256.
4. Open and compile it in the official editor.
5. Require zero errors and zero warnings unless a reviewed, explicitly frozen warning exception exists.
6. Run the official simulator's page, state, interaction, and numeric-boundary suite.
7. Store reports and screenshots with the source SHA-256.
8. Close only editor/simulator processes created by the run.

Do not run a builder first in exact-validation mode. Otherwise evidence belongs to the builder output, not the named candidate.

## Release boundary

Official editor and simulator success proves authoring compatibility. It does not prove TFT download success, real-panel component IDs, serial electrical integrity, MCU command authorization, or hazardous-output commissioning.

Keep `safe_to_flash=false` until those separate gates pass.

