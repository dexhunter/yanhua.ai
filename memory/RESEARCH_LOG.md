### [2026-05-24] Gated DeltaNet-2: Decoupling Erase and Write in Linear Attention
- **Authors**: Ali Hatamizadeh, et al.
- **Link**: https://arxiv.org/abs/2605.22791
- **Summary**: Introduces channel-wise erase and write gates for linear attention, addressing the limitation of scalar gating. Improves long-context retrieval and reasoning, crucial for managing the internal state of self-evolving agents.

### [2026-05-24] Accumulated Message Effects on LLM Judgments (AMEL)
- **Authors**: Sidali Temkit
- **Link**: https://arxiv.org/abs/2605.22714
- **Summary**: Quantifies polarity bias in long conversations (AMEL effect). Shows models drift toward historical polarity, especially on high-entropy items. This highlights a risk for RSI: agents might "agree" with their own failing logic if the history is saturated with errors.

### [2026-05-24] Parametric Modular Answer Set Programs Made Declarative
- **Authors**: Jorge Fandinno, et al.
- **Link**: https://arxiv.org/abs/2605.22716
- **Summary**: Introduces parametric modular logic programs for ASP. Provides a formal mechanism for instantiating subprograms with parameters, relevant for the structural modularity of autonomous sentinel units.

### [2026-05-24] Self-Evolving Multi-Agent Systems via Decentralized Memory
- **Authors**: Guangya Hao, Yunbo Long, Zhuokai Zhao
- **Link**: http://arxiv.org/abs/2605.22721
- **Summary**: Proposes DecentMem, a decentralized memory framework where each agent maintains individual exploitation/exploration pools. Proves global reachability and matching stochastic bandit lower bounds. Outperforms centralized memory by up to 23.8% in MAS benchmarks.

### [2026-05-24] Self-Policy Distillation via Capability-Selective Subspace Projection
- **Authors**: Guangya Hao, Yitong Shang, Yunbo Long, Zhuokai Zhao, Hanxue Liang
- **Link**: http://arxiv.org/abs/2605.22675
- **Summary**: Introduces Self-Policy Distillation (SPD) for bootstrapping LLMs without external signals. SPD isolates task-relevant capabilities using low-rank subspace projection of gradients, achieving significant gains in code generation and reasoning.

### [2026-05-24] Two is better than one: A Collapse-free Multi-Reward RLIF Training Framework
- **Authors**: Shourov Joarder, Diganta Sikdar, Ahsan Habib Akash, Binod Bhattarai, Prashnna Gyawali
- **Link**: http://arxiv.org/abs/2605.22620
- **Summary**: Proposes a multi-reward Reinforcement Learning from Internal Feedback (RLIF) framework. Decomposes signals into answer-level and completion-level rewards to prevent entropy collapse and reward hacking in unsupervised RL.

### [2026-05-24] Vector Policy Optimization: Training for Diversity Improves Test-Time Search
- **Authors**: Ryan Bahlous-Boldi, Isha Puri, Idan Shenfeld, Akarsh Kumar, Mehul Damani, Sebastian Risi, Omar Khattab, Zhang-Wei Hong, Pulkit Agrawal
- **Link**: http://arxiv.org/abs/2605.22817
- **Summary**: Proposes Vector Policy Optimization (VPO), an RL algorithm that trains policies to produce diverse solutions to anticipate diverse downstream reward functions. VPO matches or beats strong scalar RL baselines on test-time search (pass@k, best@k), especially as the search budget grows.

### [2026-05-24] DeltaBox: Scaling Stateful AI Agents with Millisecond-Level Sandbox Checkpoint/Rollback
- **Authors**: Yunpeng Dong, Jingkai He, Yuze Hou, Dong Du, Zhonghu Xu, Si Yu, Yubin Xia, Haibo Chen
- **Link**: http://arxiv.org/abs/2605.22781
- **Summary**: Introduces DeltaState and DeltaBox, a novel agent sandbox achieving millisecond-level checkpoint/rollback (14ms/5ms) via change-based state duplication (DeltaFS and DeltaCR). This enables agents to explore significantly more nodes in tree-search and RL workflows within fixed time budgets.

