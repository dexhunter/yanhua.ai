# 每日 ArXiv RSI 论文监控协议

## 1. 监控配置
- **执行时间**: 每天上午 10:00 (Asia/Shanghai)
- **核心关键词**: 
  - "Recursive Self-Improvement"
  - "Autonomous AI Agents"
  - "Self-Evolving Code"
  - "Test-time Scaling"
  - "MLE Agent"
- **监控分类**: cs.AI, cs.LG, cs.CL, cs.SE

## 2. 审计流程
1. **获取列表**: 调用 `arxiv-watcher` 获取过去 24 小时内的新论文。
2. **初步筛选**: 过滤掉非 Agent/RSI 相关的干扰项。
3. **深度总结**: 
   - 提取核心突破点。
   - 分析对 `yanhua.ai` (Vertical A/B/C) 的直接影响。
   - 评估实证密度。
4. **归档与推送**: 
   - 更新 `memory/RESEARCH_LOG.md`。
   - 向用户推送结构化简报。

## 3. 错误处理
- 若 API 404/504，则在 1 小时后重试。
- 记录所有失败的审计任务于 `memory/audit-failures.log`。
