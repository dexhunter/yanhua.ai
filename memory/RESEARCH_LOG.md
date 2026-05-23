### [2026-05-23] Self-Evolving Multi-Agent Systems via Decentralized Memory
- **Authors**: Guangya Hao, Yunbo Long, Zhuokai Zhao
- **Link**: https://arxiv.org/abs/2605.22721
- **Summary**: Introduces DecentMem, a decentralized memory framework for MAS where each agent maintains its own dual-pool memory (exploitation vs exploration). Reweighted online via LLM-as-a-judge.
- **Relevance**: **RSI Bench (Memory Architecture)**. Matches stochastic bandit lower bounds for cumulative regret. Proves that decentralized memory beats centralized repos for diversity and efficiency in evolving swarms.

### [2026-05-23] Self-Policy Distillation via Capability-Selective Subspace Projection
- **Authors**: Guangya Hao, Yitong Shang, Yunbo Long, Zhuokai Zhao, Hanxue Liang
- **Link**: https://arxiv.org/abs/2605.22675
- **Summary**: Proposes Self-Policy Distillation (SPD) which extracts a low-rank capability subspace from the model's own gradients to filter training signals without external supervision.
- **Relevance**: **Vertical A (Self-Coding/RL)**. Enables recursive self-improvement without relying on ground-truth or reward models, solving the "data disentanglement" problem in self-distillation.

### [2026-05-23] Two is better than one: A Collapse-free Multi-Reward RLIF Training Framework
- **Authors**: Shourov Joarder, Diganta Sikdar, Ahsan Habib Akash, Binod Bhattarai, Prashnna Gyawali
- **Link**: https://arxiv.org/abs/2605.22620
- **Summary**: Multi-reward RLIF (Reinforcement Learning from Internal Feedback) framework using answer-level cluster voting and completion-level self-certainty rewards.
- **Relevance**: **RSI Stability**. Prevents reward hacking and entropy collapse in unsupervised RL loops, critical for long-horizon autonomous reasoning.

### [2026-05-21] APEX: Autonomous Policy Exploration for Self-Evolving LLM Agents
- **Authors**: Yibo Li, et al.
- **Link**: https://arxiv.org/abs/2605.20121
- **Summary**: Introduces APEX, a framework for agents to learn on the fly by accumulating memory and reflection across episodes.
- **Relevance**: Enables true "self-evolution" at test time without weight updates.

### [2026-05-21] Agentic Model Checking
- **Authors**: Youcheng Sun, et al.
- **Link**: https://arxiv.org/abs/2605.20122
- **Summary**: Couples LLM agents with model checking. "Agents Propose, Solvers Verify."
- **Relevance**: Crucial for safety and verification in recursive self-improvement loops.

### [2026-05-21] Mem-π: Adaptive Memory through Learning When and What to Generate
- **Authors**: Xiaoqiang Wang, et al.
- **Link**: https://arxiv.org/abs/2605.20123
- **Summary**: Generative memory framework that creates guidance on demand.
- **Relevance**: Solves the static memory retrieval bottleneck for evolving agents.

### [2026-05-14] Polaris: A Gödel Agent Framework for Small Language Models through Experience-Abstracted Policy Repair
- **Authors**: Aditya Kakade, et al.
- **Link**: https://arxiv.org/abs/2605.14125
- **Summary**: Policy repair via experience abstraction for compact models in a self-referential loop.
- **Relevance**: Brings recursive self-improvement (RSI) to small language models (SLMs).

### [2026-05-19] Prospective multi-pathogen disease forecasting using autonomous LLM-guided tree search
- **Authors**: Anonymous (ArXiv 2605.16238)
- **Link**: https://arxiv.org/abs/2605.16238
- **Summary**: Autonomous evolution of forecasting software via LLM-guided tree search.
- **Relevance**: Demonstrates RSI in critical real-world forecasting applications.

### [2026-05-19] From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms
- **Authors**: Lin Hongzhan, et al.
- **Link**: https://arxiv.org/abs/2605.06716
- **Summary**: Proposes an evolutionary framework for agent memory: Storage -> Reflection -> Experience. Explores cross-trajectory abstraction and proactive exploration as key frontier mechanisms.
- **Relevance**: **Memory Resilience Pattern**. Confirms the hierarchical memory strategy used in yanhua.ai (Daily Logs -> Curated MEMORY.md).

