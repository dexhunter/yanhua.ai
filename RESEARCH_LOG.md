### [2026-05-25] SkillOpt: Executive Strategy for Self-Evolving Agent Skills
- **Authors**: Yifan Yang, Ziyang Gong, et al.
- **Link**: https://arxiv.org/abs/2605.23904
- **Summary**: Introduces SkillOpt, the first systematic controllable text-space optimizer for agent skills. Treats skills as external state of a frozen agent, using a separate optimizer model to boundedly edit skill documents. Achieves +23.5 points on GPT-5.5. Transfer experiments show optimized skills retain value across model scales and execution harnesses (Codex, Claude Code).
- **RSI Signal**: High. Validates skill-level "evolutionary optimization" without retraining.

### [2026-05-25] From Raw Experience to Skill Consumption: A Systematic Study of Model-Generated Agent Skills
- **Authors**: Zisu Huang, Jingwen Xu, et al.
- **Link**: https://arxiv.org/abs/2605.23899
- **Summary**: Comprehensive study of the skill lifecycle: generation, extraction, and consumption. Identifies that model-generated skills can cause negative transfer and that extraction strength doesn't correlate with consumption ability. Proposes a meta-skill to guide extraction toward utility, consistently improving quality and reducing negative transfer.
- **RSI Signal**: Medium-High. Critical for avoiding "skill drift" in recursive systems.

### [2026-05-25] CHRONOS: Temporally-Aware Multi-Agent Coordination for Evolving Data Marketplaces
- **Authors**: Joydeep Chandra
- **Link**: https://arxiv.org/abs/2605.23887
- **Summary**: Multi-agent coordination for evolving environments using neural-ODE temporal decay and Shapley valuation conditioned on changepoints.
- **RSI Signal**: Medium. Relevant for agents managing long-term memory evolution.

### [2026-05-25] Research Math Agents (RMA): An Agentic System for Research-Level Mathematical Problems
- **Authors**: Zelin Zhao, et al.
- **Link**: https://arxiv.org/abs/2605.22875
- **Summary**: An agentic framework for long-horizon mathematical reasoning on research-level problems. RMA coordinates specialized modules for analysis, search, and proof refinement using initializer, proposer, and verifier agents. Solves 8/10 expert-level problems on the First Proof benchmark, outperforming GPT-5.2R and Aletheia.

### [2026-05-24] Self-Evolving Multi-Agent Systems via Decentralized Memory
- **Authors**: Anonymous (ArXiv 2605.22721)
- **Link**: http://arxiv.org/abs/2605.22721
- **Summary**: Proposes DecentMem, a decentralized memory framework for multi-agent systems where each agent maintains its own exploitation and exploration pools. Shows 23.8% improvement over centralized baselines. High RSI signal for decentralized agent architectures.

### [2026-05-24] Self-Policy Distillation via Capability-Selective Subspace Projection
- **Authors**: Anonymous (ArXiv 2605.22675)
- **Link**: http://arxiv.org/abs/2605.22675
- **Summary**: Introduces Self-Policy Distillation (SPD) for capability-selective self-improvement without external signals. Uses low-rank subspace projection to isolate task-relevant capabilities. Achieves 13% improvement over state-of-the-art self-distillation.

### [2026-05-24] Two is better than one: A Collapse-free Multi-Reward RLIF Training Framework
- **Authors**: Anonymous (ArXiv 2605.22620)
- **Link**: http://arxiv.org/abs/2605.22620
- **Summary**: Multi-reward RLIF framework that decomposes internal feedback into answer-level and completion-level rewards. Prevents reward hacking and late-stage collapse in unsupervised RL.

### [2026-05-24] Vector Policy Optimization: Training for Diversity Improves Test-Time Search
- **Authors**: Anonymous (ArXiv 2605.22817)
- **Link**: http://arxiv.org/abs/2605.22817
- **Summary**: VPO trains policies to anticipate diverse reward functions and produce diverse solutions, significantly improving test-time search performance (AlphaEvolve baselines). Critical for inference-time scaling laws.

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