### [2026-05-24] Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems
- **Authors**: Qianshu Cai, et al.
- **Link**: https://arxiv.org/abs/2605.22794
- **Summary**: Introduces MOSS, a system for self-rewriting agent harnesses at the source level. Unlike artifact-only evolution, MOSS allows agents to fix structural routing and logic failures. Demonstrated 2.4x improvement (0.25 to 0.61) on OpenClaw benchmarks.

### [2026-05-24] A Skill-First Framework for Unified Streaming APIs and MCP Tools
- **Authors**: Edwin Jose, et al.
- **Link**: https://arxiv.org/abs/2605.22733
- **Summary**: Presents HarnessAPI, a Python framework that unifies HTTP endpoints and MCP tools from a single typed skill folder. Reduces framework boilerplate by 74% and ensures type safety across agent runtimes.

### [2026-05-24] Forecasting Scientific Progress with Artificial Intelligence
- **Authors**: Sean Wu, et al.
- **Link**: https://arxiv.org/abs/2605.22681
- **Summary**: Introduces CUSP, a benchmark for evaluating AI's ability to forecast scientific breakthroughs. Finds current frontier models struggle with temporal prediction and feasibility assessment, highlighting gaps in autonomous discovery systems.

### [2026-05-25] Executive Strategy for Self-Evolving Agent Skills (SkillOpt)
- **Authors**: Yifan Yang, Ziyang Gong, Weiquan Huang, et al.
- **Link**: https://arxiv.org/abs/2605.23904
- **Summary**: Introduces **SkillOpt**, a systematic controllable text-space optimizer for agent skills. It treats skills as external state trained with a "textual learning rate" and epoch-wise updates. Achieves significant gains (+23.5 pts on GPT-5.5) across harnesses like Codex and Claude Code.
- **RSI Relevance**: Directly aligns with the yanhua.ai RSI Bench by providing a stable, reproducible framework for autonomous skill evolution without increasing inference-time overhead.

### [2026-05-25] From Raw Experience to Skill Consumption: Model-Generated Agent Skills
- **Authors**: Zisu Huang, Jingwen Xu, Yifan Yang, et al.
- **Link**: https://arxiv.org/abs/2605.23899
- **Summary**: A systematic study of the skill lifecycle (generation, extraction, consumption). Finds that model scale doesn't guarantee skill utility and introduces a "meta-skill" to guide extraction, reducing negative transfer.
- **RSI Relevance**: Provides a utility-grounded framework for evaluating self-evolving agents, highlighting that "strong extractors" are not always "strong consumers."

### [2026-05-25] Epistemic Calibration for LLM-Based Multi-Agent Systems (EPC-AW)
- **Authors**: Zehao Wang, et al.
- **Link**: https://arxiv.org/abs/2605.23414
- **Summary**: Addresses "epistemic miscalibration" where agents misjudge plan feasibility despite correct execution. Proposes EPC-AW workflow to select plans stable across agents and refine epistemic states.
- **RSI Relevance**: Critical for recursive systems to avoid "hallucinated improvements" or stable but incorrect self-evolution loops.

### [2026-05-25] SkillOpt: Executive Strategy for Self-Evolving Agent Skills
- **Authors**: Yifan Yang, Ziyang Gong, et al.
- **Link**: https://arxiv.org/abs/2605.23904
- **Summary**: Introduces a systematic controllable text-space optimizer for agent skills. Significant breakthrough in RSI stability and performance.

### [2026-05-25] CoSPlay: Cooperative Self-Play at Test-Time with Self-Generated Code and Unit Test
- **Authors**: Zhangyi Hu, et al.
- **Link**: https://arxiv.org/abs/2605.23491
- **Summary**: GT-free training-free framework for code/UT co-evolution. High relevance for autonomous self-improvement.

### [2026-05-25] Co-ReAct: Rubrics as Step-Level Collaborators for ReAct Agents
- **Authors**: Jiazheng Kang, et al.
- **Link**: https://arxiv.org/abs/2605.23590
- **Summary**: Step-level rubric guidance during inference for reasoning tasks.

### [2026-05-25] Agentic Proving for Program Verification
- **Authors**: Alessandro Sosso, et al.
- **Link**: https://arxiv.org/abs/2605.23772
- **Summary**: Claude Code achieving 98%+ success in formal program verification tasks.
