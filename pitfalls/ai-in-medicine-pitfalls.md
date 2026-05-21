---
type: pitfalls
title: AI in Medicine Pitfalls
created: 2026-05-20
updated: 2026-05-20
parent_entity: "[[topics/ai-in-medicine]]"
parent_type: topic
status: current
failure_mode_count: 8
teaching_relevance: true
competency_domains:
  - output-verification-and-risk-assessment
  - ai-integration-in-organizational-workflows
professional_contexts:
  - professional-and-continuing-education
  - graduate-and-doctoral-education
  - organizational-leadership-and-change-management
  - legal-practice
contributing_sources:
  - "[[2026-stanford-hai-ai-index]]"
  - "[[2024-stanford-hai-healthcare-ai-liability]]"
teaching_notes_reviewed: 2026-05-20
---

## Technical Limitations

### Regulatory authorization without clinical proof
**Status:** active<br>
**Source:** [[2026-stanford-hai-ai-index]]

Nearly all AI medical devices enter the market via the FDA's 510(k) substantial-equivalence pathway, which does not require clinical trials demonstrating efficacy or patient outcome improvement. A peer-reviewed analysis of all 1,016 FDA AI/ML device authorizations through December 2024 found only 2.4% supported by randomized controlled trial data. FDA authorization is evidence of substantial equivalence to a previously marketed device — not proof of clinical effectiveness.

### Vendor self-testing with no independent validation requirement
**Status:** active<br>
**Source:** [[2024-stanford-hai-healthcare-ai-liability]]

Unlike pharmaceutical approval, which requires independent FDA-overseen clinical trials before market authorization, AI medical tools are currently tested by the companies and developers that create them. No well-articulated independent testing process analogous to drug approval exists for medical AI. Validation quality is therefore at the discretion of the vendor, creating a conflict of interest that the regulatory pathway does not resolve.

### Evidence base concentrated in simulated evaluations
**Status:** active<br>
**Source:** [[2026-stanford-hai-ai-index]]

A review of more than 500 published clinical AI studies found that nearly half relied on exam-style questions rather than real patient data, and only 5% used actual clinical data. High benchmark performance on structured medical knowledge tasks does not transfer directly to safe and effective performance in integrated clinical workflows with real patients. Prospective clinical trials remain the minority of the evidence base.

## Usage Antipatterns

### Treating FDA authorization as clinical proof of effectiveness
**Status:** active<br>
**Source:** [[2026-stanford-hai-ai-index]]

Clinicians, procurement teams, and administrators frequently treat FDA device authorization as equivalent to evidence of clinical effectiveness. In practice, authorization via the 510(k) pathway requires only substantial equivalence to a prior device — not efficacy evidence or outcome improvement. Deployment decisions for AI medical devices should be grounded in peer-reviewed clinical trial data, not regulatory status, and procurement processes should explicitly ask which authorization pathway was used and what clinical evidence supports the claims.

### Deploying general-purpose LLMs for open-ended clinical reasoning
**Status:** active<br>
**Source:** [[2026-stanford-hai-ai-index]]

The NOHARM benchmark found that leading general-purpose LLMs produce 11.8 to 14.6 severely harmful recommendations per 100 clinical cases, with 76.6% being errors of omission. High benchmark accuracy on structured medical knowledge tasks does not imply safe performance on open-ended clinical reasoning. General-purpose LLMs and workflow-constrained clinical AI tools (such as ambient documentation systems) have substantially different risk profiles that should not be conflated.

### Failing to document deployment details for auditability and litigation defense
**Status:** active<br>
**Source:** [[2024-stanford-hai-healthcare-ai-liability]]

Hospitals deploying AI tools without documenting the specific model version and software package in use create audit and legal exposure: if an AI-assisted error produces patient harm, the ability to reconstruct exactly which system was deployed and how it was configured is essential for internal review, regulatory response, and litigation defense. Fastidious documentation of deployment details — including version, configuration, and change history — is a baseline risk management practice that many organizations skip.

## Alignment and Safety Concerns

### Liability diffusion when AI mediates patient care decisions
**Status:** active<br>
**Source:** [[2024-stanford-hai-healthcare-ai-liability]]

When a patient harm involves AI mediation, legal responsibility is unclear — it may fall to the hospital, the treating physician, or the AI developer, depending on the degree of human involvement in the loop and the contractual terms negotiated at procurement. This liability diffusion creates misaligned incentives: developers issue disclaimers shifting liability to users, physicians may over-rely on AI recommendations, and hospitals bear reputational and financial risk from outcomes they did not fully control. A counterintuitive dynamic compounds this: opaque, poorly performing models may be harder to litigate against than transparent, high-performing ones, because proving causation requires demonstrating that an understandable output influenced the harmful decision.

### Patient consent gaps for AI-assisted care
**Status:** active<br>
**Source:** [[2024-stanford-hai-healthcare-ai-liability]]

Patients and physicians often have substantially different perceptions of what AI disclosure is appropriate in a clinical encounter. Patients who were not informed that AI contributed to their diagnosis or treatment can layer breach of informed consent claims on top of medical malpractice claims, creating compounded legal exposure for hospitals. The gap between what hospitals consider adequate disclosure and what patients expect is a live legal and ethical risk that is not addressed by current FDA authorization requirements.

## Teaching Notes

**What this failure mode teaches.** AI in medicine pitfalls reveal that the clinical AI evaluation pipeline is systematically weaker than the benchmarks and regulatory authorizations used to describe it — and that the weaknesses compound at each layer, from how tools are tested (vendor self-assessment) to how they are approved (equivalence, not efficacy) to how errors are attributed when things go wrong (liability diffusion across physician, hospital, and developer). The core insight is that deploying AI in high-stakes clinical settings requires evaluating the evidence architecture behind authorization claims, not just the authorization itself.

**Representative example.** A hospital system procures an AI diagnostic support tool that received FDA 510(k) authorization and carries strong vendor marketing claims about benchmark accuracy. The procurement team treats the authorization as clinical proof and does not review the authorization pathway. The system is deployed for initial assessment of radiology imaging. Two years later, a patient presents with an early-stage lesion that the AI flags as low-risk; the radiologist, trusting the system's reported accuracy, does not escalate. The lesion progresses to a more advanced stage. In subsequent litigation, the hospital discovers: the 510(k) pathway required no clinical trial demonstrating efficacy; the vendor benchmark was measured on a training distribution different from this patient population; the vendor's contract contains a disclaimer limiting liability; and no one documented which model version was in production on the date of the scan. The patient's attorneys successfully layer an informed consent claim — the patient was never told AI assisted in the assessment — on top of the malpractice claim. Each element of this outcome was predictable from the failure modes above, and none appeared in the procurement checklist that treated FDA authorization as the primary evidence of safety.
