---
type: pitfalls
title: AI in Science — Pitfalls
created: 2026-05-27
updated: 2026-05-27
parent_entity: "[[topics/ai-in-science]]"
parent_type: topic
status: current
failure_mode_count: 5
teaching_relevance: true
competency_domains:
  - output-verification-and-risk-assessment
  - capability-horizon-awareness
professional_contexts:
  - graduate-and-doctoral-education
  - teaching-and-instruction
contributing_sources:
  - "[[2026-stanford-hai-ai-science-discovery]]"
---

## Technical Limitations

### Catastrophic Forgetting of Extreme Events
**Status:** active<br>
**Source:** [[2026-stanford-hai-ai-science-discovery]]

AI climate and weather models learn to detect rare extreme events — hurricanes, atmospheric rivers, and other high-impact phenomena — early in the training process, then systematically forget this capability as training progresses and may never relearn it. Research by Elizabeth Barnes (Boston University) shows that specific network layers can be identified where this forgetting occurs, and that interventions during training may prevent it. The failure mode is especially dangerous because models perform well on in-distribution typical conditions while silently losing accuracy on the rare, high-stakes events that are most consequential for scientific inference and policy applications. A model that evaluates well on standard benchmarks may be systematically unreliable for the edge cases that matter most.

### End-to-End Research Workflow Gap
**Status:** active<br>
**Source:** [[2026-stanford-hai-ai-science-discovery]]

AI systems that perform impressively on isolated scientific subtasks fail substantially when required to execute the full, multistep research workflow that scientific discovery demands. Current frontier models answer complex research questions correctly on end-to-end benchmarks at roughly 30–40% accuracy, compared to 80%+ for PhD-level human experts. A 30% success rate on graduate-level quantum matter physics problems is documented by Eun-Ah Kim (Cornell University). The gap is not about model capability on individual steps — it reflects the compound failure rate of linking multiple uncertain inference steps, the difficulty of scientific judgment about which steps to take, and the inability to recognize when an intermediate result is wrong before building further on it.

## Usage Antipatterns

### AI Monoculture Effect
**Status:** active<br>
**Source:** [[2026-stanford-hai-ai-science-discovery]]

AI-assisted scientific papers receive approximately 300% more citations than non-AI-assisted papers in the same field, but they systematically cluster around the same large, well-structured datasets and predictable, pattern-consistent questions. The underlying mechanism, identified by James Evans (University of Chicago), is that AI excels at deductive science — filling in missing cells based on patterns already present in data — while human scientific breakthroughs characteristically require abductive science: making creative leaps when encountering surprising violations of expectations. When AI-assisted work is both easier to produce and more frequently cited, scientific incentives structurally disadvantage the surprising, expectation-violating observations that drive fundamental advances. Over time, entire fields risk converging on the same approaches and datasets, shrinking the diversity of scientific questions explored.

### Skill Atrophy in Scientific Training
**Status:** active<br>
**Source:** [[2026-stanford-hai-ai-science-discovery]]

As AI tools make it cheaper and faster to generate data than to collect it, and cheaper to use AI agents than to train doctoral students and postdoctoral researchers, institutions face structural pressure to reduce investment in the human training pipeline. But graduate students and postdoctoral researchers are not simply cheaper labor — they are the future practitioners of science, and their intellectual development through the experience of encountering, debugging, and understanding scientific problems cannot be optimized away without long-term cost to the discipline. The concern is not dramatic failure but gradual skill atrophy: scientists losing the "metaphorical muscle of actually doing things yourself" (Douglas Finkbeiner, Harvard), eroding the domain intuition needed to recognize when AI outputs are wrong, where the real scientific question lies, or when a surprising result is significant rather than artifactual.

### Peer Review Unsustainability
**Status:** active<br>
**Source:** [[2026-stanford-hai-ai-science-discovery]]

The peer review system was already burdened by modern scientific output volume before AI-generated research became prevalent. Journals report insufficient human reviewers to evaluate existing submission volumes. AI dramatically lowers the marginal cost of generating plausible-looking hypotheses and papers, threatening to increase submission volume to levels that make traditional peer review nonviable. As Benjamin Nachman (SLAC) observed at the 2026 Stanford HAI AI+Science conference: "Hypotheses are going to be cheap. There are going to be billions of these. Scientists are going to have to evolve." The failure mode is not that AI produces bad science directly, but that it floods the validation layer, making it structurally impossible for the community to maintain truth-vetting standards at scale.

## Alignment and Safety Concerns

### Bad Proxy Metrics Causing Real-World Harm
**Status:** active<br>
**Source:** [[2026-stanford-hai-ai-science-discovery]]

Scientific AI systems optimize for measurable proxies rather than the true scientific objective, and when those proxies are flawed, optimization at scale produces real-world harm. A documented example: a widely used healthcare algorithm used medical spending as a proxy for patient health need, systematically penalizing patients of color — who receive less healthcare spending at equivalent health status — and thereby directing care resources away from a population that needed them more. The alignment failure is not in the AI system per se but in the metric design: the system optimized precisely what it was told to optimize, and the designers failed to verify that the proxy captured the true objective. In scientific contexts, where AI systems increasingly drive experimental prioritization and resource allocation, this class of failure is consequential: bad proxy metrics can direct entire research programs toward artifacts rather than real phenomena.

## Teaching Notes

**What this failure mode teaches.** The failure modes in AI-assisted science share a common structure: AI systems optimize confidently and at scale for the measurable, the predictable, and the proximate — while the goals of science require attention to the rare, the surprising, and the ultimate. The AI monoculture effect illustrates how individually rational choices (use AI to maximize citations) aggregate into field-level harm (convergence on the same questions, loss of scientific diversity). This is an emergent failure: no single researcher makes a bad choice, yet the collective outcome is a narrower, more derivative science.

**Representative example.** James Evans (University of Chicago) documented that AI-assisted papers receive approximately 300% more citations than non-AI-assisted papers in the same field, but they systematically cluster around the same large, well-structured datasets and predictable questions. This creates a self-reinforcing cycle: AI-assisted work gets more citations, which draws more researchers toward AI-assisted work in the same mode, which further narrows the range of questions the field collectively explores. Scientific progress historically depends on abductive reasoning — encountering something surprising that violates expectations, then building a new hypothesis around that violation. If AI tools make deductive, pattern-consistent science far more productive than abductive, surprise-driven inquiry, structural incentives push fields away from the observations that generate fundamental advances. The failure is not that AI produces wrong answers; it is that AI systematically produces the right answers to the wrong questions.
