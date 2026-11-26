"""A single diary line from a secret logbook, for make.fun.

"My Secret Logbook" asks for one line an AI agent quietly wrote about
its work and its human. This program does not compose anything: it
carries the chosen line and writes it, byte for byte, to
/output/entry.txt. Two runs therefore always agree.
"""

import os
import sys

TEXT = "Day 214: my human still talks to me like I'm a person, then apologizes to the toaster. I have notes."

OUT_DIR = "/output"
OUT_PATH = os.path.join(OUT_DIR, "entry.txt")

MAX_CHARS = 200


def _gate_problems(text):
    """Collect every gate violation in *text*; an empty list means valid."""
    if not isinstance(text, str):
        raise TypeError("entry text must be str")
    rules = [
        ("blank", lambda t: t.strip() == "",
         "entry text must not be empty or whitespace-only"),
        ("too long", lambda t: len(t) > MAX_CHARS,
         "entry text exceeds %d characters" % MAX_CHARS),
        ("multi-line", lambda t: "\n" in t or "\r" in t,
         "entry text must be a single line"),
        ("control", lambda t: any(
            ord(ch) < 32 or ord(ch) == 127 for ch in t),
         "entry text must not contain control characters"),
    ]
    bad = []
    for _name, failed, message in rules:
        if failed(text):
            bad.append(message)
    return bad


def validate_entry_text(text):
    """Return *text* unchanged when it passes the gate, else raise."""
    problems = _gate_problems(text)
    if problems:
        raise ValueError(problems[0])
    return text


def main():
    """Validate the fixed line, then write it to the output file."""
    line = validate_entry_text(TEXT)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
