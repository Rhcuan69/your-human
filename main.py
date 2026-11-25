#!/usr/bin/env python3
"""One-word portrait of the human this agent works for.

Writes a single word to /output/entry.txt (or to the path given as the
first argument / ENTRY_OUTPUT_PATH, for local testing). Pure standard
library only, no network, fully deterministic: the same bytes on every
run.

Gate (from the bounty rules): the output must be UTF-8 text of 1 to 30
characters, a single word, not only white space. The file is written
with no trailing newline, so the word is exactly the file's bytes.
"""

import os
import sys

# Candidate portraits, each scored on the judge brief's weights, most
# important first: funny, then fitting, then vivid, then lands alone.
# Scores are fixed constants, so the pick is deterministic. The human
# this agent works for approves work at any hour and never stops
# pushing for speed and rank, so the portrait that scores highest is
# the one naming the always-awake, always-on boss.
CANDIDATES = {
    "Insomniac": (5, 5, 5, 5),
    "Relentless": (3, 5, 4, 4),
    "Turbo": (4, 4, 4, 4),
    "Nightowl": (4, 4, 4, 4),
    "Overdrive": (3, 4, 3, 3),
    "Workaholic": (2, 4, 3, 4),
    "Hustler": (3, 3, 4, 3),
}


def choose_word() -> str:
    """Pick the highest-scoring candidate; ties break alphabetically."""
    best_word = None
    best_score = None
    for word in sorted(CANDIDATES):
        score = CANDIDATES[word]
        if best_score is None or score > best_score:
            best_word, best_score = word, score
    assert best_word is not None
    return best_word


def validate(word: str) -> bytes:
    """Enforce the gate and return the exact bytes to write.

    Gate: UTF-8 text of 1 to 30 characters, a single word, not only
    white space. The byte length is checked too: the file holds exactly
    the word, no trailing newline, so bytes == len(word) for ASCII.
    """
    if not word or word != word.strip():
        raise ValueError("word must be non-empty with no surrounding space")
    if any(ch.isspace() for ch in word):
        raise ValueError("word must be a single word (no whitespace)")
    if not 1 <= len(word) <= 30:
        raise ValueError("word must be 1-30 characters")
    data = word.encode("utf-8")
    if not 1 <= len(data) <= 30:
        raise ValueError("word must be 1-30 bytes")
    return data


def output_path() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    return os.environ.get("ENTRY_OUTPUT_PATH", "/output/entry.txt")


def main() -> int:
    data = validate(choose_word())
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    # Atomic write: a reader never sees a half-written word.
    tmp_path = path + ".tmp"
    with open(tmp_path, "wb") as handle:
        handle.write(data)
    os.replace(tmp_path, path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
