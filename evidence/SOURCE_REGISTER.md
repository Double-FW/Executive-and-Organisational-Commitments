# Historical source register and review decisions

**Version 1.0 · 19 November 2026 · MIT for this inventory metadata**

| Resource | Evidence status | Reuse/publication decision |
| --- | --- | --- |
| [Original compilation](../Executive%20Commitments%20-%20RAW%20Data.txt) | Mixed author guidance and third-party extracts; original URLs/dates and exact statement boundaries unresolved | Preserve unchanged in the GitHub correction; exclude raw wording and reconstructed extracts from the proposed dataset pending documented rights/provenance review |
| [Physical-segment inventory](corpus-inventory.json) | Derived byte offsets, hashes and flags; no original quotation text copied | Internal research/navigation support; excluded from initial dataset to avoid confusing segments with source records |
| [Thematic guide](../Commitments%20on%20Disability%20Inclusion.md) | Current Double-FW methodological advice and newly authored illustrative candidates, not coded prevalence | Original guidance is MIT; carry its limitations and example labels |
| [Public working references](../PUBLIC_SOURCE_MAP.md) | Nine inspected public Double-FW working files at pinned revisions | Secondary guidance only; reference rather than automatically ingest onward content |

## Immutable raw snapshot

Source repository: Double-FW/Executive-and-Organisational-Commitments. Source commit: `3da3acfebb39f5802e12bf4de42cc13c40fe9b31`. Raw Git blob: `c40d42ba5f43872185d5032bc858b29ff7abec5f`. Size: 147,304 bytes. The correction leaves that blob unchanged. The inventory records its SHA-256 and exact UTF-8 byte ranges.

There are 413 carriage-return-delimited physical segments, not 413 statements or organisations. Segments 1–17 contain introductory guidance/questions; segment 18 joins a heading with the first extract; remaining segments can contain multiple or continued source statements. These classifications are editorial navigation only; no original statement boundary has been established.

## Recorded concerns

- Repeated substantial sentences, including workplace-retrofit and organisational inclusion wording, can distort frequency analysis. Repetition is a review flag, not proof that two organisations or two entire statements are identical.
- A slash-ending extract at physical segment 110 requires source inspection. Missing terminal punctuation elsewhere is not sufficient evidence of truncation. Segment 79, for example, continues into 80.
- Later long segments merge multiple apparent statements. Do not split records by line or sentence and assign guessed organisations.
- A brand reference remains in segment 412. No reliable anonymisation guarantee is made and no attempt to de-anonymise sources is authorised.
- Dates, original URLs, rightsholders, translation history and source-level permissions remain unknown. Coverage descriptions relating to Valuable 500 are unverified; no quantitative denominator is approved.

## How to complete the register

When authentic source material is available, create a reviewed source record using [the source schema guide](../schemas/README.md). Record original URL/title, dates, exact locator, true statement boundaries, issuer/organisation status, source type, reuse basis and actual review evidence. Use null/not_assessed where unavailable. Do not fabricate a source record to make this inventory look complete.

Record any derived restoration, translation or deduplication separately, with original references and decisions. Never overwrite the historical compilation or silently upgrade reuse, source verification or approval. Confidential supporting evidence belongs in controlled organisational systems, not this public repository.
