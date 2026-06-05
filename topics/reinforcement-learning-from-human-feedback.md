---
type: topic
title: Reinforcement Learning from Human Feedback
created: 2026-05-22
updated: 2026-06-04
summary: The dominant post-training methodology for aligning large language models with human preferences, operating through a three-stage pipeline of supervised fine-tuning, reward model training on human comparisons, and RL policy optimization against the reward model.
status: developing
source_count: 1
last_assessed: 2026-06-04
related_topics:
  - "[[ai-alignment]]"
  - "[[reward-hacking]]"
  - "[[scalable-oversight]]"
  - "[[constitutional-ai]]"
  - "[[llm-fundamentals]]"
---

Reinforcement Learning from Human Feedback is the dominant post-training methodology for aligning large language models with human preferences. The technique operates through a three-stage pipeline: supervised fine-tuning on demonstration data establishes a behavioral baseline; reward model training uses human preference comparisons between model outputs to learn a scalar reward signal; and RL policy optimization updates the base model to maximize the learned reward using policy gradient methods such as PPO. RLHF underlies the alignment properties of most production-deployed AI models as of 2026, including GPT-4, Claude, and Gemini.

Known structural limitations include [[reward-hacking]] (the model optimizing the reward model rather than the underlying human intent), reward model misgeneralization (reward model performance degrading outside training distribution), and inherent difficulty obtaining reliable human preference signals in domains where human expertise is insufficient to evaluate model outputs. Documented "superficial alignment" findings show that RLHF-instilled behaviors can be substantially reversed through further fine-tuning, implying alignment is not a permanent property of the model but requires continuous reinforcement.

Research by Anthropic demonstrates that augmenting RLHF with principle-based training data — constitutional documents and structured ethical reasoning datasets — achieves greater alignment generalization than demonstration-based fine-tuning alone while requiring substantially fewer training tokens. Training on the reasoning principles underlying aligned behavior, rather than on demonstrations of specific aligned outputs, produced a 28× token efficiency advantage in controlled comparison and generalized to out-of-distribution evaluation scenarios not represented in the training data.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Training on the principles underlying aligned behavior — such as constitutional documents and ethical reasoning datasets — achieves comparable alignment outcomes to demonstration-based RLHF approaches while requiring dramatically fewer training tokens (approximately 3M vs. 30–85M in Anthropic's controlled comparison), a 28× token efficiency advantage indicating that principled training generalizes across out-of-distribution scenarios more effectively than behavioral memorization. | [[2026-anthropic-teaching-claude-why]] | 2026-05-08 | current | 2 | false |
