#!/usr/bin/env python3
"""Lint a resume.tex against the rules in config.yaml.

Usage:  python scripts/lint.py <folder-or-tex-file>

Checks: banned terms (internal codenames), banned filler/hedge phrases, PR
links/numbers, contributor titles, leftover <PLACEHOLDER> text, proficiency
labels, and the fixed coursework line. Exit code 1 if any error is found.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _common import load_config


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    target = Path(sys.argv[1]).expanduser().resolve()
    tex = target if target.suffix == ".tex" else target / "resume.tex"
    if not tex.exists():
        sys.exit(f"Not found: {tex}")

    rules = load_config(required=False).get("rules", {})
    # Ignore LaTeX comments so the template's guidance lines don't trigger rules.
    lines = [re.sub(r"(?<!\\)%.*", "", ln) for ln in tex.read_text(encoding="utf-8").splitlines()]
    text = "\n".join(lines)
    low = text.lower()
    errors: list[str] = []

    def add(msg: str) -> None:
        errors.append(msg)

    for term in rules.get("banned_terms", []) or []:
        if term and term.lower() in low:
            add(f"banned term appears: {term!r}")
    for phrase in rules.get("banned_phrases", []) or []:
        if phrase and phrase.lower() in low:
            add(f"banned phrase appears: {phrase!r}")

    if not rules.get("allow_pr_links", False):
        if re.search(r"PR\s*#?\s*\d+|pull/\d+|/pull/", text, re.I):
            add("PR number or link found")
        if re.search(r"\((open|merged)\)", low):
            add("'(open)'/'(merged)' label found")
    if not rules.get("allow_contributor_titles", False):
        if re.search(r"\((core\s+)?(contributor|maintainer)\)", low):
            add("contributor/maintainer title found")

    if re.search(r"\((beginner|intermediate|advanced|expert)\)", low):
        add("proficiency label like '(advanced)' found")
    if re.search(r"\\underline\{", text) and re.search(r"Technical Skills", text):
        add("underline used (skills should not be underlined)")
    if re.search(r"<[A-Za-z][^<>\n]{1,60}>", text):
        add("leftover <PLACEHOLDER> text found")

    fixed = rules.get("fixed_coursework") or []
    if fixed:
        m = re.search(r"Relevant Coursework:\}?\s*(.+)", text)
        if not m:
            add("fixed_coursework is set but no 'Relevant Coursework:' line found")
        else:
            found = [c.strip() for c in re.sub(r"\\&", "&", m.group(1)).rstrip("\\ ").split(",")]
            if found != list(fixed):
                add(f"coursework differs from fixed list.\n    expected: {', '.join(fixed)}\n    found:    {', '.join(found)}")

    if errors:
        print(f"{tex}: {len(errors)} problem(s)")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"{tex}: no rule violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
