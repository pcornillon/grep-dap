# TASKS.md — grep-dap

Numbered work list. Appended, never renumbered; a task is never reopened — a follow-on
change is a new task that references the old one.

`Status:` line per task — `todo` | `doing` | `blocked (on what)` | `done (YYYY-MM-DD)`.

The file was created by the 2026-08-04 restructure. Tasks #1–#5 were **read out of the
repository**, not invented: each names where it came from. There was no task list
before, so nothing done earlier is recorded here — `LOG.md` and
`ISSUE_ANALYSES/uri_test_case/test_case_uri_log_*.tex` are the record of that work.

---

## Task #1 — Decide what happens to the `uri` branch

**Status:** blocked (on Peter)

`origin/uri` is **1 commit ahead of `main` and 3 behind**. The merge base is `07c10f9`
(2026-04-15); the branch's one commit is `c260ef7` (2026-04-28) and `main` has three on
top of the same base. Read from the branch, not recalled — `c260ef7`:

- **deletes all 14 `.py` scripts that existed at the time** (1,480 lines);
- adds an empty `MD/.gitkeep` and a `gradients_by_period_umm_c.json`;
- edits both files in `prompts/`, per its message *"Updated the two prompt files for
  running this from URI."*

Meanwhile `main` gained 18 more scripts, all of `docs/`, `project_summary.tex`, and now
the restructure — which moved every path that branch touches.

**Because it is a single stale commit, this is cheaper than it looks.** Three options:

1. **Abandon it** — delete the branch. The `gradients_by_period_umm_c.json` and the
   prompt-file edits are the only content on it that `main` does not have.
2. **Cherry-pick then abandon** — take the JSON, re-apply the prompt edits onto the
   restructured files by hand, then delete. **Cheapest of the three**, since there is
   exactly one commit to mine.
3. **Merge properly** — the expensive one: a conflict in both prompt files and a
   delete/rename conflict on every script, for no content `main` lacks.

**Nothing was done to it.** The restructure did not touch it, and this decision is
Peter's: what that branch was *for* (running the case from a URI machine?) is not
recoverable from the repository.

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
