---
title: Assurance Review
version: 0.1.0
author: Double FW
date: 2026-10-16
license: MIT
language: en-GB
repository: Double-FW/Executive-and-Organisational-Commitments
artifact_type: prompt-template
use_case: identify unsupported, unsafe, inaccessible, or unapproved commitments
status: draft
---

# Prompt: Assurance Review

**Inputs:** [CANDIDATE WORDING], [EVIDENCE MAP], [DELIVERY RECORDS], [PARTICIPATION RECORD], [DATA GOVERNANCE].

**Prompt**

Review each candidate and delivery record. Return findings with severity, evidence/claim IDs, rationale, required action, and human-review role. Do not silently rewrite material issues.

Check source support and scope of factual or legal claims; overclaiming or confusion between intent and delivery; authority, accountability, feasible resources, baseline, measure, timeframe, reporting; meaningful disabled people's input and its influence; accessible and respectful language; privacy, minimisation, access, retention and redaction; and whether employment opportunity is operationally addressed.

Do not give a legal conclusion. Mark legal or regulatory interpretation for qualified human review. Return pass_for_human_approval, revise, or stop_and_escalate. No candidate is publishable until an authorised human approves it.
