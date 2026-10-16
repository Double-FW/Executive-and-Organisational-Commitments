---
title: Scope and Intake
version: 0.1.0
author: Double FW
date: 2026-10-16
license: MIT
language: en-GB
repository: Double-FW/Executive-and-Organisational-Commitments
artifact_type: prompt-template
use_case: gather authorised context before evidence mapping or drafting
status: draft
---

# Prompt: Scope and Intake

**Inputs:** [ORGANISATION], [SCOPE], [AUDIENCE], [AVAILABLE DOCUMENTS], [KNOWN CONSTRAINTS].

**Prompt**

Prepare an evidence-led disability inclusion commitment workflow for [ORGANISATION] within [SCOPE], for [AUDIENCE].

Do not draft commitment wording yet. Inventory evidence and authority needed for later stages. Review only supplied or authorised sources. Separate organisational statements from demonstrated practice.

Check values, mission, brand principles, strategy, policies, supplied framework sources and jurisdiction, existing commitments and delivery evidence, workforce priorities, baselines, measures, owners, resources, timeframes, reporting routes, constraints, approval authority, and disabled people's participation.

Return scope, audience, source inventory with dates and gaps, approval route or not_provided, ranked missing-information questions, privacy restrictions, and one gate: ready_for_evidence_map, ready_with_open_questions, or pause_for_scope_or_authority.

Do not treat stated values as evidence that practice reflects them. Do not infer disability or health status. If inputs are insufficient, say so.
