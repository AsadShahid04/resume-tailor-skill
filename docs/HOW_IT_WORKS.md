# How it works

## The pieces

- **`SKILL.md`** is the instruction set Claude follows. It is generic: no names, no
  employers, no paths.
- **`config.yaml`** supplies everything personal: contact info, folders, banned
  terms, optional fixed coursework.
- **Your general resume** is the baseline of truth.
- **Your evidence folders** hold primary sources.
- **`scripts/`** are deterministic checks so page fit and rule compliance don't rely
  on Claude's judgment.

## Run, step by step

1. **Load config.** Stops if `config.yaml` is missing or has `CHANGE_ME` values.
2. **Parse the job posting** into skills, technologies and responsibilities.
3. **Create `<output_dir>/<company-role-year>/resume.tex`** from your general resume.
4. **Choose section order** so the most relevant material leads.
5. **Enumerate evidence recursively** and read relevant files. Verify open-source work through
   the GitHub API when enabled.
6. **Draft bullets** in XYZ format with baselines, seniority-appropriate verbs, and natural wording
   (the posting's vocabulary absorbed, never copied).
7. **`lint.py`** — banned terms/phrases, PR links, contributor titles, proficiency labels,
   leftover placeholders, fixed coursework.
8. **`build.py`** — two `pdflatex` passes; fail unless exactly one page and the last line of text
   reaches `min_fill_ratio` of the usable height (measured with `pdfplumber`).
9. **Iterate** using the page-fit levers in order: spacing → font size → inter-section space →
   wording. Margins are never a lever.
10. **Deliver** the PDF with a short note on what changed for this role.

## Why a fixed page and fill ratio?

A one-page limit is a screening convention, and a half-empty page looks unfinished.
"Maximum content that still fits" forces choosing the best material rather than
the most.

## Interview survivability

Before delivery each headline bullet is tested against five questions: show the
implementation; the number behind the percentage; the design decision and rejected
alternative; the failure mode; and company-specific plausibility. A bullet that
fails is scaled back to what you can defend live.

## Limits

- Claude can misread a document or misjudge fit. **You** must review the final
  resume.
- The page-fill check measures text position, not visual balance.
- LaTeX font availability varies by distribution; install `lmodern`.
