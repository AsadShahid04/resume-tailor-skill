#!/usr/bin/env python3
"""Compile a role folder's resume.tex and verify it is exactly one FULL page.

Usage:  python scripts/build.py <folder-or-tex-file> [--no-fill-check]

Runs pdflatex twice, then checks:
  * page count == formatting.target_pages (default 1)
  * the lowest line of text reaches formatting.min_fill_ratio of the usable
    page height (so there is no big blank gap at the bottom)
Exit code 0 = pass, 1 = fail.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from _common import load_config

try:
    import pdfplumber
except ImportError:  # pragma: no cover
    sys.exit("Missing dependency: run `pip install -r requirements.txt`")


def compile_tex(tex: Path) -> bool:
    if not shutil.which("pdflatex"):
        sys.exit("pdflatex not found. See README.md > Prerequisites.")
    for _ in range(2):  # two passes: hyperlinks/refs need it
        proc = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex.name],
            cwd=tex.parent, capture_output=True, text=True,
        )
        if proc.returncode != 0:
            print(proc.stdout[-2500:])
            print("\n[FAIL] pdflatex error (see the log excerpt above).")
            return False
    return True


def measure(pdf: Path, margins: dict) -> tuple[int, float]:
    with pdfplumber.open(pdf) as doc:
        pages = len(doc.pages)
        last = doc.pages[-1]
        words = last.extract_words()
        if not words:
            return pages, 0.0
        top_m = margins.get("top", 0.5) * 72
        bot_m = margins.get("bottom", 0.5) * 72
        usable = last.height - top_m - bot_m
        lowest = max(w["bottom"] for w in words)
        return pages, max(0.0, min(1.0, (lowest - top_m) / usable))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("target", help="role folder containing resume.tex, or a .tex file")
    ap.add_argument("--no-fill-check", action="store_true", help="only check the page count")
    args = ap.parse_args()

    target = Path(args.target).expanduser().resolve()
    tex = target if target.suffix == ".tex" else target / "resume.tex"
    if not tex.exists():
        sys.exit(f"Not found: {tex}")

    cfg = load_config(required=False)
    fmt = cfg.get("formatting", {})
    want_pages = int(fmt.get("target_pages", 1))
    min_fill = float(fmt.get("min_fill_ratio", 0.95))
    margins = fmt.get("margins_in", {})

    if not compile_tex(tex):
        return 1

    pdf = tex.with_suffix(".pdf")
    pages, fill = measure(pdf, margins)
    print(f"{pdf}\n  pages: {pages} (target {want_pages})\n  fill:  {fill:.0%} of usable height (min {min_fill:.0%})")

    ok = True
    if pages != want_pages:
        print(f"[FAIL] Expected {want_pages} page(s), got {pages}. Tighten spacing/content." if pages > want_pages
              else f"[FAIL] Expected {want_pages} page(s), got {pages}.")
        ok = False
    if not args.no_fill_check and ok and fill < min_fill:
        print("[FAIL] Page is not full: add real, accurate detail until the last line reaches the bottom margin.")
        ok = False
    if ok:
        print("[PASS] Exactly one full page.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
