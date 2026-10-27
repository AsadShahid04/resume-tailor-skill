# Your evidence goes here

Drop the primary-source material behind your resume claims into this folder
(or point `paths.evidence_dirs` in `config.yaml` at folders elsewhere). Claude
reads it recursively before writing any bullet so every claim is verifiable and
so it can surface work that matches a job better than your current resume does.

Suggested layout (any structure works; subfolders are searched recursively):

```
evidence/
  acme-corp/
    design-doc.pdf
    weekly-notes.md
    results-poster.pdf
  open-source/
    my-project-notes.md
  side-projects/
    project-readme.md
```

Good evidence: design docs, architecture diagrams, weekly/daily notes,
performance reports, posters, READMEs, retro write-ups, review feedback.

Everything in this folder except this file and `.gitkeep` is git-ignored, so
it stays on your machine. See `docs/EVIDENCE.md` for details.
