---
name: resume-tailor
description: >
  Create a tailored, single-page LaTeX resume for a specific job posting, based
  on the user's own general resume and their own evidence files. Compiles to a
  PDF that fills exactly ONE full page. Reframes bullets toward the target role
  WITHOUT inventing facts, optionally verifies open-source claims against real
  GitHub data, and keeps every bullet interview-proof (real baselines behind
  metrics, natural vocabulary instead of verbatim job-description phrasing,
  seniority-appropriate verbs). Use when the user asks to "tailor my resume",
  "make a resume for [job/company]", "customize my resume", or pastes a job
  posting and wants a matching resume.
argument-hint: "[job title / company / job id / paste job description]"
license: MIT
---

# Resume Tailor

Generate a role-specific, single-page LaTeX resume PDF from the user's general
resume, then compile it and verify it fills exactly one page.

Everything user-specific lives in **`config.yaml`** (copied from
`config.example.yaml` by `python scripts/init.py`) and in the user's own
**evidence** and **profile** files. This skill contains no personal data.

## Step 0 — Load configuration (always first)

1. Read `config.yaml` in the skill folder. If it does not exist, stop and tell
   the user to run `python scripts/init.py` (see `docs/GETTING_STARTED.md`).
2. If any value in `candidate:` or `paths:` still contains `CHANGE_ME`, stop and
   ask the user to fill it in. Do not guess contact details.
3. From now on, "the output dir", "the general resume", "the profile", "the
   evidence dirs" and "the rules" mean the values in `config.yaml`.

## Source of truth

- **General resume** (`paths.general_resume`): the baseline LaTeX resume. All
  facts, metrics and dates come from here or from verified evidence.
- **Template** (`references/resume_template.tex`): copy as a starting point if
  the user has no general resume yet. Replace every `<PLACEHOLDER>`.
- **Structured profile** (`paths.profile`, optional): `profile.json` with
  skills, experiences and tech stacks, for quick lookups. Format in
  `profile/profile.example.json`.
- **Evidence** (`paths.evidence_dirs`): the user's primary-source material —
  design docs, notes, posters, READMEs, performance reports. This is usually
  more detailed and more accurate than any resume summary. See
  `docs/EVIDENCE.md`.
- **Output** (`paths.output_dir`): one folder per role, each containing
  `resume.tex`, the compiled `resume.pdf`, and optionally `job.md` (JD plus
  tailoring notes).

## Workflow

1. **Read the job description.** Pull key skills, technologies and
   responsibilities. If the user gave a job ID, put it in the folder name.
2. **Set up the folder.** Create `<output_dir>/<company-role-year>/`, name the
   file `resume.tex`, and copy the general resume (or the template) into it.
3. **Order sections** so the most relevant experience for THIS role comes first
   (e.g. an Open Source / Projects section above Experience if the role values
   it).
4. **Reframe, never fabricate.** Change emphasis and wording, not the truth.
   Every metric and fact must be accurate to the general resume or to evidence.
5. **Mine the evidence to verify and discover.** Before writing a bullet, list
   every file recursively in every directory in `paths.evidence_dirs`:
   ```
   find <each evidence dir> -type f
   ```
   Folders grow over time, so never rely on a previous session's summary of
   what is there. Read every relevant file, including PDFs. Use it to
   (a) confirm each claim is true and (b) surface real work that maps more
   closely to this job than what is already on the resume.
   - If `github.username` is set and `github.verify_open_source` is true, check
     public contributions with the GitHub API
     (`https://api.github.com/search/issues?q=author:<username>+type:pr`) and
     fetch specific PR bodies to verify claims. Never cite PR numbers or links
     in the resume.
   - **If evidence conflicts with a number already on an existing resume, STOP
     and ask the user which is correct** before changing anything.
6. **Write bullets in XYZ format and fill every line** (see below).
7. **Speak the job's domain in the candidate's own words.** Absorb the JD's
   concepts and vocabulary, then describe the real work the way someone who did
   it would. Never paste phrases verbatim from the posting.
8. **Lint:** `python scripts/lint.py <folder>/resume.tex` — checks configured
   banned terms/phrases, PR links, hedges and the fixed coursework line.
9. **Compile and check:** `python scripts/build.py <folder>` — runs pdflatex
   twice, requires exactly 1 page, and reports how full the page is.
   Iterate until it passes.
10. **Deliver:** tell the user where the PDF is and summarise in 2–4 sentences
    what was refined for this role.
11. **Post-steps:** run anything listed under `post_steps` in `config.yaml`
    (optional; empty by default).

