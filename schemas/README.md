# Structured records: optional integration guide

**Version 1.0 · 19 November 2026 · MIT**

Use ordinary prose/tables unless a task explicitly requires machine-readable records. JSON Schema describes a format; it does not install a system or prove truth, rights, secure handling or actual human approval.

| Format | Version | Use |
| --- | --- | --- |
| [Source record](source-record.schema.json) | 1.1.0 | One genuinely identified extract, with original wording separate from interpretation and documented provenance/reuse status |
| [Claim](claim.schema.json) | 1.1.0 | A claim, actual references, uncertainty, review and conditional framework/approval details |
| [Escalation](escalation.schema.json) | 1.0.0 | Optional issue record only when real required operational fields exist |
| [Delivery template](../templates/commitment-delivery-record.yaml) | Template 1.1.0 | Provisional or approved plan headings; no JSON Schema for this template is supplied |

## Exact labels and missing values

Claims use corpus_finding, organisation_fact, framework_requirement, recommendation, inference or unknown. Factual types require a non-empty ref_id and locator in each supporting reference. These must resolve to genuine supplied sources during review; an invented string can still pass structural validation. If unsupported, retain the question as unknown/needs_evidence instead of manufacturing a factual claim.

For a framework_requirement record framework_context: issuer, jurisdiction, title, version_or_date, provision_locator, source_url, authority_type, applicability_status and decision_evidence_ref. Practitioner advice must not become a legal duty. Begin applicability as unresolved; confirmed_applicable or excluded_with_reason requires actual decision evidence. Human source/interpretation review remains necessary.

Approved claims need reviewer_role, reviewed_date and approval_evidence_ref. These record an actual human decision; agents must not create the decision or upgrade a claim to approved themselves. Syntactic completeness cannot authenticate a reviewer or approval. Source reuse_status permitted requires a supporting reuse_basis_ref. provenance_status verified requires title, URL, accessed date and a usable locator, plus substantive verification outside the schema.

Keep null for unknown values where allowed. Use not_assessed/not_provided/decision_required in the designated status field or prose; do not insert these words into date, numeric or reference fields. Source publication dates can remain unknown without inventing them. A known organisation requires a value; do not infer identity from clues in the raw corpus. Check line_end is not before line_start in application review; JSON Schema does not implement that comparison here.

## Validate and review

Use a Draft 2020-12 validator with format checking enabled; JSON parsing alone is insufficient. Validate the schema itself, then instances, then resolve references and check evidence, scope, reuse, human decisions and privacy separately. Evidence strength, quotation fidelity, legal correctness and reviewer authenticity require substantive checks.

The raw physical-segment inventory is not source-record-schema output: its units can mix documents and split sentences. Do not populate source_text_verbatim as if each segment were a verified statement. Its source-level rights remain unresolved and it is excluded from the proposed dataset.

## Migration from 1.0.0

Do not just change the version field. Retain old records as old revisions. Add explicit source provenance/issuer/jurisdiction/version/kind/reuse-basis values from evidence, using unknowns where allowed; add genuine reference IDs/locators for factual claims and framework context when relevant. Approved records need actual decision evidence and date; otherwise keep them pending review. Record the migration and new review state without silently inventing or upgrading evidence.

Escalation timestamps, IDs, policy versions and retention decisions must come from a real authorised operation where known. If required information is missing, report a readable issue and unavailable fields instead of claiming conformance or persistence. A nullable decision_owner_role does not appoint a person. No external logging endpoint or approval service is defined.