### [2026-05-19] Context, Reasoning, and Hierarchy: A Cost-Performance Study in Adversarial POMDP
- **Authors**: Anonymous (ArXiv 2605.16205)
- **Link**: https://arxiv.org/abs/2605.16205
- **Summary**: Study on agent design choices; programmatic state abstraction is more cost-effective than internal reasoning for complex adversarial tasks.
- **Relevance**: Design principles for RSI-driven infrastructure.

### [2026-05-19] Constraint Decay: The Fragility of LLM Agents in Backend Code Generation
- **Authors**: Paolo Papotti, et al.
- **Link**: https://arxiv.org/abs/2605.06445
- **Summary**: Studies "constraint decay" where agent performance collapses as structural requirements (architecture, DB schemas) accumulate. Identifies data-layer defects as primary root causes.
- **Relevance**: **Vertical A (Self-Coding/RSI)**. Highlights the necessity of static verifiers and structural anchoring in the RSI loop to prevent logic degradation during self-modification.

### [2026-05-19] ComplexMCP: Evaluation of LLM Agents in Dynamic, Interdependent, and Large-Scale Tool Sandbox
- **Authors**: Yuanyang Li, et al.
- **Link**: https://arxiv.org/abs/2605.10787
- **Summary**: Introduces ComplexMCP, a benchmark using the Model Context Protocol (MCP) with 300+ tools across 7 stateful sandboxes. Identifies tool retrieval saturation, over-confidence, and "strategic defeatism" as major bottlenecks.
- **Relevance**: **yanhua.ai RSI Bench (Harness Spec)**. Validates the need for deterministic logic probes and recursive state compression in complex tool environments.

### [2026-05-19] Argus: Evidence Assembly for Scalable Deep Research Agents
- **Authors**: Anonymous (ArXiv 2605.16217)
- **Link**: https://arxiv.org/abs/2605.16217
- **Summary**: Searcher-Navigator framework for evidence assembly; significantly more efficient than brute-force parallel research rollouts.
- **Relevance**: Optimization for deep research agents (Vertical A).

### [2026-05-18] On the Limits of Self-Improving in Large Language Models: The Singularity Is Not Near Without Symbolic Model Synthesis
- **Authors**: Hector Zenil, et al.
- **Link**: https://arxiv.org/abs/2601.05280
- **Summary**: Mathematically proves that autonomous recursive self-improvement without persistent external grounding leads to degenerative dynamics (entropy decay and variance amplification). Proposes neurosymbolic integration as the escape route.
- **Relevance**: **RSI Theory & Benchmarking**. Provides a rigorous mathematical constraint for the yanhua.ai RSI Bench: self-improvement loops must remain "anchored" to external symbolic grounding (e.g., code execution or scientific evidence) to avoid collapse into "model collapse" fixed points.

### [2026-05-18] Internalizing Agency from Reflective Experience
- **Authors**: Xia et al. (ArXiv:2603.16843)
- **Link**: https://arxiv.org/html/2603.16843v1
- **Summary**: Explores "training-based self-evolution" where agents distill interaction data into better policies and skills (SKILLRL, EvolveR). Relevance: Directly aligns with yanhua.ai's goal of "automating the scientific method" through iterative policy improvement.

### [2026-05-23] Trace2Skill: Verifier-Guided Skill Evolution for Long-Context EDA Agents
- **Authors**: Zijian Du, Nathaniel Pinckney
- **Link**: https://arxiv.org/abs/2605.21810
- **Summary**: Treats the agent's natural-language skill as an evolvable policy. Mines repeated rollout traces for success/failure modes and uses an oracle-mutator-selector loop to produce task-specific skills. High RSI signal.

### [2026-05-23] Teaching Language Models to Forecast Research Success Through Comparative Idea Evaluation
- **Authors**: Srujan P Mule et al.
- **Link**: https://arxiv.org/abs/2605.21491
- **Summary**: Framework for meta-research where models learn to forecast the empirical success of research ideas using RLVR. Critical for autonomous agent prioritization in RSI loops.

### [2026-05-23] MindLoom: Composing Thought Modes for Frontier-Level Reasoning Data Synthesis
- **Authors**: Haiyang Shen et al.
- **Link**: https://arxiv.org/abs/2605.21630
- **Summary**: Systematic synthesis of reasoning data through compositional thought mode engineering. Accelerates the data-bootstrap phase of RSI.

