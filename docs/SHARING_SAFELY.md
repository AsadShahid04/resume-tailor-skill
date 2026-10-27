# Sharing safely

Two common situations.

## A. You cloned this repo and added your own data

Personal files are git-ignored by default:

- `config.yaml`
- `profile/profile.json`
- everything in `references/evidence/` (except its README and `.gitkeep`)
- `resumes/` and `output/`

If you keep resumes inside the repo or use a different output folder, add it to `.gitignore`.

**Before every push to a public fork:**

```bash
python scripts/check_clean.py . --from-config      # name, email, phone, handles, banned terms
git status                                         # make sure nothing personal is staged
git diff --cached --stat
```

You can also pass extra strings: `python scripts/check_clean.py . "Employer Name" "InternalCodename"`.

## B. You want a friend to use your setup without your data

Give them a fresh clone of the public repo, not your working folder. They run
`python scripts/init.py` and fill in their own config and evidence. Nothing of yours is
copied, because your personal files are never committed.

## C. Sharing a resume itself

Ask Claude for a **sanitized variant** (see the end of `SKILL.md`): name, contact info, school,
employers and locations replaced by placeholders, bullets kept, still one page. Run
`check_clean.py` on the output folder with the real values to confirm nothing leaked.

## Reminders

- Employer documents may be confidential. Don't commit them anywhere.
- A secret committed once stays in git history even if you delete the file later.
  If that happens, rewrite history (`git filter-repo`) or create a fresh repo.
