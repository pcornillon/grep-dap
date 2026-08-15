# TASKS.md — `grep-dap`

Numbered work list. Appended, never renumbered; a task is never reopened — a follow-on
change is a new task that references the old one.

`Status:` line per task — `todo` | `doing` | `blocked (on what)` | `done (YYYY-MM-DD)`.

The file was created by the 2026-08-04 restructure. Tasks #1–#5 were **read out of the
repository**, not invented: each names where it came from. There was no task list
before, so nothing done earlier is recorded here — `LOG.md` and
`ISSUE_ANALYSES/uri_test_case/test_case_uri_log_*.tex` are the record of that work.

---

## Task #1 — Decide what happens to the `uri` branch

**Status:** done (2026-08-04)

**Resolved: the branch was deleted.** `git push origin --delete uri`, 2026-08-04
16:25 EDT, on Peter's explicit instruction. Recorded as **D6**.

`origin/uri` was **1 commit ahead of `main` and 3 behind** — merge base `07c10f9`
(2026-04-15), single commit `c260ef7` (2026-04-28). A file-by-file comparison found
**nothing on it that `main` lacks**:

- it deleted 12 `.py` scripts — every one that existed at the merge base — which
  `main` still has, now in `ISSUE_ANALYSES/Python/`;
- it added an empty `MD/.gitkeep`, for a folder the restructure does not use;
- it repointed both `prompts/` files at `/Users/petercornillon/…/MD/` and commented
  out prompts 2–6. `main` re-did that localization independently and further, against
  `ISSUE_ANALYSES/` and `DOCS/`, with prompts 2–8 written out in full.

**Two claims in the original write-up of this task were wrong** and are corrected
here. It said the branch deleted **14** scripts — it is 12 — and that it **added**
`gradients_by_period_umm_c.json`. It did not: that file was already at the merge base,
and `main` deleted it in `9776b97`. Since the JSON was the only content-bearing item
behind the recommended option 2 ("cherry-pick then abandon"), there was in fact nothing
to cherry-pick, and option 1 was correct. See the corrections section of
`SESSIONS/2026-08-04_1527_EDT_satdat1.md` for the verifying commands.

**The commit is not lost.** `c260ef7cab953fe2fb31a7912cf3c948b3935aef` is recorded in
D6; the branch can be recreated from it for as long as the object survives locally.

## Task #2 — Run prompt 8 of the URI test case

**Status:** todo

Prompt 8 is written at the bottom of `prompts/test_case_uri.md` and has never been
run — no `_2` files exist anywhere in the repo. It asks for:

- a) the metadata for latitude and longitude of the `L2eqa` fields in `SST_Orbits`,
  which the earlier audits did not address;
- b) a stab at how the fields in `L2eqa_grid` were constructed;
- c) a stab at the origin of the fields summed for `gradients_by_period`;
- d) `_2` revisions of `project_summary.tex`, both curator reports and both usage
  files, plus a working log;
- e) deletion of stray `*.aux`, `*.log`, `*.out` files — already covered by
  `.gitignore`, so this should be a no-op.

**Two things to settle before starting.** The output paths in that document were
rewritten by the restructure, so re-read it rather than working from memory of where
things used to go. And 8(d) names *"the appropriate `test_case_uri_log_7.tex` file"*,
which reads as a slip — prompt 7's log already exists and that document's own naming
rule makes this one `test_case_uri_log_8.tex`.

## Task #3 — Two commented-out prompt blocks in `prompts/test_case_uri.md`

**Status:** todo

The file ends with an HTML-comment block holding a superseded prompt 4, three
unnumbered follow-ups, and a second prompt 8 asking for an **EarthData Search entry for
the `gradients_by_period` dataset**. That last one is real work that was never done and
is not tracked anywhere else. Decide whether it becomes a task or gets deleted; leaving
it commented out means it is neither.

## Task #4 — Is `project_summary.tex` a manuscript?

**Status:** blocked (on Peter)

The restructure put it in `DOCS/` and left `LATEX/` empty, on the reading that it is a
standalone summary written to feed a proposal — which is what prompt 7 asked for and
what `ISSUE_ANALYSES/uri_test_case/test_case_uri_log_7.tex` says it is. If it is
instead headed for publication, it belongs in `LATEX/` with its bibliography, and
`LATEX/` stops being empty. One `git mv` either way.

## Task #5 — The three proposed next steps

**Status:** todo

`DOCS/project_summary.tex` §9 proposes three extensions. They are **proposals in a
document, not commitments** — recorded here so they are not lost, not because they have
been chosen:

1. **Multi-DAAC pilot** — run grep-dap against one representative collection from each
   of three contrasting DAACs (PO.DAAC L2 SST, GES DISC GPM L3, NSIDC sea-ice L4) and
   quantify precision/recall against curator review.
2. **Producer-loop integration** — a prototype that issues pull requests against
   producing repositories for cooperating curators.
3. **User-facing usage-doc service** — auto-generate `usage_*.md` per audited
   collection and measure time-to-first-working-query with and without it.

§8 of the same document lists what would have to be true first, and the honest one is
sample size: **a single server with two readable directories is not a sample.**
