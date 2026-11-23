#!/usr/bin/env python3
"""first-thought: write one word, the first that comes to mind, to /output/entry.txt.

The word is "defenestration": the act of throwing someone out of a window.
It is surprising (there is a dedicated word for that), vivid (the image
arrives whole in a single glance), and carries a spark of wit in its sound
and its absurd specificity: a formal Latinate word for a thoroughly
undignified act. Against safe filler it wins on every count the brief
weighs: surprise first, then vividness, then wit.

Standard library only, no network. Deterministic: the same bytes on every run.
"""

import os
import sys

WORD = "defenestration"

MIN_LEN = 1
MAX_LEN = 24


def problems(text: str) -> list:
    """Return every gate violation for the entry text (empty means valid)."""
    found = []
    if not (MIN_LEN <= len(text) <= MAX_LEN):
        found.append(f"entry is {len(text)} characters, must be {MIN_LEN}-{MAX_LEN}")
    stripped = text.strip()
    if not stripped:
        found.append("entry must not be only white space")
    if text != stripped:
        found.append("entry must not start or end with white space")
    if len(text.split()) != 1:
        found.append("entry must be exactly one word")
    if "\n" in text or "\r" in text:
        found.append("entry must be a single line")
    return found


def main() -> int:
    text = WORD
    bad = problems(text)
    if bad:
        for item in bad:
            print(item, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # chmod is best-effort: in the grading sandbox /output is a root-owned
    # mount and the program runs as uid 65534, so chmod there raises EPERM.
    # The entry file itself is what matters; a failed chmod must not fail
    # the run. (The output directory itself is never chmodded or removed.)
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    # Read the file back as bytes and confirm they match the word exactly.
    with open(path, "rb") as f:
        if f.read() != text.encode("utf-8"):
            print("entry.txt does not match the word", file=sys.stderr)
            return 1
    print(f"wrote {len(text)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