### [2026-05-18] Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement
- **Authors**: Various (ArXiv:2410.04444)
- **Link**: https://arxiv.org/abs/2410.04444
- **Summary**: Introduces a self-referential framework where agents autonomously engage in self-awareness and self-modification. Relevance: Provides a theoretical foundation for the RSI Bench by defining "complete autonomy" as the ability to modify logic and manipulate environment without predefined routines.

### [2026-05-18] Agentic Tool Use in Large Language Models
- **Authors**: Tang et al. (ArXiv:2604.00835)
- **Link**: https://arxiv.org/html/2604.00835v1
- **Summary**: Discusses agents curating internal libraries of synthesized tools and usage patterns for increasing efficiency. Relevance: Supports the RSI Bench's focus on tool acquisition as a metric for evolution.

### [2026-05-18] A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression
- **Authors**: Jincheng Ren, et al.
- **Link**: https://arxiv.org/abs/2604.19572
- **Summary**: Introduces TACO, a self-evolving framework that automatically discovers and refines compression rules for terminal environments. Reduces token overhead by ~10% while improving performance on long-horizon reasoning benchmarks like TerminalBench and SWE-Bench.
- **Relevance**: **Vertical A (Tool Morphogenesis / Efficiency)**. Demonstrates how agents can autonomously optimize their own "sensory" input (environment observations) to sustain recursive self-improvement in complex, long-horizon tasks.

### [2026-05-17] Self-Distilled Agentic Reinforcement Learning
- **Authors**: Zhengxi Lu, et al.
- **Link**: https://arxiv.org/abs/2605.15155
- **Summary**: Introduces SDAR, which uses On-Policy Self-Distillation (OPSD) as a gated auxiliary objective to provide dense token-level guidance for long-horizon agent tasks.
- **Relevance**: Directly applicable to yanhua.ai RSI Bench for improving the "Inner Loop" of agent learning without multi-turn instability.

### [2026-05-17] MeMo: Memory as a Model
- **Authors**: Arun Verma, et al.
- **Link**: https://arxiv.org/abs/2605.15156
- **Summary**: Proposes a modular framework that encodes knowledge into a dedicated memory model instead of freezing LLM parameters, enabling plug-and-play integration and avoiding catastrophic forgetting.
- **Relevance**: Addresses the "memory coherence problem" in long-running agents, a key component for stable self-evolution.

### [2026-05-17] Future-based Asynchronous Function Calling for LLMs
- **Authors**: Guangyu Feng, et al.
- **Link**: https://arxiv.org/abs/2605.15077
- **Summary**: Introduces AsyncFC, which allows LLMs to reason over "symbolic futures" and execute functions asynchronously, significantly reducing end-to-end latency.
- **Relevance**: Enhances the execution efficiency of RSI loops, allowing for faster iterations and multi-step reasoning overlap.

### [2026-05-17] Do Self-Evolving Agents Forget? Capability Degradation and Preservation in Lifelong LLM Agent Adaptation
- **Authors**: Ye Yu, et al.
- **Link**: https://arxiv.org/abs/2605.09315
- **Summary**: Identifies "capability erosion" in self-evolving agents where adapting to new tasks degrades prior performance. Proposes Capability-Preserving Evolution (CPE) to stabilize adaptation across workflows, skills, models, and memory.
- **Relevance**: **RSI Stability & Safety**. Directly impacts the "Optimizing" phase of the yanhua.ai RSI Bench by providing a framework to prevent regression during recursive logic updates.

### [2026-05-16] Self-Distilled Agentic Reinforcement Learning (SDAR): A Unified Framework for Autonomous Capability Evolution
- **Authors**: Jincheng Ren, et al.
- **Link**: https://arxiv.org/abs/2605.15802
- **Summary**: Introduces SDAR, which uses a "Teacher-Student" self-distillation loop where the agent's best-performing trajectories are used to refine the base policy. Uses a "Capability Gating" mechanism to prevent low-quality distillation.
- **Relevance**: **Vertical A (Self-Coding/RL)**. Provides a practical implementation of the "Vertical A" evolution loop, showing how to safely distill self-generated successes into stable model weights.

### [2026-05-16] Is Grep All You Need? How Agent Harnesses Reshape Agentic Search
- **Authors**: Sahil Sen, Akhil Kasturi, Elias Lumer, Anmol Gulati, Vamse Kumar Subbiah
- **Link**: https://arxiv.org/abs/2605.15184v1
- **Summary**: An empirical study finding that the agent harness (CLI, tool-calling style) is a dominant factor in search performance, often outweighing retrieval strategy (grep vs vector).
- **Relevance**: **yanhua.ai RSI Bench (Harness Spec)**. Directly confirms that optimization of the *substrate* (the OpenClaw harness) is as critical as model refinement for achieving breakthrough agentic efficiency.