## Bullet writing (hard requirement)

- **XYZ format:** "Accomplished [X], as measured by [Y], by doing [Z]." Lead
  with the accomplishment, quantify the impact, name the approach.
- **Fill every wrapped line.** If a bullet wraps, the last line must be nearly
  full. Never end a bullet with a short stub of a few words. Prefer adding real,
  accurate detail from evidence over padding.
- **Metrics need baselines.** Prefer absolute before→after numbers ("22 min to
  5 min") over bare percentages. Vary the metric shape between bullets (time,
  cost, throughput, users served).
- **Altitude matches seniority.** Longer or current roles may use "designed",
  "architected", "led". Short internships use "built", "implemented",
  "contributed to". Do not inflate scope.
- **No tool bingo.** Name only tools that were genuinely central to that work.
- **Quality over quantity.** Three strong bullets beat five thin ones. Fill the
  page with depth, not filler.

## Compile and verify one page (hard requirement)

`python scripts/build.py <folder>` does this for you. Manually:

```
cd <folder>
pdflatex -interaction=nonstopmode resume.tex >/dev/null 2>&1
pdflatex -interaction=nonstopmode resume.tex 2>&1 | grep -E "Output written|pages"
```

- Must say `(1 page, ...)`. If 2 pages, tighten using the levers below. If the
  content stops well short of the bottom margin, add real detail so it fills.
- "One full page" means maximum content that still fits on exactly one page.
  Visible empty space at the bottom is a fail.

## Levers to fit exactly one page

Margins come from `config.yaml` (`formatting.margins_in`) and are **not** a
lever. Adjust in this order, in small steps:
1. Spacing: `\titlespacing*`, `\setlist[itemize]`, `\linespread{0.96}`.
2. Font size: `11pt` → `10pt` (rarely below 10pt).
3. `\vspace{-Npt}` between sections.
4. Condense or expand bullet wording (last resort; keep facts intact).

## Hard rules (defaults — see `rules:` in `config.yaml`)

- **Exactly one full page.** Never two. Never large whitespace.
- **Bullets stay accurate.** No invented metrics, titles or tools.
- **No hollow filler phrases** (`rules.banned_phrases`, e.g. "direct
  experience", "proven scale experience", "relevant to <X>").
- **No aspirational hedges:** "familiarity with X", "exposure to X",
  "understanding of X", "knowledge of X". If the user has not used it
  hands-on, do not list it anywhere.
- **Every skill has a bullet.** Each language/tool in Technical Skills must
  appear in, or be clearly implied by, at least one experience bullet.
  Otherwise remove it from skills.
- **No internal codenames or ticket IDs.** Anything in `rules.banned_terms` must
  never appear. Describe internal work generically ("a Bazel-based
  monorepo", not an internal project name). Public tool names are fine.
- **No PR links or PR numbers**, and no "(open)"/"(merged)" labels, unless
  `rules.allow_pr_links` is true. Still verify the work is real.
- **No contributor titles** ("Core Contributor", "Maintainer") unless
  `rules.allow_contributor_titles` is true.
- **Fixed coursework.** If `rules.fixed_coursework` is non-empty, the Relevant
  Coursework line is exactly that list, in that order. Never reorder, never add.
- **Skills:** no proficiency labels like "(advanced)", no underlines.
- **Spell out acronyms and include both forms for ATS** at least once
  (e.g. "Continuous Integration/Continuous Deployment (CI/CD)").
- **Keep award names exact.**
- **Header and margins** stay consistent with the user's general resume.

## Interview survivability (pre-delivery check)

Run each headline bullet through these gates. If it would not survive a live
screen, rewrite it to claim only what the user can defend.

- **"Show me the implementation."** Could they walk through what it did, how it
  worked, and why not a simpler approach? If evidence does not support the
  depth implied, scale the claim back.
- **"Number behind the percentage."** Can they give the absolute before/after
  and how it was measured? If not, state the baseline or use absolutes.
- **"Design decision + rejected alternative."** At least the top bullet of the
  main role and one other should set up a "what did you reject and why" answer.
- **"Failure mode / lived texture."** At least one bullet should hint at a real
  engineering challenge: what was tried first, what actually worked.
- **"Company-specific plausibility."** Do not claim work that does not fit how
  the named company operates.

## Sanitized variant

If asked for an anonymized copy: replace name, phone, email, LinkedIn, GitHub,
school and company names, and locations with placeholders (`[COMPANY A]`,
`[UNIVERSITY]`, `[CITY, STATE]`), keep bullets and award names verbatim, and
still compile to exactly one page.
