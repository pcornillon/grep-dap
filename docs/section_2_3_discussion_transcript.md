# Working dialog: Section 2.3 (Machine-actionable guidance for autonomous data retrieval workflows)

*Transcript of a working session discussing the OPeNDAP ESDS proposal, Section 2.3. Prepared for a proposal coauthor. Date: 2026-05-28.*

---

## 1. The reviewer question

> **Peter:** One of the questions asked related to Section 2.3 was: *"For part 2.3 is the point to allow more AI based scientific queries to the data?"* How would you respond?

**Response:**

Not quite — that's closer to what Parts 2.1 and 2.2 enable. The distinct point of 2.3 is delivery and efficiency of retrieval, not enabling queries per se.

The distinction:

- **Part 2.1** (crawlable interfaces) is what lets AI tools *discover and query* the data at all.
- **Part 2.2** *produces* the per-collection knowledge (the markdown files with usage metadata, optimal chunk-retrieval strategies, dataset-specific quirks).
- **Part 2.3** is about *where that knowledge lives and how an agent gets it at the moment it acts*. The point is to embed the guidance directly into the DAP4 responses the agent is already pulling, so the agent doesn't have to go find the recipe separately — the operational instructions travel with the data. The payoff is stated at the end of the section: "reducing retrieval inefficiencies and failed access patterns."

So it's less "allow more AI queries" and more "make the queries agents already make succeed, and run efficiently, the first time." Part 2.3 turns the static `usage.md` documents from 2.2 into in-band, machine-actionable context that an autonomous agent consumes mid-workflow — telling it *how* to subset, which chunks to fetch, and how to compensate for known dataset problems — rather than just enabling another query channel.

Suggested fix to head off the question in the proposal text itself, since 2.3 currently reads like a continuation of 2.2. Open the section with something like:

> While Parts 1 and 2 make collections discoverable and queryable by AI tools, the value of the curated guidance is only realized if agents receive it at the point of retrieval. Part 3 therefore embeds...

---

## 2. Should the proposal include a worked example?

> **Peter:** Do you think an example of how an agent might do this would be of value (drawing on the grep-dap proof-of-concept and project summary)? CLAUDE.md can be dramatically shortened and not all sections of the test prompt need to be performed — the emphasis should be on the inferences made by the agent.

**Response:**

Yes — a worked example would strengthen 2.3 considerably, and it's arguably the single most persuasive thing to add.

**Why it helps.** Section 2.3 is currently the most abstract part of the proposal. "Embed machine-actionable guidance into DAP4 responses" is hard for a reviewer to picture. The grep-dap case study is a concrete, already-executed demonstration of the whole pipeline 2.1→2.2→2.3: the agent crawled a server (2.1), inferred and validated semantics (2.2), and emitted `usage_*.md` files designed to be handed to a *downstream* agent to actually retrieve data (2.3). It also directly answers the proposal's own stated risk — that the agent "hallucinates" — because the experiment's central discipline is confidence-graded inference with explicit refusal to guess. The example does double duty: it makes 2.3 tangible *and* pre-rebuts the limitations section.

**Summary of the experiment, emphasizing the inferences.** The test ran against the URI OPeNDAP server (sst-aqua, AVHRR/MODIS SST-fronts), 17 directories, only 2 publicly readable. The premise: OPeNDAP fixes *syntactic* metadata (shapes, dtypes, dimensions) but leaves *semantic* metadata (units, coordinates, provenance) free to vary from fully CF-compliant down to nothing. The agent's job was to act like an experienced scientist reverse-engineering an unfamiliar dataset — anchoring every claim in one of three evidence classes: catalog/naming structure, the parsed DMR, and small DAP hyperslab "data probes."

The inferences are the heart of it:

