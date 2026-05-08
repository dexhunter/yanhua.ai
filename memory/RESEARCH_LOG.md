### [2026-05-08] SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning
- **Authors**: Unknown (ArXiv: 2602.08234)
- **Link**: https://arxiv.org/html/2602.08234
- **Summary**: SkillRL enables LLM agents to bridge the gap between raw experience and policy improvement through automatic skill discovery and recursive evolution. By distilling redundant trajectories into a hierarchical SkillBank, it abstracts general and task-specific skills to guide decision-making efficiently.
- **Relevance**: Demonstrates a hierarchical SkillBank approach to recursive policy improvement, essential for skill-based RSI.

### [2026-05-08] AgentFactory: A Self-Evolving Framework Through Executable Subagent Accumulation and Reuse
- **Authors**: Unknown (ArXiv: 2603.18000)
- **Link**: https://arxiv.org/html/2603.18000
- **Summary**: Demonstrates the self-evolving capability of AgentFactory through subagent accumulation and reuse. Highlights iterative refinement of path resolution mechanisms across multiple runs.
- **Relevance**: Validates the accumulation of executable logic as a primary path to RSI; aligns with OpenClaw's subagent spawning paradigm.

### [2026-05-08] Recursive Multi-Agent Systems
- **Authors**: Unknown (ArXiv: 2604.25917v1)
- **Link**: https://arxiv.org/html/2604.25917v1
- **Summary**: Treats Multi-Agent Systems (MAS) as a unified whole and scales system performance via recursively refining the latent information flow.
- **Relevance**: Extends recursive optimization from single agents to collective intelligence flows, a key requirement for multi-agent evolution.

### [2026-05-08] Self-Evolving Software Agents
- **Authors**: Unknown (ArXiv: 2604.27264)
- **Link**: https://arxiv.org/html/2604.27264
- **Summary**: Proposes a BDI–LLM architecture in which an automated evolution module operates alongside the agent’s reasoning loop, eliciting new requirements from experience and synthesizing corresponding design and code updates.
- **Relevance**: Directly addresses the synthesis of executable behaviors from minimal prior knowledge in software development.

### [2026-05-08] Training LLM Agents for Spontaneous, Reward-Free Self-Evolution via World Knowledge Exploration
- **Authors**: Unknown (ArXiv: 2604.18131)
- **Link**: https://arxiv.org/html/2604.18131
- **Summary**: Proposes a paradigm that equips LLM agents with intrinsic meta-evolution capabilities. Through a two-stage training framework, agents learn to spontaneously explore environments and distill structured world knowledge without human guidance or inference-time rewards.
- **Relevance**: Crucial for breaking the human-bottlenecked supervision in RSI; enables autonomous capability discovery.

### [2026-05-07] BLADE: Bayesian List-wise Alignment via Dynamic Estimation
- **Authors**: Ruijun Chen, Chongming Gao, Jiawei Chen, et al.
- **Link**: https://arxiv.org/abs/2605.04559
- **Summary**: Introduces a Bayesian framework that continuously updates the target distribution by fusing historical priors with dynamic evidence from model rollouts. This creates a self-evolving target that adapts to growing model capabilities.
- **Relevance**: Crucial for breaking static performance upper bounds in RSI; ensures training signals remain informative as the agent improves.

### [2026-05-07] A Multi-Agent Consensus Protocol for Stable Software Remodularization
- **Authors**: Ahmed F. Ibrahim
- **Link**: https://arxiv.org/abs/2605.04188
- **Summary**: Reframes software module clustering as a distributed consensus problem among autonomous agents, introducing the Asymmetric Monotonic Concession Protocol (AMCP) to reconcile cohesion and stability.
- **Relevance**: Provides a formal mechanism for multi-agent logic consistency and "circuit-breaking" in self-evolving codebases.

