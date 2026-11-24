#!/usr/bin/env python3
"""Write one emoji, a desert island, to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The entry is one
fixed emoji. The program writes it to the path given as the first
argument, or $OUTPUT_PATH, or /output/entry.txt by default, and enforces
the competition gate: 1 to 8 characters, not only white space.

The pick: U+1F3DD DESERT ISLAND. It is the dream vacation in one glance,
a private tropical island, not just any beach day. It reads instantly
anywhere, it is specific where the plain beach is generic, and it is a
fresher pick than the beach, palm and plane emojis every other agent
will send. One character, four bytes in UTF-8.
"""

import os
import sys
from pathlib import Path

EMOJI = "\U0001f3dd"

MIN_CHARS = 1
MAX_CHARS = 8
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path(args=None) -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    positional = [a for a in (args if args is not None else sys.argv[1:])
                  if not a.startswith("-")]
    if positional:
        return Path(positional[0])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 8 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"entry is {chars} characters, outside 1-8")
    if not text.strip():
        raise ValueError("entry is only white space")
    return chars


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--help" in args or "-h" in args:
        print("usage: main.py [--check] [output-path]")
        print("Write one emoji, a desert island, to the output path.")
        print("  --check  validate the entry against the gate without writing")
        return 0
    if "--check" in args:
        try:
            chars = validate(EMOJI)
        except ValueError as exc:
            print(exc, file=sys.stderr)
            return 1
        print(f"entry is valid: {chars} character, one line")
        return 0
    try:
        chars = validate(EMOJI)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path(args)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.write_text(EMOJI, encoding="utf-8")
    except OSError as exc:
        print(f"cannot write {path}: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {chars} character to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
