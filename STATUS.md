# STATUS.md — `grep-dap`

Living snapshot of where the project stands. Rewritten, not appended.
Last updated: **2026-08-04 16:35 EDT** (`satdat1`).

---

## State

**The URI proof-of-concept is done through prompt 7 and the write-up exists.** Every
statement below was read out of the repository during the restructure; nothing is
recalled.

- **The test case ran against `https://sst-aqua.gso.uri.edu/opendap/`** — Hyrax behind
  nginx, DAP2 and DAP4 both advertised. It hosts **17 top-level containers, of which
  only two are publicly readable**; the other 14 return Hyrax 403 to an unauthenticated
  client. The two readable branches are **`SST_Orbits/`** and
  **`gradients_by_period/`**, and they sit at opposite ends of the metadata range —
  one carries COARDS-style semantic metadata with gaps, the other carries essentially
  none. Source: `DOCS/project_summary.tex` §3 and
  `ISSUE_ANALYSES/uri_test_case/uri_test_case_1.tex`.
- **Seven prompts have run**, each leaving a timestamped working log and, for most, a
  report:

  | Prompt | What it produced |
  |---|---|
  | 1 | server walk, directory classification, first description of the two readable branches |
  | 2 | per-variable COARDS completeness table for `SST_Orbits/` |
  | 3 | the same for `gradients_by_period/`, inferences grouped by confidence |
  | 4 | estimate of the spatial range over which the gradients were computed |
  | 5 | user-facing descriptions plus `usage_sst.md` and `usage_gradient_SST.md` |
  | 6 | the two curator letters |
  | 7 | `DOCS/project_summary.tex` — the proposal-grade summary |

- **The method produced artefacts for three audiences from one audit** — curator
  letters, user descriptions, and machine-readable usage files. That is the result the
  case study exists to demonstrate.
- **The agent made two factual errors in prompt 1 and they were caught in prompt 2** —
  a missed root-attribute set and a missed scale factor. Recorded in
  `DOCS/project_summary.tex` §7 as an argument that any deployable version needs
  automatic correction loops and independent re-runs. It is the most useful negative
  result in the repository.
- **`section_2_3_*` in `DOCS/` is proposal material, not case-study output.** It is the
  contribution grep-dap made to Section 2.3 of the OPeNDAP ESDS proposal — a discussion
  transcript dated 2026-05-28 and a boxed worked example in both Markdown and LaTeX.
  It cites the case study rather than extending it.

## The restructure — 2026-08-04

The repo was carrying an old shape: `docs/`, `scripts/`, a `CLAUDE.md` with the
"Interactions" block that has been global since 2026-07-31, and none of `STATUS.md`,
`TASKS.md`, `DECISIONS.md`, `LOG.md` or `SESSIONS/`.

| Was | Is |
|---|---|
| `docs/` (25 files) | split — investigation output to `ISSUE_ANALYSES/<issue>/`, standing reference to `DOCS/` |
| `scripts/` (32 `.py`) | `ISSUE_ANALYSES/Python/`, flat (D22) |
| `project_summary.tex` at top level | `DOCS/project_summary.tex` |
| `CLAUDE.md` | rewritten; the original archived unedited in `PRE_CONVERSION/` (D13) |
| — | `STATUS.md`, `TASKS.md`, `DECISIONS.md`, `LOG.md`, `SESSIONS/`, `LATEX/` added |

**`LATEX/` is empty on purpose.** There is no manuscript here — `project_summary.tex`
is a standalone summary document, so it went to `DOCS/`. If it is meant to become a
paper, it should move to `LATEX/`; that is Task #4.

**Path references were rewritten only where they are instructions** (D33). Rewritten:
`CLAUDE.md`, both files in `prompts/`, and the §Reproducibility artefact list in
`DOCS/project_summary.tex` — all four tell a future session where to put or find
things. **Left alone:** every `docs/…` and `scripts/…` path inside the per-prompt
working logs, the audit reports and the two curator letters. Those are dated statements
about what was done, and rewriting them would falsify the record.

## Waiting on Peter

- **Task #4 — is `project_summary.tex` a manuscript?** If it is headed for
  publication rather than for a proposal, it belongs in `LATEX/` rather than `DOCS/`.

*(Task #1, the `uri` branch, was resolved on 2026-08-04 — deleted; see D6.)*

## Active thread — resume here

**Nothing is in flight.** The restructure (`a55f97b`) is committed **and pushed**;
`main` and `origin/main` agree, and `main` is now the only branch — `uri` was deleted
on 2026-08-04 (D6). There is no longer any divergence to reconcile.

The next piece of project work is **Task #2 — prompt 8**, which is already written at
the bottom of `prompts/test_case_uri.md` and has never been run. It asks for four
things the current documentation does not cover:

1. the metadata for latitude and longitude of the `L2eqa` fields in `SST_Orbits`;
2. a stab at how the fields in `L2eqa_grid` were constructed;
3. a stab at the origin of the fields summed for `gradients_by_period`;
4. `_2` revisions of `project_summary.tex`, both curator reports and both usage files,
   plus "the appropriate `test_case_uri_log_7.tex` file" — **which reads as a slip**,
   since prompt 7's log already exists and the file-naming rule at the top of that
   document makes it `test_case_uri_log_8.tex`. Confirm before running it.

**Read `prompts/test_case_uri.md` before starting it** — its output-path lines were
rewritten by the restructure, and prompt 8(d) names filenames that now resolve to
different directories.
