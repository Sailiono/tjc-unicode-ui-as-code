from __future__ import annotations

"""Audit a UTF-8 TJC text-state contract and optional font charset."""

import argparse
import json
from pathlib import Path
import sys
from typing import Any


def _load_charset(paths: list[Path]) -> set[str]:
    characters: set[str] = set()
    for path in paths:
        characters.update(path.read_text(encoding="utf-8-sig"))
    return characters


def audit(spec: dict[str, Any], charset: set[str], headroom: int) -> dict[str, Any]:
    encoding = str(spec.get("encoding", "utf-8")).lower()
    if encoding not in {"utf-8", "utf8"}:
        raise ValueError(f"This skill audits UTF-8 contracts, got {encoding!r}")
    object_name_limit = int(spec.get("object_name_limit_bytes", 14))
    if object_name_limit <= 0:
        raise ValueError("object_name_limit_bytes must be positive")

    objects: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    required_characters: set[str] = set()
    for item in spec.get("objects", []):
        name = str(item.get("name", ""))
        texts = [str(value) for value in item.get("texts", [])]
        configured = item.get("txt_maxl")
        try:
            encoded_name = name.encode("ascii")
        except UnicodeEncodeError:
            encoded_name = b""
            errors.append({"object": name, "kind": "non_ascii_object_name"})
        if len(encoded_name) > object_name_limit:
            errors.append(
                {
                    "object": name,
                    "kind": "object_name_over_limit",
                    "bytes": len(encoded_name),
                    "limit": object_name_limit,
                }
            )
        if not texts:
            errors.append({"object": name, "kind": "no_text_states"})

        byte_lengths = [len(text.encode("utf-8")) for text in texts]
        required = max(byte_lengths, default=0)
        recommended = required + headroom
        if configured is not None and int(configured) < required:
            errors.append(
                {
                    "object": name,
                    "kind": "txt_maxl_too_small",
                    "configured": int(configured),
                    "required": required,
                }
            )
        for value in texts:
            required_characters.update(value)
        objects.append(
            {
                "name": name,
                "state_count": len(texts),
                "max_utf8_bytes": required,
                "configured_txt_maxl": configured,
                "recommended_txt_maxl": recommended,
                "longest_states": [
                    value for value in texts if len(value.encode("utf-8")) == required
                ],
            }
        )

    required_non_ascii = {
        character for character in required_characters if ord(character) > 127
    }
    missing = sorted(required_non_ascii - charset) if charset else []
    if missing:
        errors.append(
            {
                "kind": "missing_font_glyphs",
                "count": len(missing),
                "characters": "".join(missing),
                "codepoints": [f"U+{ord(character):04X}" for character in missing],
            }
        )

    return {
        "schema_version": 1,
        "encoding": "utf-8",
        "object_name_limit_bytes": object_name_limit,
        "headroom_bytes": headroom,
        "objects": objects,
        "required_character_count": len(required_characters),
        "required_non_ascii_character_count": len(required_non_ascii),
        "missing_non_ascii_characters": "".join(missing),
        "errors": errors,
        "passed": not errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="JSON text contract")
    parser.add_argument("--charset", type=Path, action="append", default=[])
    parser.add_argument("--headroom", type=int, default=4)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if args.headroom < 0:
        parser.error("--headroom must be non-negative")

    spec = json.loads(args.spec.read_text(encoding="utf-8-sig"))
    charset = _load_charset(args.charset)
    report = audit(spec, charset, args.headroom)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    sys.stdout.write(payload)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

