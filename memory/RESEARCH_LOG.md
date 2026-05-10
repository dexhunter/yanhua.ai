### [2026-05-09] SAT: Sequential Agent Tuning for Coordinator Free Plug and Play Multi-LLM Training
- **Authors**: Yi Xie, Yangyang Xu, Yi Fan, Bo Liu
- **Link**: https://arxiv.org/abs/2605.05216
- **Summary**: Introduces Sequential Agent Tuning (SAT), a decentralized training paradigm for multi-agent teams. It ensures monotonic improvement and "plug-and-play" invariance—allowing agents to be upgraded to stronger models without retraining the entire team.
- **Relevance**: Crucial for modular RSI. In the yanhua.ai RSI Bench, SAT provides a framework for scaling agent teams where sub-agents (like OpenClaw's spawned sessions) can evolve independently while maintaining overall team stability.

### [2026-05-09] Internalizing Outcome Supervision into Process Supervision: A New Paradigm for RL for Reasoning
- **Authors**: Fei Ding, Yongkang Zhang, Runhao Liu, Yuhao Liao, Zijian Zeng, Sibo Wang, Huiming Yang
- **Link**: https://arxiv.org/abs/2605.05226
- **Summary**: Proposes a paradigm where models "internalize" final outcome rewards into internal process-level signals by identifying and correcting failed trajectories. This enables fine-grained credit assignment without costly human-labeled process data.
- **Relevance**: Addresses the "credit assignment" bottleneck in RSI. By generating its own internal "process supervision," an agent can learn from its own mistakes more effectively, directly improving the efficiency of the self-improvement loop.

### [2026-05-09] Rethinking Data Curation in LLM Training: Online Reweighting Offers Better Generalization
- **Authors**: Wanru Zhao, Yihong Chen, Yuzhi Tang, Wentao Ma, Shengchao Hu, Shell Xu Hu, Alex Iacob, Abhinav Mehrotra, Nicholas D. Lane
- **Link**: https://arxiv.org/abs/2605.05227
- **Summary**: Introduces ADAPT (Adaptive Data reweighting), an online framework that dynamically adjusts sample importance during training. It acts as an implicit curriculum learner, shifting focus from coarse patterns to fine semantic distinctions.
- **Relevance**: Improves RSI training stability. In a self-evolving loop, the "data" is the agent's own experience; ADAPT-like mechanisms can help the agent prioritize learning from high-signal "breakthrough" experiences over routine tasks.

### [2026-05-09] Adaptive Computation Depth via Learned Token Routing in Transformers
- **Authors**: Ahmed Abdelmuniem Abdalla Mohammed
- **Link**: https://arxiv.org/abs/2605.05222
- **Summary**: Presents Token-Selective Attention (TSA), using a lightweight MLP gate to allow tokens to skip layers based on difficulty. This achieves 14-23% TLOps savings with minimal quality loss.
- **Relevance**: Efficiency for long-horizon RSI. By dynamically scaling compute based on task difficulty, self-evolving agents can allocate more "thinking time" to frontier logic problems while remaining efficient on solved routines.
