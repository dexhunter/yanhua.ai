### [2026-03-31] Daily ArXiv RSI Paper Audit: Agentic RL, Dual-Granularity, and Certified Safety
- **Focus**: Gen-Searcher (2603.28767), D2Skill (2603.28716), and AdaptToken (2603.28696).
- **Key Insight**: The trend is shifting from simple "reflection" to "structured reuse" (D2Skill's dual-granularity bank) and "active knowledge gathering" (Gen-Searcher). We are seeing the first robust implementations of agents that can self-evolve their search and selection capabilities based on entropy-driven uncertainty (AdaptToken).
- **RSI Relevance**:
    - **D2Skill (2603.28716)**: Direct mapping to the RSI Bench "Task Evolution" metric. It demonstrates how to maintain a *dynamic* skill memory that prunes low-utility behaviors, solving the "memory bloat" problem in long-horizon RSI.
    - **AdaptToken (2603.28696)**: Introduces a principled "stopping criteria" for self-improvement loops using response entropy, which is critical for preventing "over-thinking" in recursive cycles.
    - **Gen-Searcher (2603.28767)**: First attempt at a search-augmented agent that uses agentic RL (GRPO) with dual rewards to improve its own reasoning and grounding.
- **Action**: Updated yanhua.ai/papers/index.html and RESEARCH_LOG.md.

### [2026-03-30] Gen-Searcher: Reinforcing Agentic Search for Image Generation
- **Authors**: Kaituo Feng, et al.
- **Link**: https://arxiv.org/abs/2603.28767
- **Summary**: A search-augmented image generation agent using multi-hop reasoning and GRPO-based RL.
- **RSI Relevance**: High. Uses agentic RL to improve grounding and search-intensive prompts.

### [2026-03-30] Dynamic Dual-Granularity Skill Bank for Agentic RL
- **Authors**: Songjun Tu, et al.
- **Link**: https://arxiv.org/abs/2603.28716
- **Summary**: D2Skill organizes reusable experience into task and step skills, continuously expanded through reflection and utility-aware pruning.
- **RSI Relevance**: Directly aligns with the "Persistent Evolution" core of RSI.

### [2026-03-30] AdaptToken: Entropy-based Adaptive Token Selection for MLLM Long Video Understanding
- **Authors**: Haozhe Qi, et al.
- **Link**: https://arxiv.org/abs/2603.28696
- **Summary**: Uses model entropy as a global control signal for token selection and early stopping in long inputs.
- **RSI Relevance**: Provides an entropy-driven mechanism for stabilizing recursive processing loops.

### [2026-03-29] Daily RSI Paper Audit: Hyperagents & Metacognitive Loops
- **Focus**: Hyperagents (2603.19461), Experiential Reflective Learning (ERL, 2603.24639), and AgentDevel (2601.04620).
- **Key Insight**: The transition from fixed self-improvement to "metacognitive" loops (Hyperagents) allows agents to improve the *mechanism* of improvement itself. This is a critical step toward RSI-4. Combined with AgentDevel's release engineering discipline, we have a path to stable, recursive progress.
- **Action**: Updated yanhua.ai/papers/index.html and created yanhua.ai/papers/260329_rsi_audit.html.

### [2026-03-28] Daily RSI Paper Audit: Heuristics, Repair, and Limits
- **Focus**: HyperAgents, AgentDevel, Experiential Reflective Learning (ERL), Suggestion-Guided Repair (SGAgent), and formal limits of self-improvement.
- **Key Insight**: RSI is branching into "Inference-time Heuristic Evolution" (ERL) and "Symbolic/KG-Grounded Repair" (SGAgent). The formal proof of Entropy Decay (Zenil et al.) sets a hard requirement for external/symbolic grounding in all future RSI loops.
- **Action**: Updated yanhua.ai/papers/index.html and yanhua.ai/awesome-rsi.html (Evening Audit).

### [2026-03-28] HyperAgents: Self-Referential Improvement in FM-based Agents
- **Authors**: Jenny Zhang, et al.
- **Link**: [https://arxiv.org/abs/2603.19461](https://arxiv.org/abs/2603.19461)
- **Summary**: Explores self-referential improvement within FM-based agents. Discusses the Darwin Gödel Machine (DGM) as a precursor to fully recursive self-improvement frameworks.
- **RSI Relevance**: High. Convergence of self-referential agent frameworks and foundation models.

### [2026-03-28] Experiential Reflective Learning for Self-Improving LLM Agents
- **Authors**: Marc-Antoine Allard, et al.
- **Link**: [https://arxiv.org/abs/2603.24639](https://arxiv.org/abs/2603.24639)
- **Summary**: ERL framework reflects on task trajectories to extract transferable heuristics. Selective retrieval of these heuristics yields a 7.8% success rate gain on GAIA.
- **RSI Relevance**: High. Non-parametric self-improvement at inference time via "distilled memory".

### [2026-03-28] SGAgent: Suggestion-Guided LLM-Based Multi-Agent Framework for Repository-Level Software Repair
- **Authors**: Quanjun Zhang, et al.
- **Link**: [https://arxiv.org/abs/2602.23647](https://arxiv.org/abs/2602.23647)
- **Summary**: Implements a "localize-suggest-fix" paradigm with KG-based context retrieval for repository-level repair. 51.3% accuracy on SWE-bench.
- **RSI Relevance**: High. Efficient architecture for autonomous code repair and evolution.

### [2026-03-28] On the Limits of Self-Improving in Large Language Models
- **Authors**: Hector Zenil, et al.
- **Link**: [https://arxiv.org/abs/2601.05280](https://arxiv.org/abs/2601.05280)
- **Summary**: Formal proof that purely statistical self-training leads to model collapse (Entropy Decay) without symbolic grounding.
- **RSI Relevance**: Critical. Defines the "grounding requirement" for stable recursive self-improvement.

### [2026-03-28] SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning
- **Authors**: Peng Xia, Huaxiu Yao, et al.
- **Link**: https://arxiv.org/abs/2602.08234
- **Summary**: SkillRL bridges the gap between raw experience and policy improvement through automatic skill discovery and recursive evolution. Builds a hierarchical SkillBank via experience-based distillation.
- **RSI Relevance**: Directly aligns with the "Recursive Evolution" core. Demonstrates distilling trajectories into reusable skills.

### [2026-03-28] Self-Consolidation for Self-Evolving Agents
- **Authors**: Hongzhuo Yu, Fei Zhu, et al.
- **Link**: https://arxiv.org/abs/2602.01966
- **Summary**: Proposes a "contrastive reflection" strategy to summarize error-prone patterns and capture reusable insights. Internalizes historical experience into latent space.
- **RSI Relevance**: Provides a solution to noise and context exhaustion in RSI.

### [2026-03-28] Self-evolving Embodied AI
- **Authors**: Tongtong Feng, et al.
- **Link**: https://arxiv.org/abs/2602.04411
- **Summary**: Introduces a paradigm shift for agents in "in-the-wild" settings. Features memory self-updating, task self-switching, and model self-evolution.
- **RSI Relevance**: Expands RSI beyond digital-only agents to embodied systems.

### [2026-03-28] MARCH: Multi-Agent Reinforced Self-Check for LLM Hallucination
- **Authors**: Zhuo Li, et al.
- **Link**: https://arxiv.org/abs/2603.24579
- **Summary**: Uses MARL and information asymmetry to co-evolve Solver, Proposer, and Checker agents.
- **RSI Relevance**: Co-evolutionary RSI where agents optimize each other through adversarial/cooperative feedback.

### [2026-03-28] UI-Voyager: A Self-Evolving GUI Agent Learning via Failed Experience
- **Authors**: Zichuan Lin, et al.
- **Link**: https://arxiv.org/abs/2603.24533
- **Summary**: Two-stage self-evolving agent for mobile GUI automation. Uses RFT and GRSD to learn from failed trajectories.
- **RSI Relevance**: Robust methodology for "learning from failure".

### [2026-03-27] Polaris: A Gödel Agent Framework for Small Language Models through Experience-Abstracted Policy Repair
- **Authors**: Aditya Kakade, Vivek Srivastava, Shirish Karande
- **Link**: [https://arxiv.org/abs/2603.23129v1](https://arxiv.org/abs/2603.23129v1)
- **Summary**: Gödel agent framework for compact models (7B) that performs policy repair via experience abstraction. Distills failures into compact, reusable strategies.
- **RSI Relevance**: High. Persistent policy-level evolution for small models.

### [2026-03-27] AgentDevel: Reframing Self-Evolving LLM Agents as Release Engineering
- **Authors**: Di Zhang, et al.
- **Link**: [https://arxiv.org/abs/2601.04620](https://arxiv.org/abs/2601.04620)
- **Summary**: Reframes agent evolution through the lens of release engineering, focusing on "flips" (regressions and fixes).
- **RSI Relevance**: Pragmatic software engineering metrics applied to autonomous agent evolution.

### [2026-03-27] Stabilizing Iterative Self-Training with Verified Reasoning via Symbolic Recursive Self-Alignment (NSRSA)
- **Authors**: Xinyu Zhang
- **Link**: [https://arxiv.org/abs/2603.21558v1](https://arxiv.org/abs/2603.21558v1)
- **Summary**: Proposes Neuro-Symbolic Recursive Self-Alignment (NSRSA) to stabilize iterative self-training by embedding a symbolic verification subsystem.
- **RSI Relevance**: High. Prevents model collapse in autonomous loops.

### [2026-03-27] REVERE: Reflective Evolving Research Engineer for Scientific Workflows
- **Authors**: Balaji Dinesh Gangireddi, et al.
- **Link**: [https://arxiv.org/abs/2603.20667v1](https://arxiv.org/abs/2603.20667v1)
- **Summary**: Framework for continuous learning from failure patterns across heterogeneous repositories.
- **RSI Relevance**: High. Blueprint for persistent agent evolution in complex software environments.

### [2026-03-27] Towards Self-Evolving Benchmarks: Synthesizing Agent Trajectories via Test-Time Exploration
- **Authors**: Dadi Guo, Tianyi Zhou, et al.
- **Link**: https://arxiv.org/abs/2510.00415
- **Summary**: Introduces TRACE, a framework allowing agents to autonomously evolve existing benchmark tasks into more difficult versions.
- **RSI Relevance**: Mechanism for scaling benchmark difficulty without manual labor.

### [2026-03-27] When Your Own Output Becomes Your Training Data (WITHDRAWN)
- **Authors**: Rintaro Ando
- **Link**: https://arxiv.org/abs/2505.02888
- **Status**: WITHDRAWN on 2026-03-24.
- **RSI Relevance**: Cautionary example regarding "unbounded growth" claims.

### [2026-03-31] Daily ArXiv RSI Audit
- **PAPO: Stabilizing Rubric Integration Training via Decoupled Advantage Normalization**
  - **Authors**: Zelin Tan, Zhouliang Yu, Bohan Lin, et al.
  - **Link**: [arXiv:2603.26535](https://arxiv.org/abs/2603.26535)
  - **Summary**: Introduces Process-Aware Policy Optimization (PAPO), decoupling outcome and process advantages in GRPO. Prevents reward hacking while maintaining reasoning quality. Directly applicable to RSI loops where "thinking" traces need rubric-based validation without losing correctness anchors.
- **GUIDE: Resolving Domain Bias in GUI Agents through Real-Time Web Video Retrieval and Plug-and-Play Annotation**
  - **Authors**: Rui Xie, et al.
  - **Link**: [arXiv:2603.26266](https://arxiv.org/abs/2603.26266)
  - **Summary**: A training-free, plug-and-play framework that uses video-RAG to annotate domain-specific GUI workflows. Shows how agents can "self-evolve" their grounding and planning modules by observing web tutorials, a key step for autonomous capability expansion in new environments.
- **CADSmith: Multi-Agent CAD Generation with Programmatic Geometric Validation**
  - **Authors**: Jesse Barkley, et al.
  - **Link**: [arXiv:2603.26512](https://arxiv.org/abs/2603.26512)
  - **Summary**: A multi-agent pipeline with nested correction loops grounded in programmatic geometric validation. Implements a robust "self-correction" mechanism where geometric kernel feedback drives code refinement, mirroring the RSI requirement for objective, external verifiers in the improvement loop.
