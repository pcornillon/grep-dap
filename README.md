# `grep-dap`

**A system to learn what is inside an existing OPeNDAP repository when the repository
will not say.**

The DAP protocol was built with a rigid *syntactic* metadata structure — enough to
find, subset and plot the data — and a deliberately free *semantic* one — units, long
names, provenance, everything you need to know what the numbers **mean**. The freedom
was the point: a rigid semantic requirement would have stopped many providers from
serving their data at all. The cost is that semantic metadata on real servers runs
from fully CF-compliant to entirely absent, sometimes in adjacent directories of the
same server.

grep-dap asks whether a GenAI agent, disciplined by the protocol and by direct
statistical probing of the data, can close that gap — and produce two things at once:

- for **curators**, a prioritised, evidence-backed list of what is missing or malformed
  in the metadata they are responsible for;
- for **users and their own agents**, `usage_*.md` documents that make the data
  workable even while the metadata stays incomplete.

Every claim is anchored in catalog structure, the DAP4 DMR, or a small hyperslab
request that tests one hypothesis. Inferences are separated from stated facts and
graded by confidence, and the agent refuses to guess where the evidence will not carry
it — an agent that invents a plausible `date_created` is worse than no audit at all.

## Where it stands

A **proof-of-concept against the URI OPeNDAP server** (`sst-aqua.gso.uri.edu`) is
complete: seven prompts, two readable dataset branches at opposite ends of the metadata
range, and the full set of artefacts — audit reports, two curator letters, two usage
documents, and a proposal-grade summary.

Start with **`DOCS/project_summary.tex`**. It is the whole story in one document:
motivation, method, the case study, what the case shows is feasible, the limitations,
and what a NASA-scale version would need.

## Layout

| Path | What is in it |
|---|---|
| `DOCS/` | `project_summary.tex`, the OPeNDAP/pydap reference, and material contributed to the OPeNDAP ESDS proposal |
| `ISSUE_ANALYSES/uri_test_case/` | the URI case study — working logs, audit reports, curator letters, usage documents |
| `ISSUE_ANALYSES/study_phase/` | the initial OPeNDAP/pydap study |
| `ISSUE_ANALYSES/Python/` | all 32 probe scripts, flat |
| `prompts/` | the prompt specs that drive a run |
| `CLAUDE.md`, `STATUS.md`, `TASKS.md`, `DECISIONS.md`, `LOG.md` | the project's working record |

Python runs in the `ocean14` conda environment and talks to servers with
[pydap](https://pydap.github.io/pydap/en/intro.html).

## Reproducing the case study

Every artefact links to the script and input that produced it, so any claim in the
audits can be re-verified against the live server. The scripts are in
`ISSUE_ANALYSES/Python/`; which one produced what is tabulated in
`ISSUE_ANALYSES/uri_test_case/README.md`.

Note that **14 of the URI server's 17 containers return 403 to a public client**, so an
external reproduction sees only `SST_Orbits/` and `gradients_by_period/` — which is
exactly what the case study saw.
