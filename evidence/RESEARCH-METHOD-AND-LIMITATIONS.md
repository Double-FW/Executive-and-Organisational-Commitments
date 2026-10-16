---
title: Research Method and Limitations
version: 0.1.0
author: Double FW
date: 2026-10-16
license: MIT
language: en-GB
repository: Double-FW/Executive-and-Organisational-Commitments
artifact_type: evidence-method
use_case: interpretation and citation of the Valuable 500 executive commitment corpus
status: draft
review_owner: researcher-and-repository-maintainers
review_due: 2027-04-16
---

# Research Method and Limitations

## Purpose

This note separates known information about the evidence base from details that still need recording. It prevents thematic synthesis from being mistaken for a complete, independently reproducible coding study.

## Corpus description

The repository contains Executive Commitments - RAW Data.txt, an anonymised compilation of executive commitment material. The researcher describes the material as gathered across all Valuable 500 member organisations. The accompanying source document describes it as combining more than 500 executive statements.

Those descriptions may refer to different units: organisations and statements. Confirm the exact number of organisations, statements, source documents, and period covered before publishing a denominator or prevalence figure. Physical line counts are not counts of commitments or organisations.

The corpus contains commitment language. It does not establish that organisations delivered commitments or achieved employment, accessibility, or inclusion outcomes.

## Current analytical approach

The researcher describes gathering and anatomising themes across member-organisation material, then building thematic documentation from that work. The repository's thematic guide is a synthesis. It is useful for exploration and prompt development, but the published files do not define a complete codebook or a reproducible statement-level coding protocol.

Document the following before presenting theme frequency as measured prevalence:

- unit of analysis: organisation, document, statement, commitment, or excerpt;
- corpus inclusion and exclusion rules, coverage period, and source discovery method;
- whether themes are multi-label and how overlaps are counted;
- theme definitions and treatment of ambiguous cases;
- coder, reviewer, adjudication, and validation approach;
- any automated or AI-assisted coding, including tools, prompt versions, and human checks;
- denominator and calculation for every frequency;
- treatment of missing, duplicate, translated, paraphrased, or incomplete statements.

## Evidence classes

Keep these classes distinct:

1. **Corpus observation:** what source statements say, supported by extract IDs and locators.
2. **Organisation-specific evidence:** current policy, strategy, data, delivery records, or other supplied documents.
3. **Framework or regulatory source:** authoritative source with issuer, jurisdiction, title, version/date, and locator.
4. **Interpretation:** analytical conclusion drawn from cited sources.
5. **Recommendation:** proposed practice, labelled as advice rather than a corpus finding or legal duty.

Use schemas/source-record.schema.json for source records and schemas/claim.schema.json for claims.

## Known limitations and safeguards

- Anonymisation or absent locators may limit independent verification. Record provenance status; do not guess an organisation or source.
- A member-organisation corpus is not automatically representative of all employers, sectors, regions, or disabled people's experiences.
- Public commitment language is self-presentation and may omit operational practice, disagreement, or outcomes.
- Theme presence does not establish quality, delivery, effectiveness, or causation.
- Broad terms such as “inclusive”, “accessible”, “belonging”, and “continuous improvement” need context and operational evidence.
- Recruitment outreach is not evidence of accessible selection, hiring, adjustments, retention, progression, pay, or work quality.
- Workforce disability measures may create privacy and disclosure risks. The corpus cannot define an organisation's data governance basis.
- Theme overlap is expected. Every count must state whether it counts organisations, statements, extracts, or mentions.
- Estimates in exploratory analysis are hypotheses until checked against a documented method and source records.

## Reporting rule

For each quantitative claim, report numerator, denominator, unit, inclusion rules, coding method, date/version, and uncertainty. If any are missing, label the result exploratory or do not report it as a count.

## Method record to complete

Before publishing measured prevalence, maintain a versioned record of the codebook, corpus snapshot or hash, inclusion criteria, unit of analysis, coder/reviewer roles, adjudication rules, counting procedure, and limitations. Changes to themes or rules require a new version and a note on whether earlier counts were recalculated.