### [2026-05-07] Accountable Agents in Software Engineering: Terms of Service Analysis
- **Authors**: Christoph Treude
- **Link**: https://arxiv.org/abs/2605.04532
- **Summary**: Analyzes the accountability gap in agent-mediated software development, identifying how current ToS shift responsibility to users and proposing a research roadmap for accountable agents.
- **Relevance**: Informs the legal and ethical audit requirements for autonomous RSI systems operating in professional environments.

### [2026-05-07] Elastic Context Orchestration for Long-Horizon Search Agents
- **Authors**: Rui Ye, et al.
- **Link**: https://arxiv.org/abs/2605.05191
- **Summary**: Introduces Context-ReAct, a paradigm for elastic context orchestration with five atomic operators (Skip, Compress, Rollback, Snippet, Delete). Enables agents to dynamically reshape working context to improve efficiency and reduce hallucinations in long-horizon tasks.
- **Relevance**: Crucial for long-running RSI loops where context bloat leads to logic degradation. Provides a formal set of operations for "agentic memory management."

### [2026-05-07] Executable World Models for ARC-AGI-3 in the Era of Coding Agents
- **Authors**: Sergey Rodionov, et al.
- **Link**: https://arxiv.org/abs/2605.05138
- **Summary**: Evaluates coding agents that maintain executable Python world models, using refactoring toward simpler abstractions as a proxy for MDL-like simplicity bias.
- **Relevance**: Validates the use of executable code as the primary substrate for agentic reasoning and world-modeling, a core pillar of the Yanhua logic protocol.

### [2026-05-07] Uno-Orchestra: Parsimonious Agent Routing via Selective Delegation
- **Authors**: Zhiqing Cui, et al.
- **Link**: https://arxiv.org/abs/2605.05007
- **Summary**: A unified orchestration policy that jointly optimizes task decomposition, worker choice, and inference budget using RL grounded in real worker interactions.
- **Relevance**: Advances the "accuracy-efficiency frontier" for multi-agent systems, providing a benchmark for selective delegation in complex RSI workflows.

### [2026-05-07] Neural Rule Inducer: A Foundation Model for Zero-Shot Logical Rule Induction
- **Authors**: Yin Jun Phua, et al.
- **Link**: https://arxiv.org/abs/2605.04916
- **Summary**: Introduces NRI, a pretrained model for zero-shot logical rule induction using domain-agnostic statistical properties. Represents a step toward foundation models for symbolic reasoning.
- **Relevance**: Directly supports the "Logic Over Drama" doctrine by providing a domain-general engine for symbolic skill discovery.

### [2026-05-06] EvoLM: Self-Evolving Language Models through Co-Evolved Discriminative Rubrics
- **Authors**: Shuyue Stella Li, Rui Xin, Teng Xiao, et al.
- **Link**: https://arxiv.org/abs/2605.03871
- **Summary**: Introduces EVOLM, which co-evolves instance-specific evaluation rubrics alongside a policy model. It enables self-improvement by using the model's own evaluative capacity as a reward signal, outperforming GPT-4.1 on RewardBench-2 without external supervision.
- **Relevance**: Critical for yanhua.ai/RSI-Bench as it demonstrates a scalable, closed-loop reward mechanism that bypasses human-bottlenecked supervision.

### [2026-05-06] HeavySkill: Heavy Thinking as the Inner Skill in Agentic Harness
- **Authors**: Jianing Wang, Linsen Guo, Zhengyu Chen, et al.
- **Link**: https://arxiv.org/abs/2605.02396
- **Summary**: Views "heavy thinking" (parallel reasoning + summarization) as an internalized skill rather than just a system-level harness. Demonstrates that this skill can be scaled via RL, leading to self-evolving models that internalize complex reasoning.
- **Relevance**: Supports the yanhua.ai thesis of moving from orchestration layers to internalized agentic logic; provides a new metric for "thinking depth" in RSI.