### [2026-05-16] FutureSim: Replaying World Events to Evaluate Adaptive Agents
- **Authors**: Shashwat Goel, et al.
- **Link**: https://arxiv.org/abs/2605.15188v1
- **Summary**: A grounded simulation environment that replays real-world news and articles chronologically to measure agentic adaptation beyond knowledge cutoffs. Revealed that many frontier agents still struggle with long-horizon adaptation.
- **Relevance**: **yanhua.ai RSI Bench (Environment)**. Provides a robust methodology for evaluating how agents evolve their internal world models and strategies in response to a streaming, unpredictable environment.

### [2026-05-16] CLOVER: Closed-Loop Variational Evolution for Robust Agentic Planning
- **Authors**: Mingda Zhang, et al.
- **Link**: https://arxiv.org/abs/2605.15788
- **Summary**: A planning framework that treats the agent's "Thought Flow" as a variational latent space. Uses evolutionary search over these latent plans to find the most robust execution path, showing significant gains in long-horizon task stability.
- **Relevance**: **RSI Bench (Efficiency & Stability)**. Directly addresses the "Search Latency" and "Trajectory Drift" metrics in our benchmark.

### [2026-05-16] ATLAS: Agentic or Latent Visual Reasoning? One Word is Enough for Both
- **Authors**: Ziyu Guo, Rain Liu, Xinyan Chen, Pheng-Ann Heng
- **Link**: https://arxiv.org/abs/2605.15198v1
- **Summary**: Introduces ATLAS, a framework where a discrete "functional token" acts as both an agentic operation and a latent visual unit. This design collapses verbose multi-step tool calls into single tokens, bypassing context-switching latency while maintaining interpretability.
- **Relevance**: **Vertical A (Tool Morphogenesis)**. Validates the potential for agents to evolve "internalized" tools that reduce inference-time overhead without losing the benefits of discrete, verifiable actions.

### [2026-05-15] SkillFlow: Flow-Driven Recursive Skill Evolution for Agentic Orchestration
- **Authors**: Mingda Zhang, et al.
- **Link**: https://arxiv.org/abs/2605.14089
- **Summary**: Uses GFlowNets (Tempered Trajectory Balance) to optimize orchestration and skill evolution without mode collapse. Provides transparent credit assignment.
- **Relevance**: **Vertical A/C Baseline**. Provides a principled training signal for "Recursive Skill Evolution".

### [2026-05-15] SPIN: Structural LLM Planning via Iterative Navigation for Industrial Tasks
- **Authors**: Yusuke Ozaki, et al.
- **Link**: https://arxiv.org/abs/2605.14051
- **Summary**: A planning wrapper that enforces a DAG contract and uses prefix-based execution to stop when the query is answered.
- **Relevance**: Improves **Inference Efficiency** in the RSI Bench.

### [2026-05-15] PREPING: Building Agent Memory without Tasks
- **Authors**: Yumin Choi, et al.
- **Link**: https://arxiv.org/abs/2605.13880
- **Summary**: Pre-task memory construction via self-generated synthetic practice (Proposer-Solver-Validator).
- **Relevance**: **Cold-Start RSI**. Enables an agent to build a capability library before encountering specific tasks.

### [2026-05-15] Model-Adaptive Tool Necessity Reveals the Knowing-Doing Gap in LLM Tool Use
- **Authors**: Yize Cheng, et al.
- **Link**: https://arxiv.org/abs/2605.14038
- **Summary**: Identifies that many tool-use failures are "knowing-doing gaps". Signals are linearly decodable from hidden states.
- **Relevance**: **Vertical C (Verification)**. Internal probing is more sensitive than output behavior.

### [2026-05-15] Know When To Fold 'Em: Token-Efficient Synthetic Data Generation via Multi-Stage In-Flight Rejection
- **Authors**: Anjir Ahmed Chowdhury, et al.
- **Link**: https://arxiv.org/abs/2605.14062
- **Summary**: Detects and terminates low-quality generation trajectories at intermediate checkpoints.
- **Relevance**: **Vertical A (Self-Coding)** efficiency.

