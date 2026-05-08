import sys
from datetime import datetime

new_papers = [
    {
        "title": "EvoLM: Self-Evolving Language Models through Co-Evolved Discriminative Rubrics",
        "authors": "Shuyue Stella Li, Rui Xin, Teng Xiao, et al.",
        "link": "https://arxiv.org/abs/2605.03871",
        "summary": "Introduces EVOLM, which co-evolves instance-specific evaluation rubrics alongside a policy model. It enables self-improvement by using the model's own evaluative capacity as a reward signal, outperforming GPT-4.1 on RewardBench-2 without external supervision.",
        "relevance": "Critical for yanhua.ai/RSI-Bench as it demonstrates a scalable, closed-loop reward mechanism that bypasses human-bottlenecked supervision.",
        "tag": "RSI-4/8 Evaluation"
    },
    {
        "title": "Learning Correct Behavior from Examples: Validating Sequential Execution in Autonomous Agents",
        "authors": "Reshabh K Sharma, Gaurav Mittal, Yu Hu",
        "link": "https://arxiv.org/abs/2605.03159",
        "summary": "Uses compiler theory (dominator analysis) and multimodal LLMs to learn and validate 'ground truth' execution models from few-shot traces.",
        "relevance": "Essential for the yanhua.ai/RSI-Bench verification engine; enables automated 'correctness' scoring for induced skills.",
        "tag": "RSI-4 Verification"
    },
    {
        "title": "A Multi-Agent Consensus Protocol for Stable Software Remodularization",
        "authors": "Ahmed F. Ibrahim",
        "link": "https://arxiv.org/abs/2605.04188",
        "summary": "Reframes software module clustering as a distributed consensus problem among autonomous agents, introducing the Asymmetric Monotonic Concession Protocol (AMCP) to reconcile cohesion and stability.",
        "relevance": "Provides a formal mechanism for multi-agent logic consistency and 'circuit-breaking' in self-evolving codebases.",
        "tag": "RSI-9 Stability"
    }
]

file_path = 'yanhua_site/papers/index.html' # Adjusted for local workspace if needed
# Actually, I should probably just edit the file I fetched if I can find it locally.
# Based on the web_fetch, it's at https://yanhua.ai/papers/index.html.
# I will check if there is a local 'yanhua.ai' or 'public_html' folder.
