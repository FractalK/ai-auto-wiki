---
type: topic
title: AI in Science
created: 2026-05-20
updated: 2026-06-05
summary: The application of AI systems to scientific research tasks, characterized by domain-specific capability gaps on end-to-end workflows, the first autonomous AI resolution of a prominent open mathematical problem (2026), and the consistent finding that specialized smaller models frequently outperform much larger general-purpose models on narrow scientific tasks.
status: developing
source_count: 3
last_assessed: 2026-06-05
related_topics:
  - "[[ai-capability-benchmarking]]"
  - "[[ai-in-medicine]]"
  - "[[ai-agentic-workflows]]"
technical_depth: research
teaching_relevance: true
competency_domains:
  - capability-horizon-awareness
  - output-verification-and-risk-assessment
professional_contexts:
  - graduate-and-doctoral-education
  - teaching-and-instruction
teaching_notes_reviewed: 2026-06-05
---

AI's role in science spans three evolving categories that coexist at different maturity levels: machine learning applied to scientific data for predictive and explainable models (established and now commonplace); AI systems assisting scientist workflows through literature synthesis, experiment design, and data analysis (expanding rapidly in 2025); and autonomous AI systems generating new discoveries with limited human guidance (emerging, early stage). The most visible 2025 advances occurred in the second and third categories. A consistent finding across all three is that AI performs well on isolated subtasks but falls substantially short of expert performance when required to execute the full multistep workflows that actual scientific research demands. Experimental validation also remains a bottleneck: AI systems can propose novel candidates at scale, but confirming discoveries through wet-lab experiments or observational data is costly and time-consuming.

## Publications and Field Penetration

AI-related scientific publications have grown substantially. In the Web of Science database, natural sciences AI publications reached approximately 80,150 in 2025, a 26% increase from 2024. Physical sciences and life sciences each grew roughly 27–28%; Earth science grew 23% to approximately 20,460 papers. As a share of total scientific output, AI penetration in Earth science reached 8.8% — the highest of any scientific category — compared with 6.8% for natural sciences overall, 6.5% for life sciences, and 5.8% for physical sciences. All four were below 1% in 2010, indicating a decade of rapid acceleration.

A consistent institutional pattern: most AI foundation models for science originate from academic institutions collaborating across countries, in contrast to the industry-dominated landscape of general-purpose AI development. Earth science datasets come entirely from government and academic sources, while industry leads in weather and climate foundation model development.

## Performance on Scientific Tasks

Performance benchmarks reveal consistent domain-specific patterns. AI models outperform human chemists on average on ChemBench (2,700+ question-answer pairs) but struggle with basic tasks and score below 20% on ReplicationBench for astrophysics paper-scale replication. On PHYBench (500 original physics problems), Gemini 2.5 Pro scored 36.9% against a human expert baseline of 61.9%. LLM-SRBench, testing equation discovery, found best systems at 31.5%.

The most revealing pattern emerges from end-to-end scientific research benchmarks. On PaperArena — which tests whether LLM agents can answer real research questions by stitching evidence across multiple papers — the best agent reached 38.8% accuracy against a PhD expert baseline of 83.5%. On BixBench, frontier models achieved roughly 17% accuracy on real-world bioinformatics analysis tasks. On UnivEarth, LLM agents answered Earth observation questions with 33% accuracy while their code failed 58% of the time. Across scientific domains, AI systems fall substantially short of expert performance when required to execute full research workflows — consistently scoring roughly half of what PhD experts achieve on end-to-end tasks.

A second pattern: specialized smaller models frequently outperform much larger general-purpose models on narrow scientific tasks. MSAPairformer (111 million parameters) outperformed previous leading methods on the ProteinGym benchmark; GPN-Star (200 million parameters) outperformed a genomics model nearly 200 times its size. Scale alone does not determine scientific AI performance.

## Autonomous Science Agents

