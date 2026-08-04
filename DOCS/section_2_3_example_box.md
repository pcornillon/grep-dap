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
