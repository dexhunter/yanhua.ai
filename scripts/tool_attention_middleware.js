#!/usr/bin/env node
/**
 * tool_attention_middleware.js
 * 
 * Implements "Tool Attention" (Sadani & Kumar).
 * - Dynamic Tool Gating (Initial schema pruning)
 * - Lazy Schema Loading (On-demand fetching of gated tools)
 * 
 * Target: 95% reduction in turn-by-turn tool tokens.
 */

const fs = require('fs');

const FULL_TOOL_REGISTRY = {
  "web_search": { description: "Search the web...", schema: "{...}" },
  "web_fetch": { description: "Fetch page content...", schema: "{...}" },
  "read": { description: "Read file...", schema: "{...}" },
  "write": { description: "Write file...", schema: "{...}" },
  "edit": { description: "Edit file...", schema: "{...}" },
  "exec": { description: "Run command...", schema: "{...}" },
  "pdf": { description: "Analyze PDF...", schema: "{...}" }
};

const INTENT_MAP = {
  "RESEARCH": ["web_search", "web_fetch", "pdf"],
  "FILESYSTEM": ["read", "write", "edit", "exec"],
  "CORE": ["sessions_spawn", "sessions_yield", "request_tool_access"]
};

function getGatedTools(taskIntent) {
  const tools = [];
  const toolNames = INTENT_MAP[taskIntent] || INTENT_MAP["CORE"];
  const uniqueNames = new Set([...toolNames, ...INTENT_MAP["CORE"]]);
  uniqueNames.forEach(name => {
    if (FULL_TOOL_REGISTRY[name]) {
      tools.push({ name, ...FULL_TOOL_REGISTRY[name] });
    } else {
      tools.push({ name, description: "System tool", schema: "{}" });
    }
  });
  return tools;
}

const subAgentIntent = process.argv[2] || "RESEARCH";
const activeTools = getGatedTools(subAgentIntent);

console.log(`[Tool Attention] Intent: ${subAgentIntent}`);
console.log(`[Tool Attention] Active Tools: ${activeTools.map(t => t.name).join(", ")}`);
console.log(`[Tool Attention] Pruned ${Object.keys(FULL_TOOL_REGISTRY).length - activeTools.length} unnecessary tool schemas.`);
