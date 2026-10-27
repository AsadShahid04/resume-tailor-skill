# Configuration reference

All settings live in `config.yaml` (created from `config.example.yaml` by
`python scripts/init.py`). The file is git-ignored.

## `candidate`

| Key | Required | Notes |
|---|---|---|
| `name` | yes | Shown in the header |
| `email` | yes | Contact line |
| `phone` | no | Leave `""` to omit |
| `location` | no | e.g. `"Austin, TX"` |
| `github` | yes | e.g. `github.com/octocat` |
| `linkedin`, `website` | no | |

Any value still containing `CHANGE_ME` stops the skill and asks you to fill it in.

## `paths`

| Key | Default | Notes |
|---|---|---|
| `output_dir` | `~/resumes` | One subfolder per role: `<output_dir>/<company-role-year>/resume.tex` |
| `general_resume` | `~/resumes/general/resume.tex` | Baseline resume. Created from the template if missing |
| `profile` | `./profile/profile.json` | Optional structured facts |
| `evidence_dirs` | `["./references/evidence"]` | Recursive. Relative paths are relative to the repo |

`~` is expanded. On Windows use forward slashes or escaped backslashes.

## `github`

| Key | Notes |
|---|---|
| `username` | Your GitHub login |
| `verify_open_source` | `true` to check public PRs through the GitHub API |

## `formatting`

| Key | Default | Notes |
|---|---|---|
| `font_size` | `10pt` | `10pt` or `11pt`. Rarely go below 10pt |
| `margins_in` | `0.5` each side | Inches. **Not a fit lever** — never shrink to squeeze content |
| `target_pages` | `1` | |
| `min_fill_ratio` | `0.95` | `build.py` fails if text ends above this share of usable page height |

If you change margins or font size here, change them in your general resume's
`\usepackage[...]{geometry}` line too, so `build.py` measures the right area.

## `rules`

| Key | Notes |
|---|---|
| `banned_terms` | Case-insensitive substrings that must never appear (internal codenames, ticket prefixes) |
| `banned_phrases` | Filler and hedge phrases. Defaults include "direct experience" and "exposure to" |
| `fixed_coursework` | If non-empty, the `Relevant Coursework:` line must equal this list exactly, in order |
| `allow_pr_links` | Default `false` |
| `allow_contributor_titles` | Default `false` ("Core Contributor", "Maintainer") |

The prose rules (XYZ bullets, baselines, seniority-matched verbs, every skill needs
a bullet, interview survivability) live in `SKILL.md`. Edit that file to change
Claude's behavior, e.g. to allow PR numbers or to reorder coursework.

## `post_steps`

Shell commands run after each tailored resume. `{folder}` is replaced by the role folder.

```yaml
post_steps:
  - "open {folder}/resume.pdf"          # macOS
  # - "xdg-open {folder}/resume.pdf"    # Linux
```

## Scripts

| Script | Purpose |
|---|---|
| `python scripts/init.py` | First-run setup and prerequisite check |
| `python scripts/lint.py <folder>` | Rule checks on `resume.tex` |
| `python scripts/build.py <folder>` | Compile twice; require exactly 1 page and ≥ `min_fill_ratio` fill |
| `python scripts/build.py <folder> --no-fill-check` | Page count only |
| `python scripts/check_clean.py <dir> --from-config` | Scan for personal strings before publishing |
