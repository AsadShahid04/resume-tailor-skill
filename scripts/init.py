#!/usr/bin/env python3
"""First-run setup: create config.yaml, folders, and check prerequisites.

Usage:  python scripts/init.py
Safe to re-run: it never overwrites an existing config.yaml or resume.
"""
from __future__ import annotations

import shutil
import sys

from _common import REPO_ROOT, CONFIG_PATH, load_config, resolve


def main() -> int:
    example = REPO_ROOT / "config.example.yaml"

    if CONFIG_PATH.exists():
        print(f"[ok] config.yaml already exists: {CONFIG_PATH}")
    else:
        shutil.copy(example, CONFIG_PATH)
        print(f"[new] Created {CONFIG_PATH} from config.example.yaml")

    profile_example = REPO_ROOT / "profile" / "profile.example.json"
    profile = REPO_ROOT / "profile" / "profile.json"
    if not profile.exists():
        shutil.copy(profile_example, profile)
        print(f"[new] Created {profile} (edit it, or delete it if you don't want a profile)")

    cfg = load_config()
    paths = cfg.get("paths", {})

    out_dir = resolve(paths.get("output_dir", "~/resumes"))
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[ok] Output dir: {out_dir}")

    general = resolve(paths.get("general_resume", str(out_dir / "general" / "resume.tex")))
    if general.exists():
        print(f"[ok] General resume: {general}")
    else:
        general.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO_ROOT / "references" / "resume_template.tex", general)
        print(f"[new] Copied the template to {general} — replace the placeholders with your facts")

    for d in paths.get("evidence_dirs", []):
        p = resolve(d)
        p.mkdir(parents=True, exist_ok=True)
        print(f"[ok] Evidence dir: {p}")

    problems = 0
    if shutil.which("pdflatex"):
        print("[ok] pdflatex found")
    else:
        problems += 1
        print("[!!] pdflatex not found — install a LaTeX distribution (see README.md > Prerequisites)")

    remaining = [k for k, v in (cfg.get("candidate") or {}).items() if "CHANGE_ME" in str(v)]
    if remaining:
        problems += 1
        print(f"[!!] Fill these in config.yaml > candidate: {', '.join(remaining)}")

    print("\nNext: edit config.yaml, add evidence, then ask Claude to tailor a resume.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
