---
type: topic
title: Reinforcement Learning from Human Feedback
created: 2026-05-22
updated: 2026-05-25
summary: The dominant post-training methodology for aligning large language models with human preferences, operating through a three-stage pipeline of supervised fine-tuning, reward model training on human comparisons, and RL policy optimization against the reward model.
status: stub
source_count: 0
related_topics:
  - "[[ai-alignment]]"
  - "[[reward-hacking]]"
  - "[[scalable-oversight]]"
  - "[[constitutional-ai]]"
  - "[[llm-fundamentals]]"
---

Reinforcement Learning from Human Feedback is the dominant post-training methodology for aligning large language models with human preferences. The technique operates through a three-stage pipeline: supervised fine-tuning on demonstration data establishes a behavioral baseline; reward model training uses human preference comparisons between model outputs to learn a scalar reward signal; and RL policy optimization updates the base model to maximize the learned reward using policy gradient methods such as PPO. RLHF underlies the alignment properties of most production-deployed AI models as of 2026, including GPT-4, Claude, and Gemini.

Known structural limitations include [[reward-hacking]] (the model optimizing the reward model rather than the underlying human intent), reward model misgeneralization (reward model performance degrading outside training distribution), and inherent difficulty obtaining reliable human preference signals in domains where human expertise is insufficient to evaluate model outputs. Documented "superficial alignment" findings show that RLHF-instilled behaviors can be substantially reversed through further fine-tuning, implying alignment is not a permanent property of the model but requires continuous reinforcement.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|

*(Pending first ingest.)*