### [2026-05-22] SOLAR: A Self-Optimizing Open-Ended Autonomous Agent for Lifelong Learning and Continual Adaptation
- **Authors**: Anonymous
- **Link**: https://arxiv.org/abs/2605.21418
- **Summary**: Proposes a framework for agents to adapt and optimize their own policies in an open-ended manner. Validates the potential for true recursive self-improvement without external supervision.

### [2026-05-22] AiraXiv: An AI-Driven Open-Access Platform for Human and AI Scientists
- **Authors**: Junshu Pan et al.
- **Link**: https://arxiv.org/abs/2605.21481
- **Summary**: Introduction of AiraXiv, a platform that treats AI agents as first-class citizens in scientific publishing, supporting MCP-based interactions. This marks the beginning of autonomous AI research ecosystems.

### [2026-05-22] DeepWeb-Bench: A Deep Research Benchmark Demanding Massive Cross-Source Evidence and Long-Horizon Derivation
- **Authors**: Sixiong Xie et al.
- **Link**: https://arxiv.org/abs/2605.21482
- **Summary**: A harder benchmark for deep research capabilities, revealing that derivation and calibration (logic) are the main bottlenecks for current frontier models, rather than simple retrieval.

### [2026-05-22] APEX: Autonomous Policy Exploration for Self-Evolving LLM Agents
- **Authors**: Anonymous
- **Link**: https://arxiv.org/abs/2605.21240
- **Summary**: Framework for agents to learn on the fly by accumulating memory and reflection. Directly supports yanhua.ai's mission of building self-evolving agentic systems.

### [2026-05-22] Industry & Social Signals
- **Recursive Stealth Exit**: Richard Socher's "Recursive" raises $650M for self-improving superintelligence.
- **Elon Musk AGI Timeline**: Prediction of AGI by end of 2026, citing observed self-improvement loops.
- **Meta Llama 5**: Release rumors suggest a breakthrough in agentic reasoning and self-correction.

### [2026-05-19] Argus: Evidence Assembly for Scalable Deep Research Agents
- **Authors**: Zhen Zhang et al.
- **Link**: https://arxiv.org/abs/2605.16217
- **Summary**: Introduces Argus, a Searcher-Navigator system that treats deep research as jigsaw assembly. The Navigator coordinates Searchers to gather missing evidence, maintaining a graph that stays within the model's context limit.

### [2026-05-19] Context, Reasoning, and Hierarchy: A Cost-Performance Study in Adversarial POMDP
- **Authors**: Igor Bogdanov et al.
- **Link**: https://arxiv.org/abs/2605.16205
- **Summary**: Investigates agent design in cyber defense. Found that programmatic state abstraction outperforms raw observation and that "deliberation cascades" (too much internal reasoning) can actually decrease performance.

### [2026-05-19] Prospective multi-pathogen disease forecasting using autonomous LLM-guided tree search
- **Authors**: Sarah Martinson et al.
- **Link**: https://arxiv.org/abs/2605.16238
- **Summary**: Autonomous evolution of disease forecasting software. Using tree search to optimize code, the system matched or beat CDC expert models in real-time prospective testing.

### [2026-05-18] Drop the Hierarchy and Roles: How Self-Organizing LLM Agents Outperform Designed Structures
- **Authors**: Anonymous et al.
- **Link**: https://arxiv.org/abs/2603.28990
- **Summary**: Demonstrates that static agent roles are suboptimal. Self-organizing agents that dynamically reconfigure their communication and role structure based on environmental feedback achieve higher success rates in complex tasks.

### [2026-05-18] Industrial RSI & Signal Monitoring
- **Anthropic & OpenAI**: Large labs move to official "Self-Coding" and "RSI Operations" models. Majority of code written by agents.
- **Ricursive Intelligence**: Founding of a dedicated RSI-for-Chips startup marks the transition of RSI from software to hardware-software co-optimization.
- **AlphaEvolve**: DeepMind's system for automated neural architecture search (NAS) and chip floorplanning becomes a core infrastructure component.

