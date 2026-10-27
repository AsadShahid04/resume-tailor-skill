"""Shared helpers for resume-tailor scripts."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("Missing dependency: run `pip install -r requirements.txt`")

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "config.yaml"


def load_config(required: bool = True) -> dict:
    """Load config.yaml (falls back to config.example.yaml when not required)."""
    path = CONFIG_PATH
    if not path.exists():
        if required:
            sys.exit(
                "config.yaml not found. Run `python scripts/init.py` first "
                "(see docs/GETTING_STARTED.md)."
            )
        path = REPO_ROOT / "config.example.yaml"
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def resolve(path_str: str) -> Path:
    """Expand ~ and resolve repo-relative paths."""
    p = Path(path_str).expanduser()
    return p if p.is_absolute() else (REPO_ROOT / p).resolve()
