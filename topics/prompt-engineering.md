---
type: topic
title: Prompt Engineering
created: 2026-05-26
updated: 2026-05-26
summary: The research and practice discipline focused on designing, structuring, and phrasing natural language inputs to elicit desired outputs from large language models, encompassing techniques from zero-shot and few-shot prompting to structured multi-page instruction documents used in agentic delegation.
status: developing
source_count: 1
last_assessed: 2026-05-26
related_topics:
  - "[[llm-fundamentals]]"
  - "[[ai-agentic-workflows]]"
technical_depth: practitioner
---

Prompt engineering is the study and practice of designing inputs to large language models (LLMs) to optimize response quality. Because LLMs are accessed through a natural language interface, even minor differences in prompt phrasing — structure, style, length, politeness level, or whether examples are included — can produce measurably different outputs. The field encompasses techniques ranging from zero-shot prompting (no examples provided) and few-shot prompting (task examples included in the prompt) to structured multi-page instruction documents used in agentic workflows. As AI agents are increasingly tasked with complex, multi-step work, prompt engineering has expanded from single-turn query optimization to designing delegation frameworks that specify goals, scope, and evaluation criteria across extended interactions.

## Tone and Politeness Effects

One examined dimension of prompt variation is politeness level. Prior research on GPT-3.5 and Llama2-70B (Yin et al. 2024) found that impolite prompts tend to hurt performance while overly polite phrasing does not guarantee better outcomes. A 2025 study by Dobariya and Kumar at Penn State found the opposite pattern on ChatGPT-4o: very rude prompts (84.8% accuracy) outperformed very polite prompts (80.8%) on a 50-question MCQ benchmark across mathematics, science, and history, with all politeness–rudeness pairings statistically significant by paired t-tests (p < 0.05). This reversal suggests that RLHF updates in newer models alter how tone-inflected phrasing is processed, though the causal mechanism is not yet established. Candidate explanations include prompt perplexity effects and length variation, but whether the emotional payload of politeness cues affects the model independently of these factors remains unknown.

Despite finding higher accuracy with rude prompts in their experimental setting, the authors explicitly do not recommend adopting hostile phrasing in real-world applications, citing negative effects on user experience, accessibility, and the risk of normalizing harmful communication norms. This tension between experimentally demonstrable performance gains and deployment ethics illustrates a broader challenge in prompt engineering research: technique-level findings must be evaluated against system-level consequences before being applied in practice.

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| ChatGPT-4o MCQ accuracy — very polite tone | 80.8% | 50 MCQ questions (math/science/history); 10 runs; ChatGPT-4o API; range [80, 82]% | 2025-10 | [[2025-dobariya-prompt-politeness-llm-accuracy]] | current |
| ChatGPT-4o MCQ accuracy — polite tone | 81.4% | 50 MCQ questions; 10 runs; ChatGPT-4o API; range [80, 82]% | 2025-10 | [[2025-dobariya-prompt-politeness-llm-accuracy]] | current |
| ChatGPT-4o MCQ accuracy — neutral tone | 82.2% | 50 MCQ questions; 10 runs; ChatGPT-4o API; range [82, 84]% | 2025-10 | [[2025-dobariya-prompt-politeness-llm-accuracy]] | current |
| ChatGPT-4o MCQ accuracy — rude tone | 82.8% | 50 MCQ questions; 10 runs; ChatGPT-4o API; range [82, 84]% | 2025-10 | [[2025-dobariya-prompt-politeness-llm-accuracy]] | current |
| ChatGPT-4o MCQ accuracy — very rude tone | 84.8% | 50 MCQ questions; 10 runs; ChatGPT-4o API; range [82, 86]% | 2025-10 | [[2025-dobariya-prompt-politeness-llm-accuracy]] | current |

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| On a 50-question MCQ benchmark across mathematics, science, and history, ChatGPT-4o achieved statistically significantly higher accuracy with very rude prompts (84.8%) than with very polite prompts (80.8%), with all politeness–rudeness pairings confirmed significant by paired t-tests (p < 0.05). | [[2025-dobariya-prompt-politeness-llm-accuracy]] | 2025-10 | current | 2 | false |
| The direction of the politeness–accuracy relationship appears to depend on model generation: older models (GPT-3.5, Llama2-70B) showed worse performance on rude prompts while ChatGPT-4o showed better performance on rude prompts, suggesting that RLHF updates in newer models alter how tone-inflected phrasing is processed. | [[2025-dobariya-prompt-politeness-llm-accuracy]] | 2025-10 | current | 2 | false |
| The mechanism by which prompt politeness affects LLM accuracy remains unresolved; candidate explanations include prompt perplexity effects and length variation, but whether the emotional payload of politeness cues matters to the model independently of these factors is unknown. | [[2025-dobariya-prompt-politeness-llm-accuracy]] | 2025-10 | current | 2 | false |