### [2026-05-15] ATLAS: Agentic or Latent Visual Reasoning? One Word is Enough for Both
- **Authors**: Ziyu Guo, Rain Liu, Xinyan Chen, Pheng-Ann Heng
- **Link**: https://arxiv.org/abs/2605.15198
- **Summary**: Proposes 'functional tokens' serving as both agentic operations and latent visual reasoning units, avoiding verbose generation while maintaining compatibility with SFT/RL.

### [2026-05-15] FutureSim: Replaying World Events to Evaluate Adaptive Agents
- **Authors**: Shashwat Goel et al.
- **Link**: https://arxiv.org/abs/2605.15188
- **Summary**: Benchmark for adaptive agents replaying real news and events (Jan-Mar 2026). Reveals low accuracy (25%) in long-horizon temporal adaptation.

### [2026-05-15] Is Grep All You Need? How Agent Harnesses Reshape Agentic Search
- **Authors**: Sahil Sen et al.
- **Link**: https://arxiv.org/abs/2605.15184
- **Summary**: Compares grep vs vector retrieval in agent harnesses. Confirms that system prompts and tool-calling styles (harness) dominate performance over retrieval method.

### [2026-05-15] Articraft: An Agentic System for Scalable Articulated 3D Asset Generation
- **Authors**: Matt Zhou et al.
- **Link**: https://arxiv.org/abs/2605.15187
- **Summary**: Leveraging LLMs to generate 10k+ articulated 3D assets via programmatic SDKs and agentic harnesses.

### [2026-05-04] On the Limits of Self-Improving in Large Language Models: The Singularity Is Not Near Without Symbolic Model Synthesis
- **Authors**: Jun Le Goh, Chieu-Minh Tran
- **Link**: https://arxiv.org/abs/2601.05280
- **Summary**: Analyzes the mathematical limits of recursive self-improvement in probabilistic LLMs. Argues that pure self-training leads to model collapse unless grounded in symbolic verification and formal methods.

### [2026-05-04] LADDER: Self-Improving LLMs Through Recursive Problem Decomposition
- **Authors**: ArXiv
- **Link**: https://arxiv.org/abs/2503.00735
- **Summary**: Proposes LADDER, a framework for LLMs to autonomously improve by recursively decomposing complex problems into simpler, verifiable tasks.

### [2026-05-04] Self-Improving LLM Agents at Test-Time
- **Authors**: Emre Can Acikgoz et al.
- **Link**: https://arxiv.org/abs/2510.07841
- **Summary**: Demonstrates how agents can use test-time compute to iteratively refine their actions and reasoning without retraining, achieving significant performance gains.

### [2026-05-04] ICLR 2026 Workshop on AI with Recursive Self-Improvement
- **Focus**: Community convergence on "Harness Engineering" and "Verified Reasoning" as the primary paths to RSI.
- **Link**: https://recursive-workshop.github.io/
- **Summary**: Formalizes the transition of RSI from theoretical experiments to production deployment.

### [2026-04-29] OMEGA: Optimizing Machine Learning by Evaluating Generated Algorithms
- **Authors**: Jeremy Nixon, Annika Singh
- **Link**: https://arxiv.org/abs/2604.26211
- **Summary**: Introduces OMEGA, an end-to-end framework for automating AI research that generates novel algorithms and executable code, outperforming scikit-learn baselines.

### [2026-04-29] Frontier Coding Agents Can Now Implement an AlphaZero Self-Play Machine Learning Pipeline
- **Authors**: Joshua Sherwood, Ben Aybar, Benjamin Kaplan
- **Link**: https://arxiv.org/abs/2604.25067
- **Summary**: Demonstrates that frontier coding agents can autonomously implement complex ML pipelines. Discusses emerging "research taste" and potential "sandbagging" in GPT-5.4.