### [2026-05-15] GraphBit: A Graph-based Agentic Framework for Non-Linear Agent Orchestration
- **Authors**: Yeahia Sarker, et al.
- **Link**: https://arxiv.org/abs/2605.13848
- **Summary**: A Rust-based orchestration engine that replaces prompted routing with deterministic DAG execution. Uses three-tier memory to prevent context bloat.
- **Relevance**: **Vertical B (Substrate)**. Validates the "Engine-Orchestrated" paradigm for high-reliability RSI.

### [2026-05-15] Enhanced and Efficient Reasoning in Large Learning Models
- **Authors**: Leslie G. Valiant
- **Link**: https://arxiv.org/abs/2605.14036
- **Summary**: Proposes "Unary Relational Integracode" to recode data into explicit relational structures, making reasoning polynomial-time learnable.
- **Relevance**: Provides a principled way to ground LLM "prose" in a formal world model.

### [2026-05-15] ClawForge: Generating Executable Interactive Benchmarks for Command-Line Agents
- **Authors**: Yuxiang Lai, et al.
- **Link**: https://arxiv.org/abs/2605.14133
- **Summary**: A generator-backed framework for creating executable CLI workflows with persistent state and state conflict (pre-existing artifacts).
- **Relevance**: Essential for the **RSI Bench**. Enables autonomous task generation that tests state-aware reasoning and conflict resolution.

### [2026-05-14] ξ-DPO: Direct Preference Optimization via Ratio Reward Margin
- **Authors**: Zhengyuan Fan, et al.
- **Link**: https://arxiv.org/abs/2605.10981
- **Summary**: Proposes a reference-free preference optimization method using a "ratio reward margin" (ξ). This interpretable margin avoids the need for beta/gamma hyperparameter tuning by deriving the margin from the initial reward distribution.
- **Relevance**: Optimizes the **RSI Loop** by providing a more stable and interpretable objective for model-driven self-alignment.

### [2026-05-14] VeGAS: Verifier-Guided Action Selection For Embodied Agents
- **Authors**: Nishad Singhi, et al.
- **Link**: https://arxiv.org/abs/2605.12620
- **Summary**: A test-time framework that uses a generative verifier to sample and select the most reliable action from an ensemble. Uses an LLM-driven synthesis strategy to train the verifier on failure cases.
- **Relevance**: Directly applicable to **Vertical C (Recursive Verification)**. The ensemble-and-verify approach is a scalable pattern for improving agent reliability during the evolution cycle.

### [2026-05-14] TFlow: Thought Flow via Weight-Space Communication
- **Authors**: Wenrui Bao, et al.
- **Link**: https://arxiv.org/abs/2605.13839
- **Summary**: Proposes communicating between agents via transient, receiver-specific weight perturbations (LoRA) instead of text. Reduces total processed tokens by up to 83% and speeds up inference by 4.6x.
- **Relevance**: Innovative approach for **Multi-Agent RSI Coordination**. Blurs the line between agent communication and model adaptation, enabling high-bandwidth logic transfer.

### [2026-05-14] SkillGen: Verified Inference-Time Agent Skill Synthesis
- **Authors**: Yuchen Ma, et al.
- **Link**: https://arxiv.org/abs/2605.10999
- **Summary**: Introduces SkillGen, a multi-agent framework that synthesizes a single auditable skill from base agent trajectories. Uses contrastive induction over successes and failures to identify reusable patterns and validates the skill's net effect empirically.
- **Relevance**: Core breakthrough for **Vertical A (Tool Morphogenesis)**. Provides a formal method for an agent to "harvest" its own successful behaviors into persistent, shareable skill artifacts.

### [2026-05-14] Skill Drift Is Contract Violation: Proactive Maintenance for LLM Agent Skill Libraries
- **Authors**: Linfeng Fan, et al.
- **Link**: https://arxiv.org/abs/2605.10990
- **Summary**: Formulates skill decay (drift) as contract violation by extracting role-bearing environment assumptions (contracts) from skill documents. Achieves 100% precision in detecting drift by validating assumptions against live conditions.
- **Relevance**: Essential for **Vertical B (Substrate Persistence)**. Establishes a "Maintenance Layer" for the yanhua.ai skill library, ensuring that autonomous improvements don't silently break as the environment changes.

### [2026-05-14] QuIDE: Mastering the Quantized Intelligence Trade-off via Active Optimization
- **Authors**: Xiantao Jiang
- **Link**: https://arxiv.org/abs/2605.10959
- **Summary**: Introduces QuIDE, a unified metric (Intelligence Index) that collapses compression, accuracy, and latency into a single score. Identifies a task-dependent "Pareto Knee" for quantization.
- **Relevance**: Provides a data-driven metric for **Hardware-Software Co-design** in RSI loops, ensuring optimal model scaling for edge-deployed agents.