Several multiagent systems designed to approximate the structure of a human research team became prominent in 2025. Google's AI Co-Scientist uses a generate-debate-evolve loop in which agents iteratively produce and refine evidence-grounded hypotheses; it was validated in three biomedical areas and achieved 78.4% top-1 accuracy on GPQA Diamond. Sakana's AI Scientist-v2 produced the first fully AI-generated paper accepted at a peer-reviewed workshop (ICLR 2025), using agentic tree search without human-coded templates. Kosmos executed an average of 42,000 lines of code per run and read 1,500 papers, with collaborators reporting single runs approximating six months of research.

In Earth science, Aardvark Weather replaced the traditional numerical weather prediction pipeline with a single ML system end-to-end — the first AI system to run a full forecasting pipeline autonomously. FourCastNet 3 generates a 60-day global forecast at 0.25-degree resolution in under 4 minutes, running 8 to 60 times faster than prior approaches. In ocean science, the Samudra model simulates 1,000 years of climate per day on a single GPU — compared to 12 years per day for traditional numerical models — enabling long-horizon climate experiments previously infeasible at any research budget.

Despite these advances, the list of experimentally confirmed AI discoveries remains short. Published confirmed discoveries include novel proteins from ProtAgents, 92 antibody candidates for SARS-CoV-2 (>90% successfully bound their target), two cancer drug targets (GPR160 and ARG2), five metal-organic frameworks, and one novel chromophore. Key roadblocks include workforce training gaps, API and interoperability standards, and funding structures not yet supporting the maintenance and scaling of autonomous research infrastructure. A 2026 experimental case added a validated end-to-end result: James Zou's Virtual Lab — AI agents running autonomous group meetings to design experiments — produced COVID variant antibody binders in days that wet-lab testing confirmed outperformed previous human-designed nanobodies.

