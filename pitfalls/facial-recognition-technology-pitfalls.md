---
type: pitfalls
title: Facial Recognition Technology Pitfalls
created: 2026-06-05
updated: 2026-06-05
parent_entity: "[[topics/facial-recognition-technology]]"
parent_type: topic
status: current
failure_mode_count: 5
teaching_relevance: true
competency_domains:
  - output-verification-and-risk-assessment
  - ai-safety-and-alignment-literacy
professional_contexts:
  - legal-practice
  - domestic-civil-service-and-public-administration
contributing_sources:
  - "[[2026-aclu-facial-recognition-wrongful-arrests]]"
teaching_notes_reviewed: 2026-06-05
---

## Technical Limitations

### Structural False Match Rate
**Status:** active<br>
**Source:** [[2026-aclu-facial-recognition-wrongful-arrests]]

FRT systems are designed to return similar faces from a database, not to confirm identity. The output is a ranked similarity list; the vast majority of people it returns are innocent. False matches are not edge cases — they are a predictable and documented consequence of the system's design. At least 14 documented wrongful arrests in the United States have resulted from police treating FRT false matches as identifications.

### Demographic Disparities in False Match Rates
**Status:** active<br>
**Source:** [[2026-aclu-facial-recognition-wrongful-arrests]]

Multiple independent studies have documented higher false match rates for people of color, women, younger people, and the elderly. Most documented FRT wrongful arrests in the United States have involved Black individuals, reflecting both training data composition issues and the structural difficulty of differentiation within demographic groups that are underrepresented in training sets. Demographic disparities skew risk without eliminating it across populations.

## Usage Antipatterns

### Treating Similarity Rankings as Identity Confirmation
**Status:** active<br>
**Source:** [[2026-aclu-facial-recognition-wrongful-arrests]]

Police investigators routinely treat FRT results as positive identification rather than as similarity rankings requiring verification. In documented cases, officers applied for arrest warrants with evidence consisting only of the FRT result plus their own visual comparison — without geographic alibi checks, physical characteristic cross-referencing, or other independent corroboration. Police department policies warning against this pattern have not prevented it.

### Contaminating Photo Lineups with FRT Results
**Status:** active<br>
**Source:** [[2026-aclu-facial-recognition-wrongful-arrests]]

Presenting FRT-flagged suspects in photo lineups to witnesses converts a single inference chain into what appears to be independent corroboration. Witnesses who view a lineup containing the FRT-selected person — who more closely resembles the suspect photo than the filler photos — predictably select that person. At least seven of the 14 documented FRT wrongful arrests involved this pattern. Detroit police adopted a prohibition on this practice following settlement of the Robert Williams case; Indiana enacted a statewide version.

### Withholding FRT Reliance from Courts
**Status:** active<br>
**Source:** [[2026-aclu-facial-recognition-wrongful-arrests]]

In multiple documented cases, including the Kimberlee Williams case, police did not disclose their reliance on FRT to courts when applying for arrest warrants. This prevents judicial oversight of FRT-dependent evidence, insulating flawed identification chains from scrutiny at the point where review is most consequential.

## Alignment and Safety Concerns

### Investigative Anchoring and Evidence Suppression
**Status:** active<br>
**Source:** [[2026-aclu-facial-recognition-wrongful-arrests]]

FRT output creates a strong anchoring effect: once an investigator receives a name from FRT, subsequent evidence is interpreted through that frame. Documented cases show officers ignoring visible physical differences between suspects and FRT-identified individuals (full-sleeve tattoos, pregnancy, major height/weight discrepancy), geographic impossibility (suspects living in different states from crime scenes), and pending DNA or fingerprint results that would have exonerated the person. The system does not cause tunnel vision directly; it produces a high-confidence-appearing output that activates it in human investigators and is difficult to dislodge once established.

## Teaching Notes

**What this failure mode teaches.** FRT wrongful arrests illustrate a general pattern: AI systems producing probabilistic outputs (similarity rankings) that humans interpret as deterministic identifications, compounded by anchoring effects that suppress independent verification of disconfirming evidence. The failure is partly technical (structural false match rates, demographic disparities) and partly procedural — verification requirements that exist in policy do not survive the anchoring effect in practice unless they are structurally enforced at each step.

**Representative example.** Kimberlee Williams, an Oklahoma grandmother, spent six months in jail for bank fraud committed in Maryland despite having never visited the state. A facial recognition system identified her as matching bank security camera images of the suspect, and Maryland detectives in three counties proceeded to obtain arrest warrants without establishing whether she could have been in Maryland during the relevant period. Her social media posts, geotagged to Oklahoma at Christmas, would have established a clear alibi; they were never checked. The physical differences between Ms. Williams and the suspect were visible in the photos; investigators nevertheless concluded the two looked similar. Each county's referral described the identification with progressively less detail about how it was obtained, treating the FRT result as established fact by the time the third warrant was applied for. She was arrested in Oklahoma while accompanying her daughter on a delivery, spent months in custody waiting for extradition, was released without a phone or money in December, and was left to find her way home across the country. She lost her job and five years later continues to fear re-arrest for crimes she had nothing to do with.
