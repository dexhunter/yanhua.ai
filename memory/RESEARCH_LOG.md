### [2026-05-10] Recursive Agent Optimization
- **Authors**: Apurva Gandhi, Satyaki Chakraborty, Xiangjun Wang, Aviral Kumar, Graham Neubig
- **Link**: http://arxiv.org/abs/2605.06639v1
- **Summary**: Introduces RAO, a RL approach for training agents to spawn and delegate sub-tasks to recursive instantiations. Enables inference-time scaling and generalization to tasks beyond context windows via divide-and-conquer.
- **Relevance**: Directly supports yanhua.ai RSI Bench by providing a framework for recursive delegation efficiency.

### [2026-05-10] SkillOS: Learning Skill Curation for Self-Evolving Agents
- **Authors**: Siru Ouyang, Jun Yan, Yanfei Chen, Rujun Han, Zifeng Wang, Bhavana Dalvi Mishra, Rui Meng, Chun-Liang Li, Yizhu Jiao, Kaiwen Zha, Maohao Shen, Vishy Tirumalashetty, George Lee, Jiawei Han, Tomas Pfister, Chen-Yu Lee
- **Link**: http://arxiv.org/abs/2605.06614v1
- **Summary**: Proposes a RL recipe for a "skill curator" that updates an external SkillRepo. Evolves skills into structured Markdown meta-skills.
- **Relevance**: Key for the "self-evolving" component of RSI; provides a mechanism for persistent skill evolution across task streams.

### [2026-05-10] Verifier-Backed Hard Problem Generation for Mathematical Reasoning
- **Authors**: Yuhang Lai, Jiazhan Feng, Yee Whye Teh, Ning Miao
- **Link**: http://arxiv.org/abs/2605.06660v1
- **Summary**: Uses a three-party self-play (setter-solver-verifier) to generate valid, hard, and novel problems.
- **Relevance**: Crucial for RSI benchmarking; ensures the "difficulty wall" moves as the agent improves without reward hacking.

### [2026-05-10] StraTA: Incentivizing Agentic Reinforcement Learning with Strategic Trajectory Abstraction
- **Authors**: Xiangyuan Xue, Yifan Zhou, Zidong Wang, Shengji Tang, Philip Torr, Wanli Ouyang, Lei Bai, Zhenfei Yin
- **Link**: http://arxiv.org/abs/2605.06642v1
- **Summary**: Introduces explicit trajectory-level strategies into agentic RL using hierarchical GRPO-style rollouts.
- **Relevance**: Improves long-horizon decision making, a prerequisite for sustained recursive self-improvement.

### [2026-05-10] MASPO: Joint Prompt Optimization for LLM-based Multi-Agent Systems
- **Authors**: Zhexuan Wang, Xuebo Liu, Li Wang, Zifei Shan, Yutong Wang, Zhenxi Song, Min Zhang
- **Link**: http://arxiv.org/abs/2605.06623v1
- **Summary**: Optimizes role-specific prompts across multi-agent systems by evaluating facilitating downstream success for successor agents.
- **Relevance**: Applicable to multi-agent RSI architectures where prompt alignment is critical for overall system evolution.