In mathematics, an OpenAI general-purpose reasoning model autonomously disproved the Erdős planar unit distance conjecture in May 2026 — a problem in combinatorial geometry posed in 1946 and studied intensively for 80 years without resolution. The model constructed point configurations with a polynomial improvement over the best known square grid construction (δ ≥ 0.014 per a subsequent refinement by Princeton's Will Sawin), using tools from algebraic number theory — specifically infinite class field towers and Golod–Shafarevich theory — that domain experts had not previously connected to discrete geometry. The proof was verified by Fields medalist Tim Gowers and leading number theorists Arul Shankar and Jacob Tsimerman. This is the first documented case of an AI autonomously resolving a prominent open problem central to an active mathematical subfield, achieved by a general-purpose reasoner without domain-specific training or proof scaffolding.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| On scientific benchmarks, frontier AI models outperform human chemists on average on ChemBench but score below 20% on astrophysics paper replication, 36.9% against a 61.9% human expert baseline on PHYBench, and 38.8% against an 83.5% PhD expert baseline on PaperArena — demonstrating that AI scientific capability is highly domain-specific and that end-to-end research tasks remain substantially below expert level. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| MSAPairformer (111M parameters) beat previous leading methods on ProteinGym, and GPN-Star (200M parameters) outperformed a genomics model nearly 200 times larger — demonstrating that specialized smaller models can exceed much larger general-purpose models on narrow scientific benchmarks and that scale alone does not determine scientific AI performance. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| In 2025, autonomous science agent systems demonstrated end-to-end workflow execution: Aardvark Weather replaced the full numerical weather prediction pipeline; Google's AI Co-Scientist achieved 78.4% top-1 on GPQA Diamond and validated hypotheses in three biomedical areas; and Sakana's AI Scientist-v2 produced the first fully AI-generated paper accepted at a peer-reviewed workshop — but the list of experimentally confirmed AI discoveries remains short, indicating a persistent gap between computational proposals and validated results. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| James Zou's Virtual Lab, using AI agents running autonomous group meetings to design experiments, produced COVID variant antibody binders within days that were experimentally confirmed in a wet lab to outperform previous human-designed nanobodies — a validated case of fully autonomous AI research producing results superior to human-directed science on a specific biological design task. | [[2026-stanford-hai-ai-science-discovery]] | 2026-05-27 | current | 1 | false |
| AI-assisted scientific papers receive approximately 300% more citations than non-AI-assisted papers but systematically converge toward the same large datasets and predictable questions, creating an AI monoculture effect that risks shrinking the diversity of scientific questions explored and disincentivizing abductive, surprise-driven scientific breakthroughs. | [[2026-stanford-hai-ai-science-discovery]] | 2026-05-27 | current | 1 | false |
| An OpenAI general-purpose reasoning model autonomously disproved the Erdős planar unit distance conjecture (1946) — constructing point configurations with a polynomial improvement over the best known square grid construction (fixed positive exponent δ ≥ 0.014 per Will Sawin's refinement) using algebraic number theory tools verified by Fields medalist Tim Gowers — marking the first autonomous AI resolution of a prominent open problem central to an active mathematical subfield. | [[2026-openai-discrete-geometry-conjecture]] | 2026-05-20 | current | 2 | false |

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| Natural sciences AI publications | ~80,150 | Web of Science database; natural sciences category | 2025 | [[2026-stanford-hai-ai-index]] | current |
| Natural sciences AI publications — annual growth | 26% | Web of Science; year-over-year 2024→2025 | 2025 | [[2026-stanford-hai-ai-index]] | current |
| Earth science AI penetration (share of field output) | 8.8% | Share of total Earth science publications with AI content | 2025 | [[2026-stanford-hai-ai-index]] | current |
| AI frontier model success rate — graduate physics problems | 30% | Eun-Ah Kim assessment; graduate-level quantum matter physics | 2025 | [[2026-stanford-hai-ai-science-discovery]] | current |
| pass@1 accuracy — Erdős unit distance problem | 48% | Log scale test-time compute factor ×16 from baseline; pass@1 metric | 2026-05 | [[2026-openai-discrete-geometry-conjecture]] | current |

## Structural Risks and Human Judgment

A key distinction from scientific practitioners is that AI excels at deductive science — filling in missing cells based on learned patterns — while scientific breakthroughs characteristically require abductive science, making creative leaps when encountering surprising violations of expectations. When AI-assisted papers systematically receive far more citations than non-AI papers, scientific incentives pull research toward predictable, pattern-consistent questions and away from the surprising observations that historically generate fundamental advances.

Two additional structural risks compound this: peer review systems are already strained by modern publication volume, and AI-generated research could push them past functional viability without significant institutional changes to how science validates and curates knowledge. In scientific training, the concern is gradual skill atrophy — AI tools make it cheaper to generate data than to collect it and cheaper to use agents than to train doctoral students, but graduate students and postdocs are the future of scientific practice, and their development cannot be optimized away without long-term cost to the discipline.

## Teaching Notes

**Concept in plain terms.** AI in science means using machine learning and autonomous agents to accelerate research — analyzing datasets, designing experiments, and in some cases conducting discovery autonomously. AI excels at isolated subtasks within known domains but falls substantially below expert performance on full research workflows: AI agents score roughly 30–40% on end-to-end research benchmarks where PhD experts score 80%+.

**Why it matters for instruction.** Science is where AI's capabilities and limitations are most concrete and most consequential. Instructors need to convey calibrated expectations: documented breakthroughs exist in specific constrained domains — Samudra running 1,000 years of climate simulations per day, the Virtual Lab producing antibodies experimentally confirmed to outperform human designs, and an OpenAI general-purpose model autonomously resolving an 80-year-old open problem in combinatorial geometry — but these coexist with 30% success rates on graduate-level physics and systematic failure on full research workflows.

**Common misconceptions.** Students assume AI capabilities are uniform across scientific domains, or that benchmark progress translates directly to research utility. Capability is highly domain-specific, and the AI monoculture effect shows that AI incentivizes predictable, citation-maximizing research rather than the surprising, hypothesis-violating observations that drive fundamental advances.

**Suggested framing.** Open with three data points in sequence: one AI system runs 1,000 years of climate simulations per day; a second autonomously proved an open problem in combinatorial geometry that mathematicians failed to resolve over 80 years; a third answers complex research questions correctly only 38.8% of the time where PhD experts score 83.5%. Ask students what to infer about AI scientific capability from all three facts simultaneously.
