# Historical Context

This project was built between 2019 and 2020 by Maryna Antonevych as a
Bachelor's qualification thesis ("Intelligent application for identification
of agricultural plant diseases based on deep learning") at the Faculty of
Information Technology, Taras Shevchenko National University of Kyiv,
supervised by I. M. Domanetska. It was defended in June 2020, and an earlier
version of the work was also presented as conference proceedings at the VI
International Scientific and Practical Conference "Information Technologies
and Interactions" (IT&I-2019).

## What "2020" means here

- The model, code, dataset choice, and reported results below are exactly
  what existed in 2020 — nothing has been retrained, re-evaluated, or
  improved.
- The original environment: Python 3.6, PyTorch/torchvision (pinned per
  training run — see [`docs/results.md`](results.md)), Flask, MySQL 8.0,
  developed and trained on CPU only, on Windows.
- No GPU, no modern MLOps tooling, no containerization, and no automated
  tests existed in the original project. That was standard for a 2020
  undergraduate CPU-bound ML project, not an oversight to "fix."

## What "2026" means here

The repository structure, README, architecture docs, English presentation
materials, and this documentation set were written in 2026 to make the
original work legible to a modern technical audience (recruiters, engineers).
None of this backdates new tools, results, or design decisions onto the 2020
implementation — see [`docs/methodology.md`](methodology.md) and
[`docs/results.md`](results.md) for what is historical fact versus what is
2026 framing.

## Why some material from the original source is not in this repository

The original Google Drive folder was a shared class/department drive and
contained, alongside this project's own materials, complete thesis
submissions and presentations belonging to other students, private
correspondence with the supervisor, and defense-day video recordings. None of
that is this author's own deliverable to publish, so it was excluded. See the
final restoration report for the full exclusion list.
