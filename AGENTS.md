---
title: Agent Guidance for Evidence-Led Organisational Commitments
version: 0.1.0
author: Double FW
date: 2026-10-16
license: MIT
language: en-GB
repository: Double-FW/Executive-and-Organisational-Commitments
artifact_type: agent-governance-guidance
use_case: evidence-led drafting, review, delivery, and renewal of disability inclusion commitments
status: draft
review_owner: repository-maintainers
review_due: 2027-04-16
---

# Agent Guidance

This file governs human and AI use of this repository to assess and draft organisational commitments. It is not legal advice, a compliance certificate, or authority to make commitments for an organisation.

## Machine-readable policy

~~~yaml
policy_version: "0.1.0"
status: draft
workflow:
  ordered_stages:
    - scope_and_intake
    - evidence_map
    - gap_analysis
    - drafting
    - delivery_and_measurement
    - assurance
    - review_and_renewal
  allow_stage_skip: false
  return_to_prior_stage_when_new_evidence_arrives: true
evidence:
  claim_types: [corpus_finding, organisation_document, framework_or_regulatory_source, recommendation, inference]
  factual_claim_requires_source_ref: true
  preserve_source_wording: true
  separate_interpretation_from_source_text: true
  treat_unverified_estimates_as_counts: false
  treat_commitment_text_as_proof_of_delivery: false
generation:
  invent_targets_baselines_owners_dates_budgets_or_authority: false
  infer_disability_or_health_status: false
  use_brand_values_as_evidence_of_performance: false
  draft_public_commitment_without_human_approval: false
  require_employment_opportunity_review: true
human_review:
  required_before_publication: true
  required_for_legal_or_regulatory_interpretation: true
  required_for_sensitive_workforce_data_use: true
  required_for_unresolved_evidence_conflict: true
  required_when_disabled_people_lacked_meaningful_input: true
observability:
  record_stage_and_prompt_version: true
  record_source_refs_and_claim_ids: true
  record_escalation_reason_and_disposition: true
  minimise_personal_data: true
  redact_health_or_disability_details_unless_authorised_and_necessary: true
  retention: "Use the organisation's approved retention schedule; do not invent one."
~~~

## Quick start

1. Confirm organisation, scope, audience, decision-maker, and authority.
2. Collect current values, strategy, policies, relevant framework sources, existing commitments, operational evidence, workforce priorities, baselines, resources, and constraints.
3. Run the prompts in prompts/README.md order. Keep stage outputs and source references.
4. Create one delivery record per proposed commitment using templates/commitment-delivery-record.yaml.
5. Pause where evidence, authority, ownership, privacy controls, disabled people's input, or human approval is missing.
6. Obtain authorised human approval before publication and schedule a review against reported outcomes.

## Decision flow

~~~mermaid
flowchart TD
  A["Scope and authority confirmed?"] -->|No| B["Pause and request decision"]
  A -->|Yes| C["Evidence traceable?"]
  C -->|No| B
  C -->|Yes| D["Draft and attach delivery record"]
  D --> E["Assurance and disabled people's input complete?"]
  E -->|No| B
  E -->|Yes| F["Human approval before publication"]
~~~

## Evidence and citation rules

- Treat Executive Commitments - RAW Data.txt as a source compilation. Preserve wording and sequence when structuring it. Physical lines are not counts of organisations or commitments.
- Treat Commitments on Disability Inclusion.md as thematic synthesis and drafting guidance, not as a substitute for source evidence.
- Label claims as corpus findings, organisation-specific evidence, framework or regulatory sources, recommendations, or inferences. Cite stable source IDs and exact locators.
- Preserve uncertainty, disagreement, source dates, scope limits, and missing provenance. Do not present estimates as measured counts without a documented method and denominator.
- Values, mission, and brand language provide context; they do not demonstrate practice.
- Stated intent is not evidence of implementation or impact. Do not infer employment outcomes from rhetoric.
- Use a multi-label theme taxonomy so one statement may be coded to multiple themes.

## Output contract

Return the requested structured output, source and claim IDs for factual assertions, unknowns and unresolved decisions, confidence with a rationale, and required human reviewers. Use not_provided, not_verified, or decision_required for missing information. Never silently fill gaps.

## Prompt examples

**Authority unclear**

> I can map the evidence and prepare a draft for review. The decision-maker and approval route are not yet confirmed. Who can approve this commitment, and what resources are available?

**No baseline supplied**

> The evidence supports a proposed action, but no baseline or target was supplied. I have left both as open decisions and have not created a numerical promise.

## Escalation and observability

Create an escalation record conforming to schemas/escalation.schema.json for legal or regulatory interpretation, unsupported public claims, sensitive workforce data, conflicts between stated values and operational evidence, missing authority or resources, or absent meaningful disabled-person participation.

Record only an event ID, UTC timestamp, stage, prompt and policy versions, relevant source and claim IDs, issue category, decision owner, reviewer, disposition, rationale, and next review date. Keep restricted detail in an approved system and refer to it with a redacted identifier.

Do not put names, diagnoses, adjustment details, or identifiable employee narratives in general-purpose logs. Follow the organisation's approved access, retention, and deletion controls. If these controls are not supplied, pause and request governance direction.

## Version and review

| Version | Date | Change | Status |
|---|---|---|---|
| 0.1.0 | 2026-10-16 | Initial evidence-led workflow draft | Requires repository and subject-matter review |

Review at least every six months and sooner when corpus, schemas, frameworks, or governance change. Presence of this draft does not mean it is approved.

