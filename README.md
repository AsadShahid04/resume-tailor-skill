# resume-tailor

A [Claude skill](https://docs.claude.com) that turns **your own** resume and **your own evidence** into a tailored, single-page LaTeX resume for each job you apply to, without inventing a single fact.

You paste a job posting. Claude reads it, digs through your design docs, notes and GitHub history, reframes your real work toward the role, and compiles a PDF that fills **exactly one page**.

## Why this exists

Generic resumes lose to tailored ones, but tailoring by hand is slow, and tailoring with a plain chatbot invites three failure modes:

1. **Fabrication.** The model "improves" a bullet by inventing a metric or a tool you never used.
2. **Tell-tale phrasing.** Bullets that copy the job description word for word are an obvious tailoring giveaway.
3. **Page-fit drift.** Every edit spills onto a second page or leaves a blank gap at the bottom.

This skill fixes those with hard rules and checks:

| Problem | What the skill does |
|---|---|
| Invented facts | Every claim must trace to your general resume or to your evidence files. Conflicts between sources stop the run and ask you. |
| Verbatim JD phrasing | Claude must absorb the JD's vocabulary and describe your work in your own words. |
| Inflated bullets | Verbs must match real seniority; metrics need absolute baselines; tools must be central to the work. |
| Padding | Every skill listed must appear in a bullet; hedges like "exposure to" are banned. |
| Page fit | `scripts/build.py` compiles twice and fails unless the result is 1 page **and** the text reaches the bottom margin. |
| Leaks | `scripts/lint.py` blocks your configured internal codenames, PR links, filler phrases and placeholder text. |

## How it works

```
 job posting ──┐
               ▼
        ┌──────────────┐   reads    ┌─────────────────────────┐
        │ Claude +     │──────────► │ config.yaml  (your rules)│
        │ SKILL.md     │──────────► │ general resume (.tex)    │
        │              │──────────► │ evidence/  (your docs)   │
        │              │──────────► │ GitHub API (optional)    │
        └──────┬───────┘            └─────────────────────────┘
               │ writes
               ▼
   <output_dir>/<company-role-year>/resume.tex
               │
               ▼
   scripts/lint.py  →  scripts/build.py  →  resume.pdf (exactly 1 full page)
```

1. **Config.** Claude loads `config.yaml` (your contact info, paths, rules).
2. **Read the job.** Key skills, technologies and responsibilities are extracted.
3. **Mine your evidence.** Every file under your evidence folders is listed and read, including PDFs. This is where the specific, defensible details come from.
4. **Verify (optional).** If you set your GitHub username, open-source claims are checked against real public PRs.
5. **Write.** Bullets use the XYZ format ("Accomplished X, measured by Y, by doing Z"), with baselines, in your voice, and every wrapped line filled.
6. **Check.** Lint for rule violations, then compile and measure the page.
7. **Deliver.** You get the PDF and a short summary of what changed for this role.

Details: [docs/HOW_IT_WORKS.md](docs/HOW_IT_WORKS.md).

## Prerequisites

| Need | Why | Install |
|---|---|---|
| **Claude** with skills support (Claude Code, or the Claude app with custom skills) | Runs the skill | see [Install the skill](#install-the-skill) |
| **Python 3.9+** | Helper scripts | [python.org](https://www.python.org/downloads/) |
| **A LaTeX distribution with `pdflatex`** | Compiles the resume | macOS: `brew install --cask mactex-no-gui` (or `brew install basictex`). Ubuntu/Debian: `sudo apt install texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended lmodern`. Windows: MiKTeX or TeX Live |
| **Python packages** | `build.py` / `lint.py` / `init.py` | `pip install -r requirements.txt` |
| *(optional)* GitHub username | To verify your open-source contributions | none |

If you installed BasicTeX on macOS you may also need:
`sudo tlmgr update --self && sudo tlmgr install enumitem titlesec lm collection-fontsrecommended`.

## Quick start

```bash
git clone https://github.com/<you>/resume-tailor-skill.git
cd resume-tailor-skill

python -m venv .venv && source .venv/bin/activate   # optional but recommended
pip install -r requirements.txt

python scripts/init.py          # creates config.yaml, folders, and a starter resume
```

Then:

1. **Edit `config.yaml`** — your name, contact info, and paths (see [Things you should fill in](#things-you-should-fill-in)).
2. **Edit your general resume** at the path you set in `paths.general_resume` (the starter is a copy of `references/resume_template.tex`). Replace every `<placeholder>` with true facts.
3. **Add evidence** — see [Uploading your evidence](#uploading-your-evidence-and-references).
4. **Install the skill** — see below.
5. Ask Claude: *"Tailor my resume for this job: \<paste posting\>"*.

Try the scripts on the included fictional sample first:

```bash
python scripts/build.py examples/sample_resume.tex
```

## Install the skill

**Claude Code** — put the repo (or a copy of it) in your skills folder:

```bash
mkdir -p ~/.claude/skills
cp -R resume-tailor-skill ~/.claude/skills/resume-tailor
# or symlink it so edits are picked up: ln -s "$PWD" ~/.claude/skills/resume-tailor
```

Use a project-level skill instead by placing it at `<your-project>/.claude/skills/resume-tailor`.

**Claude app (custom skills)** — zip the folder contents (so `SKILL.md` is at the top level of the zip) and upload it under your Settings → Capabilities → Skills. Because the app runs the skill in a sandbox, point `paths.*` at folders it can reach, or attach your resume and evidence in the chat.

Verify it loaded by asking Claude *"what skills do you have?"* — `resume-tailor` should be listed.

## Uploading your evidence and references

The skill is only as good as the material behind it. Evidence is what lets Claude write *specific* bullets ("replaced a sequential job with partitioned SQL transformations, 3 h → 25 min") instead of vague ones, and what lets it refuse to claim things you can't back up.

**Where it goes:** `references/evidence/` by default, or any folders listed in `paths.evidence_dirs`. Subfolders are searched recursively, so organize however you like:

```
references/evidence/
  acme-corp/            design-doc.pdf  weekly-notes.md  results-poster.pdf
  northwind/            pipeline-readme.md  retro.md
  open-source/          my-contributions.md
  side-projects/        kv-store-notes.md
```

**What to include:** design docs, architecture diagrams, weekly or daily notes, performance reports, posters, READMEs, retros, written feedback, anything with real numbers, tools and decisions. **Formats:** Markdown, text, PDF, and images of diagrams all work.

**Tips**
- Add the **baseline and the measurement method** next to every number. Interviewers ask.
- Note **what you rejected and why** for key design decisions.
- Keep one folder per employer or project; Claude re-lists the tree on every run, so new files are picked up automatically.
- Evidence is git-ignored. It never leaves your machine unless you share it with Claude.

Full guide: [docs/EVIDENCE.md](docs/EVIDENCE.md).

## Things you should fill in

| Where | What | Notes |
|---|---|---|
| `config.yaml` → `candidate` | Name, email, phone, GitHub, LinkedIn | Anything left as `CHANGE_ME` stops the skill and asks you |
| `config.yaml` → `paths.output_dir` | **Where tailored resumes are saved**, one folder per role | Default `~/resumes` |
| `config.yaml` → `paths.general_resume` | Your baseline resume `.tex` | Created from the template on first run |
| `config.yaml` → `paths.evidence_dirs` | Folders of your own documents | Searched recursively |
| `config.yaml` → `github.username` | Your GitHub login | Enables PR verification when `verify_open_source: true` |
| `config.yaml` → `formatting` | Font size and margins | Margins are fixed, never used to squeeze content |
| `config.yaml` → `rules.banned_terms` | Internal codenames, ticket prefixes, project names | Case-insensitive, enforced by `lint.py` |
| `config.yaml` → `rules.fixed_coursework` | Transcript-verified course list | Optional; locks order and content |
| `config.yaml` → `post_steps` | Commands to run after each build | e.g. `open {folder}/resume.pdf` |
| `profile/profile.json` | Structured facts, baselines, rejected alternatives | Optional; a fast lookup for Claude |
| General resume `.tex` | Every `<placeholder>` | Only true facts |

Reference: [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

## Repository layout

```
resume-tailor-skill/
├── SKILL.md                    # the skill Claude runs
├── config.example.yaml         # copy → config.yaml (git-ignored)
├── requirements.txt            # Python packages for scripts/
├── profile/profile.example.json
├── references/
│   ├── resume_template.tex     # starter resume with placeholders
│   └── evidence/               # YOUR documents go here (git-ignored)
├── scripts/
│   ├── init.py                 # first-run setup
│   ├── build.py                # compile + exactly-one-full-page check
│   ├── lint.py                 # rule checks on resume.tex
│   └── check_clean.py          # scan for personal strings before publishing
├── examples/sample_resume.tex  # fictional filled example (+ PDF)
└── docs/                       # guides
```

## Sharing your own version safely

If you fork this and fill it with your own data, `config.yaml`, `profile/profile.json`, and everything in `references/evidence/` are git-ignored. Before you push, run:

```bash
python scripts/check_clean.py . --from-config
```

It scans the repo for your name, email, phone, handles and banned terms. More in [docs/SHARING_SAFELY.md](docs/SHARING_SAFELY.md).

## Contributing

Issues and PRs are welcome — especially more templates (two-column, academic, 11pt), Windows testing, and additional lint rules. Please keep the repo free of anyone's real personal information.

## License

[MIT](LICENSE)
