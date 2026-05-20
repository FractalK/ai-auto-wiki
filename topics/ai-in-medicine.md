---
type: topic
title: AI in Medicine
created: 2026-05-20
updated: 2026-05-20
summary: The application of AI to medicine spans molecular biology, clinical workflows, and patient engagement — characterized by strong benchmark performance on isolated tasks, widespread adoption of narrow workflow tools (especially ambient documentation), and a persistent gap between simulated evaluations and real-patient evidence, with only 2.4% of FDA-authorized AI devices supported by randomized controlled trial data.
status: developing
source_count: 1
last_assessed: 2026-05-20
related_topics:
  - "[[ai-capability-benchmarking]]"
  - "[[ai-governance-policy]]"
  - "[[ai-in-science]]"
  - "[[ai-agentic-workflows]]"
technical_depth: practitioner
teaching_relevance: true
competency_domains:
  - output-verification-and-risk-assessment
  - capability-horizon-awareness
  - ai-integration-in-organizational-workflows
professional_contexts:
  - professional-and-continuing-education
  - graduate-and-doctoral-education
  - organizational-leadership-and-change-management
teaching_notes_reviewed: 2026-05-20
---

AI's application to medicine operates across three distinct layers that differ sharply in maturity and evidence quality: molecular and genomic research (protein structure prediction, virtual cell models, therapeutic design), clinical workflows (imaging diagnostics, LLM reasoning, agentic systems, ambient documentation), and patient-facing engagement. A consistent finding across all three mirrors the pattern in AI for science generally — isolated benchmark performance is high, but translation to validated real-world outcomes is slower and methodologically weaker than the benchmark numbers suggest.

## Molecular and Genomic AI

Protein research publications grew 71% in 2025, reaching 3,855 papers (from 2,259 in 2024). The data scale underlying this work also expanded: Tahoe-100M compiles single-cell profiles across 100 million cells, and BaseData aggregates 9.8 billion gene expression measurements. Despite this expansion, the pattern observed in general AI holds: scale alone does not determine performance. MSAPairformer (111 million parameters) outperformed previous leading methods on ProteinGym benchmark for protein fitness prediction. GPN-Star (200 million parameters), focused on functional and regulatory genomics, outperformed Evo 2 — a 40-billion-parameter DNA language model — on multiple variant effect prediction tasks.

In protein structure prediction, subsequent models released after AlphaFold 3 have converged on similar parameter scales (370 million to 923 million parameters) rather than continuing to grow, and AlphaFold 3's FoldBench accuracy (63.10%) has not been significantly surpassed by any of the larger models released since. Data quality and curation, not model size, appear to be the primary bottleneck.