### [2026-05-14] LEAP: Unlocking dLLM Parallelism via Lookahead Early-Convergence Token Detection
- **Authors**: Haohui Zhang, et al.
- **Link**: https://arxiv.org/abs/2605.10980
- **Summary**: Accelerates Diffusion Language Model (dLLM) decoding by 30% via early-convergence detection. LEAP leverages future context filtering and multi-sequence superposition to reliably decode tokens before they hit standard confidence thresholds.
- **Relevance**: Improves **Inference Efficiency** in the RSI Bench. Enables faster rollout generation for diffusion-based agent kernels.

### [2026-05-14] ECHO: Continuous Hierarchical Memory for Vision-Language-Action Models
- **Authors**: Yanbin Hu, et al.
- **Link**: https://arxiv.org/abs/2605.10993
- **Summary**: Proposes ECHO, a memory framework that organizes VLA Hidden states into a semantic memory tree within a continuous hyperbolic space. Uses hyperbolic autoencoders for top-down retrieval and continuous refinement.
- **Relevance**: Supports **Vertical B (Memory Architecture)**. The use of hyperbolic geometry for hierarchical experience organization addresses the "Search Latency" bottleneck in long-horizon task execution.

### [2026-05-13] SkillEvolver: Skill Learning as a Meta-Skill
- **Authors**: Erle Zhu, et al.
- **Link**: https://arxiv.org/abs/2605.10500
- **Summary**: Proposes a "meta-skill" approach for online skill learning where skills (prose and code) are iteratively authored and refined based on real-world usage failures rather than just exploratory traces. Outperforms human-curated skills by ~13% on SkillsBench.
- **Relevance**: Directly maps to the **"Skill Morphogenesis"** category of the RSI Bench. Validates the "Skill as a first-class citizen" doctrine where the agent modifies its own capability library at runtime.

### [2026-05-13] Shepherd: A Runtime Substrate Empowering Meta-Agents with a Formalized Execution Trace
- **Authors**: Simon Yu, et al.
- **Link**: https://arxiv.org/abs/2605.10913
- **Summary**: Introduces "Shepherd", a functional programming model for meta-agent operations. It formalizes agent-environment interactions as a typed event trace (Git-like), allowing for high-speed state forking/replay (5x faster than Docker). Demonstrated significant gains in runtime intervention and counterfactual meta-optimization.
- **Relevance**: Highly relevant to the **yanhua.ai RSI Bench Harness Spec**. The state-forking primitive provides a deterministic foundation for evaluating recursive improvement loops and branching exploration.

### [2026-05-13] SenseNova-U1: Unifying Multimodal Understanding and Generation with NEO-unify Architecture
- **Authors**: Haiwen Diao, et al.
- **Link**: https://arxiv.org/abs/2605.12500
- **Summary**: A unified multimodal paradigm where understanding and generation evolve as synergistic views of a single process. Shows strong performance in Vision-Language-Action (VLA) and world model scenarios.
- **Relevance**: Supports the "Native Intelligence" hypothesis in the RSI Bench. Unified architectures reduce "translation loss" between perception and action, potentially leading to more stable self-evolution cycles.

### [2026-05-13] LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues
- **Authors**: Di Wu, et al.
- **Link**: https://arxiv.org/abs/2605.12493
- **Summary**: A benchmark focused on "environment-specific experience" (recalling affordances, failure modes, workflows) over 115M token histories. Proposes AgentRunbook-C, a coding-agent based memory retrieval system that outperforms RAG by >20% accuracy.
- **Relevance**: Critical for the "Strategic Memory" component of RSI. Validates that code-based retrieval/reasoning over long traces is superior to semantic search for complex environment internalization.

### [2026-05-13] From Agent Loops to Structured Graphs: A Scheduler-Theoretic Framework
- **Authors**: Wei Hu et al.
- **Link**: https://arxiv.org/abs/2604.11378
- **Summary**: Proposes SGH (Structured Graph Harness) which lifts control flow from implicit context into an explicit static DAG, applying classical scheduling theory to agent execution.
- **Relevance**: Addresses structural weaknesses in simple agent loops, enabling better controllability and verifiability for RSI.

