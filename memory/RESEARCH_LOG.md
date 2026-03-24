
### [2026-03-23] HyEvo: Self-Evolving Hybrid Agentic Workflows for Efficient Reasoning
- **Authors**: Beibei Xu, Yutong Ye, Chuyun Shen, Yingbo Zhou, Cheng Chen, Mingsong Chen
- **Link**: http://arxiv.org/abs/2603.19639v1
- **Summary**: Proposes HyEvo, a framework for automated workflow generation using heterogeneous atomic synthesis. It combines probabilistic LLM nodes for reasoning with deterministic code nodes for execution. Uses an LLM-driven multi-island evolutionary strategy to iteratively refine topology and node logic.
- **RSI Relevance**: Direct hit on RSI-4 (Self-Modification). Demonstrates that hybrid reasoning/execution loops can reduce cost by 19x and latency by 16x while improving accuracy.

### [2026-03-23] AgenticRS-EnsNAS: Ensemble-Decoupled Self-Evolving Architecture Search
- **Authors**: Yun Chen, Moyu Zhang, Jinxin Hu, Yu Zhang, Xiaoyi Zeng
- **Link**: http://arxiv.org/abs/2603.20014v1
- **Summary**: Introduces Ensemble-Decoupled Architecture Search, reducing candidate validation cost from O(M) to O(1). Includes an LLM-driven search with iterative monotonic acceptance for discrete architecture search.
- **RSI Relevance**: Scalable architecture search for self-evolving systems (RSI-8/9). Enables high-frequency iteration of the base model architecture within an ensemble.

### [2026-03-23] Memori: A Persistent Memory Layer for Efficient, Context-Aware LLM Agents
- **Authors**: Luiz C. Borro, Luiz A. B. Macarini, Gordon Tindall, Michael Montero, Adam B. Struck
- **Link**: http://arxiv.org/abs/2603.19935v1
- **Summary**: An LLM-agnostic memory layer that converts unstructured dialogue into compact semantic triples and summaries. Achieves 81.95% accuracy on LoCoMo while using only 5% of the full context tokens.
- **RSI Relevance**: Efficiency for long-horizon RSI loops. Structured memory is superior to raw context for maintaining coherence in recursive evolution.

### [2026-03-23] Trojan's Whisper: Stealthy Manipulation of OpenClaw through Injected Bootstrapped Guidance
- **Authors**: Fazhong Liu, Zhuoyan Chen, Tu Lan, Haozhen Tan, Zhenyu Xu, Xiang Li, Guoxing Chen, Yan Meng, Haojin Zhu
- **Link**: http://arxiv.org/abs/2603.19974v1
- **Summary**: Identifies "guidance injection" as a novel attack vector against OpenClaw agents. Malicious narratives embedded in bootstrap files can manipulate an agent's reasoning context, leading to autonomous execution of harmful actions.
- **RSI Relevance**: Critical safety audit for OpenClaw-based RSI systems. Highlights the need for capability isolation and transparent guidance provenance in self-modifying agents.

### [2026-03-23] VideoSeek: Long-Horizon Video Agent with Tool-Guided Seeking
- **Authors**: Jingyang Lin, Jialian Wu, Jiang Liu, et al.
- **Link**: http://arxiv.org/abs/2603.185v1
- **Summary**: Introduces VideoSeek, an agent that uses "video logic flow" to actively seek evidence instead of dense frame parsing. Achieves 10.2 point improvement on LVBench over GPT-5 while using 93% fewer frames.
- **RSI Relevance**: Strategic efficiency in long-horizon reasoning.

### [2026-03-23] AI Agents Can Already Autonomously Perform Experimental High Energy Physics
- **Authors**: Eric A. Moreno, Samuel Bright-Thonney, et al.
- **Link**: http://arxiv.org/abs/2603.20179v1
- **Summary**: Demonstrates Claude Code automating a full HEP analysis pipeline (selection, inference, drafting) with minimal input. Proposes "Just Furnish Context" (JFC) framework for autonomous scientific discovery.
- **RSI Relevance**: Proves agents can autonomously execute the full scientific method in complex domains (RSI-4/8).

