# Troubleshooting

| Symptom | Fix |
|---|---|
| `pdflatex not found` | Install a LaTeX distribution (README → Prerequisites) and reopen your terminal |
| `LaTeX Error: File 'lmodern.sty' not found` | `sudo apt install lmodern` or `sudo tlmgr install lm` |
| `File 'enumitem.sty'` / `titlesec.sty` not found | `sudo tlmgr install enumitem titlesec` (or install `texlive-latex-extra`) |
| `config.yaml not found` | Run `python scripts/init.py` |
| Skill stops and asks for `CHANGE_ME` fields | Fill in `candidate:` in `config.yaml` |
| `ModuleNotFoundError: yaml` / `pdfplumber` | `pip install -r requirements.txt` (inside your venv) |
| `[FAIL] Expected 1 page(s), got 2` | Tighten spacing, then font size, then wording. Never margins |
| `[FAIL] Page is not full` | Add real, accurate detail from your evidence; don't pad |
| `leftover <PLACEHOLDER> text found` | A `<...>` from the template is still in `resume.tex` |
| Claude doesn't use the skill | Confirm the folder is at `~/.claude/skills/resume-tailor/SKILL.md` and start a new session |
| GitHub verification rate-limited | Export a `GITHUB_TOKEN` or turn `verify_open_source` off |
| Fill ratio looks wrong after changing margins | Update the `geometry` line in your `.tex` to match `formatting.margins_in` |
