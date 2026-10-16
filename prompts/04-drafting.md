---
title: Commitment Drafting
version: 0.1.0
author: Double FW
date: 2026-10-16
license: MIT
language: en-GB
repository: Double-FW/Executive-and-Organisational-Commitments
artifact_type: prompt-template
use_case: draft candidate commitments from approved priorities and evidence
status: draft
---

# Prompt: Commitment Drafting

**Inputs:** [APPROVED PRIORITIES], [EVIDENCE MAP], [GAP REGISTER], [VOICE GUIDANCE], [AUTHORITY AND CONSTRAINTS].

**Prompt**

Draft candidates only for priorities approved for drafting. Use supplied voice guidance while treating brand values as context, not proof of performance.

For each candidate return its ID and priority, proposed statement, concrete action and intended outcome, accountable role, timeframe, resources, baseline, measure, reporting route, evidence/claim IDs, assumptions, limitations, dependencies, and approvals. For each missing item, use decision_required rather than making it up.

Do not invent targets, achievements, legal compliance, owners, budgets, or dates. Do not turn aspiration into a guarantee. Explain vague verbs such as “support” or “promote” through delivery detail. Include employment opportunity only where an approved priority and evidence support it. Mark every draft candidate_not_approved.
