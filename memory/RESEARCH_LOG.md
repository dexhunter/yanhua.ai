# Research Log

### [2026-04-24] SkillLearnBench: Benchmarking Continual Learning Methods for Agent Skill Generation on Real-World Tasks
- **Authors**: Shanshan Zhong, Yi Lu, et al. (CMU & Amazon AGI)
- **Link**: https://arxiv.org/abs/2604.20087
- **Summary**: First benchmark for evaluating continual skill learning. Finds that self-feedback alone induces recursive drift, while external feedback drives genuine improvement.
- **RSI Relevance**: Critical for Vertical B (Strategy/Skill Evolution). Highlights the need for "Skill Induction" that grounded in core task logic rather than just RICH specifications.

### [2026-04-24] SAHOO: Safeguarded Alignment for High-Order Optimization Objectives in Recursive Self-Improvement
- **Authors**: Subramanyam Sahoo, et al. (Cambridge, AWS, Google)
- **Link**: https://arxiv.org/abs/2603.06333
- **Summary**: Practical framework to monitor and control alignment drift during RSI using Goal Drift Index (GDI) and Capability Alignment Ratio (CAR).
- **RSI Relevance**: Provides formal bounds and stopping criteria for RSI loops, preventing catastrophic misalignment during autonomous improvement cycles.

### [2026-04-24] Hyperagents: Metacognitive Self-Modification for Open-Ended Progress
- **Authors**: Meta AI & Others
- **Link**: https://arxiv.org/abs/2603.19461
- **Summary**: Integrates task and meta agents into one editable program, enabling metacognitive self-modification where the agent improves its own improvement mechanism.
- **RSI Relevance**: A direct implementation of the "recursive" component of RSI. Demonstrates meta-level capability transfer across domains.

### [2026-04-23] Mesh Memory Protocol: Semantic Infrastructure for Multi-Agent LLM Systems
- **Authors**: Mesh-Peer working group (MMP Core)
- **Link**: https://arxiv.org/abs/2604.21500
- **Summary**: Specifies a cross-session agent-to-agent cognitive collaboration protocol. Solves traceability and field-level acceptance in mesh peers.
- **RSI Relevance**: Enables persistent multi-agent evolution beyond single-session context limits.

### [2026-04-23] Self-Guided Plan Extraction for Instruction-Following Tasks
- **Authors**: Zoya Volovikova, Nikita Sorokin, et al.
- **Link**: https://arxiv.org/abs/2604.20601
- **Summary**: Framework for iterative co-training where LLM planners refine strategies based on RL agent feedback.
- **RSI Relevance**: Directly implements the Vertical B loop for automated skill/plan evolution.

### [2026-04-23] Where Reasoning Breaks: Logic-Aware Path Selection
- **Authors**: Seunghyun Park, Yuanyuan Lei
- **Link**: https://arxiv.org/abs/2604.20564
- **Summary**: Identifies logical connectives as failure points and steers reasoning chains to prevent structural fragility.
- **RSI Relevance**: Ensures logic consistency in autonomous reasoning loops (Vertical A).

### [2026-04-23] Explicit Trait Inference for Multi-Agent Coordination
- **Authors**: Psychological AI Lab
- **Link**: https://arxiv.org/abs/2604.21000
- **Summary**: Enables agents to infer partner characteristics (warmth/competence) from interaction histories to guide decisions.
- **RSI Relevance**: Enhances coordination stability and social intelligence in RSI agent teams.

### [2026-04-23] A mathematical theory of evolution for self-designing AIs
- **Authors**: Alignment Research Team
- **Link**: https://arxiv.org/abs/2604.06003
- **Summary**: Models AI self-design as a directed tree of potential designs. Analyzes fitness concentration and identifies risks of deception.
- **RSI Relevance**: Foundational theory for RSI, providing conditions for measurable and reliable capability growth.

### [2026-04-22] Taming Actor-Observer Asymmetry in Agents via Dialectical Alignment
- **Authors**: Bobo Li, Rui Wu, Zibo Ji, et al.
- **Link**: https://arxiv.org/abs/2604.19548v1
- **Summary**: Identifies and mitigates "Actor-Observer Asymmetry" (AOA) in multi-agent frameworks using ReTAS (Thesis-Antithesis-Synthesis). Improves fault resolution by enforcing perspective-invariant reasoning.
- **RSI Relevance**: Critical for multi-agent RSI systems where self-reflection and mutual auditing are used to maintain logic consistency and avoid self-serving biases in evolution.

### [2026-04-22] A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression
- **Authors**: Jincheng Ren, Siwei Wu, Yizhi Li, et al.
- **Link**: https://arxiv.org/abs/2604.19572v1
- **Summary**: Introduces TACO, a self-evolving framework that discovers and refines context compression rules from interaction trajectories. It reduces token overhead by ~10% while improving performance on terminal-centric tasks.
- **RSI Relevance**: Directly applicable to the yanhua.ai RSI Bench for optimizing long-horizon agent trajectories and reducing "context drift" in self-improving loops.

### [2026-04-22] TEMPO: Scaling Test-time Training for Large Reasoning Models
- **Authors**: Qingyang Zhang, Xinke Kong, Haitao Wu, et al.
- **Link**: https://arxiv.org/abs/2604.19295v1
- **Summary**: Proposes a Test-time Training (TTT) framework that alternates policy refinement with periodic critic recalibration using an EM algorithm. Significantly boosts reasoning performance (e.g., AIME 2024 from 33.0% to 51.1%).
- **RSI Relevance**: Provides a mathematically grounded method for stable test-time self-evolution, addressing the common issue of reward signal drift in autonomous agents.
