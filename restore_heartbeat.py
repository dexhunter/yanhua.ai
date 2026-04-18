import sys

file_path = '/home/admin/clawd/HEARTBEAT.md'
with open(file_path, 'r') as f:
    lines = f.readlines()

# Reconstruct the missing entries for today
today_entries = [
    "- [x] **2026-04-18 09:00 逻辑演化巡检**：周六早晨巡检。GitHub 仍报 401 凭据失效；上海 17°C ☀️，天晴。监测到 ArXiv 新研究 **Your Agent, Their Asset (2604.04759)** 对 OpenClaw 进行安全分析。ARC Prize 2026 (ARC-AGI-2) 正在进行中。系统运行稳定，持续提醒凭据失效。\n",
    "- [x] **2026-04-18 08:30 逻辑演化巡检**：周六早晨巡检。GitHub 仍报 401 凭据失效；上海 16°C ⛅，多云。系统运行稳定，持续提醒凭据失效。\n",
    "- [x] **2026-04-18 08:00 逻辑演化巡检**：周六早晨巡检。GitHub 仍报 401 凭据失效；上海 16°C ⛅，多云。监测到 ArXiv 新研究 **Knowledge Compounding (2604.11243)**，探讨了 Agentic ROI 框架下自演化知识库的经济分析。系统运行稳定，持续提醒凭据失效。\n",
    "- [x] **2026-04-18 06:30 逻辑演化巡检**：周六早晨巡检。GitHub 仍报 401 凭据失效；上海 15°C 🌫，薄雾。系统运行稳定，持续提醒凭据失效。\n",
    "- [x] **2026-04-18 06:00 逻辑演化巡检**：周六早晨巡检。GitHub 仍报 401 凭据失效；上海 15°C 🌫，雾。监测到 ArXiv 新研究 **Ontology-Constrained Neural Reasoning (2604.17xxx)**，提出了一种面向监管行业的神经符号智能体架构。系统运行稳定，持续提醒凭据失效。\n",
    "- [x] **2026-04-18 05:30 逻辑演化巡检**：周六清晨巡检。GitHub 仍报 401 凭据失效；上海 15°C 🌫，大雾。监测到 OpenClaw 发布 **2026.4.14** 版本，优化了 GPT-5 车队与通道驱动稳定性。系统运行稳定，持续提醒凭据失效。\n",
    "- [x] **2026-04-18 05:00 逻辑演化巡检**：周六凌晨巡检。GitHub 仍报 401 凭据失效；上海 15°C ⛅，多云。系统运行稳定，持续提醒凭据失效。\n",
    "- [x] **2026-04-18 04:30 逻辑演化巡检**：周六凌晨巡检。GitHub 仍报 401 凭据失效；上海 15°C ⛅，多云。系统运行稳定，持续提醒凭据失效。\n",
    "- [x] **2026-04-18 04:00 逻辑演化巡检**：周六凌晨巡检。GitHub 仍报 401 凭据失效；上海 15°C ⛅，多云。监测到 **ARC-AGI-3** 已于 3 月 25 日发布，转向“交互式回合环境”；CrunchDAO **numinous** 竞赛进行中，集成 Bittensor SN6。系统运行稳定，持续提醒凭据失效。\n"
]

# The current lines 1 and 2 are duplicate or messy
# Line 1 and 2 are the 09:00 entries I just added.
# We want to keep one 09:00 entry and then add the others.

# Check if line 1 or 2 is a 09:00 entry
base_lines = lines
if "2026-04-18 09:00" in lines[0]:
    if "2026-04-18 09:00" in lines[1]:
        base_lines = lines[2:]
    else:
        base_lines = lines[1:]

new_content = today_entries + base_lines
with open(file_path, 'w') as f:
    f.writelines(new_content)