- **Coordinate orientation from data probes.** The zero-metadata gradient dataset had no coordinate variables. The agent classified 6 known-land and 6 known-ocean points against the pixel-count field; only one of four candidate lat/lon conventions got all 12 right, fixing lat as south-to-north (−89.5+k) and lon as −180→+180 unambiguously. A verifiable inference from data, not a guess.
- **Sibling-dataset inheritance.** The gradient sums carried no units; the agent inferred °C/km from the better-annotated sibling `SST_Orbits/` on the same server.
- **Variable-name grammar.** The regular `{day,night}_sum_{SST,...}_squared` structure let it infer a sum / sum-of-squares / count bookkeeping scheme.
- **Quantitative physical inference.** It estimated the spatial support of the gradient operator — a number found nowhere in the metadata — at 5±2 km, via three independent methods (pixel-count ratios, RMSE matching against centered differences, autocorrelation) that converged.
- **Catching errors a human would miss.** It flagged two factually wrong unit declarations (a wind speed labeled "mm", a pixel count labeled "C") by comparing declared units against actual value ranges and sibling variables.
- **Knowing what it can't know.** Inferences were graded on a 3×2 matrix — confidence (very confident / guessed / will-not-guess) × importance (essential / nice-to-have) — and the agent explicitly refused to fabricate unsupported fields like `date_created` or processing history.

The output split into three audiences from one audit: a curator punch-list, a human-readable dataset description, and the agent-facing `usage_*.md` — the last being exactly the 2.3 artifact.

**On trimming the demo.** For a proposal figure or sidebar you don't need the full 8-prompt sequence or the LaTeX-logging scaffolding — that's process overhead, not signal. The compelling narrative is: zero-metadata dataset → agent probes the data → recovers coordinates, units, and operator scale, each tagged with its evidence and confidence → emits a machine-actionable usage file.

---

## 3. Important reframing for the ESDS context

> **Peter:** Keep in mind the dataset we tested on was one I created, and it has no metadata. We're proposing to ESDS, which holds NASA datasets. Those already have pretty detailed semantic metadata, so the effort is more verification and accumulation from each granule for entire datasets.

This reframing is reflected in the boxed example below: the proof-of-concept proved the inference machinery on a metadata-free dataset, but for NASA collections the job is **verification + cross-granule accumulation** of metadata that already largely exists, not recovery from scratch. The two mislabeled-units catches are retained as evidence that the value-range check finds real errors even in well-annotated data.

---

## 4. Draft boxed example for Section 2.3

> **Worked example: from per-granule verification to a retrieval recipe**
>
> We have already exercised this workflow end-to-end against a live Hyrax server (the grep-dap proof-of-concept). The example below recasts that demonstration for the EDC setting, where collections already carry detailed CMR and CF metadata and the agent's job is therefore *verification* and *cross-granule accumulation* rather than recovery from scratch.
>
> **What the agent does, per collection.** Walking the granules of a collection through OPeNDAP, the agent (1) confirms that the stated semantic metadata is internally consistent across granules and consistent with the data itself, and (2) accumulates collection-level facts that no single granule record exposes. Each finding is anchored in evidence and graded by confidence, and the agent explicitly refuses to assert anything it cannot defend.
>
> - **Value-range vs. declared units.** A small DAP4 hyperslab request confirms that a variable declared `units="kelvin"` actually spans ~270–310, not ~−3–35. In the proof-of-concept this same check caught two genuinely mislabeled variables (a wind speed declared `"mm"`, a pixel count declared `"C"`).
> - **Cross-granule accumulation.** Per-granule spatial/temporal bounds, fill-value usage, and valid ranges are aggregated into a single collection-level envelope, and divergence between granules is flagged.
> - **Cross-checks against CMR.** Accumulated bounds are compared with the collection's CMR record; disagreements are surfaced for an expert rather than silently overwritten.
> - **Retrieval-relevant structure.** DMR++ chunk sizes and layout are read directly, yielding concrete subsetting guidance (chunk-aligned request shapes, byte ranges, and dataset-specific pitfalls).
>
> **The 2.3 payload.** These verified, evidence-tagged facts are written to a per-collection `usage.md` and embedded in the collection's DAP4 responses. A downstream autonomous agent then consumes it in-band, at the moment of retrieval, and issues a correct, chunk-aligned subsetting request on the first attempt—without a separate discovery round-trip and without guessing at units, coordinate orientation, or fill conventions. This is the difference Part 3 delivers: the curated guidance from Part 2 travels with the data, turning queries that agents already make into queries that succeed.