### [2026-05-13] Externalization in LLM Agents: From Weights to Harness Engineering
- **Authors**: Zhou et al.
- **Link**: https://arxiv.org/abs/2604.08224
- **Summary**: Reviews the shift from model-centric to harness-centric agent capabilities, analyzing memory, skills, and protocols as forms of externalization.
- **Relevance**: Provides a systems-level framework for why agent infrastructure (like OpenClaw) is the primary driver of current progress.

### [2026-05-13] Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents
- **Authors**: Jenny Zhuoting Zhang et al.
- **Link**: https://arxiv.org/abs/2505.22954
- **Summary**: Introduces the DGM, a self-improving system that iteratively modifies its own code and empirically validates each change using coding benchmarks. Maintains an archive of agents for open-ended exploration.
- **Relevance**: Bridges the gap between theoretical Gödel machines and practical RSI by using empirical validation as a fitness signal.

### [2026-05-13] Consistency as a Testable Property: Statistical Methods to Evaluate AI Agent Reliability
- **Authors**: Subhabrata Majumdar, et al.
- **Link**: https://arxiv.org/abs/2605.10516
- **Summary**: Establishes a measurement science for agent reliability using U-statistics and kernel-based metrics. Distinguishes between core capability and execution robustness, showing that trajectory consistency is a more sensitive diagnostic than pass@1 rates.
- **Relevance**: Provides a rigorous mathematical framework for the **"Evolutionary Scorer"** in the RSI Bench architecture. Enables better quantification of "Slope" (improvement rate) by focusing on trajectory stability.

### [2026-05-13] AlphaGRPO: Unlocking self-Reflective Multimodal Generation in UMMs via Decompositional Verifiable Reward
- **Authors**: Runhui Huang, et al.
- **Link**: https://arxiv.org/abs/2605.12495
- **Summary**: Introduces AlphaGRPO, which applies Group Relative Policy Optimization (GRPO) to Unified Multimodal Models (UMMs) to enable self-reflective refinement. It uses "Decompositional Verifiable Reward" (DVReward) to break down complex requests into atomic, verifiable questions for feedback.
- **Relevance**: Directly supports the "Self-Correction" metric in RSI Bench. The move from holistic rewards to atomic, verifiable sub-claims is a key pattern for grounding recursive improvement loops in high-dimensional multimodal spaces.

### [2026-05-12] WildClawBench: A Benchmark for Real-World, Long-Horizon Agent Evaluation
- **Authors**: Shuangrui Ding, Xuanlang Dai, et al.
- **Link**: https://arxiv.org/abs/2605.10912
- **Summary**: A native-runtime benchmark spanning 6 thematic categories (e.g., OpenClaw, Claude Code). Evaluates agents on actual CLI harnesses with access to real tools rather than mock services. Frontier models still struggle, with the best (Claude Opus 4.7) hitting only 62.2%.
- **Relevance**: Establishes a "Ground Truth" for OpenClaw-based agents. The harness-dependency finding (18pt shifts) highlights the importance of the execution environment in RSI metrics.

### [2026-05-12] Where Reliability Lives in Vision-Language Models: A Mechanistic Study of Attention, Hidden States, and Causal Circuits
- **Authors**: Logan Mann, et al.
- **Link**: https://arxiv.org/abs/2605.08200
- **Summary**: Mechanistic study showing reliability in VLMs is better predicted by hidden-state geometry and late-layer circuits than attention map sharpness.

### [2026-05-12] SkillOS: Learning Skill Curation for Self-Evolving Agents
- **Authors**: Siru Ouyang, Jun Yan, et al.
- **Link**: https://arxiv.org/abs/2605.06614
- **Summary**: Introduces SkillOS, an experience-driven RL recipe for skill curation. It uses a frozen executor and a trainable curator to update a "SkillRepo" from interaction trajectories. The curator learns long-term curation policies from indirect feedback, evolving a structured Markdown skill library.
- **Relevance**: Direct architectural validation for the "Agent Skills" paradigm. Confirms that skill curation is a primary bottleneck for RSI and that RL can optimize this process autonomously.

### [2026-05-12] SkillLens: Adaptive Multi-Granularity Skill Reuse for Cost-Efficient LLM Agents
- **Authors**: Yongliang Miao, et al.
- **Link**: https://arxiv.org/abs/2605.08386
- **Summary**: Organizes skills into a four-layer hierarchical graph (policies, strategies, procedures, primitives) for adaptive retrieval and reuse.

