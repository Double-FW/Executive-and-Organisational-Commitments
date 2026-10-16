---
title: Gap Analysis
version: 0.1.0
author: Double FW
date: 2026-10-16
license: MIT
language: en-GB
repository: Double-FW/Executive-and-Organisational-Commitments
artifact_type: prompt-template
use_case: compare commitments with evidence, values, priorities, and delivery capacity
status: draft
---

# Prompt: Gap Analysis

**Inputs:** [APPROVED SCOPE], [EVIDENCE MAP], [CURRENT COMMITMENTS], [DELIVERY EVIDENCE], [WORKFORCE PRIORITIES].

**Prompt**

Assess current commitments against the agreed scope and evidence map. A value, mission statement, or brand position does not prove corresponding practice.

For each gap provide an ID, description, domain, claim/source IDs, type, evidence strength, uncertainty, consequence, evidence or question needed, whether it blocks drafting, and required human review. Gap types include contradiction, unsupported claim, missing owner, missing authority/resources, missing measure/baseline/timeframe, delivery-evidence gap, and employment-opportunity gap.

Check workforce opportunity across recruitment access, selection, hiring, adjustments, retention, progression, development, and work quality. Do not infer one stage from evidence about another.

Return a prioritised register and one gate: drafting_supported, drafting_supported_with_open_decisions, or pause_for_evidence. Label recommendations as recommendations.
