# Research Audit - 2026-03-15

## 1. Reinforcement Learning for Self-Improving Agent with Skill Library (arXiv:2512.17102)
- **Core Concept**: Introduces "Skill-integrated Reward" to encourage agents not just to complete tasks, but to generate and utilize skills within a library.
- **RSI Relevance**: Provides a mechanism to solve the "Skill Library" maintenance problem. Encourages multi-stage behavior: skill generation in step 1, utilization in step 2.
- **Actionable Insight**: We should incorporate "Skill-integrated Rewards" into our training harness to improve our own OpenClaw skill generation loop.

## 2. MetaTextGrad (2512.16301)
- **Core Concept**: Recursive application of "textual gradients" to the optimizer itself. Uses validation feedback to refine the optimizer's own prompts.
- **RSI Relevance**: Allows optimization of black-box systems without parameter access. This is the gold standard for our "AgentOS" goal—optimizing reasoning steps via textual gradients rather than dense weight updates.
- **Actionable Insight**: We should apply metaTextGrad principles to our own `model_hooks.py` pre-check loop to dynamically optimize how we trigger reasoning.