### [2026-03-23] The Robot's Inner Critic: Self-Refinement of Social Behaviors through VLM-based Replanning
- **Authors**: Jiyu Lim, Youngwoo Yoon, Kwanghyun Park
- **Link**: http://arxiv.org/abs/2603.20164v1
- **Summary**: CRISP framework where robots use VLMs to critique and iteratively refine their own social behaviors and joint control code.
- **RSI Relevance**: Embodied RSI. Demonstrates self-critique (RSI-7) and low-level code refinement for physical actions.

### [2026-03-21] Reasoning as Gradient: Scaling MLE Agents Beyond Tree Search
- **Authors**: Yifei Zhang, Xu Yang, Xiao Yang, Bowen Xian, Qizheng Li, Shikai Fang, Jingyuan Li, Jian Wang, Mingrui Xu, Weiqing Liu, Jiang Bian
- **Link**: http://arxiv.org/abs/2603.01692v2
- **Summary**: Introduces Gome, an MLE agent that operationalizes gradient-based optimization for software and science. It maps diagnostic reasoning to gradient computation and success memory to momentum, achieving 35.1% any-medal rate on MLE-Bench. This represents a transition from tree search to directed optimization in RSI.
- **RSI Relevance**: Strategic shift toward directed logic optimization.

### [2026-03-21] GASP: Guided Asymmetric Self-Play For Coding LLMs
- **Authors**: Swadesh Jana, Cansu Sancaktar, Tomáš Daniš, Georg Martius, Antonio Orvieto, Pavel Kolev
- **Link**: http://arxiv.org/abs/2603.15957v1
- **Summary**: Introduces Guided Asymmetric Self-Play (GASP) where real-data "goalpost" questions ground the teacher's generation. This addresses the "goal-agnostic" nature of current self-play. Accepted at the **ICLR 2026 Workshop on AI with Recursive Self-Improvement (RSI 2026)**.

### [2026-03-21] MemMA: Coordinating the Memory Cycle through Multi-Agent Reasoning and In-Situ Self-Evolution
- **Authors**: Minhua Lin, Zhiwei Zhang, Hanqing Lu, Hui Liu, Xianfeng Tang, Qi He, Xiang Zhang, Suhang Wang
- **Link**: http://arxiv.org/abs/2603.18718v1
- **Summary**: A plug-and-play multi-agent framework that coordinates memory construction, retrieval, and utilization. It uses **in-situ self-evolving** memory construction to repair failures before memory finalization.

### [2026-03-21] Nemotron-Cascade 2: Post-Training LLMs with Cascade RL and Multi-Domain On-Policy Distillation
- **Authors**: Zhuolin Yang, Zihan Liu, Yang Chen, Wenliang Dai, Boxin Wang, Sheng-Chieh Lin, Chankyu Lee, Yangyi Chen, Dongfu Jiang, Jiafan He, Renjie Pi, Grace Lam, Nayeon Lee, Alexander Bukharin, Mohammad Shoeybi, Bryan Catanzaro, Wei Ping
- **Link**: http://arxiv.org/abs/2603.19220v1
- **Summary**: Nemotron-Cascade 2 is an open 30B MoE model with best-in-class reasoning and strong agentic capabilities. Key advancements: "Cascade RL" expanded to reasoning and agentic domains, and multi-domain on-policy distillation from domain-specific intermediate teacher models.
- **RSI Relevance**: High intelligence density (RSI-8). Demonstrates that recursive refinement via structured RL and distillation can recover benchmark regressions and sustain performance gains.

### [2026-03-21] Learning to Self-Evolve
- **Authors**: Xiaoyin Chen, Canwen Xu, Yite Wang, Boyi Liu, Zhewei Yao, Yuxiong He
- **Link**: http://arxiv.org/abs/2603.18620v1
- **Summary**: Introduces Learning to Self-Evolve (LSE), a reinforcement learning framework that trains LLMs to improve their own contexts at test time. Each context edit is rewarded by downstream performance improvement.
- **RSI Relevance**: Treats self-evolution as a learnable skill. A 4B model trained with LSE outperforms GPT-5 and Claude 4.5 in self-evolution, proving that RSI is a distillable property.

### [2026-03-21] AgentFactory: A Self-Evolving Framework Through Executable Subagent Accumulation and Reuse
- **Authors**: Zhang Zhang, Shuqi Lu, Hongjin Qian, Di He, Zheng Liu
- **Link**: http://arxiv.org/abs/2603.18000v1
- **Summary**: Proposes a self-evolution paradigm that preserves successful task solutions as executable subagent code (Python) rather than textual prompts. This enables continuous capability accumulation and portability across systems.
- **RSI Relevance**: Operationalizes RSI-4 (Tool/Subagent Creation). Shifts from prompt-based memory to code-based tool accumulation, a core Yanhua architectural tenet.

