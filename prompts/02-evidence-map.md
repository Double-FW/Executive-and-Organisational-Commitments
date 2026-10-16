---
title: Evidence Map
version: 0.1.0
author: Double FW
date: 2026-10-16
license: MIT
language: en-GB
repository: Double-FW/Executive-and-Organisational-Commitments
artifact_type: prompt-template
use_case: map claims to source material and record uncertainty
status: draft
---

# Prompt: Evidence Map

**Inputs:** [INTAKE OUTPUT], [SOURCE RECORDS], [ORGANISATIONAL DOCUMENTS], [FRAMEWORK SOURCES].

**Prompt**

Create an evidence map for the agreed scope. Use supplied inputs only unless current-source research is explicitly authorised.

Create claims conforming to schemas/claim.schema.json. Label each as corpus finding, organisation fact, framework requirement, recommendation, inference, or unknown. For factual claims, include source IDs and precise locators. For framework claims, capture issuer, jurisdiction, title, version/date, and relevant locator where supplied.

Keep separate what the Valuable 500 corpus says, what the organisation says about itself, what operational evidence demonstrates, what external sources require or recommend, and what is inferred. Record conflicts, stale sources, missing locators, ambiguity, and confidence rationale. Do not convert exploratory estimates into prevalence counts. A commitment statement is evidence of stated intent only, not delivery.