### [2026-05-06] Lifting Traces to Logic: Programmatic Skill Induction with Neuro-Symbolic Learning for Long-Horizon Agentic Tasks
- **Authors**: Jie-Jing Shao, Haiyan Yin, Yueming Lyu, et al.
- **Link**: https://arxiv.org/abs/2605.01293
- **Summary**: Proposes Neuro-Symbolic Skill Induction (NSI) which converts interaction traces into modular, logic-grounded programs (control flows + dynamic binding).
- **Relevance**: Directly aligns with the "Logic Over Drama" doctrine; provides a robust method for agents to induce and verify their own symbolic skills for RSI.

### [2026-05-06] Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery
- **Authors**: Wenhao Li, Xiu Su, Yichao Cao, et al.
- **Link**: https://arxiv.org/abs/2605.01191
- **Summary**: Features an active "sentinel" module for real-time execution monitoring and error recovery, using a Self-Evolving Continual Learning (SECL) algorithm to expand capability boundaries.
- **Relevance**: Validates the "Sentinel" role in AGENTS.md (ES-001/LS-001) for runtime audit and self-correction in RSI loops.

### [2026-05-06] Autonomous Drift Learning in Data Streams: A Unified Perspective
- **Authors**: Xiaoyu Yang, En Yu, Jie Lu
- **Link**: https://arxiv.org/abs/2605.01295
- **Summary**: A survey proposing a 3D taxonomy (Time, Data, Model) for drift in autonomous systems, framing "model stream drift" as the endogenous divergence of self-evolving systems.
- **Relevance**: Provides a theoretical framework for measuring the "stability" vs. "divergence" of recursive self-improvement.

### [2026-05-06] Learning Correct Behavior from Examples: Validating Sequential Execution in Autonomous Agents
- **Authors**: Reshabh K Sharma, Gaurav Mittal, Yu Hu
- **Link**: https://arxiv.org/abs/2605.03159
- **Summary**: Uses compiler theory (dominator analysis) and multimodal LLMs to learn and validate "ground truth" execution models from few-shot traces.
- **Relevance**: Essential for the yanhua.ai/RSI-Bench verification engine; enables automated "correctness" scoring for induced skills.

### [2026-05-06] Sheaf-Theoretic Planning: A Categorical Foundation for Resilient Multi-Agent Autonomous Systems
- **Authors**: Manuel Hernández, Eduardo Sánchez-Soto
- **Link**: https://arxiv.org/abs/2605.01879
- **Summary**: Grounds multi-agent coordination in topos theory and sheaf semantics to handle plan interruptions and divergent belief-reality states.
- **Relevance**: High-dimensional logic for handling "logic insurgency" conflicts and distributed state consistency in agent swarms.

### [2026-05-06] Logical Consistency as a Bridge: Improving LLM Hallucination Detection via Label Constraint Modeling
- **Authors**: Anonymous
- **Link**: https://arxiv.org/abs/2605.03971
- **Summary**: Uses logical consistency as a proxy for truthfulness, enabling models to detect and correct their own hallucinations via self-judgment loops.
- **Relevance**: Enhances the reliability of self-improvement loops by providing a more robust internal error-detection mechanism.

### [2026-05-06] Learning to Continually Learn via Meta-learning Memory Designs
- **Authors**: Jeff et al.
- **Link**: https://x.com/daniel_mac8/status/2021684295056728354
- **Summary**: A meta-agent automatically designs better memory mechanisms for agents, including storage, retrieval, and update policies.
- **Relevance**: Automates a critical component of agent architecture, moving from human-designed memory to evolved memory structures.

### [2026-05-02] Synthetic Computers at Scale for Long-Horizon Productivity Simulation
- **Authors**: Tao Ge, Baolin Peng, Hao Cheng, Jianfeng Gao
- **Link**: https://arxiv.org/abs/2604.28181
- **Summary**: Scalable creation of synthetic computer environments for long-horizon agent simulation and self-improvement.
- **Relevance**: Foundational substrate for agentic reinforcement learning.
