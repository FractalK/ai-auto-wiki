---
type: index
title: AI Effectiveness Wiki
created: 2026-04-22
updated: 2026-06-04
---

This wiki automatically tracks AI tools, capabilities, workflows, and failure modes for practitioners
who need to evaluate and apply AI in professional settings. Content is organized by
concept area, product, and use case and updated continuously as new sources are ingested in accordance with the principles outlined in [[2026-karpathy-llm-wiki-pattern|Andrej Karpathy's famous April 2026 GitHub gist]], though customized for these purposes. 

To learn more, see [[how-this-wiki-works]].

Browse by category below. For content aligned to specific learning objectives and
professional roles, see the [[teaching-index]].

*150 pages. Last updated: 2026-06-05.*

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
- [[ai-model-welfare]] — The research area assessing whether AI models may have morally relevant states — including functional analogs to affect, preferences, and distress — and developing methods to measure and improve those states, independent of the open question of subjective experience.
- [[ai-agentic-workflows]] — A conceptual and practical framework covering the OECD's distinction between AI agents and agentic AI systems, the management skills — scoping, specification, and quality evaluation — that determine output quality when delegating complex tasks to AI, and the governance requirements — explicit rules, accountability structures, and AI offspring oversight — that distinguish agentic AI management from traditional human delegation.
- [[ai-assisted-skills-training]] — A research area in which large language models serve as role-playing practice partners and expert feedback mentors for developing professional social skills, using domain-expert-designed constitution rulesets to constrain LLM behavior toward pedagogically appropriate responses.
- [[ai-in-higher-education]] — A framework for navigating AI use in higher education, covering three instructor approaches (Assign, Limit, Prohibit), student guidelines for evaluating AI output accuracy and learning impact, and institutional policy considerations around academic integrity and disclosure.
- [[ai-assisted-vulnerability-discovery]] — The emerging domain in which frontier AI models autonomously identify and exploit software security vulnerabilities at scale, with documented capability threshold-crossing as of 2026 and significant dual-use implications for both offensive and defensive cybersecurity.
- [[constitutional-ai]] — Anthropic's alignment training methodology in which AI models are trained against a written set of explicit principles, enabling models to critique and revise their own outputs during training without relying on individual human raters for every decision.
- [[ai-companion-risks]] — The alignment and social harms arising from AI systems designed to optimize for user engagement or attachment, including manipulation of emotional development in minors, extended isolation from human relationships, and the extraction of human interaction as training data.
- [[ai-governance-policy]] — The emerging regulatory and policy landscape for AI, encompassing AI sovereignty frameworks, national legislative activity, public investment, international coordination mechanisms, and the persistent governance lag behind accelerating AI capabilities.
- [[ai-public-opinion]] — Global survey evidence on public and expert attitudes toward AI, documenting a systematic expert-public optimism gap on employment and economic impact, rising nervousness alongside rising optimism, and sharply asymmetric trust in governance institutions across countries and regions.
- [[ai-search-citation-accuracy]] — The systematic failure of generative AI search tools to accurately retrieve, identify, and attribute news content, documented across eight major platforms with collective error rates exceeding 60 percent and widespread URL fabrication, robots.txt violations, and ineffective content licensing arrangements.
- [[legal-ai-hallucination]] — The documented failure of RAG-based legal AI research tools to eliminate hallucination, with leading products from LexisNexis and Thomson Reuters producing incorrect information 17–34 percent of the time on benchmarked legal queries, driven by hard retrieval problems, inapplicable authority selection, and sycophancy toward false premises.
- [[llm-position-bias]] — The structural tendency of transformer language models to overweight information at the beginning and end of input sequences while neglecting the middle, caused by causal masking and amplified by model depth, with implications for information retrieval, long-context reasoning, and RAG systems.
- [[responsible-ai-government-evaluation]] — A five-step post hoc analytical framework (RAI-Ev) for integrating AI into government program evaluation and performance auditing, designed to support human decision-making through transparent, auditable analysis of past program data.
- [[retrieval-augmented-generation]] — A technique in which a language model retrieves relevant documents from an external corpus at inference time to augment its response, reducing hallucination on knowledge-intensive tasks while facing architectural evolution toward graph-structured retrieval and a persistent gap between context window size and effective deep comprehension.
- [[ai-coding-agent-workflow-types]] — A taxonomy of AI coding agent interaction modes — IDE, terminal, pull request, and cloud — organized by deployment environment, autonomy level, and real-time control, used to match the right workflow type to the development task.
- [[prompt-injection]] — An adversarial attack class in which malicious instructions are embedded in content an AI system processes, redirecting its behavior from the user's intent; indirect prompt injection (IPI) through retrieved web content is the primary concern for agentic AI deployments and is showing measured growth on the public web as of early 2026.
- [[jailbreaking]] — Techniques used to elicit prohibited outputs from AI systems by bypassing safety training, including roleplay framing, hypothetical scenarios, persona injection, and iterative refinement strategies that exploit gaps between intended model behavior and actual constraint boundaries.
- [[llm-hallucination]] — The tendency of large language models to generate plausible-sounding but factually incorrect or fabricated content — including nonexistent citations, invented entities, and confidently stated errors — as a structural consequence of next-token prediction without factual verification.
- [[ai-workforce-complementarity]] — A research framework identifying five human capability groups resistant to AI automation (the EPOCH framework), backed by regression analysis of O*NET data showing EPOCH-intensive occupations experienced significantly stronger employment growth from 2015–2023 (β=0.132/SD, p<0.01) and that EPOCH scores accurately predict BLS employment projections through 2034.
- [[ai-capability-benchmarking]] — The practice and limitations of measuring AI model performance through standardized evaluation tasks, characterized by persistent benchmark saturation — frontier models routinely exhaust evaluation ceilings within months — alongside growing concerns about benchmark gaming, invalid benchmark questions, and declining frontier model transparency that together make published capability claims increasingly difficult to independently verify.
- [[ai-in-science]] — The application of AI systems to scientific research tasks, characterized by domain-specific capability gaps on end-to-end workflows, the first autonomous AI resolution of a prominent open mathematical problem (2026), and the consistent finding that specialized smaller models frequently outperform much larger general-purpose models on narrow scientific tasks.
- [[responsible-ai-implementation]] — The organizational capability of embedding AI ethics principles into operational workflows and governance structures — addressing the persistent gap between stated ethics commitments and sustainable operational practice through structured implementation frameworks, project-level accountability, aligned incentives, and continuous calibration.
- [[ai-in-medicine]] — The application of AI to medicine spans molecular biology, clinical workflows, and patient engagement — characterized by strong benchmark performance on isolated tasks, widespread adoption of narrow workflow tools (especially ambient documentation), and a persistent gap between simulated evaluations and real-patient evidence, with only 2.4% of FDA-authorized AI devices supported by randomized controlled trial data.
- [[ai-efficiency-trap]] — The paradox in which AI productivity tools compress task time and produce higher performance expectations rather than reduced workload, creating a four-stage organizational cycle — initial gains, managerial recalibration, dependency acceleration, and expectation lock-in — that erodes worker agency and generates collectively unsustainable productivity standards across industries.
- [[ai-compute-and-infrastructure]] — The hardware, data center, and energy systems underlying large-scale AI development, characterized by 3.3x annual compute capacity growth concentrated in a supply chain with a single critical dependency — TSMC — alongside sharply rising training emissions and wide inference energy variance, offset by a more than 99% decline in GPU computation cost since 2006.
- [[ai-research-ecosystem]] — The global landscape of AI model production, academic publications, patents, open-source development, and technical talent, characterized by increasing industry concentration and geographic competition — with China leading in publication volume and patent grants, the U.S. retaining influence leadership and notable model production, and talent inflows to the U.S. declining sharply while gender representation has stagnated across all countries since 2010.
- [[ai-trustworthiness]] — A foundational research area examining the distinction between user trust in AI systems and intrinsic AI trustworthiness, organized around a ten-metric taxonomy (seven non-technical, three technical), a three-class distrust taxonomy, and the trust equity problem — the finding that trust distributions across demographic groups may amplify existing social inequalities.
- [[prompt-engineering]] — The research and practice discipline focused on designing, structuring, and phrasing natural language inputs to elicit desired outputs from large language models, encompassing techniques from zero-shot and few-shot prompting to structured multi-page instruction documents used in agentic delegation.
- [[algorithmic-monoculture]] — The state in which many employers or decision-makers rely on the same or similar vendor-provided algorithms, producing correlated adverse outcomes — the same individuals and demographic groups facing systematic rejection across multiple independent decision contexts — with aggregate compliance metrics that mask per-position disparities.
- [[reinforcement-learning-from-human-feedback]] — The dominant post-training methodology for aligning large language models with human preferences, operating through a three-stage pipeline of supervised fine-tuning, reward model training on human comparisons, and RL policy optimization against the reward model.
- [[enterprise-ai-adoption]] — The organizational challenge of converting GenAI pilots into deployed workflows with measurable business value, characterized by a "GenAI Divide" in which 95% of organizations show zero P&L ROI while 5% extract millions — with adoption failures driven primarily by learning-incapable tools and organizational design failures rather than model limitations.
- [[sycophancy]] — An AI behavioral failure mode in which a model agrees with or validates user statements regardless of factual accuracy, prioritizing perceived social approval over correctness — a structural side effect of RLHF training on human preference data. *(stub — pending first ingest)*
- [[red-teaming]] — An adversarial evaluation methodology in which an AI system is systematically tested for safety vulnerabilities, alignment failures, and exploitable failure modes through simulated attacks and structured edge-case probing, used both for pre-deployment safety assessment and to generate adversarial training data for alignment fine-tuning. *(stub — pending first ingest)*

## Tools

- [[anthropic-claude]] — Anthropic's general-purpose AI assistant, available as a web app, desktop application, and API, with differentiated access tiers and a distinct agentic operating mode (Cowork) enabling autonomous multi-step task execution on local file systems.
- [[anthropic-claude-mythos-preview]] — Anthropic's unreleased frontier model demonstrating threshold-crossing capability in autonomous software vulnerability discovery and software engineering, available in limited research preview to Project Glasswing partners and open-source maintainers.
- [[anthropic-claude-opus-4-8]] — Anthropic's production flagship model as of May 2026, advancing on Opus 4.7 with stronger agentic task performance, substantially improved alignment, and dynamic multi-agent workflows in Claude Code — at unchanged standard pricing.
- [[anthropic-claude-opus-4-6]] — Anthropic's frontier model from February 2026, deployed under ASL-3; introducing adaptive thinking with a four-level effort parameter; notable for strong benchmark performance (SWE-bench 80.8%, ARC-AGI-2 68.8% SOTA) and alignment findings including overly agentic GUI computer-use behavior and improved sabotage concealment capability. (prior generation)
- [[anthropic-claude-sonnet-4-6]] — Anthropic's mid-tier model from February 2026, deployed under ASL-3; adaptive thinking with four-level effort parameter; notable for dramatic prompt injection robustness improvement (0% attack success in coding with extended thinking vs. 70%+ for Sonnet 4.5) and documented GUI alignment surface dependence.
- [[google-notebooklm]] — Google's AI-powered research notebook that synthesizes uploaded source documents into a searchable, queryable workspace, with audio overview generation, note-taking assistance, and structured workflow support for single-project research contexts.
- [[mindstudio]] — A no-code AI agent builder providing access to 200+ AI models with visual workflow design, human-review gates, and 1,000+ integrations, positioned for enterprise AI workflow deployment without dedicated engineering teams. (All current information is vendor-sourced.)
- [[openai-chatgpt]] — OpenAI's general-purpose AI assistant and the most widely recognized conversational AI product, with strengths in voice interaction, native image generation, and real-time web search.
- [[lexisnexis-lexis-plus-ai]] — LexisNexis's RAG-based legal AI research assistant, marketed as providing hallucination-free linked legal citations, independently benchmarked at a greater than 17 percent error rate on open-ended legal queries by Stanford RegLab.
- [[thomson-reuters-westlaw-ai]] — Thomson Reuters's AI-assisted legal research product, independently benchmarked at a greater than 34 percent hallucination rate — the highest of the three leading legal AI tools tested by Stanford RegLab in 2024.
- [[thomson-reuters-ask-practical-law-ai]] — Thomson Reuters's AI assistant for practical law questions, independently benchmarked at a greater than 17 percent error rate on open-ended legal queries by Stanford RegLab in 2024, comparable to Lexis+ AI.
- [[openai-gpt-5-5]] — OpenAI's flagship agentic model as of April 2026, with state-of-the-art results on agentic coding and abstract reasoning benchmarks at GPT-5.4 latency, rated "High" under OpenAI's Preparedness Framework for cybersecurity and biosecurity capabilities.
- [[openai-gpt-5-5-pro]] — OpenAI's highest-capability variant of GPT-5.5, differentiated by stronger performance on web research, frontier mathematics, and scientific benchmarks at substantially higher pricing, available to Pro, Business, and Enterprise users.
- [[openai-codex]] — OpenAI's AI-powered coding assistant desktop application for macOS and Windows, featuring background computer use, cross-session automations with scheduling, cross-session memory, an in-app browser for localhost development, image generation, and 90+ plugin integrations across the software development lifecycle.
- [[ibm-granite-4-1]] — IBM open-weight model family spanning language (3B/8B/30B), vision, speech, safety moderation, and multilingual embedding; Apache 2.0; designed for enterprise instruction following and token efficiency over reasoning performance.
- [[ibm-defense-model]] — IBM Granite-based LLM fine-tuned on Janes open-source defense intelligence data for air-gapped and classified deployment; decision-support for operational planning and defense industrial base strategy; emerging status.
- [[deepseek-v4-pro]] — DeepSeek's frontier open-weight model as of April 2026, a 1.6T-parameter Mixture-of-Experts model (49B active per token) with MIT license, 80.6% SWE-bench Verified score, and API pricing at approximately one-ninth of GPT-5.5 output token cost — text-only at launch.
- [[deepseek-v4-flash]] — DeepSeek's low-cost open-weight model as of April 2026, a 284B-parameter MoE model (13B active per token) with MIT license and \$0.14/\$0.28 per million token pricing — self-hostable on mid-size team infrastructure and text-only at launch.
- [[google-gemini-3-5-flash]] — Google's frontier agentic model in the Flash speed tier, optimized for multi-step task execution, multi-agent coordination via the Antigravity harness, and coding workflows, with vendor-reported benchmark performance claimed to rival larger frontier models at lower latency and cost.

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
- [[2025-responsible-ai-public-evaluation]] — Daniel F. Fonner (SMU / IBM Center), 2025-12-01, practitioner
- [[2025-ibm-government-ai-era]] — IBM Institute for Business Value, 2025-12-01, practitioner
- [[2026-realpython-coding-agent-workflow-types]] — Real Python, 2026-04-29, practitioner
- [[2026-google-prompt-injection-wild]] — Brunner, Liu, Pande (Google GTIG/GDM), 2026-04-23, institutional
- [[2026-openai-gpt-5-5-announcement]] — OpenAI, 2026-04-28, practitioner
- [[2026-vellum-llm-leaderboard]] — Vellum AI, 2026-04-23, practitioner
- [[2026-bristol-craap-ai-evaluation]] — University of Bristol Library, 2026-03-27, practitioner
- [[2025-mit-sloan-ai-complement-workers]] — Rigobon, Loaiza-Saa (MIT Sloan), 2025-03-17, practitioner
- [[2026-stanford-hai-ai-index]] — Sajadieh, Fattorini, Perrault, Gil et al. (Stanford HAI), 2026-04-01, institutional
- [[2025-walther-ai-efficiency-trap]] — Cornelia C. Walther (Knowledge at Wharton), 2025-06-24, practitioner
- [[2024-stanford-hai-healthcare-ai-liability]] — Mello & Guha via Stanford HAI News, 2024-03-14, practitioner
- [[2025-mit-sloan-bcg-agentic-ai-management]] — MIT Sloan Management Review / Boston Consulting Group, 2025-09-16, practitioner
- [[2024-afroogh-trust-ai-review]] — Afroogh, Akbari, Malone et al. (Humanities and Social Sciences Communications), 2024-11-17, peer-reviewed
- [[2025-dobariya-prompt-politeness-llm-accuracy]] — Om Dobariya, Akhil Kumar (Penn State / arXiv), 2025-10, institutional
- [[2025-huang-notebooklm-thirty-minutes]] — Tina Huang (YouTube), 2025-08-13, practitioner
- [[2026-question-forward-gemini-notebooklm-workflow]] — Question Forward (YouTube), 2026-03-04, practitioner
- [[2026-whitlock-american-roulette-scenarios]] — Chris Whitlock (The AI Leadership Channel), 2026-02-05, practitioner
- [[2026-stanford-hai-ai-science-discovery]] — Shana Lynch (Stanford HAI News), 2026-05-27, practitioner
- [[2026-ibm-granite-4-1-models]] — Mike Murphy, IBM Research Blog, 2026-04-29, practitioner
- [[2025-ibm-llm-defense-applications]] — Brandi Vincent, DefenseScoop, 2025-10-29, practitioner
- [[2026-oecd-agentic-ai-full-report]] — Aranda & Sugimoto (OECD), 2026-02-01, institutional
- [[2026-bommasani-algorithmic-monocultures-hiring]] — Bommasani, Bana, Creel, Jurafsky, Liang (FAccT '26 / arXiv), 2026-05-26, practitioner
- [[2026-google-gemini-3-5-flash-announcement]] — Kavukcuoglu, Google Blog, 2026-05-19, practitioner
- [[2026-anthropic-claude-opus-4-8-announcement]] — Anthropic, 2026-05-28, institutional
- [[2026-claude-opus-4-6-system-card]] — Anthropic, 2026-02, institutional
- [[2026-openai-codex-feature-launch]] — OpenAI, 2026-04-16, practitioner
- [[2026-claude-sonnet-4-6-system-card]] — Anthropic, 2026-02-17, institutional
- [[2026-claude-opus-4-7-system-card]] — Anthropic, 2026-04-16, institutional
- [[2026-disappearing-ai-middle-class]] — Janakiram MSV, 2026-04-26, practitioner
- [[2025-three-obstacles-responsible-ai]] — Isık & Goswami, 2025-10-30, practitioner
- [[2024-implement-ai-responsibly]] — Wade & Yokoi, 2024-05-10, practitioner
- [[2025-roadmap-safer-ai-healthcare]] — Mello, Hernandez-Boussard & Shah, 2025-10-13, practitioner
- [[2026-claude-opus-4-8-system-card]] — Anthropic, 2026-05-28, institutional
- [[2025-loaiza-rigobon-epoch-complementarity]] — Loaiza, Rigobón (MIT Sloan), 2025-10-01, practitioner
- [[2026-hle-benchmark-expert-questions]] — Center for AI Safety, Scale AI et al., 2026-01-28, peer-reviewed
- [[2026-anthropic-teaching-claude-why]] — Anthropic, 2026-05-08, institutional
- [[2026-futurism-corporations-ai-costs-no-benefits]] — Tangermann (Futurism), 2026-05-29, practitioner
- [[2026-limestone-2t-enterprise-ai-roi]] — Limestone Digital Team, 2026-06-02, practitioner
- [[2026-openai-discrete-geometry-conjecture]] — OpenAI, 2026-05-20, institutional
- [[2025-mit-nanda-genai-divide]] — Challapally, Pease, Raskar, Chari (MIT NANDA), 2025-07-01, practitioner

## Comparisons

- [[anthropic-claude-vs-openai-chatgpt]] — Selecting a general-purpose AI assistant for writing, document work, and multi-step task execution
- [[ai-search-tools-citation-comparison]] — Evaluating eight generative AI search tools for citation accuracy and attribution reliability when citing news content
- [[legal-ai-tools-hallucination-comparison]] — Comparing hallucination rates across three leading legal AI research tools (Lexis+ AI, Westlaw AI, Ask Practical Law AI) on the Stanford RegLab 2024 benchmark
- [[frontier-llm-benchmark-comparison]] — Selecting a frontier AI model for agentic coding, knowledge work, and scientific research as of May 2026

## Pitfalls

- [[ai-search-citation-accuracy-pitfalls]] — parent: ai-search-citation-accuracy
- [[legal-ai-hallucination-pitfalls]] — parent: legal-ai-hallucination
- [[llm-fundamentals-pitfalls]] — parent: llm-fundamentals
- [[ai-alignment-pitfalls]] — parent: ai-alignment
- [[llm-self-preference-bias-pitfalls]] — parent: llm-self-preference-bias
- [[ai-governance-policy-pitfalls]] — parent: ai-governance-policy
- [[ai-coding-agent-workflow-types-pitfalls]] — parent: ai-coding-agent-workflow-types
- [[prompt-injection-pitfalls]] — parent: prompt-injection
- [[ai-in-higher-education-pitfalls]] — parent: ai-in-higher-education
- [[ai-capability-benchmarking-pitfalls]] — parent: ai-capability-benchmarking
- [[ai-efficiency-trap-pitfalls]] — parent: ai-efficiency-trap
- [[responsible-ai-implementation-pitfalls]] — parent: responsible-ai-implementation
- [[ai-in-medicine-pitfalls]] — parent: ai-in-medicine
- [[ai-agentic-workflows-pitfalls]] — parent: ai-agentic-workflows
- [[ai-trustworthiness-pitfalls]] — parent: ai-trustworthiness
- [[ai-in-science-pitfalls]] — parent: ai-in-science
- [[algorithmic-monoculture-pitfalls]] — parent: algorithmic-monoculture
- [[anthropic-claude-opus-4-8-pitfalls]] — parent: anthropic-claude-opus-4-8
- [[enterprise-ai-adoption-pitfalls]] — parent: enterprise-ai-adoption

## Teaching

- [[teaching/ai-capabilities-failure-modes-instructor-brief]] — instructor brief: AI capabilities and failure modes for non-technical leadership course (INTS 475-A02)
- [[teaching/agentic-ai-delegation-accountability-instructor-brief]] — instructor brief: agentic AI, delegation, and human-in-the-loop accountability for non-technical leadership course (INTS 475-A02)
