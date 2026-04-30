---
type: topic
title: AI-Assisted Skills Training
created: 2026-04-22
updated: 2026-04-22
summary: A research area in which large language models serve as role-playing practice partners and expert feedback mentors for developing professional social skills, using domain-expert-designed constitution rulesets to constrain LLM behavior toward pedagogically appropriate responses.
status: developing
source_count: 1
last_assessed: 2026-04-22
teaching_relevance: true
competency_domains:
  - practical-ai-use-and-interaction
professional_contexts:
  - teaching-and-instruction
  - professional-and-continuing-education
  - non-profit-and-ngo-work
  - graduate-and-doctoral-education
technical_depth: practitioner
teaching_notes_reviewed: 2026-04-30
---

Using large language models to help professionals practice social and communication skills represents a distinct application pattern. Unlike productivity use cases where AI replaces or accelerates human work, AI-assisted skills training positions LLMs as practice partners and feedback mentors — tools that expand access to rehearsal opportunities without substituting for the human skills being developed. The core research question is whether LLM-based practice produces measurable improvement in real professional social skills. The early evidence suggests it does, but only when the practice system is carefully designed.

## The AP/AM Architecture

Research led by Diyi Yang at Stanford has developed an AI Partner / AI Mentor (AP/AM) dual-role framework. The AI Partner is a role-playing practice counterpart — designed to behave like a client, patient, or colleague presenting a specific scenario. The AI Mentor provides feedback after practice sessions, pointing out strengths and suggesting alternative approaches modeled on experienced supervisor guidance.

Three systems have been built using this framework, funded by the Stanford Institute for Human-Centered AI: Rehearsal (conflict resolution skills), a peer-counseling skills system, and CARE (novice therapy skills). Each targets a population that needs more rehearsal opportunities than its current training environment provides: novice therapists, counselors in community settings, and professionals navigating workplace conflict.

## The Constitution Problem

Out-of-the-box LLMs do not function as adequate practice partners. Default model behavior is too cooperative and forthcoming: they are sycophantic, over-disclose information immediately, and respond in ways that do not create opportunities to practice the intended skills. A conflict resolution practice partner that agrees with every proposed solution trains nothing useful. A therapy practice client who immediately discloses all concerns gives the novice therapist no opportunity to practice open-ended questioning.

The solution is domain-expert-designed constitution rulesets: structured sets of rules and criteria specifying how the practice partner should behave. For therapy skill training, example rules include "show initial skepticism about seeking help," "don't disclose too much at the start," and "be resistant about accepting suggested solutions." The model checks each of its responses against the full constitution before outputting, regenerating any response that violates the rules. This approach was developed collaboratively with domain experts in conflict resolution, psychotherapy, and motivational interviewing. Designing effective constitutions is currently the primary bottleneck for scaling to new practice domains.

## Mentor Quality

The AI Mentor component requires a fine-tuned model rather than a base instruction-tuned LLM. In the CARE system, therapist supervisors from the Stanford School of Medicine used an evidence-based communication framework to review and annotate emotional support conversation transcripts. The model was fine-tuned on those supervisors' critiques. To further reduce low-quality feedback, the team added a self-refinement step: the model generates multiple candidate feedback responses, selects the highest-scoring ones, and is further optimized on those choices. The resulting mentor gives feedback about strengths and areas for improvement and suggests alternative response approaches modeled on how experienced counselors advise novices.

## Empirical Results

A 90-person randomized controlled trial of CARE compared a practice-with-feedback group against a practice-without-feedback control group. Practice alone built confidence in both groups. Feedback was necessary for skill development: the feedback group showed increased empathy and client-centered responding, while the control group defaulted to solution-focused responses that reduced the client's opportunity to arrive at their own solutions. The finding that "practice matters for confidence, feedback matters for competence" is a central result of this line of research.

## Scope and Limitations

Current systems are not designed to replace peer practice or human supervision — they expand access to between-session rehearsal and scalable feedback, particularly for under-resourced organizations such as nonprofits, peer-counseling programs, and community mental health centers where training is limited. Personalization remains an unsolved challenge: practice difficulty needs calibration to individual skill levels, and current systems do not adapt dynamically to user progression. Building a new practice domain requires substantial expert involvement, making rapid scaling to new use cases difficult.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| In a 90-person randomized controlled trial of the CARE system, LLM practice with feedback increased empathy and client-centered responding, while practice without feedback increased solution-focused responses that reduced client-directed problem-solving opportunities. | [[2026-stanford-hai-llms-workplace-skills]] | 2026-04-20 | current | 1 | false |
| Out-of-the-box LLMs do not function as adequate social skills practice partners: default behaviors including sycophancy, over-disclosure, and excessive cooperativeness must be overridden through domain-expert-designed constitution rulesets to create pedagogically appropriate practice scenarios. | [[2026-stanford-hai-llms-workplace-skills]] | 2026-04-20 | current | 1 | false |
| Stanford's AP/AM dual-role architecture has produced three working social skills practice systems (Rehearsal for conflict resolution, a peer-counseling system, and CARE for novice therapy skills), each requiring domain expert co-design and validated against a distinct professional training context. | [[2026-stanford-hai-llms-workplace-skills]] | 2026-04-20 | current | 1 | false |
| CARE's AI Mentor quality was improved by having the model generate multiple candidate feedback responses, selecting highest-scoring options, and further optimizing on those choices — a self-refinement step required to reduce the rate of low-quality feedback. | [[2026-stanford-hai-llms-workplace-skills]] | 2026-04-20 | current | 1 | false |

## Teaching Notes

**Concept in plain terms.** AI-assisted skills training uses large language models as role-playing practice partners and feedback providers for developing professional social skills — such as conflict resolution, therapy, and counseling — in contexts where human practice partners are scarce or expensive. The key design insight is that out-of-the-box LLMs are too cooperative to be useful practice partners and must be deliberately constrained by domain-expert-designed rule sets.

**Why it matters for instruction.** This topic shows that effective AI deployment in professional training requires deliberate expert co-design of the AI's constraints — not just access to a capable model. The Stanford AP/AM research offers instructors a concrete case where prompt engineering and domain expertise combine to produce measurable learning outcomes, and where default AI behavior actively undermines the pedagogical goal.

**Common misconceptions.** Students often assume that a capable AI would naturally make a good coach or training partner. The AP/AM research shows the opposite: default AI cooperativeness — sycophancy, over-disclosure, excessive agreement — actively prevents the kinds of productive friction that professional skills training requires. Effective training demands deliberately making the AI less helpful in specific ways.

**Suggested framing.** Present AI-assisted skills training as a case study in the gap between general AI capability and domain-appropriate AI deployment — where the work of aligning AI behavior to training objectives requires systematic expert involvement, and where the design of the constitution is the primary bottleneck for scaling to new domains.
