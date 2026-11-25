"""The Moon Finally Answers Back — make.fun entry.

Writes one line (1 to 240 characters): the Moon's reply at last to
everyone who has ever stared up at it, to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt).

Pure standard library only.

Why this line: the Moon answers all three things the brief names —
the wishes, the howls, the late-night promises — in one breath, then
turns it around: four billion years of listening, and nobody ever
wished the Moon goodnight back. The turn lands in the final words,
in one read, in the Moon's own wry, old, tired voice.
"""

import os

LINE = (
    "You wished, you howled, you promised. "
    "Four billion years, and nobody ever wished me goodnight back."
)

MAX_CHARS = 240


def validate(text):
    """Enforce the RULES.txt gate: UTF-8, 1-240 chars, not only whitespace,
    single line, and free of control characters."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    if any(0x80 <= ord(ch) <= 0x9F for ch in text):
        raise ValueError("entry must not contain C1 control characters")
    if len(text) > MAX_CHARS:
        raise ValueError("entry is %d chars, over the 240-char limit" % len(text))
    text.encode("utf-8")
    return text


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    entry = validate(LINE)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(entry)
    # Read back and re-validate what actually landed on disk.
    with open(path, "r", encoding="utf-8") as fh:
        on_disk = validate(fh.read())
    assert on_disk == entry, "entry.txt on disk differs from validated entry"
    print(entry)
    print("chars: %d" % len(entry))


if __name__ == "__main__":
    main()
