# DECISIONS.md — grep-dap

Numbered design decisions, with rationale, so a future session does not relitigate a
settled choice or misread a deliberate one as an oversight.
Each entry: **the decision → why → where it lives → any live tension.**
Appended, numbered, never renumbered.

**D1–D4 were not made during the restructure that created this file.** They were
already operating — stated in `prompts/test_case_uri.md`, in
`DOCS/project_summary.tex`, and in the shape of the audit reports — and were promoted
here on 2026-08-04 so they stop living only inside documents. Each cites its source.
**They are drafts until Peter confirms them.**

---

### D1. Separate stated, inferred and not-safely-guessable, and grade every inference
- **Decision:** an audit never emits a flat metadata record. It partitions every
  attribute into **stated** (the server says so), **inferred** (the agent concluded it
  from evidence), and **not safely guessable**, and it grades each inference by
  confidence — statistical support from a data probe, naming-grammar regularity,
  consistency with a better-annotated sibling. The same partition is applied twice
  over: **essential** versus **would-be-nice** attributes.
- **Why:** the consumer of the audit has to know what is safe to act on automatically
  and what needs producer confirmation. A single undifferentiated answer collapses that
  distinction and is unusable for both audiences. The rejected alternative — emit one
  best guess per field — is what makes an automated metadata service untrustworthy.
- **Where:** `prompts/test_case_uri.md` prompt 3, which asks for exactly this grouping;
  `DOCS/project_summary.tex` §2; the audit reports
  `ISSUE_ANALYSES/uri_test_case/uri_test_case_{2,3}.tex`.

### D2. Refuse to guess rather than fill a field
- **Decision:** where the evidence does not support a value, the agent says so and
  leaves the field empty. It does not supply a plausible one.
- **Why:** *"An agent that cheerfully fabricates a plausible `date_created` or
  `processing_history` is worse than no audit at all"* — `DOCS/project_summary.tex` §7.
  A wrong-but-plausible attribute propagates silently into every downstream use, while
  a missing one is visible. D1's confidence grading is the first line of defence and
  this is the second.
- **Where:** `DOCS/project_summary.tex` §2 and §7; the "not comfortable guessing" group
  in `ISSUE_ANALYSES/uri_test_case/uri_test_case_3.tex`.
- **Live tension:** `project_summary.tex` §7 lists both defences as **needing empirical
  evaluation**. Neither has been measured.

### D3. One audit, three artefacts — curator, user, agent
- **Decision:** a single pass over an archive produces three deliverables with
  different audiences and different registers: a **short curator letter** naming what
  is missing or malformed, a **user-facing description** long enough to decide whether
  the dataset fits a question, and a **machine-readable `usage_*.md`** a downstream AI
  agent can be handed directly.
- **Why:** the three audiences want different things from the same evidence, and
  generating them separately would mean auditing three times and letting the three
  drift. Demonstrated rather than argued: prompts 5 and 6 produced all three from the
  prompt 1–4 audit without re-probing the server.
- **Where:** `prompts/test_case_uri.md` prompts 5 and 6;
  `ISSUE_ANALYSES/uri_test_case/curator_report_*.tex`, `usage_sst.md`,
  `usage_gradient_SST.md`; `DOCS/project_summary.tex` §5.

### D4. Anchor every claim in catalog structure, structural metadata, or a data probe
- **Decision:** the agent's three admissible classes of evidence are catalog-level
  structure (directory and file-naming grammar, version tags), structural metadata (the
  DAP4 DMR or DAP2 DDS+DAS, parsed depth-aware), and **small DAP hyperslab requests
  that each test one hypothesis**. Every claim in an audit links back to the structural
  feature, naming-grammar item or probe that supports it.
- **Why:** it is what makes the audit re-verifiable against the live server rather than
  a reading of the metadata, and probing is what catches metadata that is present but
  wrong — a variable declared `units="kelvin"` whose values span 270–310 is confirmed;
  one that spans −3–35 is not. The rejected alternative, trusting declared metadata, is
  exactly the failure the project exists to address.
- **Where:** `DOCS/project_summary.tex` §2 and §10; every script in
  `ISSUE_ANALYSES/Python/`.

### D5. Investigation output lives with its investigation; `DOCS/` holds only what spans them
- **Decision:** in the 2026-08-04 restructure, the old `docs/` was **split** rather
  than renamed. Each investigation's working logs, audit reports and deliverables went
  to `ISSUE_ANALYSES/<issue>/`; only standing reference and cross-cutting material went
  to `DOCS/`. All 32 probe scripts went flat into `ISSUE_ANALYSES/Python/`.
- **Why:** the global standard's `ISSUE_ANALYSES/` (D22 in `claude-config`) is exactly
  this repo's shape — the whole of its content to date is two investigations plus the
  probes they wrote. The rejected alternative was the literal reading, `docs/` → `DOCS/`
  wholesale with `scripts/` left at the top level as code. That was rejected because
  `scripts/` is not a package and nothing imports it: the files are per-investigation
  probes, and D22 exists because whether a probe will be reused is not knowable when it
  is written.
- **Where:** `DOCS/`, `ISSUE_ANALYSES/`, and the two issue `README.md` files, each of
  which opens with the scripts its investigation used.
- **Live tension:** `CLAUDE.md` describes grep-dap as *"a package for inferring the
  contents of an OPeNDAP server."* When real package code appears it goes at the top
  level in a lowercase directory — `src/` or `grep_dap/` — and **not** into
  `ISSUE_ANALYSES/Python/`, which stays what it is: the probe drawer.

### D6. Delete the `uri` branch — it held nothing `main` lacks
- **Decision:** `origin/uri` was deleted on 2026-08-04 (`git push origin --delete
  uri`). Its one commit is
  **`c260ef7cab953fe2fb31a7912cf3c948b3935aef`** (2026-04-28), recorded here so the
  branch can be recreated if the judgment below is ever doubted. Do not go looking for
  work on that branch: there is none.
- **Why:** the branch was made in April to localize the project onto Peter's machine
  after the clone from `Sea-Meets-the-Stars`. It was pushed once and abandoned. Three
  weeks later the same localization was done again on `main`, further and against the
  current layout — `ISSUE_ANALYSES/` and `DOCS/` rather than the `MD/` folder `uri`
  proposed, with prompts 2–8 written out where `uri` had commented 2–6 out. A
  file-by-file comparison found **every** change on `c260ef7` superseded: the 12
  script deletions (`main` keeps the scripts), the empty `MD/.gitkeep`, and both
  prompt files. The rejected alternatives were merging it — which would have deleted
  all 32 probe scripts and conflicted on every renamed path — and keeping it as a
  historical marker, rejected because a divergent branch reads as unmerged work and
  had already cost two sessions.
- **Where:** nothing in the repository depends on it. `TASKS.md` #1;
  `SESSIONS/2026-08-04_1527_EDT_satdat1.md`, whose corrections section holds the
  verifying commands.
- **Live tension:** the record of *why* the branch existed — what "running this from
  URI" was meant to change about the run — is not recoverable from the repository, and
  deleting the branch does not make it more so. If that intent mattered, it is in
  Peter's memory, not in git.