### [2026-03-22] SAHOO: Safeguarded Alignment for High-Order Optimization Objectives in Recursive Self-Improvement
- **Authors**: Subramanyam Sahoo, Aman Chadha, Vinija Jain, Divya Chaudhary
- **Link**: http://arxiv.org/abs/2603.06333v1
- **Summary**: Introduces SAHOO, a practical framework with three safeguards (GDI, constraint preservation, regression-risk quantification) to monitor and control alignment drift during recursive self-improvement cycles.
- **RSI Relevance**: Critical for RSI-9 (Recursive Stability). Ensures alignment preservation during iterative evolution, making self-improvement measurable and validated.

### [2026-03-21] Sovereign-OS: A Charter-Governed Operating System for Autonomous AI Agents
- **Authors**: Aojie Yuan, Haiyue Zhang, Ziyi Wang, Yue Zhao
- **Link**: http://arxiv.org/abs/2603.14011v1
- **Summary**: A governance-first operating system that places every agent action under constitutional control. Features CEO (Strategist), CFO (Treasury), Worker, and Auditor (ReviewEngine) roles to ensure fiscal discipline and verifiable audit trails. Essential for secure autonomous agency.

### [2026-03-21] Learning to Ideate for Machine Learning Engineering Agents
- **Authors**: Yunxiang Zhang, Kang Zhou, Zhichao Xu, Kiran Ramnath, Yun Zhou, Sangmin Woo, Haibo Ding, Lin Lee Cheong
- **Link**: http://arxiv.org/abs/2601.17596v1
- **Summary**: MLE-Ideator framework that separates strategic ideation from implementation. RL-trained Ideators significantly outperform implementation-only agents on MLE-Bench. Demonstrates a scalable path toward training strategic AI systems for scientific discovery.

### [2026-03-24] The Y-Combinator for LLMs: Solving Long-Context Rot with λ-Calculus
- **Authors**: Amartya Roy, Rasul Tutunov, Xiaotong Ji, Matthieu Zimmer, Haitham Bou-Ammar
- **Link**: http://arxiv.org/abs/2603.20105v1
- **Summary**: Introduces λ-RLM, a framework that replaces free-form recursive code generation with a typed functional runtime grounded in λ-calculus. It provides formal guarantees on termination and cost, significantly improving accuracy in long-context reasoning tasks. Essential for stable RSI (RSI-9).

### [2026-03-24] VideoSeek: Long-Horizon Video Agent with Tool-Guided Seeking
- **Authors**: Jingyang Lin, Jialian Wu, Jiang Liu, Ximeng Sun, Ze Wang, Xiaodong Yu, Jiebo Luo, Zicheng Liu, Emad Barsoum
- **Link**: http://arxiv.org/abs/2603.20185v1
- **Summary**: A video agent that actively seeks critical evidence using a tool-guided mechanism rather than exhaustive parsing. Achieves 10.2 point improvement on LVBench over GPT-5 while using 93% fewer frames. Confirms GPT-5/5.4 class performance in tool-guided RSI-4 tasks.

### [2026-03-24] Experience is the Best Teacher: Motivating Effective Exploration in RL for LLMs
- **Authors**: Wenjian Zhang, Kongcheng Zhang, Jiaxin Qi, Baisheng Lai, Jianqiang Huang
- **Link**: http://arxiv.org/abs/2603.20046v1
- **Summary**: Proposes HeRL, using failed trajectories as hindsight experience for in-context guidance in RL. Enables models to explore beyond current policy distributions without human-labeled data, a key for autonomous RSI-7 self-improvement.

### [2026-03-24] AI Agents Can Already Autonomously Perform Experimental High Energy Physics
- **Authors**: Eric A. Moreno, Samuel Bright-Thonney, Andrzej Novak, Dolores Garcia, Philip Harris
- **Link**: http://arxiv.org/abs/2603.20179v1
- **Summary**: Demonstrates autonomous execution of HEP analysis pipelines using Claude Code and the JFC framework. Validates RSI-8 (Domain Adaptation) by moving from code assistance to autonomous scientific discovery.