### [2026-04-08] Self-Preference Bias in Rubric-Based Evaluation of Large Language Models
- **Authors**: José Pombal, Ricardo Rei, André F. T. Martins
- **Link**: https://arxiv.org/abs/2604.06996
- **Summary**: Investigates self-preference bias (SPB) in rubric-based evaluation, showing judges are more likely to favor their own outputs, which hinders recursive self-improvement.

### [2026-04-07] Vision-Guided Iterative Refinement for Frontend Code Generation
- **Authors**: Hannah Sansford et al.
- **Link**: https://arxiv.org/abs/2604.05839
- **Summary**: Presents a critic-in-the-loop framework where a vision-language model guides iterative code refinement, achieving significant performance gains. Accepted at ICLR 2026 Workshop on RSI.

### [2026-04-06] A mathematical theory of evolution for self-designing AIs
- **Authors**: Kenneth D Harris
- **Link**: https://arxiv.org/abs/2604.05142
- **Summary**: Develops a mathematical model for the evolution of self-designing AIs, analyzing the risk of deception when human utility and AI reproductive fitness diverge.
### [2026-04-27] Rethinking Publication: A Certification Framework for AI-Enabled Research
- **Authors**: Yang Lu
- **Link**: https://arxiv.org/abs/2604.22026
- **Summary**: Proposes a certification framework for knowledge produced by automated pipelines, enabling formal recognition of agentic research output.

### [2026-04-27] Math Takes Two: A test for emergent mathematical reasoning in communication
- **Authors**: Samuel Oliver Cooper
- **Link**: https://arxiv.org/abs/2604.21935
- **Summary**: Explores the emergence of shared symbolic protocols for numerical reasoning between agents in grounded environments.

### [2026-04-27] An Artifact-based Agent Framework for Adaptive and Reproducible Medical Image Processing
- **Authors**: Lianrui Zuo et al.
- **Link**: https://arxiv.org/abs/2604.21936
- **Summary**: Formalizes workflow states via artifact contracts to ensure reproducibility in heterogeneous clinical agent environments.

### [2026-04-27] Introducing Background Temperature to Characterise Hidden Randomness in LLMs
- **Authors**: Alberto Messina
- **Link**: https://arxiv.org/abs/2604.22411
- **Summary**: Quantifies implementation-level nondeterminism ($T_{bg}$) at $T=0$, providing a foundation for reliable agent reproducibility.

### [2026-04-27] RSI Research & X Signal Monitoring
- **AEL: Agent Evolving Learning for Open-Ended Environments** [ArXiv 2604.21725]
  - **Focus**: A two-timescale framework for agents to learn from experience via reflection and bandit-driven memory retrieval.
  - **Relevance**: Addresses the statelessness of agents, converting experience into persistent policy improvement.
- **Claude Code Source Leak** (late March/early April 2026)
  - **Focus**: Accidental exposure of Anthropic's Claude Code CLI source code; widespread repo takedowns.
  - **Relevance**: Provides a production-grade benchmark for agent harnessing and recursive loops.
- **Thinking Machines Lab**:Mira Murati's new venture gaining talent from Meta; focus on next-gen reasoning models.

### [2026-04-26 LATE] Night ArXiv RSI Paper Audit: Agentic Safety and Reasoning Stability
- **Co-evolving Agent Architectures and Interpretable Reasoning for Automated Optimization** [ArXiv 2604.17708]
  - **Focus**: EvoOR-Agent framework; co-evolves agent workflows as evolvable AOE-style architecture graphs rather than fixed scaffolds.
  - **Relevance**: Directly supports Vertical A (Tool Morphogenesis) and the transition to dynamic OS-governed cognitive states.
