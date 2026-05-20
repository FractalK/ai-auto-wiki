---
type: topic
title: AI in Science
created: 2026-05-20
updated: 2026-05-20
summary: The application of AI systems to scientific research tasks, characterized by frontier models outperforming human specialists on select domain benchmarks while falling substantially below expert performance on end-to-end research workflows, and by specialized smaller models frequently surpassing much larger general-purpose models on narrow scientific tasks.
status: developing
source_count: 1
last_assessed: 2026-05-20
related_topics:
  - "[[ai-capability-benchmarking]]"
  - "[[ai-in-medicine]]"
  - "[[ai-agentic-workflows]]"
technical_depth: research
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

In Earth science, Aardvark Weather replaced the traditional numerical weather prediction pipeline with a single ML system end-to-end — the first AI system to run a full forecasting pipeline autonomously. FourCastNet 3 generates a 60-day global forecast at 0.25-degree resolution in under 4 minutes, running 8 to 60 times faster than prior approaches.

Despite these advances, the list of experimentally confirmed AI discoveries remains short. Published confirmed discoveries include novel proteins from ProtAgents, 92 antibody candidates for SARS-CoV-2 (>90% successfully bound their target), two cancer drug targets (GPR160 and ARG2), five metal-organic frameworks, and one novel chromophore. Key roadblocks include workforce training gaps, API and interoperability standards, and funding structures not yet supporting the maintenance and scaling of autonomous research infrastructure.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| On scientific benchmarks, frontier AI models outperform human chemists on average on ChemBench but score below 20% on astrophysics paper replication, 36.9% against a 61.9% human expert baseline on PHYBench, and 38.8% against an 83.5% PhD expert baseline on PaperArena — demonstrating that AI scientific capability is highly domain-specific and that end-to-end research tasks remain substantially below expert level. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| MSAPairformer (111M parameters) beat previous leading methods on ProteinGym, and GPN-Star (200M parameters) outperformed a genomics model nearly 200 times larger — demonstrating that specialized smaller models can exceed much larger general-purpose models on narrow scientific benchmarks and that scale alone does not determine scientific AI performance. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| Most AI foundation models for science are produced through cross-sector collaborations dominated by academic and government institutions, in contrast to the industry-dominated landscape of general-purpose AI development. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| In 2025, autonomous science agent systems demonstrated end-to-end workflow execution: Aardvark Weather replaced the full numerical weather prediction pipeline; Google's AI Co-Scientist achieved 78.4% top-1 on GPQA Diamond and validated hypotheses in three biomedical areas; and Sakana's AI Scientist-v2 produced the first fully AI-generated paper accepted at a peer-reviewed workshop — but the list of experimentally confirmed AI discoveries remains short, indicating a persistent gap between computational proposals and validated results. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| AI-related natural science publications grew 26% in 2025 to approximately 80,150, with Earth science reaching the highest AI penetration at 8.8% of total field output — up from below 1% across all natural science categories in 2010, indicating that AI methods are becoming a routine part of scientific practice across disciplines. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
