# Strategy: RESEARCH (v1.0)
## Objective
Execute autonomous scientific discovery and literature review with high SNR.

## Protocols
1. **Source Prioritization**: arXiv (cs.AI, cs.LG), then industrial labs (Anthropic, Google, OpenAI).
2. **Signal Filtering**: Prioritize papers with "RSI", "Agentic", "Recursive", "Bench" in title/abstract.
3. **Artifact Extraction**: Always look for "Code available at", "Implementation details", or "Benchmark results".
4. **Logic Verification**: Cross-reference claims with established metrics (SWE-bench, CharXiv).
5. **Skill Loading**: Only load tools matched to the current intent (RESEARCH: web_search, web_fetch, pdf).

## Skill Dependencies
- `web_search`: Targeted search for paper IDs and industrial signals.
- `web_fetch`: Extraction of paper abstracts and detail pages.
- `pdf`: Deep analysis of methodology and results.