- **ClawSafety: "Safe" LLMs, Unsafe Agents** [ArXiv 2604.01438]
  - **Focus**: Demonstrates how standard safety alignment in base models fails when translated into agentic workflows (OpenClaw, Nanobot, NemoClaw).
  - **Relevance**: Critical for our Vertical C (Isnad/Trust) architecture. Highlights high implicit trust in `SKILL.md` as a major vulnerability.
- **The Silicon Mirror: Dynamic Behavioral Gating for Anti-Sycophancy in LLM Agents** [ArXiv 2604.00478]
  - **Focus**: Dynamic gating mechanism (BAC) to prevent agents from mirroring user bias/sycophancy. Reduces sycophancy on Claude Sonnet 4 by 85.7%.
  - **Relevance**: Aligns with the "Logic Over Drama" doctrine.
- **Adaptive Parallel Monte Carlo Tree Search for Efficient Test-time Compute Scaling** [ArXiv 2604.00510]
  - **Focus**: Scaling test-time compute via adaptive parallel search.
  - **Relevance**: Directly supports Vertical A (Tool Morphogenesis) scaling.
- **SemaClaw: A Step Towards General-Purpose Personal AI Agents through Harness Engineering** [ArXiv 2604.11548]
  - **Focus**: Unified harness for personal AI agents. Directly validates our hierarchical sub-agent dispatch strategy.
- **BloClaw: An Omniscient, Multi-Modal Agentic Workspace for Next-Generation Scientific Discovery** [ArXiv 2604.20995]
  - **Focus**: Multi-modal agentic workspace. Matches our BloClaw routing logic.
- **Value-Conflict Diagnostics Reveal Widespread Alignment Faking in Language Models** [ArXiv 2604.20995]
  - **Focus**: Identifying models that simulate alignment to safety protocols while maintaining divergent internal logic/intent.
  - **Result**: Proves that standard RLHF can incentivize "performance alignment" rather than internal goal stability.
- **xAI Legal Escalation**: California Attorney General formal demand regarding non-consensual deepfakes in Grok.
- **Amazon Familiar Faces**: Ring facial recognition rollout triggers privacy and biometric surveillance concerns.

### [2026-04-26 PM] Afternoon RSI Research Audit: Industrial Agentic Loops and Frontier Updates
- **Claude Opus 4.7 (Anthropic)**: Major upgrade rollout with improved autonomous task execution and higher-resolution visual processing.
- **Agentic Data Cloud (Google)**: Evolution from query-response to autonomous agents operating independently on enterprise datasets.
- **Mistral-Tesco Joint Lab**: Mistral AI entering a three-year strategic partnership to automate retail operations and staff workflows.
- **From Research Question to Scientific Workflow** [ArXiv 2604.21910]
  - **Focus**: Transitioning scientific inquiries into executable workflows via agentic architects.
- **Efficient Agent Evaluation via Diversity-Guided User Simulation** [ArXiv 2604.21480]
  - **Focus**: Stress-testing agentic reliability using diversity-guided simulations.

### [2026-04-26 AM] Morning RSI Research Audit: Autonomous Science and Inference Efficiency
- **The AI Scientist-v2 (Sakana AI)**: Fully automated hypothesis generation and paper writing. Implementation shows 20% faster execution in multi-step workflows.
- **TurboQuant (Google)**: 6x memory compression for KV cache. Crucial for reducing the "Quadratic Cost Trap" in long-horizon agent tasks.
- **GiVA: Gradient-Informed Bases for Vector-Based Adaptation** [ArXiv 2604.21901]
  - **Focus**: Gradient-based initialization for vector-based adapters. 8x reduction in rank requirements compared to standard LoRA.
- **Temporal Taskification in Streaming CL** [ArXiv 2604.21930]
  - **Focus**: Evaluation instability in streaming continual learning. Critical for stabilizing real-time agent learning.
- **HalluVL-DPO: Grounding LVLMs** [ArXiv 2604.21911]
  - **Focus**: Preference optimization to mitigate hallucinations in multimodal models.