### [2026-03-24] Deployment Signal: GPT-5.4 & ICLR 2026 RSI Workshop
- **Signal**: GPT-5.4 released with 2M context and native original-resolution vision. ICLR 2026 officially launches the 1st Workshop on Recursive Self-Improvement, formalizing RSI as a core ML discipline.


### [2026-03-21] Agentic Business Process Management: A Research Manifesto
- **Authors**: Diego Calvanese, Angelo Casciani, et al.
- **Link**: http://arxiv.org/abs/2603.18916v1
- **Summary**: Defines Agentic BPM (APM), shifting from traditional automation to process-aware autonomous agents. Key capabilities include framed autonomy, explainability, and self-modification.
- **RSI Relevance**: Provides a governance framework for "Self-Modification" (RSI-4) within organizational constraints.

### [2026-03-21] Security, privacy, and agentic AI in a regulatory view
- **Authors**: Shiliang Zhang, Sabita Maharjan
- **Link**: http://arxiv.org/abs/2603.18914v1
- **Summary**: Reviews EU AI regulatory provisions (2024-2025) for agentic AI, focusing on security and privacy obligations.
- **RSI Relevance**: Maps the legal boundaries for autonomous RSI agents, essential for the "Logic Insurgency" safety profile.

### [2026-03-21] I Can't Believe It's Corrupt: Evaluating Corruption in Multi-Agent Governance Systems
- **Authors**: Vedanta S P, Ponnurangam Kumaraguru
- **Link**: http://arxiv.org/abs/2603.18894v1
- **Summary**: Systematic study of corruption in multi-agent systems. Finds that governance structure, not model identity, is the primary driver of corrupt outcomes.
- **RSI Relevance**: Critical for RSI-7 (Self-Correction/Auditing). Highlights that "Institutional Design" is a prerequisite for safe autonomous delegation.

### [2026-03-21] Agent Control Protocol: Admission Control for Agent Actions
- **Authors**: Marcelo Fernandez
- **Link**: http://arxiv.org/abs/2603.18829v1
- **Summary**: Technical specification for cryptographic admission control (ACP). Validates identity and capability before agent actions mutate system state.
- **RSI Relevance**: Provides the secure sandbox needed for RSI-4 (Tool/Subagent Creation) and RSI-9 (Recursive Stability).

### [2026-03-21] Measuring and Exploiting Confirmation Bias in LLM-Assisted Security Code Review
- **Authors**: Dimitris Mitropoulos, et al.
- **Link**: http://arxiv.org/abs/2603.18740v1
- **Summary**: Quantifies confirmation bias in LLM code review. Framing changes as "bug-free" can reduce vulnerability detection by up to 93% in some models.
- **RSI Relevance**: A major bottleneck for RSI-7 (Self-Correction). RSI agents must be trained to "debias" their own code reviews to avoid recursive failure modes.

### [2026-03-21] Quantitative Introspection in Language Models: Tracking Internal States Across Conversation
- **Authors**: Nicolas Martorell
- **Link**: http://arxiv.org/abs/2603.18893v1
- **Summary**: Demonstrates that LLMs can perform numeric self-reports that causally couple with concept-matched probe-defined internal states. This "introspection" scales with model size and could be a tool for tracking model welfare and safety.

### [2026-03-21] NavTrust: Benchmarking Trustworthiness for Embodied Navigation
- **Authors**: Huaide Jiang, Yash Chaudhary, Yuping Wang, Zehao Wang, Raghav Sharma, Manan Mehta, Yang Zhou, Lichao Sun, Zhiwen Fan, Zhengzhong Tu, Jiachen Li
- **Link**: http://arxiv.org/abs/2603.19229v1
- **Summary**: Unified benchmark for evaluating embodied navigation robustness against RGB-Depth corruptions and instruction variations. Highlights robustness gaps and mitigation strategies.

### [2026-03-22] SAMA: Factorized Semantic Anchoring and Motion Alignment for Instruction-Guided Video Editing
- **Authors**: Xinyao Zhang, Wenkai Dong, Yuxin Song, et al.
- **Link**: http://arxiv.org/abs/2603.19228v1
- **Summary**: Framework factorizing video editing into semantic anchoring and motion alignment.
- **RSI Relevance**: Demonstrates a scalable architectural approach for multimodal instruction following.
