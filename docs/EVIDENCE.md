# Evidence & references

"Evidence" is any primary-source material that backs up what you did. Claude reads
it before writing bullets, for two reasons:

1. **Verify** — confirm every claim and number is true.
2. **Discover** — surface real work that matches a job better than what's already
   on your resume.

## Where to put it

By default: `references/evidence/`. To use folders elsewhere (a notes vault, a
Downloads folder), list them in `config.yaml`:

```yaml
paths:
  evidence_dirs:
    - "./references/evidence"
    - "~/Documents/work-notes"
    - "~/Documents/school-projects"
```

Folders are searched **recursively** and re-listed every run, so adding a file is
all you need to do.

> Everything in `references/evidence/` except `README.md` and `.gitkeep` is
> git-ignored. If you point `evidence_dirs` at folders outside the repo, they are
> never part of the repo at all.

## What makes good evidence

| Type | Why it helps |
|---|---|
| Design docs / architecture write-ups | Real components, tradeoffs, and rejected alternatives |
| Weekly or daily notes | Lived detail: what broke, what you tried first |
| Performance reports, dashboards (PDF/screenshots) | Baselines and measurement methods behind your numbers |
| Posters / final presentations | Your own summary of impact |
| READMEs and repo notes | Tech stack, scope, test counts |
| Manager or peer feedback | Scope and seniority you can claim honestly |
| `open-source.md` listing repos, what you changed, and why | Lets Claude cross-check against GitHub |

## Suggested note template

For any project, one short file like this beats a pile of raw documents:

```markdown
# <Project> at <Company> (<Mon YYYY> – <Mon YYYY>)

**Role / scope:** what I owned vs. what the team owned
**Problem:** what was slow, broken, or missing
**What I built:** components, languages, tools (only what was central)
**Numbers:** before → after, how measured, over what period
**Design decision:** what I chose, the alternative I rejected, why
**Hard part:** what failed first, how I found it, what actually worked
**Verification:** tests, benchmarks, rollout
```

## Confidential material

Your employer's internal documents may be confidential. Put in evidence only what
you're allowed to use, and expect Claude to describe internal systems generically
on the resume ("a Bazel-based monorepo", not an internal codename). Add internal
names to `rules.banned_terms` so `lint.py` fails if one slips in.

## When evidence and your resume disagree

If a design doc says 18% and your resume says 22%, Claude will stop and ask which is
right rather than silently choosing. Resolve it once, then update the resume.

## Open-source claims

Set `github.username` and `github.verify_open_source: true`. Claude will list your
public PRs with the GitHub API and read PR descriptions to confirm claims. Resume
text still never includes PR numbers or links (unless you set `allow_pr_links: true`).
Unauthenticated API calls are rate-limited; if you hit limits, set a `GITHUB_TOKEN`
environment variable.
