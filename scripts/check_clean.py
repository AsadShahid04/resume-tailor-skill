#!/usr/bin/env python3
"""Scan a folder for strings that should never be published.

Use this before pushing your own fork/copy to a public repo, or before sharing
a sanitized resume.

Usage:
    python scripts/check_clean.py <folder> "Your Name" "you@example.com" "ProjectCodename" ...
    python scripts/check_clean.py <folder> --from-config      # uses config.yaml candidate + rules.banned_terms

Matching is case-insensitive over every text file (git-ignored build output and
.git are skipped). Exit code 1 if anything is found.
"""
from __future__ import annotations

import sys
from pathlib import Path

from _common import load_config

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules"}
SKIP_FILES = {"config.yaml"}  # local config is git-ignored on purpose


def candidate_strings(cfg: dict) -> list[str]:
    out: list[str] = []
    for k, v in (cfg.get("candidate") or {}).items():
        v = str(v or "").strip()
        if v and "CHANGE_ME" not in v:
            out.append(v)
    out += [t for t in (cfg.get("rules", {}).get("banned_terms") or []) if t]
    return out


def main() -> int:
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    root = Path(args[0]).expanduser().resolve()
    needles = args[1:]
    if needles == ["--from-config"]:
        needles = candidate_strings(load_config())
    needles = [n for n in needles if n]
    if not needles:
        sys.exit("No strings to search for.")

    hits = 0
    for path in root.rglob("*"):
        if not path.is_file() or SKIP_DIRS & set(path.parts) or path.name in SKIP_FILES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # binary file
        for lineno, line in enumerate(text.splitlines(), 1):
            low = line.lower()
            for n in needles:
                if n.lower() in low:
                    hits += 1
                    print(f"{path.relative_to(root)}:{lineno}: contains {n!r}")
    if hits:
        print(f"\n{hits} match(es). Remove them before publishing.")
        return 1
    print("Clean: none of the given strings were found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
