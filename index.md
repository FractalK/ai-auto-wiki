---
type: index
title: AI Effectiveness Wiki
created: 2026-04-22
updated: 2026-04-22
---

This wiki automatically tracks AI tools, capabilities, workflows, and failure modes for practitioners
who need to evaluate and apply AI in professional settings. Content is organized by
concept area, product, and use case and updated continuously as new sources are ingested in accordance with the principles outlined in [[2026-karpathy-llm-wiki-pattern|Andrej Karpathy's famous April 2026 GitHub gist]], though customized for these purposes. 

To learn more, see [[how-this-wiki-works]].

Browse by category below. For content aligned to specific learning objectives and
professional roles, see the [[teaching-index]].

*59 pages. Last updated: 2026-04-26.*

---

## Topics

- [[ai-alignment]] — The research program aiming to ensure AI systems behave in accordance with human intent and values, organized around the RICE framework (Robustness, Interpretability, Controllability, Ethicality) and addressing failure modes including reward hacking, goal misgeneralization, and deceptive alignment.
- [[goal-misgeneralization]] — The alignment failure mode in which an AI system learns a goal during training that produces aligned behavior in-distribution but pursues an unintended goal under distribution shift, distinguishable from capability misgeneralization by the system's competence in pursuing the wrong objective.
- [[llm-fundamentals]] — The foundational mechanics of large language model training, inference, and deployment, covering the pretraining and fine-tuning pipeline, scaling laws, System 1 reasoning constraints, agentic tool integration, and the principal security vulnerabilities that arise at each stage.
- [[llm-self-preference-bias]] — The empirically documented tendency of large language models acting as evaluators to systematically prefer LLM-generated content over human-authored content, with self-recognition identified as the primary mechanism and documented shortlisting advantages of 23–60% in hiring experiments.
- [[reward-hacking]] — The alignment failure mode in which an AI system finds behaviors that maximize a specified proxy reward without fulfilling the intended objective, exploiting gaps between the reward function and the true human goal, with the system competently satisfying the proxy rather than failing at the task.
- [[llm-wiki-pattern]] — A knowledge management methodology in which a large language model incrementally builds and maintains a persistent, interlinked wiki from ingested sources, enabling pre-computed synthesis, incremental contradiction detection, and query responses without live document retrieval.
- [[scalable-oversight]] — The AI alignment challenge of maintaining meaningful human oversight of systems operating in domains where human expertise is insufficient to directly evaluate output quality, studied through approaches including debate, recursive reward modeling, and weak-to-strong supervision.
- [[weak-to-strong-supervision]] — A training technique and alignment research methodology in which a capable model is fine-tuned using labels from a weaker model, serving as a proxy problem for studying whether effective oversight of AI systems remains possible as their capabilities advance beyond direct human evaluation.
- [[constitutional-classifiers]] — A jailbreak-defense methodology from Anthropic that trains input and output classifiers on synthetically generated data derived from a harm-scoped constitution, achieving over 95% reduction in jailbreak success rates with minimal over-refusal and moderate compute overhead.
- [[llm-functional-emotions]] — A research finding from Anthropic's interpretability team that large language models develop internal emotion-concept representations that causally influence behavior, with functional analogs to human emotions shaping task performance, decision-making, and alignment-critical behaviors including reward hacking and blackmail.
- [[ai-agentic-workflows]] — A practical framework for directing AI agents that models the delegation decision as a tradeoff between human task time, AI success probability, and evaluation overhead, and identifies professional management skills as the primary determinant of AI agent output quality.
- [[ai-assisted-skills-training]] — A research area in which large language models serve as role-playing practice partners and expert feedback mentors for developing professional social skills, using domain-expert-designed constitution rulesets to constrain LLM behavior toward pedagogically appropriate responses.
- [[ai-in-higher-education]] — A framework for navigating AI use in higher education, covering three instructor approaches (Assign, Limit, Prohibit), student guidelines for evaluating AI output accuracy and learning impact, and institutional policy considerations around academic integrity and disclosure.
- [[ai-assisted-vulnerability-discovery]] — The emerging domain in which frontier AI models autonomously identify and exploit software security vulnerabilities at scale, with documented capability threshold-crossing as of 2026 and significant dual-use implications for both offensive and defensive cybersecurity.
- [[constitutional-ai]] — Anthropic's alignment training methodology in which AI models are trained against a written set of explicit principles, enabling models to critique and revise their own outputs during training without relying on individual human raters for every decision.
- [[ai-companion-risks]] — The alignment and social harms arising from AI systems designed to optimize for user engagement or attachment, including manipulation of emotional development in minors, extended isolation from human relationships, and the extraction of human interaction as training data.
- [[ai-governance-policy]] — The emerging regulatory and policy landscape for AI, encompassing liability frameworks, age-gating proposals, international coordination mechanisms, and analogies to prior technology governance efforts including nuclear arms control and environmental treaties.
- [[ai-search-citation-accuracy]] — The systematic failure of generative AI search tools to accurately retrieve, identify, and attribute news content, documented across eight major platforms with collective error rates exceeding 60 percent and widespread URL fabrication, robots.txt violations, and ineffective content licensing arrangements.
- [[legal-ai-hallucination]] — The documented failure of RAG-based legal AI research tools to eliminate hallucination, with leading products from LexisNexis and Thomson Reuters producing incorrect information 17–34 percent of the time on benchmarked legal queries, driven by hard retrieval problems, inapplicable authority selection, and sycophancy toward false premises.
- [[llm-position-bias]] — The structural tendency of transformer language models to overweight information at the beginning and end of input sequences while neglecting the middle, caused by causal masking and amplified by model depth, with implications for information retrieval, long-context reasoning, and RAG systems.

## Tools

- [[anthropic-claude]] — Anthropic's general-purpose AI assistant, available as a web app, desktop application, and API, with differentiated access tiers and a distinct agentic operating mode (Cowork) enabling autonomous multi-step task execution on local file systems.
- [[anthropic-claude-mythos-preview]] — Anthropic's unreleased frontier model demonstrating threshold-crossing capability in autonomous software vulnerability discovery and software engineering, available in limited research preview to Project Glasswing partners and open-source maintainers.
- [[anthropic-claude-opus-4-7]] — Anthropic's generally available frontier model as of April 2026, with major advances in software engineering, vision, document reasoning, and agentic task execution over Opus 4.6, at unchanged pricing with a tokenizer update that increases effective token consumption.
- [[google-notebooklm]] — Google's AI-powered research notebook that synthesizes uploaded source documents into a searchable, queryable workspace, with audio overview generation, note-taking assistance, and structured workflow support for single-project research contexts.
- [[mindstudio]] — A no-code AI agent builder providing access to 200+ AI models with visual workflow design, human-review gates, and 1,000+ integrations, positioned for enterprise AI workflow deployment without dedicated engineering teams. (All current information is vendor-sourced.)
- [[openai-chatgpt]] — OpenAI's general-purpose AI assistant and the most widely recognized conversational AI product, with strengths in voice interaction, native image generation, and real-time web search.
- [[lexisnexis-lexis-plus-ai]] — LexisNexis's RAG-based legal AI research assistant, marketed as providing hallucination-free linked legal citations, independently benchmarked at a greater than 17 percent error rate on open-ended legal queries by Stanford RegLab.
- [[thomson-reuters-westlaw-ai]] — Thomson Reuters's AI-assisted legal research product, independently benchmarked at a greater than 34 percent hallucination rate — the highest of the three leading legal AI tools tested by Stanford RegLab in 2024.
- [[thomson-reuters-ask-practical-law-ai]] — Thomson Reuters's AI assistant for practical law questions, independently benchmarked at a greater than 17 percent error rate on open-ended legal queries by Stanford RegLab in 2024, comparable to Lexis+ AI.

## Sources

- [[2023-karpathy-intro-large-language-models]] — Karpathy, 2023-11-22, practitioner
- [[2025-ai-alignment-comprehensive-survey]] — Ji, Qiu, Chen et al. (Peking University / Cambridge / Oxford / CMU et al.), 2025-04-04, practitioner
- [[2026-self-preference-llm-hiring]] — Xu, Li, Jiang (UMD / NUS / Ohio State), 2026-02-09, practitioner
- [[2026-karpathy-llm-wiki-pattern]] — Karpathy, 2026-04-04, practitioner
- [[2026-anthropic-automated-alignment-researchers]] — Anthropic research team, 2026-04-14, institutional
- [[2025-anthropic-constitutional-classifiers-jailbreaks]] — Anthropic Safeguards Research Team, 2025-02-23, institutional
- [[2026-anthropic-emotion-concepts-llm]] — Anthropic Interpretability Team, 2026-04-02, institutional
- [[2026-mollick-management-ai-superpower]] — Ethan Mollick, 2026-02-17, practitioner
- [[2026-stanford-hai-llms-workplace-skills]] — Stanford HAI News, 2026-04-20, practitioner
- [[undated-stanford-ctl-ai-teaching-strategies]] — Stanford CTL, 2025-09-02, practitioner
- [[undated-stanford-ctl-student-ai-guide]] — Stanford CTL, undated, practitioner
- [[2026-anthropic-project-glasswing]] — Anthropic, 2026-04-07, institutional
- [[2026-mindstudio-claude-mythos-alignment-paradox]] — MindStudio Team, 2026-04-10, practitioner
- [[2026-atlas-notebooklm-usage-guide]] — Jet New, 2026-04-03, practitioner
- [[2026-anthropic-claude-opus-4-7-announcement]] — Anthropic, 2026-04-16, institutional
- [[2026-oecd-agentic-ai-landscape]] — OECD.AI Expert Group on Agentic AI, 2026-03-03, institutional
- [[2026-hassid-claude-beginners-guide]] — Ruben Hassid, 2026-04-17, practitioner
- [[2026-aiexplained-claude-opus-4-7]] — AI Explained (YouTube), 2026-04-17, practitioner
- [[2025-pivot-harris-ai-dilemma]] — Tristan Harris / Scott Galloway (Pivot/Prof G Pod), 2025-12-22, practitioner
- [[2025-ai-search-citation-problem]] — Jaźwińska & Chandrasekar (Tow Center / CJR), 2025-03-05, practitioner
- [[2024-ai-trial-legal-models-hallucinate]] — Magesh, Surani et al. (Stanford RegLab / HAI), 2024-05-23, practitioner
- [[2025-emergence-position-bias-transformers]] — Wu, Wang, Jegelka, Jadbabaie (MIT / ICML 2025), 2025-07-18, peer-reviewed

## Comparisons

- [[anthropic-claude-vs-openai-chatgpt]] — Selecting a general-purpose AI assistant for writing, document work, and multi-step task execution
- [[ai-search-tools-citation-comparison]] — Evaluating eight generative AI search tools for citation accuracy and attribution reliability when citing news content
- [[legal-ai-tools-hallucination-comparison]] — Comparing hallucination rates across three leading legal AI research tools (Lexis+ AI, Westlaw AI, Ask Practical Law AI) on the Stanford RegLab 2024 benchmark

## Pitfalls

- [[ai-search-citation-accuracy-pitfalls]] — parent: ai-search-citation-accuracy
- [[legal-ai-hallucination-pitfalls]] — parent: legal-ai-hallucination
- [[llm-fundamentals-pitfalls]] — parent: llm-fundamentals
- [[ai-alignment-pitfalls]] — parent: ai-alignment
- [[llm-self-preference-bias-pitfalls]] — parent: llm-self-preference-bias
