# uri_test_case — the URI OPeNDAP server proof-of-concept

The six-step (now seven-prompt) case study that grep-dap's method rests on. Server:
`https://sst-aqua.gso.uri.edu/opendap/` — Hyrax behind nginx, DAP2 and DAP4 both
advertised, **17 top-level containers of which only 2 are readable by an
unauthenticated client**: `SST_Orbits/` and `gradients_by_period/`. The other 14
return 403.

The two readable branches were the point: one carries COARDS-style semantic metadata
with gaps, the other carries essentially none. Driven by `prompts/test_case_uri.md`.

## The scripts this issue uses

All of them live flat in `../Python/` (D22). Grouped by what they were written for.

| Script | What it does |
|---|---|
| `uri_root_walk.py` | walks the server root catalog |
| `uri_walk_public.py` | walks only what is publicly readable |
| `uri_walk_sst_orbits.py` | walks `SST_Orbits/`, capped at depth 2, 2 children per level |
| `explore_all_dirs.py` | checks accessibility of all 17 directories and finds real files |
| `explore_sst_orbit.py` | first look at `SST_Orbits` file metadata and data |
| `explore_gradients.py` | first look at `gradients_by_period` files |
| `explore_gradients_data.py` | samples gradient data, 5-day gradients |
| `explore_metadata_comparison.py` | compares metadata across files and years |
| `sst_orbits_dmr_inventory.py` | full DMR inventory of an `SST_Orbits` sample file |
| `sst_orbits_coards_audit.py` | COARDS completeness scorer for that file |
| `uri_sample_data.py` | data probes that validate metadata inferences |
| `uri_sample_equator.py` | equatorial slice of one orbit — confirms the SST is realistic |
| `gradients_dmr_inventory.py` | DMR inventory of a `gradients_by_period` sample |
| `gradients_deep_analysis.py` | infers COARDS metadata for that branch |
| `gradients_coords_inference.py` | infers coordinate values, validates the grid |
| `gradients_geom_test.py` | determines lat/lon orientation |
| `gradients_geom_resolve.py` | resolves the lat/lon convention against known geography |
| `gradients_lon_origin.py` | determines the longitude origin |
| `gradients_signs_test.py` | sign conventions and inter-variable consistency |
| `gradients_science_analysis.py` | reconstructs the processing pipeline |
| `gradients_final_validation.py` | final coordinate and variance-computation check |
| `gradient_spatial_scale.py`, `gradient_spatial_scale2.py` | first estimates of the gradient spatial scale |
| `grad_scale_pull.py`, `grad_scale_findregion.py`, `grad_scale_block.py`, `grad_scale_block2.py` | locate and pull regions with usable thermal structure (Mediterranean, Pacific) |
| `grad_scale_1d.py`, `grad_scale_match.py`, `grad_scale_magnitude.py`, `grad_scale_autocorr.py` | the four independent estimators of the operator's spatial support |
| `usage_sanity.py` | checks the `usage_*.md` recipes actually run |

## What is here

| File | What it is |
|---|---|
| `test_case_uri_log_{1…7}.tex` | the timestamped working logs, one per prompt |
| `uri_test_case_{1…5}.tex` | the audit reports for prompts 1–5 |
| `curator_report_sst_orbits.tex` | curator letter — what is missing in `SST_Orbits/` |
| `curator_report_gradients_by_period.tex` | curator letter — the same for `gradients_by_period/` |
| `usage_sst.md`, `usage_gradient_SST.md` | the agent-facing usage documents |
| `*.toc` | LaTeX build artefacts, carried along with their sources |

The proposal-grade summary of all of it is **`../../DOCS/project_summary.tex`**
(prompt 7).

## Reading the paths inside these documents

They still say `docs/…` and `scripts/…`. **That is deliberate** — they are dated
records of what was done in May 2026, and the restructure of 2026-08-04 rewrote paths
only where they are instructions a future session will follow (`claude-config` D33).
`docs/x.tex` in one of these files is now `ISSUE_ANALYSES/uri_test_case/x.tex` or
`DOCS/x.tex`; `scripts/y.py` is now `ISSUE_ANALYSES/Python/y.py`.

## The one negative result worth carrying forward

**The agent got two things wrong in prompt 1** — it missed a root-attribute set and a
scale factor — and **prompt 2 caught both**. `../../DOCS/project_summary.tex` §7 draws
the conclusion: any deployable version of this needs automatic correction loops and
independent re-runs as a built-in feature, not as a hope.