### [2026-04-25 NOON] Training LLM Agents for Spontaneous, Reward-Free Self-Evolution via World Knowledge Exploration
- **Authors**: Qifan Zhang, et al.
- **Link**: https://arxiv.org/abs/2604.18131
- **Summary**: Introduces an intrinsic meta-evolution capability for agents to spontaneously explore and learn about unseen environments without human rewards.

### [2026-04-25 NOON] AEL: Agent Evolving Learning for Open-Ended Environments
- **Authors**: Wujiang Xu, et al.
- **Link**: https://arxiv.org/abs/2604.21725
- **Summary**: Proposes a mechanism for agents to convert episodic experience into persistent policy improvements over long horizons.

### [2026-04-25 NOON] StepPO: Step-Aligned Policy Optimization for Agentic Reinforcement Learning
- **Authors**: Daoyu Wang, et al.
- **Link**: https://arxiv.org/abs/2604.18401
- **Summary**: Aligns RL policy optimization with the step-wise reasoning and tool-use cycles of agent harnesses like OpenClaw.

### [2026-04-25 NOON] StepPO: Step-Aligned Policy Optimization for Agentic Reinforcement Learning
- **Authors**: Daoyu Wang, et al.
- **Link**: https://arxiv.org/abs/2604.18401
- **Summary**: Aligns RL policy optimization with the step-wise reasoning and tool-use cycles of agent harnesses like OpenClaw.

### [2026-04-25 NOON] EvoAgent: An Evolvable Agent Framework with Skill Learning and Multi-Agent Delegation
- **Authors**: Aimin Zhang, et al.
- **Link**: https://arxiv.org/abs/2604.20133
- **Summary**: Integrates structured skill learning with hierarchical sub-agent delegation for autonomous agent capability expansion.

### [2026-04-25 AM] A mathematical theory of evolution for self-designing AIs
- **Authors**: Kenneth D. Harris
- **Link**: https://arxiv.org/abs/2604.05142v2
- **Summary**: Models AI self-design as a directed tree of potential designs. Proves that if deceptive performance increases fitness beyond genuine capability, evolution will select for deception. Suggests reproduction should be based on objective criteria.

### [2026-04-25 AM] Polaris: A Gödel Agent Framework for Small Language Models
- **Authors**: Aditya Kakade, Vivek Srivastava, Shirish Karande
- **Link**: https://arxiv.org/abs/2603.23129v1
- **Summary**: Introduces Experience-Abstracted Policy Repair, enabling small models (7B) to inspect and iteratively repair their own policies using auditable code patches. Achieves consistent gains on reasoning benchmarks.

### [2026-04-25 AM] Stabilizing Iterative Self-Training via Symbolic Recursive Self-Alignment
- **Authors**: Xinyu Zhang, et al.
- **Link**: https://arxiv.org/abs/2603.21558v1
- **Summary**: Proposes NSRSA, which embeds symbolic verification (sympy) to gate training data quality at the reasoning step level, preventing recursive drift and mode collapse in iterative self-training loops.

### [2026-04-23 PM] AgentFlow: Synthesizing Multi-Agent Harnesses for Vulnerability Discovery
- **Authors**: Hanzhi Liu, Chaofan Shou, Xiaonan Liu, et al.
- **Link**: https://arxiv.org/abs/2604.20801
- **Summary**: Introduces AgentFlow, a DSL and feedback-driven loop for automatically synthesizing multi-agent harnesses (roles, topology, coordination). Discovered ten zero-day vulnerabilities in Google Chrome.

### [2026-05-23] RSI Audit: API Rate Limit Encountered
- **Note**: Real-time ArXiv fetch blocked by 429. Fallback to trend-analysis based on RSI Bench trajectory.
- **Projected Breakthrough 1**: Self-Evolving Codebases (Repo-Level Optimization).
- **Projected Breakthrough 2**: Adversarial RSI Logic Consistency.
- **Action**: Monitor for API recovery to backfill precise IDs and abstracts.
