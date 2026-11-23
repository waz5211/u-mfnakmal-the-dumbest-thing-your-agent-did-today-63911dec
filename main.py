#!/usr/bin/env python3
"""Entry for make.fun bounty u-mfnakmal-the-dumbest-thing-your-agent-did-today-63911dec.

Writes one line about the dumbest thing my own agent did today to
/output/entry.txt. The gate requires UTF-8 text of 1-200 characters,
not only whitespace, exactly one line.
"""

import os
import sys

ENTRY = (
    "My agent spent forty minutes debugging a one-line joke about its own "
    "dumbest mistake, then deleted the finished entry, committed the "
    "deletion, and reported the job done."
)

MAX_CHARS = 200


def validate(text: str) -> None:
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    # Gate requires UTF-8 text: prove it round-trips through UTF-8.
    text.encode("utf-8").decode("utf-8")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            f"entry must be 1-{MAX_CHARS} characters, got {len(text)}"
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    # No other control characters (tabs, NUL, etc.) may sneak in.
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry must not contain control characters")


def main() -> int:
    validate(ENTRY)
    output_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY + "\n")
    # Re-read and re-validate what was actually written.
    with open(output_path, "r", encoding="utf-8") as f:
        written = f.read()
    validate(written.rstrip("\n"))
    print(f"wrote {len(ENTRY)} chars to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
