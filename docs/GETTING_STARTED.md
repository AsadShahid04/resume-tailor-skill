# Getting started

A 15-minute walkthrough from clone to your first tailored resume.

## 1. Install prerequisites

1. **Python 3.9+** — check with `python3 --version`.
2. **LaTeX with `pdflatex`** — check with `pdflatex --version`. If it's missing:
   - macOS: `brew install --cask mactex-no-gui` (large) or `brew install basictex` (small; then run
     `sudo tlmgr update --self && sudo tlmgr install enumitem titlesec lm collection-fontsrecommended`)
   - Ubuntu/Debian: `sudo apt install texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended lmodern`
   - Windows: install [MiKTeX](https://miktex.org/) or TeX Live
3. **Python packages:**
   ```bash
   python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 2. Initialize

```bash
python scripts/init.py
```

This creates (without overwriting anything that exists):
- `config.yaml` from `config.example.yaml`
- `profile/profile.json` from the example
- your output folder, evidence folder(s), and a starter `general/resume.tex`

It then prints `[ok]` / `[!!]` lines for anything still missing.

## 3. Fill in `config.yaml`

At minimum set `candidate.name`, `candidate.email`, `candidate.github`, and decide
`paths.output_dir`. See [CONFIGURATION.md](CONFIGURATION.md) for every option.

## 4. Write your general resume

Open the file at `paths.general_resume` and replace every `<placeholder>`. This is
your **baseline of truth**: Claude may reframe it for a role, but facts and
numbers must come from here or from your evidence.

Compile it to check:

```bash
python scripts/build.py ~/resumes/general
```

A real, filled resume should print `[PASS] Exactly one full page.` If it says the
page isn't full, add real detail; if it says 2 pages, tighten (see the levers in
`SKILL.md`).

## 5. Add evidence

Drop design docs, notes, READMEs, and reports into `references/evidence/`. See
[EVIDENCE.md](EVIDENCE.md).

## 6. Install the skill

Claude Code:
```bash
mkdir -p ~/.claude/skills
ln -s "$PWD" ~/.claude/skills/resume-tailor      # or copy the folder
```
Claude app: zip the folder contents (with `SKILL.md` at the top of the zip) and upload as a custom skill.

## 7. Tailor a resume

Start a new Claude session and say:

> Tailor my resume for this role. \<paste the full job posting\>

You should get a new folder like `~/resumes/acme-backend-2026/` containing `resume.tex`
and `resume.pdf`. Check it:

```bash
python scripts/lint.py ~/resumes/acme-backend-2026
python scripts/build.py ~/resumes/acme-backend-2026
```

## 8. Review before sending

Read every bullet and ask: *could I explain this in a live interview, including the
baseline behind each number and the alternative I rejected?* If not, edit or delete it.
You are responsible for what goes on your resume.
