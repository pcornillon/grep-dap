# CLAUDE.md — `grep-dap`

**What:** an experiment in using a GenAI agent to infer, verify and document the
semantic metadata of an OPeNDAP archive.
**Produces:** per-archive curator punch-lists and agent-facing `usage_*.md` documents,
plus `DOCS/project_summary.tex`, the proposal-grade writeup of the method.
**State:** the URI proof-of-concept is complete through prompt 7; prompt 8 is written
and unexecuted. See `STATUS.md`.

This file is auto-loaded by Claude Code at the start of every session in this repo.
Peter's universal working rules load separately from `~/.claude/CLAUDE.md` and are
**not** repeated here.

**Read in this order before starting work:**

| File | What it holds |
|------|---------------|
| `CLAUDE.md` (this file) | what the project is, the one idea, the layout, the code rules |
| `STATUS.md` | where things stand right now, ending in the **active thread** |
| `LOG.md` | one line per prompt — scan this to see what has been done |
| `DECISIONS.md` | why the approach is shaped the way it is — numbered `D##` |
| `TASKS.md` | the work list: numbered tasks with `Status:` lines |

## What this project is

**grep-dap** learns what is inside an existing OPeNDAP archive when the archive will
not say.

The DAP protocol was designed with deliberately asymmetric metadata: a **rigid
syntactic** structure — shapes, dtypes, dimensions, groups, everything needed to plot
the data — and a **virtually free semantic** structure — units, long names, standard
names, provenance, everything needed to *label* the plot. The asymmetry was
intentional: a rigid semantic requirement would have kept providers from serving their
data at all. The cost is that semantic metadata across real servers runs from fully
CF-compliant to entirely absent, sometimes in adjacent directories of the same server.

So an analyst meeting an unfamiliar OPeNDAP dataset either trusts the producer and
risks silent misinterpretation, or reverse-engineers the semantics from structure,
naming, the statistical behaviour of the data, and better-annotated siblings. The
second is what an experienced scientist does. It is also the kind of multi-modal,
judgement-laden inspection a GenAI agent can now attempt.

Two audiences, one audit:

- **Curators** get a prioritised, evidence-backed punch list of what is missing or
  malformed in metadata they are responsible for.
- **Users and their agents** get `usage_*.md` documents that make the data workable
  even while the metadata stays incomplete.

## The one idea that makes this tractable

**An OPeNDAP endpoint is a probeable environment, and the agent is a sceptical
external reader whose every claim must be anchored in one of three classes of
evidence:**

1. **Catalog-level structure** — directory names, file-naming grammar, version tags.
   `AQUA_MODIS_orbit_NNNNNN_YYYYMMDDThhmmss_L2_SST-URI_24-2.nc4` encodes platform,
   instrument, orbit, start time, level, producer and version without opening the file.
2. **Structural metadata** — the DAP4 DMR (or DAP2 DDS+DAS), parsed depth-aware, so
   every group, dimension, variable, dtype, shape, fill value, scale factor and
   declared attribute is captured.
3. **Data probes** — small, deliberately chosen DAP hyperslab requests that test one
   hypothesis each: *is this variable in °C?*, *does lat run S–N or N–S?*, *what is
   the effective spatial support of this derivative operator?*

The output is never a single declarative answer. It separates **stated**, **inferred**
and **not safely guessable**, and grades each inference by confidence, so a downstream
consumer knows what is safe to act on automatically and what needs producer
confirmation. An agent that cheerfully invents a plausible `date_created` is worse
than no audit at all — see **D1** and **D2**.

## Layout

```
CLAUDE.md          this file — project context
STATUS.md          where things stand + active thread
DECISIONS.md       numbered design decisions (D##)
TASKS.md           numbered work list with Status: lines
LOG.md             append-only one-line-per-prompt index, ★ on the substantive ones
README.md          human-facing overview

DOCS/              standing reference and cross-cutting documents
  project_summary.tex              the proposal-grade writeup (prompt 7)
  opendap_readme.tex               OPeNDAP + pydap reference, from the study phase
  section_2_3_*                    material contributed to the OPeNDAP ESDS proposal
ISSUE_ANALYSES/    the investigations (D22)
  study_phase/                     learn OPeNDAP and pydap
  uri_test_case/                   the URI server proof-of-concept, prompts 1–7
  Python/                          every probe script, flat — 32 files
LATEX/             empty — no manuscript here
SESSIONS/          curated session logs, one per session, P## per prompt
PRE_CONVERSION/    the pre-restructure CLAUDE.md, archived unedited (D13)

prompts/           the prompt specs that drive the runs — study_phase.md,
                   test_case_uri.md. These are inputs, not analyses; they stay
                   at the top level.
```

**`ISSUE_ANALYSES/Python/` is flat and holds every script**, whichever investigation
wrote it — whether a probe will be reused is not knowable when it is written. Each
issue folder's `README.md` opens with the scripts that issue uses.

## Code guidelines

- Reuse existing code when possible.
- Generate **methods, not classes**.
- Include inline comments.
- Use **matplotlib** for plotting.
- Run Python in the **`ocean14`** conda environment.
- Talk to an OPeNDAP server with **pydap** — https://pydap.github.io/pydap/en/intro.html

## Where output goes

- Scripts → `ISSUE_ANALYSES/Python/`, flat.
- An investigation's logs, reports and outputs → `ISSUE_ANALYSES/<issue>/`.
- Standing reference and anything that spans investigations → `DOCS/`.

## Reference

OPeNDAP servers at NASA:
https://www.earthdata.nasa.gov/engage/open-data-services-software/earthdata-developer-portal/opendap
