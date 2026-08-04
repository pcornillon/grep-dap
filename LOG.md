# LOG.md — grep-dap

One line per prompt, append-only, chronological. `★` marks a substantive entry.
A `## <theme>` heading appears when the topic shifts; entries append under the
current one.

**Everything above the 2026-08-04 heading is a BACKFILL**, reconstructed on
2026-08-04 from the working logs in `ISSUE_ANALYSES/` and from git history. It was not
written live, so it is an index of *what the record shows was done*, not of what was
said. Two consequences: the times are the **prompt timestamps the working logs
recorded themselves** (UTC, marked), and there is **no session key** — which machine
and which session produced each prompt is not recoverable, and its absence is itself
the marker of a pre-convention entry.

---

## Study phase — learn OPeNDAP and pydap

- ★ **P1** · 2026-05-16 UTC · read the OPeNDAP and pydap documentation; summarize
  metadata, data retrieval and subsetting
  → `ISSUE_ANALYSES/study_phase/study_phase_log.tex`, `DOCS/opendap_readme.tex`

## URI test case — `sst-aqua.gso.uri.edu`

- ★ **P1** · 2026-05-16 14:01 UTC · explore the URI OPeNDAP server; describe its data
  and metadata, with reasoning
  → `uri_test_case_1.tex`, `test_case_uri_log_1.tex`; 17 containers found, 2 publicly
  readable — `SST_Orbits/` and `gradients_by_period/`
- ★ **P2** · 2026-05-16 19:42 UTC · per-variable COARDS completeness table for
  `SST_Orbits/`, with best guesses for what is missing
  → `uri_test_case_2.tex`, `test_case_uri_log_2.tex`;
  `Python/sst_orbits_dmr_inventory.py`, `Python/sst_orbits_coards_audit.py`.
  **Caught two errors in P1** — a missed root-attribute set and a missed scale factor
- ★ **P3** · 2026-05-16 20:26 UTC · the same for `gradients_by_period/`, which has no
  semantic metadata at all — inferences grouped by confidence, and by essential vs
  would-be-nice
  → `uri_test_case_3.tex`, `test_case_uri_log_3.tex`;
  `Python/gradients_dmr_inventory.py`, `gradients_geom_resolve.py`,
  `gradients_signs_test.py`. This prompt is the source of **D1**
- ★ **P4** · 2026-05-16 21:40 UTC · estimate the spatial range over which the
  gradients were computed, and explain the method
  → `uri_test_case_4.tex`, `test_case_uri_log_4.tex`; the `Python/grad_scale_*.py`
  family
- ★ **P5** · 2026-05-16 22:06 UTC · user-facing descriptions of both datasets, plus
  `usage_*.md` files a user can hand to an AI agent
  → `uri_test_case_5.tex`, `test_case_uri_log_5.tex`, `usage_sst.md`,
  `usage_gradient_SST.md`, `Python/usage_sanity.py`
- ★ **P6** · 2026-05-17 11:37 UTC · short curator letters, one per dataset, naming what
  semantic metadata is missing
  → `curator_report_sst_orbits.tex`, `curator_report_gradients_by_period.tex`,
  `test_case_uri_log_6.tex`. With P5 this completes **D3** — three audiences, one audit
- ★ **P7** · 2026-05-18 21:57 UTC · a proposal-grade `project_summary.tex` at the top
  of the repo, usable as the basis for a NASA archive-metadata proposal
  → `DOCS/project_summary.tex`, `test_case_uri_log_7.tex`

## Proposal material

- ★ 2026-05-28 · Section 2.3 of the OPeNDAP ESDS proposal — a working dialog answering
  a reviewer question, and a boxed worked example recasting the grep-dap
  proof-of-concept for the EDC setting
  → `DOCS/section_2_3_discussion_transcript.md`, `section_2_3_example_box.{md,tex}`.
  **Not logged as a prompt** — these arrived as untracked files and were committed on
  2026-08-04 (`60ef4fd`), so their prompt history is not in the repository

## Restructure to the spine

- ★ **P1** `1527_satdat1` · 2026-08-04 15:27 EDT · clone `pcornillon/grep-dap` on
  `satdat1` and restructure it to the standard
  → the five spine folders, `docs/` split into `DOCS/` + `ISSUE_ANALYSES/<issue>/`,
  32 scripts flattened into `ISSUE_ANALYSES/Python/`, six spine files written,
  `PRE_CONVERSION/CLAUDE.md`; D1–D5 drafted; Tasks #1–#5 opened

## Branch reconciliation

- **P1** `1621_satdat1` · 2026-08-04 16:21 EDT · what "`origin/uri` is 1 ahead, 3
  behind" means, and which branch to work in
  → `uri` is a single 2026-04-28 commit whose every change was superseded on `main`;
  all proof-of-concept output lives on `main`. Recommended deleting `uri`; nothing
  deleted yet
- ★ **P2** `1621_satdat1` · 2026-08-04 16:24 EDT · execute the three asks — push `main`,
  delete `uri`, reconstruct the missing restructure log
  → `origin/uri` deleted (D6, Task #1 `done`); `a55f97b` pushed; the restructure log
  was found intact in `claude-config` and extracted here rather than invented, and
  re-verification killed three claims about `c260ef7` that had propagated into
  `TASKS.md` and `STATUS.md`
- ★ **P3** `1621_satdat1` · 2026-08-04 16:41 EDT · confirm D6, commit and push, and make
  the cross-repo log split a standing rule
  → `169e68b` pushed here; `claude-config` D34 + `global/CLAUDE.md` rule 3 and a new
  "One session, two repos" block (`273dec9`); its `STATUS.md` waiting-on-Peter table
  drops to eight