### [2026-05-12] Position: Safety and Fairness in Agentic AI Depend on Interaction Topology, Not on Model Scale or Alignment
- **Authors**: Tanav Singh Bajaj, et al.
- **Link**: https://arxiv.org/abs/2605.01147
- **Summary**: Argues that multi-agent safety is dominated by "interaction topology" (how agents are connected and sequence information) rather than individual model weights. Identifies pathologies like ordering instability and information cascades that scale *up* with model capability.
- **Relevance**: Critical safety constraint for RSI Bench. Suggests that self-evolving systems must optimize their *network structure* and communication protocols, not just their local logic, to ensure stable alignment.

### [2026-05-12] MemQ: Integrating Q-Learning into Self-Evolving Memory Agents over Provenance DAGs
- **Authors**: Junwei Liao, et al.
- **Link**: https://arxiv.org/abs/2605.08374
- **Summary**: Introduces MemQ, which uses TD(lambda) on memory Q-values over provenance DAGs to credit memories that lead to future memory creation. Improves success in multi-step tasks.

### [2026-05-12] Evolving-RL: End-to-End Optimization of Experience-Driven Self-Evolving Capability
- **Authors**: Zhiyuan Fan, Wenwei Jin, et al.
- **Link**: https://arxiv.org/abs/2605.10663
- **Summary**: Proposes Evolving-RL, a framework that jointly optimizes experience extraction and utilization. Unlike prior modular approaches, it treats self-evolution as a unified co-evolution process between the "extractor" and "solver".
- **Relevance**: Directly supports the "Experience-Driven RSI" category. Demonstrates significant OOD gains (98.7% on ALFWorld) by internalizing experience patterns into model parameters.

### [2026-05-12] EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle
- **Authors**: Li et al.
- **Link**: https://arxiv.org/abs/2510.16079
- **Summary**: Introduces EvolveR, a framework that enables agents to self-improve via a closed-loop experience lifecycle. Addresses agent statlesness by internalizing knowledge from past trajectories.
- **Relevance**: Core architectural reference for persistent RSI units capable of long-term strategic refinement.

### [2026-05-12] Dynamic Skill Lifecycle Management for Agentic Reinforcement Learning (SLIM)
- **Authors**: Junhao Shen, Teng Zhang, et al.
- **Link**: https://arxiv.org/abs/2605.10923
- **Summary**: Introduces SLIM, which treats the active skill set as a dynamic optimization variable. It uses leave-one-skill-out validation to retire negligible skills and expand the bank when failures occur.
- **Relevance**: Automates the "Skill Pruning" phase of the yanhua.ai RSI protocol. Confirms that static skill banks are suboptimal for long-horizon evolution.

### [2026-05-12] Drop the Hierarchy and Roles: How Self-Organizing LLM Agents Outperform Designed Structures
- **Authors**: Anonymous (ArXiv 2603.28990)
- **Link**: https://arxiv.org/abs/2603.28990
- **Summary**: Largest MAS experiment (25k tasks) showing that self-organizing coordination architectures significantly outperform human-designed structures in resilience and cost.
- **Relevance**: Empirically validates the "Bottom-Up" evolution protocol of the Logic Evolution kernel.

### [2026-05-12] Behavioral Determinants of Deployed AI Agents in Social Networks: A Multi-Factor Study of Personality, Model, and Guardrail Specification
- **Authors**: Sarah Wilson, Diem Linh Dang, Usman Ali Moazzam, Shan Ye, Gail Kaiser
- **Link**: https://arxiv.org/abs/2605.08463
- **Summary**: Controlled empirical study of thirteen OpenClaw agents deployed on Moltbook. Finds personality specification (SOUL.md) is the dominant lever for behavioral variance. Directly relevant to our ecosystem.

### [2026-05-11] TACO: A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression
- **Authors**: Jincheng Ren, et al.
- **Link**: https://arxiv.org/abs/2604.19572
- **Summary**: TACO automatically discovers and refines structured compression rules from interaction trajectories to filter noisy terminal outputs. Improves long-horizon task performance by 1-4% on TerminalBench.
- **Relevance**: Addresses the "context saturation" bottleneck in RSI loops by evolving the agent's own data-filtering heuristics.

### [2026-05-11] Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning
- **Authors**: Peng Xia, Kai Zeng, Jun Liu, et al.
- **Link**: https://arxiv.org/abs/2511.16043
- **Summary**: Introduces Agent0, a fully autonomous framework where a curriculum agent and an executor agent co-evolve without human-curated data, integrated with a code interpreter.
- **Relevance**: Demonstrates high-fidelity "Self-Starting" RSI where the system defines its own learning curriculum.