Virtual cell model publications grew from 7 in 2023 to 24 in 2025. Notable releases include Evo 2, STATE (a perturbation-response model), and AlphaGenome (DeepMind's multimodal model). Automated discovery agents extended into medicine: Robin linked hypothesis generation with experimental data to identify a novel treatment candidate for dry age-related macular degeneration; the Virtual Lab produced 92 nanobody binder designs for SARS-CoV-2 using a multiagent framework; Biomni unified a biomedical action space across 25 subfields, integrating 150 specialized tools. These outputs still require experimental validation.

## Clinical Applications and Deployment

Medical imaging training data remains roughly 100 times smaller in sample count than non-medical AI, with data scarcity especially pronounced for three-dimensional CT and MRI modalities. Despite this constraint, prospective clinical trials validating imaging AI grew 28.5% in 2025, from 417 to 536 — the kind of evidence hospitals require before adopting these tools.

LLM clinical reasoning has advanced substantially on benchmark tasks. OpenAI's o1-preview included the correct diagnosis in 78% of NEJM clinicopathological conferences, with 52% top-1 accuracy. On management reasoning vignettes, its median score was 86%, compared with 42% for GPT-4 alone, 41% for physicians with GPT-4 access, and 34% for physicians with conventional resources. On 76 real emergency department cases, it produced diagnoses rated "exact or very close" in 67%–83% of cases. The important caveat: these reflect isolated cognitive evaluations, not real-world clinical integration.

Multiagent frameworks have pushed performance further. Microsoft's AI Diagnostic Orchestrator paired with OpenAI's o3 reasoning model achieved 85.5% accuracy on diagnostically challenging NEJM cases, compared with approximately 20% among 21 practicing physicians working under comparable conditions. Across multiagent evaluations, diagnostic accuracy gains over single-agent baselines ranged from 7% to over 60% depending on task complexity. On MedAgentBench — which tests agents in a virtual electronic health record environment across 300 clinical tasks — the best model achieved 69.7% task success. The evidence base for reliable autonomous clinical agents remains early-stage.

In deployment, ambient AI documentation tools showed the most consistent measurable outcomes. Sharp HealthCare reported an 83% reduction in note-writing effort and a 3.5%–6% increase in physician clinical productivity. Northwestern Medicine reported 11.3 additional patients seen per month and a 112% return on investment. A Stanford Health Care prospective study found a median 20 minutes of time savings per half-day clinic. Two sepsis prediction systems reported mortality reductions at scale: the TREWS system across 13 Cleveland Clinic hospitals produced an 18.7% relative reduction in sepsis mortality; COMPOSER at UC San Diego Health produced a 17% reduction with an estimated 50 lives saved annually.

The regulatory picture is more cautious. By December 2025, the FDA had authorized 1,357 AI/ML medical devices — 258 in 2025 alone — but a peer-reviewed analysis found that only 2.4% of devices with clinical studies were supported by randomized controlled trial data, with nearly all entering via the 510(k) substantial-equivalence pathway. Separately, the NOHARM benchmark found that leading LLMs produced 11.8 to 14.6 severely harmful recommendations per 100 clinical cases, with 76.6% being errors of omission. These LLM findings apply to general-purpose models on open-ended tasks, not the narrower workflow-constrained tools driving current adoption.

## Patient Engagement and Ethics

AI-generated overviews now appear in 84%–92% of health-related Google searches across five query categories, making them a routine feature of how patients access health information. Patient perspectives on clinical AI show conditional acceptance: patients endorse AI in assistive roles but not in autonomous decision-making, and trust is clinician-mediated rather than technology-evaluated.

Ethics discussion in medical AI publications grew from 37.1% in 2024 to 43.4% in 2025, with the absolute count more than doubling. The growth concentrated on governance rather than algorithmic or societal concerns. Biosecurity remains a notable gap: only 14 publications in 2025 addressed it. Global health publications show a different pattern — societal concerns (equity, justice, accessibility) ranked highest, a divergence from the governance-dominated mainstream.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Ambient AI documentation tools achieved measurable outcomes at enterprise scale in 2025: Sharp HealthCare reported an 83% reduction in note-writing effort; Northwestern Medicine reported a 112% return on investment; two sepsis prediction systems (TREWS and COMPOSER) reported 17%–18.7% relative mortality reductions in large-scale hospital deployments — demonstrating that narrow, workflow-constrained clinical AI can deliver verified outcomes when clinician oversight is maintained. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| A review of more than 500 published clinical AI studies found that nearly half relied on exam-style questions rather than real patient data and only 5% used actual clinical data; separately, the NOHARM benchmark found leading LLMs produced 11.8 to 14.6 severely harmful recommendations per 100 clinical cases — indicating that the clinical AI evidence base largely reflects simulated performance and that general-purpose LLMs pose safety risks in open-ended clinical reasoning tasks. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| Microsoft's AI Diagnostic Orchestrator paired with OpenAI's o3 achieved 85.5% accuracy on diagnostically challenging NEJM cases versus approximately 20% among 21 practicing physicians, and OpenAI's o1-preview scored 86% on management reasoning compared with 34% for physicians using conventional resources — demonstrating that AI systems have surpassed most existing clinical reasoning benchmarks, though these results reflect isolated cognitive evaluations rather than real-world clinical integration. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| By December 2025, the FDA had authorized 1,357 AI/ML medical devices from 693 companies across 17 clinical specialties — with 258 authorizations in 2025 alone — but a peer-reviewed analysis of all 1,016 authorizations through December 2024 found only 2.4% of devices with clinical studies were supported by randomized controlled trial data, nearly all entering via the 510(k) substantial-equivalence pathway, indicating a substantial gap between regulatory authorization and clinical evidence quality. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| In molecular AI, GPN-Star (200 million parameters) outperformed Evo 2 (40 billion parameters) on variant effect prediction tasks, and AlphaFold 3's FoldBench accuracy (63.10%) has not been surpassed by any of the larger cofolding models released since — replicating the pattern from general scientific AI benchmarks that specialized smaller models frequently exceed larger general-purpose models and that data quality rather than scale is the primary bottleneck for molecular AI performance. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |

## Teaching Notes

**Concept in plain terms.** AI in medicine encompasses three layers — molecular tools for protein design and genomic analysis, clinical workflow tools (ambient documentation, diagnostic reasoning, imaging), and patient-facing applications — that differ sharply in how well their benchmark claims translate to evidence that would actually change clinical practice.

**Why it matters for instruction.** Students encounter AI medical claims constantly — from LLM diagnostic accuracy headlines to FDA device approvals — without frameworks for evaluating evidentiary strength. Understanding the gap between benchmark performance and clinical validation is foundational for any professional who will make or advise AI adoption decisions in healthcare.

**Common misconceptions.** Students often conflate FDA device authorization with clinical proof of effectiveness; in reality, nearly all AI medical devices enter via a substantial-equivalence pathway, and only 2.4% are supported by randomized controlled trial data. Similarly, headline LLM accuracy on clinical reasoning benchmarks does not translate directly to improved patient outcomes in integrated workflows.

**Suggested framing.** Use the three-layer structure as an organizing scaffold, then apply the evidence-quality question to each layer: what kind of evidence exists, and what gap remains between benchmark and bedside?
